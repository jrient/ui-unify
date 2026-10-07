# -*- coding: utf-8 -*-
"""重建 demo 页的「图表」分区：算好 SVG 几何后直接回写两份 demo。

用法（仓库根目录）：python3 deploy/gen-demo-charts.py

为什么要脚本：图表 SVG 的坐标、路径、堆叠缝都是算出来的，手写必错；
改数据或改版面时改这里再重跑，不要直接编辑 demo.html 里的 <svg>。
注意 viewBox 的长宽比要贴近所在卡片的比例（一栏约 300×168、两栏约 460×184），
否则 SVG 等比缩放后会在卡片里「信箱化」留出大片空白。
"""

def f(v): return ('%.1f' % v).rstrip('0').rstrip('.')


def nice_domain(values, ticks=3, include=()):
    """诚实值轴：必含 0（不截断）、步长取 1/2/2.5/5×10ⁿ、全零数据给有限兜底。
    返回 (floor, ceil, [刻度…])。include 用来把阈值/目标线也纳入值域。"""
    import math
    vals = list(values) + list(include)
    lo, hi = min(0, min(vals)), max(0, max(vals))
    if lo == hi == 0:          # 全零：给 0–1 的兜底跨度，标记都落在基线上，这才是真相
        hi = 1
    raw = (hi - lo) / ticks
    mag = 10 ** math.floor(math.log10(raw))
    step = next(m * mag for m in (1, 2, 2.5, 5, 10) if m * mag >= raw - 1e-9)
    floor, ceil = math.floor(lo / step) * step, math.ceil(hi / step) * step
    n = round((ceil - floor) / step)
    tks = [floor + step * k for k in range(n + 1)]
    tks = [int(t) if float(t).is_integer() else t for t in tks]
    assert floor <= 0 <= ceil and floor <= min(vals) and max(vals) <= ceil, "值轴必须包住 0 与全部数据"
    return floor, ceil, tks

def bar_v(x, y, w, h, r=4):
    """柱：只圆顶端，底端贴基线为直角"""
    r = min(r, w/2, h)
    return (f"M{f(x)},{f(y+h)} L{f(x)},{f(y+r)} Q{f(x)},{f(y)} {f(x+r)},{f(y)} "
            f"L{f(x+w-r)},{f(y)} Q{f(x+w)},{f(y)} {f(x+w)},{f(y+r)} L{f(x+w)},{f(y+h)} Z")

def bar_h(x, y, w, h, r=4, side='right'):
    """条：只圆远离基线的一端"""
    r = min(r, h/2, w)
    if side == 'right':
        return (f"M{f(x)},{f(y)} L{f(x+w-r)},{f(y)} Q{f(x+w)},{f(y)} {f(x+w)},{f(y+r)} "
                f"L{f(x+w)},{f(y+h-r)} Q{f(x+w)},{f(y+h)} {f(x+w-r)},{f(y+h)} L{f(x)},{f(y+h)} Z")
    return (f"M{f(x+w)},{f(y)} L{f(x+r)},{f(y)} Q{f(x)},{f(y)} {f(x)},{f(y+r)} "
            f"L{f(x)},{f(y+h-r)} Q{f(x)},{f(y+h)} {f(x+r)},{f(y+h)} L{f(x+w)},{f(y+h)} Z")

out = []
w = out.append

# ============ 图 1：吞吐趋势（折线 + 面积，2 系列，24 点） ============
done  = [62,48,35,28,24,26,31,58,96,124,138,142,131,118,126,151,166,158,140,121,104,92,81,70]
queue = [18,14,11,9,8,9,12,26,44,58,61,52,38,31,34,47,58,49,36,27,21,17,14,12]
W,H = 680,196
L,R,T,B = 38,62,30,26
pw, ph = W-L-R, H-T-B
_, ymax, YT = nice_domain(done + queue)
X = lambda i: L + pw*i/(len(done)-1)
Y = lambda v: T + ph*(1 - v/ymax)

s1 = " ".join(f"{f(X(i))},{f(Y(v))}" for i,v in enumerate(done))
s2 = " ".join(f"{f(X(i))},{f(Y(v))}" for i,v in enumerate(queue))
area1 = f"M{f(L)},{f(T+ph)} L" + " L".join(f"{f(X(i))},{f(Y(v))}" for i,v in enumerate(done)) + f" L{f(L+pw)},{f(T+ph)} Z"
# 只有主系列铺面积：两层 0.12 面积叠在一起会混色发脏，还会被读成堆叠

grid = "".join(f'<line x1="{f(L)}" y1="{f(Y(v))}" x2="{f(L+pw)}" y2="{f(Y(v))}"/>' for v in YT[1:])
yticks = "".join(f'<text class="ui-chart-tick" x="{f(L-8)}" y="{f(Y(v)+4)}" text-anchor="end">{v}</text>' for v in YT)
XT = (0,6,12,18,23)
xticks = "".join(f'<text class="ui-chart-tick" x="{f(X(i))}" y="{f(T+ph+16)}" '
                 f'text-anchor="{"start" if i==XT[0] else "end" if i==XT[-1] else "middle"}">{i:02d}:00</text>'
                 for i in XT)   # 首末刻度向内对齐：不和 Y 轴「0」撞角，也不越出右边界

