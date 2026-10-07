# -*- coding: utf-8 -*-
"""图表几何校验：把 style-guide §3.6 里能测量的规则变成断言，渲染后实测，不靠肉眼。

用法（仓库根目录）：python3 deploy/verify-charts.py [--chrome /usr/bin/google-chrome-stable]
      自测反例：  python3 deploy/verify-charts.py --self-test   （确认每条规则真能报错）
依赖：pip install playwright（浏览器用系统 Chrome，或 `playwright install chromium`）

校验项（任一失败即非零退出）：
  1. 页面在各断点下不出现横向滚动
  2. 每个 SVG 的缩放倍率落在 0.92–1.04；落在下限时允许卡片内横向滚动
  3. 含汉字的 <text> 实际渲染 ≥12px，且不是 mono 字体
  4. 可见文字不越出所在 SVG 的边界
  5. 同一 SVG 内可见文字两两不重叠（tooltip/准星等 hover 层除外）
  6. 可见文字不压在其他系列的数据标记上（自己的标记、网格、轴线除外）
  7. 正交：切换全部 data-accent × data-palette，所有数据标记（含 sparkline）颜色不变

为什么要这个：规则只写在文档里，示例一定会坏——diagram-design 的 ADR 0005 是同一个结论。
"""
import argparse, asyncio, os, sys
from playwright.async_api import async_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGES = ["assets/demo.html", "assets/demo.standalone.html"]
WIDTHS = [390, 768, 1024, 1280, 1400, 1920]
SCALE_MIN, SCALE_MAX = 0.92, 1.04

JS = r"""() => {
  const fails = [];
  const visible = el => {
    for (let n = el; n && n.tagName !== 'svg'; n = n.parentElement) {
      const cs = getComputedStyle(n);
      if (cs.display === 'none' || cs.visibility === 'hidden' || parseFloat(cs.opacity) === 0) return false;
    }
    return true;
  };
  const inter = (a, b, pad = 0) =>
    Math.min(a.right, b.right) - Math.max(a.left, b.left) > pad &&
    Math.min(a.bottom, b.bottom) - Math.max(a.top, b.top) > pad;
  document.querySelectorAll('.ui-chart-body > svg').forEach((svg, si) => {
    const title = svg.closest('.ui-chart')?.querySelector('.ui-chart-title')?.textContent.trim() || `svg#${si}`;
    const vb = svg.viewBox.baseVal, box = svg.getBoundingClientRect(), k = box.width / vb.width;
    const body = svg.parentElement;
    const scrolls = body.scrollWidth > body.clientWidth + 1;
    if (k < SCALE_MIN - .005 && !scrolls) fails.push(`[${title}] 缩放 ${k.toFixed(2)} 低于下限却没有卡内滚动`);
    if (k > SCALE_MAX + .005) fails.push(`[${title}] 缩放 ${k.toFixed(2)} 超过上限 ${SCALE_MAX}`);
    const texts = [...svg.querySelectorAll('text')].filter(t => visible(t) && t.textContent.trim());
    const rects = texts.map(t => t.getBoundingClientRect());
    texts.forEach((t, i) => {
      const r = rects[i], cs = getComputedStyle(t), s = t.textContent.trim().slice(0, 10);
      if (/[一-鿿]/.test(t.textContent)) {
        const px = parseFloat(cs.fontSize) * k;
        if (px < 11.95) fails.push(`[${title}] 汉字「${s}」实际 ${px.toFixed(1)}px < 12px`);
        if (/mono/i.test(cs.fontFamily.split(',')[0])) fails.push(`[${title}] 汉字「${s}」用了 mono 字体`);
      }
      if (r.left < box.left - 1 || r.right > box.right + 1 || r.top < box.top - 1 || r.bottom > box.bottom + 1)
        fails.push(`[${title}] 文字「${s}」越出 SVG 边界`);
    });
    for (let i = 0; i < texts.length; i++) for (let j = i + 1; j < texts.length; j++)
      if (inter(rects[i], rects[j], 1)) fails.push(`[${title}] 文字重叠「${texts[i].textContent.trim().slice(0,8)}」×「${texts[j].textContent.trim().slice(0,8)}」`);
    // 文字 vs 数据标记：只查实心标记（柱/段/单元格/环），线和面积允许贴近（直接标注本来就挨着线尾）
    const marks = [...svg.querySelectorAll('.ui-chart-bar, .ui-chart-seg, .ui-chart-cell')].filter(visible);
    texts.forEach((t, i) => marks.forEach(m => {
      if (t.closest('.ui-chart-hit') && t.closest('.ui-chart-hit') === m.closest('.ui-chart-hit')) return; // 同组：自己的标注
      if (inter(rects[i], m.getBoundingClientRect(), 1.5))
        fails.push(`[${title}] 文字「${t.textContent.trim().slice(0,8)}」压在数据标记上`);
    }));
  });
  return fails;
}""".replace("SCALE_MIN", str(SCALE_MIN)).replace("SCALE_MAX", str(SCALE_MAX))