# 事件标记：时刻，不是值。标签放在绘图区上方的留白里，最多 3 个
EVENTS = [(8, "发版 v2.4", None), (15, "扩容 +2 节点", "ui-cok")]
assert len(EVENTS) <= 3
events1 = "".join(
    f'<g class="ui-chart-event {cls or ""}"><line x1="{f(X(i))}" y1="{T-6}" x2="{f(X(i))}" y2="{f(T+ph)}"/>'
    f'<circle cx="{f(X(i))}" cy="{T-6}" r="3"/>'
    f'<text x="{f(X(i)+7)}" y="{T-2}">{label}</text></g>' for i, label, cls in EVENTS)
hits = []
for i,(a,b) in enumerate(zip(done,queue)):
    x = X(i); half = pw/(len(done)-1)/2
    bx = max(L, x-half); bw = min(half*2, L+pw-bx)
    tw, th = 124, 56
    tx = x+10 if x < L+pw*0.6 else x-tw-10
    ty = 8 if min(Y(a), Y(b)) > T + ph*0.5 else T + ph - th - 4   # 值在上半区时放到下方，不挡拐点
    hits.append(
      f'<g class="ui-chart-hit" tabindex="0" role="img" aria-label="{i:02d}:00 完成 {a} 段每分，等待 {b} 段每分">'
      f'<rect class="box" x="{f(bx)}" y="{f(T)}" width="{f(bw)}" height="{f(ph)}"/>'
      f'<line class="cross" x1="{f(x)}" y1="{f(T)}" x2="{f(x)}" y2="{f(T+ph)}"/>'
      f'<g class="peak"><circle class="ui-chart-dot ui-s1" cx="{f(x)}" cy="{f(Y(a))}" r="3.5"/>'
      f'<circle class="ui-chart-dot ui-s2" cx="{f(x)}" cy="{f(Y(b))}" r="3.5"/></g>'
      f'<g class="tip"><rect class="ui-chart-tip-bg" x="{f(tx)}" y="{ty}" width="{tw}" height="{th}"/>'
      f'<text class="ui-chart-tip-t" x="{f(tx+10)}" y="{ty+17}">{i:02d}:00</text>'
      f'<text class="ui-chart-tip-k" x="{f(tx+10)}" y="{ty+34}">完成</text>'
      f'<text class="ui-chart-tip-v" x="{f(tx+tw-10)}" y="{ty+34}" text-anchor="end">{a}</text>'
      f'<text class="ui-chart-tip-k" x="{f(tx+10)}" y="{ty+49}">等待</text>'
      f'<text class="ui-chart-tip-v" x="{f(tx+tw-10)}" y="{ty+49}" text-anchor="end">{b}</text></g></g>')

w(f'''        <div class="ui-card">
          <div class="ui-chart">
            <div class="ui-chart-head">
              <div>
                <h3 class="ui-chart-title">吞吐量与等待队列</h3>
                <p class="ui-chart-sub">过去 24 小时，单位：段 / 分钟</p>
              </div>
              <div class="ui-chart-legend ui-chart-tools">
                <span class="ui-chart-legend-item ui-s1" data-s="1"><i class="sw line"></i>完成吞吐<span class="val">{done[-1]}</span></span>
                <span class="ui-chart-legend-item ui-s2" data-s="2"><i class="sw line"></i>等待队列<span class="val">{queue[-1]}</span></span>
              </div>
            </div>
            <div class="ui-chart-body" style="--vbw:{W}">
              <svg viewBox="0 0 {W} {H}" role="group" aria-label="24 小时吞吐量与等待队列折线图">
                <g class="ui-chart-grid">{grid}</g>
                <path class="ui-chart-area ui-s1" data-s="1" d="{area1}"/>
                <polyline class="ui-chart-line ui-s2" data-s="2" points="{s2}"/>
                <polyline class="ui-chart-line ui-s1" data-s="1" points="{s1}"/>
                <circle class="ui-chart-dot ui-s1" cx="{f(X(23))}" cy="{f(Y(done[-1]))}" r="3.5"/>
                <text class="ui-chart-label" x="{f(X(23)+8)}" y="{f(Y(done[-1])+4)}">{done[-1]}</text>
                <line class="ui-chart-axis" x1="{f(L)}" y1="{f(T+ph)}" x2="{f(L+pw)}" y2="{f(T+ph)}"/>
                {yticks}{xticks}
                {events1}
                {''.join(hits)}
              </svg>
            </div>
            <div class="ui-chart-foot"><span>峰值 {max(done)} 段/分（{done.index(max(done)):02d}:00）· 竖线＝事件</span><span>均值 {round(sum(done)/len(done))} 段/分</span></div>
            <details class="ui-chart-a11y">
              <summary>数据表格</summary>
              <div class="wrap"><table class="ui-table">
                <thead><tr><th>时间</th><th class="num">完成吞吐</th><th class="num">等待队列</th></tr></thead>
                <tbody>{''.join(f"<tr><td>{i:02d}:00</td><td class='num'>{a}</td><td class='num'>{b}</td></tr>" for i,(a,b) in enumerate(zip(done,queue)) if i%3==0)}</tbody>
              </table></div>
            </details>
          </div>
        </div>''')