# 只取承载数据的那个颜色属性：面状标记看 fill、线状看 stroke、HTML 色块看 background。
# 柱间 2px 缝是 stroke: var(--surface)，它本来就该随色系变，不能算进来。
MARKS_JS = r"""() => {
  const pick = [
    ['.ui-chart-area, .ui-chart-bar, .ui-chart-seg, .ui-chart-cell', 'fill'],
    ['.ui-chart-line, .ui-chart-ring', 'stroke'],
    ['.ui-spark > i, .ui-chart-legend-item > .sw, .ui-meter > i, .ui-bullet .bar', 'backgroundColor'],
  ];
  return pick.map(([sel, prop]) => [...document.querySelectorAll(sel)].map(e => getComputedStyle(e)[prop]).join(',')).join(';');
}"""


async def check_orthogonal(b, page):
    """同一明暗下，任意强调色 × 色系组合的数据标记颜色必须与默认完全一致。"""
    fails = []
    pg = await b.new_page(viewport={"width": 1400, "height": 900})
    await pg.goto("file://" + os.path.join(ROOT, page))
    accents = await pg.evaluate("[...document.querySelectorAll('#accent-seg button')].map(b => b.dataset.accent || '')")
    palettes = await pg.evaluate("[...document.querySelectorAll('select.ui-select option')].map(o => o.value)")
    for theme in ("light", "dark"):
        await pg.evaluate(f"document.documentElement.dataset.theme = '{theme}'")
        await pg.evaluate("delete document.documentElement.dataset.accent; delete document.documentElement.dataset.palette")
        base = await pg.evaluate(MARKS_JS)
        for a in accents:
            for pl in palettes:
                await pg.evaluate(f"document.documentElement.dataset.accent = '{a}'; document.documentElement.dataset.palette = '{pl}'")
                if await pg.evaluate(MARKS_JS) != base:
                    fails.append(f"{page} {theme}：accent={a or '默认'} palette={pl or '默认'} 时数据标记颜色变了（图表色必须与主题正交）")
    await pg.close()
    return fails


async def main(chrome):
    fails = []
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path=chrome) if chrome else await p.chromium.launch()
        for page in PAGES:
            for w in WIDTHS:
                pg = await b.new_page(viewport={"width": w, "height": 900})
                await pg.goto("file://" + os.path.join(ROOT, page))
                await pg.wait_for_timeout(150)
                if await pg.evaluate("document.documentElement.scrollWidth") > w:
                    fails.append(f"{page} @{w}px：页面横向溢出")
                for f in await pg.evaluate(JS):
                    fails.append(f"{page} @{w}px：{f}")
                await pg.close()
            fails += await check_orthogonal(b, page)
        await b.close()
    uniq = list(dict.fromkeys(fails))
    if uniq:
        print(f"FAIL {len(uniq)} 项：")
        for f in uniq: print("  ✗", f)
        return 1
    print(f"全部通过（{len(PAGES)} 页 × {len(WIDTHS)} 个断点）")
    return 0


async def self_test(chrome):
    """反方向：fixtures/verify-charts-bad.html 里每张图各违反一条规则，必须全部被报出。"""
    expect = {"汉字进mono": "mono", "文字重叠": "重叠", "文字越界": "越出", "压在标记上": "压在数据标记", "放大越限": "超过上限",
              "正交": "随强调色"}
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path=chrome) if chrome else await p.chromium.launch()
        pg = await b.new_page(viewport={"width": 1000, "height": 900})
        await pg.goto("file://" + os.path.join(ROOT, "deploy/fixtures/verify-charts-bad.html"))
        got = await pg.evaluate(JS)
        before = await pg.evaluate(MARKS_JS)
        await pg.evaluate("document.documentElement.dataset.accent = 'amber'")
        if await pg.evaluate(MARKS_JS) != before:
            got.append("[正交] 数据标记随强调色变化")
        await b.close()
    missed = [k for k, v in expect.items() if not any(f"[{k}]" in g and v in g for g in got)]
    for k in expect: print(("  ✗ 漏报 " if k in missed else "  ✓ 抓到 ") + k)
    print("自测通过" if not missed else f"自测失败：{len(missed)} 条规则没被抓到")
    return 1 if missed else 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--chrome", default=os.environ.get("CHROME"))
    ap.add_argument("--self-test", action="store_true", help="跑反例样本，确认每条规则都能报错")
    a = ap.parse_args()
    if a.self_test:
        sys.exit(asyncio.run(self_test(a.chrome)))
    sys.exit(asyncio.run(main(a.chrome)))