# ============ 图 2：终态分布（环形，状态色） ============
parts = [("成功",113,"ui-cok"),("重试",12,"ui-cwarn"),("失败",3,"ui-cdanger")]
total = sum(p[1] for p in parts)
r = 54; C = 2*3.141592653589793*r; gap = 3
off = 0; arcs = []
for name,v,cls in parts:
    seg = C*v/total
    arcs.append(f'<circle class="ui-chart-ring {cls}" cx="80" cy="80" r="{r}" '
                f'stroke-dasharray="{f(max(seg-gap,1))} {f(C-max(seg-gap,1))}" stroke-dashoffset="{f(-off)}"/>')
    off += seg
w(f'''        <div class="ui-card">
          <div class="ui-chart">
            <div class="ui-chart-head"><div>
              <h3 class="ui-chart-title">任务终态分布</h3>
              <p class="ui-chart-sub">今日累计 {total} 个批次</p>
            </div></div>
            <div class="ui-chart-body square" style="--vbw:160">
              <svg viewBox="0 0 160 160" role="img" aria-label="任务终态环形图：{'、'.join(f'{n} {v}' for n,v,_ in parts)}">
                <g transform="rotate(-90 80 80)">
                  <circle class="ui-chart-ring-track" cx="80" cy="80" r="{r}"/>
                  {''.join(arcs)}
                </g>
                <text class="ui-chart-center-num" x="80" y="80">{total}</text>
                <text class="ui-chart-center-cap" x="80" y="106">总批次</text>
              </svg>
            </div>
            <div class="ui-chart-legend" style="flex-direction:column;align-items:flex-start;gap:6px">
{''.join(f'<span class="ui-chart-legend-item {cls}"><i class="sw dot"></i>{n}<span class="val">{v}</span><span>{v/total*100:.1f}%</span></span>' for n,v,cls in parts)}
            </div>
            <details class="ui-chart-a11y"><summary>数据表格</summary><div class="wrap"><table class="ui-table">
              <thead><tr><th>终态</th><th class="num">批次</th><th class="num">占比</th></tr></thead>
              <tbody>{''.join(f'<tr><td>{n}</td><td class="num">{v}</td><td class="num">{v/total*100:.1f}%</td></tr>' for n,v,_ in parts)}</tbody>
            </table></div></details>
          </div>
        </div>''')

# ============ 图 3：阶段耗时 Top 5（横向条形，单系列） ============
rows = [("视频切分",42),("台词翻译",38),("字幕对齐",24),("音轨合成",18),("质量校验",12)]
W3,H3 = 312,178; L3,R3 = 62,34; T3 = 6
bw3 = W3-L3-R3; mx = nice_domain([v for _,v in rows], include=[60])[1] * 1.1; rowh = (H3-T3-14)/len(rows); bh = 14
bars = []
for i,(name,v) in enumerate(rows):
    y = T3 + rowh*i + (rowh-bh)/2
    wd = bw3*v/mx
    bars.append(
      f'<g class="ui-chart-hit" tabindex="0" role="img" aria-label="{name} {v} 秒">'
      f'<rect class="box" x="0" y="{f(T3+rowh*i)}" width="{W3}" height="{f(rowh)}"/>'
      f'<path class="ui-chart-bar ui-s1" d="{bar_h(L3,y,wd,bh)}"/>'
      f'<path class="ui-chart-tex" d="{bar_h(L3,y,wd,bh)}"/>'
      f'<text class="ui-chart-tick name" x="{L3-8}" y="{f(y+bh-3)}" text-anchor="end">{name}</text>'
      f'<text class="ui-chart-label" x="{f(L3+wd+8)}" y="{f(y+bh-3)}">{v}s</text></g>')
rule_x = L3 + bw3*60/mx   # 60s 超时阈值（落在轴外就说明标尺不对）
rule3 = (f'<line class="ui-chart-rule" x1="{f(rule_x)}" y1="{T3}" x2="{f(rule_x)}" y2="{H3-14}"/>'
         f'<text class="ui-chart-rule-label" x="{f(rule_x)}" y="{H3-4}" text-anchor="middle">阈值 60s</text>') if rule_x < W3 else ""
w(f'''        <div class="ui-card">
          <div class="ui-chart">
            <div class="ui-chart-head"><div>
              <h3 class="ui-chart-title">阶段耗时 Top 5</h3>
              <p class="ui-chart-sub">单次批处理中位耗时，单位：秒</p>
            </div></div>
            <div class="ui-chart-body" style="--vbw:{W3}">
              <svg viewBox="0 0 {W3} {H3}" role="group" aria-label="阶段耗时横向条形图">
                <line class="ui-chart-axis" x1="{L3}" y1="{T3}" x2="{L3}" y2="{H3-14}"/>
                {rule3}
                {''.join(bars)}
              </svg>
            </div>
            <div class="ui-chart-foot"><span>单系列不配图例，单位写在副标题</span><span>虚线＝超时阈值</span></div>
            <details class="ui-chart-a11y"><summary>数据表格</summary><div class="wrap"><table class="ui-table">
              <thead><tr><th>阶段</th><th class="num">耗时</th></tr></thead>
              <tbody>{''.join(f"<tr><td>{n}</td><td class='num'>{v}s</td></tr>" for n,v in rows)}</tbody>
            </table></div></details>
          </div>
        </div>''')

# ============ 图 4：近 7 日峰值（纵向柱状） ============
days = [("周一",108),("周二",121),("周三",96),("周四",134),("周五",166),("周六",73),("周日",61)]
W4,H4 = 312,168; L4,R4,T4,B4 = 26,64,20,22
pw4, ph4 = W4-L4-R4, H4-T4-B4; _, mx4, YT4 = nice_domain([v for _,v in days])
slot = pw4/len(days); bw4 = 18
cols = []
for i,(d,v) in enumerate(days):
    x = L4 + slot*i + (slot-bw4)/2
    h = ph4*v/mx4; y = T4+ph4-h
    cols.append(
      f'<g class="ui-chart-hit" tabindex="0" role="img" aria-label="{d} 峰值 {v}">'
      f'<rect class="box" x="{f(L4+slot*i)}" y="{T4}" width="{f(slot)}" height="{f(ph4)}"/>'
      f'<path class="ui-chart-bar ui-s1" d="{bar_v(x,y,bw4,h)}"/>'
      f'<path class="ui-chart-tex" d="{bar_v(x,y,bw4,h)}"/>'
      f'<text class="ui-chart-label" x="{f(x+bw4/2)}" y="{f(y-6)}" text-anchor="middle">{v}</text>'
      f'<text class="ui-chart-tick name" x="{f(x+bw4/2)}" y="{f(T4+ph4+16)}" text-anchor="middle">{d[1]}</text></g>')
avg4 = round(sum(v for _,v in days)/len(days))
grid4 = "".join(f'<line x1="{L4}" y1="{f(T4+ph4-ph4*v/mx4)}" x2="{f(L4+pw4)}" y2="{f(T4+ph4-ph4*v/mx4)}"/>' for v in YT4[1:])
yt4 = "".join(f'<text class="ui-chart-tick" x="{L4-6}" y="{f(T4+ph4-ph4*v/mx4+4)}" text-anchor="end">{v}</text>' for v in (YT4[0], YT4[-1]))
w(f'''        <div class="ui-card">
          <div class="ui-chart">
            <div class="ui-chart-head"><div>
              <h3 class="ui-chart-title">近 7 日并发峰值</h3>
              <p class="ui-chart-sub">每日最高并发任务数</p>
            </div></div>
            <div class="ui-chart-body" style="--vbw:{W4}">
              <svg viewBox="0 0 {W4} {H4}" role="group" aria-label="近 7 日并发峰值柱状图">
                <g class="ui-chart-grid">{grid4}</g>
                {''.join(cols)}
                <line class="ui-chart-rule" x1="{L4}" y1="{f(T4+ph4-ph4*avg4/mx4)}" x2="{f(L4+pw4)}" y2="{f(T4+ph4-ph4*avg4/mx4)}"/>
                <text class="ui-chart-rule-label" x="{f(L4+pw4+6)}" y="{f(T4+ph4-ph4*avg4/mx4+4)}">均值 {avg4}</text>
                <line class="ui-chart-axis" x1="{L4}" y1="{f(T4+ph4)}" x2="{f(L4+pw4)}" y2="{f(T4+ph4)}"/>
                {yt4}
              </svg>
            </div>
            <div class="ui-chart-foot"><span>只圆柱顶，柱脚直角贴基线</span><span>最高 {max(days, key=lambda d: d[1])[0]} {max(v for _,v in days)}</span></div>
            <details class="ui-chart-a11y"><summary>数据表格</summary><div class="wrap"><table class="ui-table">
              <thead><tr><th>日期</th><th class="num">峰值并发</th></tr></thead>
              <tbody>{''.join(f"<tr><td>{d}</td><td class='num'>{v}</td></tr>" for d,v in days)}</tbody>
            </table></div></details>
          </div>
        </div>''')

# ============ 图 5：节点 × 时段 热力（顺序渐变） ============
import math
nodes = ["node-01","node-02","node-03","node-04","node-05","node-06"]
vals = [[(i*7+j*11+ (i*j)%13) % 100 for j in range(12)] for i in range(len(nodes))]
cell, cg = 14, 2
L5, T5 = 52, 12
W5 = L5 + 12*(cell+cg) + 4; H5 = T5 + len(nodes)*(cell+cg) + 16
cells = []
for i,row in enumerate(vals):
    for j,v in enumerate(row):
        q = min(7, max(1, math.ceil(v/100*7) or 1))
        x = L5 + j*(cell+cg); y = T5 + i*(cell+cg)
        cells.append(f'<rect class="ui-chart-cell ui-q{q}" x="{x}" y="{y}" width="{cell}" height="{cell}">'
                     f'<title>{nodes[i]} {j*2:02d}:00 利用率 {v}%</title></rect>')
    cells.append(f'<text class="ui-chart-tick id" x="{L5-6}" y="{T5+i*(cell+cg)+11}" text-anchor="end">{nodes[i]}</text>')
for j in (0,3,6,9):
    cells.append(f'<text class="ui-chart-tick" x="{L5+j*(cell+cg)+cell/2}" y="{T5+len(nodes)*(cell+cg)+12}" text-anchor="middle">{j*2:02d}</text>')
steps = "".join(f'<i class="ui-q{k}"></i>' for k in range(1,8))
w(f'''        <div class="ui-card">
          <div class="ui-chart">
            <div class="ui-chart-head"><div>
              <h3 class="ui-chart-title">节点调度热力</h3>
              <p class="ui-chart-sub">6 节点 × 12 个两小时桶，利用率</p>
            </div></div>
            <div class="ui-chart-body" style="--vbw:{W5}">
              <svg viewBox="0 0 {W5} {H5}" role="img" aria-label="节点调度热力图，6 节点 24 小时利用率">
                {''.join(cells)}
              </svg>
            </div>
            <div class="ui-chart-scale"><span>低</span><span class="steps">{steps}</span><span>高</span></div>
            <div class="ui-chart-foot"><span>单色相，离画布越远＝值越大</span><span>峰值 {max(max(r) for r in vals)}% {nodes[max(range(len(vals)), key=lambda i: max(vals[i]))]}</span></div>
            <details class="ui-chart-a11y"><summary>数据表格</summary><div class="wrap"><table class="ui-table">
              <thead><tr><th>节点</th><th class="num">均值</th><th class="num">峰值</th></tr></thead>
              <tbody>{''.join(f"<tr><td>{n}</td><td class='num'>{sum(r)//len(r)}%</td><td class='num'>{max(r)}%</td></tr>" for n,r in zip(nodes,vals))}</tbody>
            </table></div></details>
          </div>
        </div>''')

# ============ 图 6：同比增减（发散条形） ============
div = [("视频切分",+34),("台词翻译",+18),("字幕对齐",+6),("音轨合成",-4),("质量校验",-21),("归档导出",-38)]
W6,H6 = 500,184; L6 = 76; T6 = 6
axis6 = L6 + (W6-L6-8)/2
half = (W6-L6-8)/2 - 34
rowh6 = (H6-T6)/len(div); bh6 = 14
dbars = []
for i,(n,v) in enumerate(div):
    y = T6 + rowh6*i + (rowh6-bh6)/2
    wd = half*abs(v)/40
    if v >= 0:   # 变慢 = 暖红一极
        cls = "ui-dn2" if v >= 20 else "ui-dn1"
        d = bar_h(axis6, y, wd, bh6, side='right'); tx, anc = axis6+wd+6, "start"
    else:        # 变快 = 冷蓝一极
        cls = "ui-dp2" if v <= -20 else "ui-dp1"
        d = bar_h(axis6-wd, y, wd, bh6, side='left'); tx, anc = axis6-wd-6, "end"
    dbars.append(
      f'<g class="ui-chart-hit" tabindex="0" role="img" aria-label="{n} 同比 {v:+d}%">'
      f'<rect class="box" x="0" y="{f(T6+rowh6*i)}" width="{W6}" height="{f(rowh6)}"/>'
      f'<path class="ui-chart-bar {cls}" d="{d}"/><path class="ui-chart-tex{" alt" if v<0 else ""}" d="{d}"/>'
      f'<text class="ui-chart-tick name" x="{L6-8}" y="{f(y+bh6-3)}" text-anchor="end">{n}</text>'
      f'<text class="ui-chart-label" x="{f(tx)}" y="{f(y+bh6-3)}" text-anchor="{anc}">{v:+d}%</text></g>')
w(f'''        <div class="ui-card">
          <div class="ui-chart">
            <div class="ui-chart-head"><div>
              <h3 class="ui-chart-title">阶段耗时同比</h3>
              <p class="ui-chart-sub">对比上周同期，正为变慢、负为变快</p>
            </div></div>
            <div class="ui-chart-body" style="--vbw:{W6}">
              <svg viewBox="0 0 {W6} {H6}" role="group" aria-label="阶段耗时同比发散条形图">
                {''.join(dbars)}
                <line class="ui-chart-axis" x1="{f(axis6)}" y1="{T6}" x2="{f(axis6)}" y2="{H6}"/>
              </svg>
            </div>
            <div class="ui-chart-legend">
              <span class="ui-chart-legend-item ui-dp2"><i class="sw"></i>变快</span>
              <span class="ui-chart-legend-item ui-dmid"><i class="sw"></i>持平</span>
              <span class="ui-chart-legend-item ui-dn2"><i class="sw"></i>变慢</span>
            </div>
            <details class="ui-chart-a11y"><summary>数据表格</summary><div class="wrap"><table class="ui-table">
              <thead><tr><th>阶段</th><th class="num">同比</th></tr></thead>
              <tbody>{''.join(f"<tr><td>{n}</td><td class='num'>{v:+d}%</td></tr>" for n,v in div)}</tbody>
            </table></div></details>
          </div>
        </div>''')

# ============ 图 7：来源构成（堆叠柱，2px 缝） ============
# 第 4 段是长尾归并出来的「其他」——不是第 4 个色相，用中性灰
stack = [("周一",[48,32,28,9]),("周二",[56,30,35,11]),("周三",[41,26,29,7]),
         ("周四",[62,38,34,12]),("周五",[71,44,51,14]),("周六",[33,18,22,6]),("周日",[28,15,0,5])]   # 周日 API 为 0：不画、不留缝
SEG_CLS = ["ui-s1","ui-s2","ui-s3","ui-sother"]; SEG_KEY = ["1","2","3","other"]
W7,H7 = 500,184; L7,R7,T7,B7 = 30,10,12,22
pw7, ph7 = W7-L7-R7, H7-T7-B7; _, mx7, YT7 = nice_domain([sum(v) for _,v in stack]); SEG_NAME = ["定时","手动","API","其他"]
slot7 = pw7/len(stack); bw7 = 26
segs = []
for i,(d,vs) in enumerate(stack):
    x = L7 + slot7*i + (slot7-bw7)/2
    acc = 0
    nz = [k for k,v in enumerate(vs) if v > 0]   # 0 值不画：画 1px 等于把「没有」说成「有一点」
    for k,v in enumerate(vs):
        if v <= 0:
            continue
        h = ph7*v/mx7
        y = T7+ph7-(ph7*(acc+v)/mx7)
        gap = 0 if k == nz[0] else 2                 # 缝只留在段与段之间，最底段贴基线
        hh = max(h-gap, 1)
        d_ = bar_v(x, y, bw7, hh) if k == nz[-1] else f"M{f(x)},{f(y)} h{bw7} v{f(hh)} h-{bw7} Z"   # 圆角给最上面的非零段
        segs.append(f'<path class="ui-chart-bar {SEG_CLS[k]}" data-s="{SEG_KEY[k]}" d="{d_}">'
                    f'<title>{d} {SEG_NAME[k]} {v}</title></path>')
        acc += v
    segs.append(f'<text class="ui-chart-tick name" x="{f(x+bw7/2)}" y="{f(T7+ph7+16)}" text-anchor="middle">{d[1]}</text>')
grid7 = "".join(f'<line x1="{L7}" y1="{f(T7+ph7-ph7*v/mx7)}" x2="{f(L7+pw7)}" y2="{f(T7+ph7-ph7*v/mx7)}"/>' for v in YT7[1:])
yt7 = "".join(f'<text class="ui-chart-tick" x="{L7-6}" y="{f(T7+ph7-ph7*v/mx7+4)}" text-anchor="end">{v}</text>' for v in (YT7[0], YT7[-1]))
w(f'''        <div class="ui-card">
          <div class="ui-chart">
            <div class="ui-chart-head">
              <div>
                <h3 class="ui-chart-title">任务来源构成</h3>
                <p class="ui-chart-sub">近 7 日按触发来源堆叠</p>
              </div>
              <div class="ui-chart-legend ui-chart-tools">
                <span class="ui-chart-legend-item ui-s1" data-s="1"><i class="sw"></i>定时</span>
                <span class="ui-chart-legend-item ui-s2" data-s="2"><i class="sw"></i>手动</span>
                <span class="ui-chart-legend-item ui-s3" data-s="3"><i class="sw"></i>API</span>
                <span class="ui-chart-legend-item ui-sother" data-s="other"><i class="sw"></i>其他</span>
              </div>
            </div>
            <div class="ui-chart-body" style="--vbw:{W7}">
              <svg viewBox="0 0 {W7} {H7}" role="group" aria-label="任务来源堆叠柱状图">
                <g class="ui-chart-grid">{grid7}</g>
                {''.join(segs)}
                {yt7}
                <line class="ui-chart-axis" x1="{L7}" y1="{f(T7+ph7)}" x2="{f(L7+pw7)}" y2="{f(T7+ph7)}"/>
              </svg>
            </div>
            <div class="ui-chart-foot"><span>长尾归并成灰色「其他」，不生成第 4 个色相</span><span>合计 {sum(sum(v) for _,v in stack)}</span></div>
            <details class="ui-chart-a11y"><summary>数据表格</summary><div class="wrap"><table class="ui-table">
              <thead><tr><th>日期</th><th class="num">定时</th><th class="num">手动</th><th class="num">API</th><th class="num">其他</th></tr></thead>
              <tbody>{''.join(f"<tr><td>{d}</td>" + "".join(f"<td class='num'>{x}</td>" for x in v) + "</tr>" for d,v in stack)}</tbody>
            </table></div></details>
          </div>
        </div>''')


# ============ 图 8：资源配额（子弹图，HTML） ============
quota = [("CPU", 62, 80, "%"), ("内存", 91, 85, "%"), ("存储", 40, 70, "%"), ("并发槽", 18, 20, "")]
rows8 = []
for n, actual, target, unit in quota:
    assert 0 <= actual <= 100 and 0 < target <= 100, "子弹图值域固定 0–100，越界说明单位错了"
    over = actual > target
    badge = '<span class="ui-badge danger"><span class="ui-dot"></span>超配额</span>' if over else ''
    cap = 24 if n == "并发槽" else 100        # 并发槽是计数，换算到轨道百分比
    a_pct, t_pct = actual / cap * 100, target / cap * 100
    rows8.append(
      f'<span class="name">{n}</span>'
      f'<span class="track" role="img" aria-label="{n} 实际 {actual}{unit}，目标 {target}{unit}{"，已超出" if over else ""}">'
      f'<span class="bar" style="width:{a_pct:.1f}%"></span><span class="target" style="left:{t_pct:.1f}%"></span></span>'
      f'<span class="nums"><b>{actual}{unit}</b> / {target}{unit}</span><span class="flag">{badge}</span>')
w(f"""        <div class="ui-card">
          <div class="ui-chart">
            <div class="ui-chart-head"><div>
              <h3 class="ui-chart-title">资源配额</h3>
              <p class="ui-chart-sub">实条＝实际用量，竖线＝目标；超出用徽章说明，不靠变色</p>
            </div></div>
            <div class="ui-bullet">{''.join(rows8)}</div>
            <div class="ui-chart-foot"><span>.ui-bullet · 纯 HTML，与 .ui-progress 同一套轨道语言</span><span>{sum(1 for _, a, t, _ in quota if a > t)} 项超配额</span></div>
          </div>
        </div>""")

# ============ 图 9：表格里的占比条（.ui-meter 嵌进 .ui-table） ============
batches = [("batch-07", [41, 3, 0]), ("batch-06", [36, 6, 2]), ("batch-05", [29, 2, 1]), ("batch-04", [7, 1, 0])]
METER = [("成功", "ui-cok"), ("重试", "ui-cwarn"), ("失败", "ui-cdanger")]
trs = []
for name, vs in batches:
    tot = sum(vs); assert tot > 0
    segs9 = "".join(f'<i class="{cls}" style="flex-grow:{v}"></i>' for v, (_, cls) in zip(vs, METER) if v > 0)   # 0 值不画
    label = "，".join(f"{n} {v}" for v, (n, _) in zip(vs, METER))
    trs.append(f'<tr><td class="num">{name}</td><td><span class="ui-meter" role="img" aria-label="{name}：{label}">{segs9}</span></td>'
               f'<td class="num">{tot}</td><td class="num">{vs[0]/tot*100:.0f}%</td></tr>')
w(f"""        <div class="ui-card">
          <div class="ui-chart">
            <div class="ui-chart-head">
              <div>
                <h3 class="ui-chart-title">批次结果构成</h3>
                <p class="ui-chart-sub">占比条直接放进表格行，扫一眼就能比</p>
              </div>
              <div class="ui-chart-legend ui-chart-tools">
                {''.join(f'<span class="ui-chart-legend-item {cls}"><i class="sw dot"></i>{n}</span>' for n, cls in METER)}
              </div>
            </div>
            <table class="ui-table">
              <thead><tr><th>批次</th><th style="width:45%">构成</th><th class="num">段数</th><th class="num">成功率</th></tr></thead>
              <tbody>{''.join(trs)}</tbody>
            </table>
            <div class="ui-chart-foot"><span>.ui-meter · 按原始数值 flex-grow 分配，0 值不画</span><span>状态色不占分类槽</span></div>
          </div>
        </div>""")


# ============ 图 10：小倍数（6 个节点，共用同一纵轴） ============
import math as _m
mnodes = ["node-01","node-02","node-03","node-04","node-05","node-06"]
series10 = [[round(40 + 35*_m.sin((j + i*2) / 3.2) + i*9 + (j % 5)) for j in range(24)] for i in range(len(mnodes))]
_, mx10, _ = nice_domain([v for r in series10 for v in r])   # 共用纵轴：全部格子取同一个上限
VW, VH = 150, 44
cells10 = []
for n, r in zip(mnodes, series10):
    pts = " ".join(f"{f(VW*j/(len(r)-1))},{f(VH*(1 - v/mx10))}" for j, v in enumerate(r))
    cells10.append(f'<div class="cell"><div class="head"><span class="id">{n}</span><b>{r[-1]}</b></div>'
                   f'<svg viewBox="0 0 {VW} {VH}" preserveAspectRatio="none" role="img" aria-label="{n} 24 小时吞吐，末值 {r[-1]}，峰值 {max(r)}">'
                   f'<line class="ui-chart-axis" x1="0" y1="{VH}" x2="{VW}" y2="{VH}"/>'
                   f'<polyline class="ui-chart-line ui-s1" points="{pts}"/></svg></div>')
w(f"""        <div class="ui-card">
          <div class="ui-chart">
            <div class="ui-chart-head"><div>
              <h3 class="ui-chart-title">各节点吞吐</h3>
              <p class="ui-chart-sub">6 条线挤一张图会成面条，拆成小倍数逐格比</p>
            </div></div>
            <div class="ui-multiples">{''.join(cells10)}</div>
            <div class="ui-chart-foot"><span>所有格子共用纵轴 0–{mx10} 段/分 · 同一颜色，身份看格子标题</span><span>.ui-multiples</span></div>
            <details class="ui-chart-a11y"><summary>数据表格</summary><div class="wrap"><table class="ui-table">
              <thead><tr><th>节点</th><th class="num">末值</th><th class="num">峰值</th><th class="num">均值</th></tr></thead>
              <tbody>{''.join(f"<tr><td class='num'>{n}</td><td class='num'>{r[-1]}</td><td class='num'>{max(r)}</td><td class='num'>{round(sum(r)/len(r))}</td></tr>" for n, r in zip(mnodes, series10))}</tbody>
            </table></div></details>
          </div>
        </div>""")

section = f'''      <!-- 图表 / data viz -->
      <p class="sec-label">图表</p>
      <div class="row" style="margin:-4px 0 -8px">
        <span class="ui-muted" style="font-size:12px">图表色板与色系/强调色正交：切上面的色系或强调色，图表配色不变。</span>
        <label class="ui-check" style="margin-left:auto"><input type="checkbox" onchange="document.documentElement.dataset.chartTexture = this.checked ? 'on' : ''"><span>纹理通道（CVD / 打印）</span></label>
      </div>
      <svg width="0" height="0" aria-hidden="true" focusable="false" style="position:absolute">
        <defs>
          <pattern id="ui-tex-45" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
            <line class="ui-tex-line" x1="0" y1="0" x2="0" y2="6"/>
          </pattern>
          <pattern id="ui-tex-135" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(135)">
            <line class="ui-tex-line" x1="0" y1="0" x2="0" y2="6"/>
          </pattern>
        </defs>
      </svg>
      <div class="grid-chart-a">
{out[0]}
{out[1]}
      </div>
      <div class="grid-3">
{out[2]}
{out[3]}
{out[4]}
      </div>
      <div class="grid-chart-b">
{out[5]}
{out[6]}
      </div>
      <div class="grid-chart-b">
{out[7]}
{out[8]}
      </div>
{out[9]}
      <div class="grid-2">
        <div class="ui-card">
          <div class="ui-chart">
            <div class="ui-chart-head"><div>
              <h3 class="ui-chart-title">加载中</h3>
              <p class="ui-chart-sub">骨架占位与真图等高，数据回来时页面不跳</p>
            </div></div>
            <div class="ui-chart-body compact">
              <div class="ui-chart-skeleton" role="status" aria-label="图表加载中">
                <i style="height:46%"></i><i style="height:68%"></i><i style="height:52%"></i><i style="height:81%"></i>
                <i style="height:63%"></i><i style="height:92%"></i><i style="height:57%"></i>
              </div>
            </div>
            <div class="ui-chart-foot"><span>.ui-chart-skeleton</span><span>减少动态偏好下停止微光</span></div>
          </div>
        </div>
        <div class="ui-card">
          <div class="ui-chart">
            <div class="ui-chart-head"><div>
              <h3 class="ui-chart-title">暂无数据</h3>
              <p class="ui-chart-sub">空态说清楚为什么空、下一步做什么</p>
            </div></div>
            <div class="ui-chart-body compact">
              <div class="ui-chart-empty">
                <span class="glyph" aria-hidden="true">◇</span>
                <span class="title">所选时间段内没有任务运行</span>
                <span class="desc">换个时间范围，或先跑一个批次</span>
              </div>
            </div>
            <div class="ui-chart-foot"><span>.ui-chart-empty</span><span>与 .ui-empty 同一套视觉语言</span></div>
          </div>
        </div>
      </div>
'''

import os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def splice(path, end_anchor):
    s = open(path).read()
    i = s.index('      <!-- 图表 / data viz -->')
    j = s.index(end_anchor)
    open(path, 'w').write(s[:i] + section + '\n' + s[j:])

splice(os.path.join(ROOT, 'assets/demo.html'), '      <!-- 数据表格 + 分页 -->')
sa = os.path.join(ROOT, 'assets/demo.standalone.html')
splice(sa, '      <div class="ui-card">\n        <div class="row" style="margin-bottom:12px">')

# 单文件版同步内联最新 tokens.css / base.css
s = open(sa).read()
tok = open(os.path.join(ROOT, 'assets/tokens.css')).read().rstrip()
base = open(os.path.join(ROOT, 'assets/base.css')).read().rstrip()
m1 = s[s.index('/* ===== tokens.css'):s.index('（light-dark 单份定义，原样内联）===== */') + len('（light-dark 单份定义，原样内联）===== */')]
ver = tok.split('tokens v', 1)[1].split(' ', 1)[0]
m2 = '/* ===== base.css（原样内联）===== */'
m3 = '/* ===== demo 页面自身排版（不属于设计体系）===== */'
s = (s[:s.index(m1)] + f'/* ===== tokens.css v{ver}（light-dark 单份定义，原样内联）===== */\n' + tok
     + '\n\n' + m2 + '\n' + base + '\n\n' + s[s.index(m3):])
open(sa, 'w').write(s)
print('已重建 assets/demo.html 与 assets/demo.standalone.html 的图表分区')
