#!/usr/bin/env python3
"""从 tokens.css 解析 palette/accent，跑 色系 × 强调色 × 明暗 全矩阵 WCAG 校验。"""
import re, sys, colorsys
CSS = open('assets/tokens.css').read()
def lin(c):
    c/=255
    return c/12.92 if c<=0.03928 else ((c+0.055)/1.055)**2.4
def L_(h):
    h=h.lstrip('#')
    if len(h)==3: h=''.join(x*2 for x in h)
    return sum(k*lin(int(h[i:i+2],16)) for k,i in ((0.2126,0),(0.7152,2),(0.0722,4)))
def ratio(a,b):
    la,lb=L_(a),L_(b); hi,lo=max(la,lb),min(la,lb); return (hi+0.05)/(lo+0.05)
def hls(h):
    h=h.lstrip('#'); r,g,b=[int(h[i:i+2],16)/255 for i in (0,2,4)]
    H,L,S=colorsys.rgb_to_hls(r,g,b); return H*360,L*100,S*100
def pb(t):
    return {m.group(1):(m.group(2),m.group(3)) for m in
            re.finditer(r'(--[\w-]+):\s*light-dark\(\s*(#[0-9a-fA-F]{3,6})\s*,\s*(#[0-9a-fA-F]{3,6})\s*\)', t)}

root = CSS.split(':root {',1)[1].split('\n}',1)[0]
base = pb(root)
NEU = ('--bg','--surface','--surface-2','--elevated','--text','--text-2','--text-3')
palettes = {'default': {k:base[k] for k in NEU if k in base}}
for m in re.finditer(r':root\[data-palette="([\w-]+)"\]\s*\{(.*?)\n\}', CSS, re.S):
    palettes[m.group(1)] = pb(m.group(2))
accents = {'green': {k:v for k,v in base.items() if k in ('--accent','--accent-text')}}
for m in re.finditer(r':root\[data-accent="([\w-]+)"\]\s*\{(.*?)\n\}', CSS, re.S):
    accents[m.group(1)] = pb(m.group(2))
sem = {k:base[k] for k in ('--ok','--warn','--danger') if k in base}

fails=[]
print(f"色系 {len(palettes)} 个 × 强调色 {len(accents)} 个 × 明暗 2 = {len(palettes)*len(accents)*2} 组合\n")
print("=== 1. 色系内部文字 + 画布明度带 ===")
for pn,p in palettes.items():
    for i,mode in enumerate(('light','dark')):
        bg,sf = p['--bg'][i], p['--surface'][i]
        _,Lbg,Sbg = hls(bg); _,Lsf,Ssf = hls(sf)
        # 浅色只卡上限（护眼：画布不许过亮）；下限由强调色真实对比度把关，
        # 因为 HLS 明度不是 WCAG 亮度的可靠代理（Gruvbox #fbf1c7 明度 88% 但对比度达标）。
        band = (Lbg<=96.5) if mode=='light' else (8<=Lbg<=19.5)
        if not band: fails.append(f"{pn}/{mode} 画布明度 {Lbg:.1f}% 越界")
        print(f"  {pn:9s} {mode:5s} bg L={Lbg:4.1f}% S={Sbg:4.1f}% {'✓' if band else '✗越界'}  surface L={Lsf:4.1f}%", end="")
        for tk,aa in (('--text',4.5),('--text-2',4.5),('--text-3',2.4)):
            if tk not in p: fails.append(f"{pn} 缺 {tk}"); continue
            for sn,sv in (('bg',bg),('surface',sf)):
                if tk=='--text-3' and sn=='surface': continue
                r=ratio(p[tk][i],sv)
                if r<aa: fails.append(f"{pn}/{mode} {tk} on {sn} = {r:.2f} < {aa}")
        print("")
print("\n=== 2. 强调色 × 色系 交叉矩阵（每色系最低值）===")
for pn,p in palettes.items():
    for i,mode in enumerate(('light','dark')):
        worst=(99,'')
        for an,a in accents.items():
            for tk in ('--accent','--accent-text'):
                if tk not in a: continue
                for sn in ('--bg','--surface'):
                    r=ratio(a[tk][i], p[sn][i])
                    if r<worst[0]: worst=(r,f"{an} {tk[2:]} on {sn[2:]}")
                    if r<4.5: fails.append(f"{pn}/{mode} {an}.{tk[2:]} on {sn[2:]} = {r:.2f}")
        print(f"  {pn:9s} {mode:5s} 最低 {worst[0]:5.2f}  ({worst[1]})")
print("\n=== 3. 语义状态色 × 色系 ===")
for pn,p in palettes.items():
    for i,mode in enumerate(('light','dark')):
        worst=(99,'')
        for sn_,sv in sem.items():
            r=ratio(sv[i], p['--bg'][i])
            if r<worst[0]: worst=(r,sn_[2:])
            if r<4.5: fails.append(f"{pn}/{mode} {sn_[2:]} on bg = {r:.2f}")
        print(f"  {pn:9s} {mode:5s} 最低 {worst[0]:5.2f}  ({worst[1]})")
print("\n=== 4. 色系互辨识度（任意两色系画布 RGB 通道差最大值须 ≥ 8）===")
def rgb(h):
    h=h.lstrip('#'); return [int(h[i:i+2],16) for i in (0,2,4)]
names=list(palettes)
for i,mode in enumerate(('light','dark')):
    for a in range(len(names)):
        for b in range(a+1,len(names)):
            ca,cb = palettes[names[a]]['--bg'][i], palettes[names[b]]['--bg'][i]
            d=max(abs(x-y) for x,y in zip(rgb(ca),rgb(cb)))
            tag = 'OK ' if d>=8 else 'FAIL'
            if d<8: fails.append(f"{mode} {names[a]} vs {names[b]} 画布仅差 {d}/255，肉眼难辨")
            if d<14: print(f"  {tag} 差 {d:3d}  {mode:5s} {names[a]} vs {names[b]}")
    print(f"  {mode}: 共 {len(names)*(len(names)-1)//2} 对，最小差值 " +
          str(min(max(abs(x-y) for x,y in zip(rgb(palettes[names[a]]['--bg'][i]),rgb(palettes[names[b]]['--bg'][i])))
                  for a in range(len(names)) for b in range(a+1,len(names)))))

print("\n=== 5. 护眼底线：浅色侧不得出现纯白 ===")
for pn,p_ in palettes.items():
    for tk in ('--bg','--surface','--elevated'):
        if tk not in p_: continue
        v=p_[tk][0].lower()
        if v in ('#ffffff','#fff'):
            fails.append(f"{pn} 浅色 {tk} 是纯白 {v}")
            print(f"  FAIL {pn} {tk} = {v}")
print("  浅色侧纯白检查完毕")

print("\n=== 6. 色阶方向（浅色 surface-2 下陷；暗色逐层提亮）===")
def hL(h):
    v=[int(h.lstrip('#')[i:i+2],16)/255 for i in (0,2,4)]
    import colorsys as _c; return _c.rgb_to_hls(*v)[1]*100
for pn,p_ in palettes.items():
    need=('--bg','--surface','--surface-2','--elevated')
    if any(t not in p_ for t in need): continue
    b,s_,s2,e=[hL(p_[t][0]) for t in need]
    if not (s2 < b < s_ < e):
        fails.append(f"{pn} 浅色色阶方向错（应 surface-2 < bg < surface < elevated）")
        print(f"  FAIL {pn} 浅色 s2={s2:.1f} bg={b:.1f} surface={s_:.1f} elevated={e:.1f}")
    d=[hL(p_[t][1]) for t in need]
    if not (d[0]<d[1]<d[2]<d[3]):
        fails.append(f"{pn} 暗色色阶非单调递增")
        print(f"  FAIL {pn} 暗色 " + " → ".join(f"{x:.1f}" for x in d))
print("  色阶方向检查完毕")

print("\n=== 7. 文字三档层级（text > text-2 > text-3，且各档至少拉开 1.0）===")
for pn,p_ in palettes.items():
    if any(t not in p_ for t in ('--text','--text-2','--text-3','--bg')): continue
    for i,mode in enumerate(('light','dark')):
        bg=p_['--bg'][i]
        v=[ratio(p_[t][i],bg) for t in ('--text','--text-2','--text-3')]
        if not (v[0]>v[1]>v[2] and (v[0]-v[1])>=1.0 and (v[1]-v[2])>=1.0):
            fails.append(f"{pn}/{mode} 文字层级倒挂或过近: {v[0]:.2f}/{v[1]:.2f}/{v[2]:.2f}")
            print(f"  FAIL {pn} {mode} {v[0]:.2f} / {v[1]:.2f} / {v[2]:.2f}")
print("  文字层级检查完毕")

print("\n=== 8. 图表色板 × 全部色系卡片面（图表画在 --surface 上）===")
chart = {k:v for k,v in base.items() if k.startswith('--chart-')}
CAT = [f'--chart-{i}' for i in range(1,9)]
SEQ = [f'--chart-seq-{i}' for i in range(1,8)]
ORD = [f'--chart-ord-{i}' for i in range(1,5)]
missing = [k for k in CAT+SEQ+ORD+['--chart-other'] if k not in chart]
if missing: fails.append("tokens.css 缺图表色: " + ",".join(missing))
for pn,p_ in palettes.items():
    for i,mode in enumerate(('light','dark')):
        sf = p_['--surface'][i]
        rs = [ratio(chart[k][i], sf) for k in CAT if k in chart]
        worst = min(rs); soft = sum(1 for r in rs if r < 3.0)
        # <2.0 视为在该底面上基本看不见 → FAIL；2.0~3.0 是「需直接标注/表格兜底」的 WARN 带
        if worst < 2.0: fails.append(f"{pn}/{mode} 分类色最低对比 {worst:.2f} < 2.0（卡片面上看不见）")
        print(f"  {pn:9s} {mode:5s} 分类色最低 {worst:4.2f}  需兜底(<3:1) {soft}/8", end="")
        # 顺序渐变：对比度必须随档位单调上升（1=近零 → 7=最大）
        sq = [ratio(chart[k][i], sf) for k in SEQ if k in chart]
        mono = all(b > a for a,b in zip(sq, sq[1:]))
        if not mono: fails.append(f"{pn}/{mode} 顺序渐变对比度非单调: " + "/".join(f"{x:.2f}" for x in sq))
        # 序数渐变：最靠近画布的一端仍要 ≥2:1
        od = min(ratio(chart[k][i], sf) for k in ORD if k in chart)
        if od < 2.0: fails.append(f"{pn}/{mode} 序数渐变近底端 {od:.2f} < 2.0")
        # 「其他」灰槽承载长尾，要求比分类色更硬：所有卡片面上都得 ≥3:1
        ot = ratio(chart['--chart-other'][i], sf) if '--chart-other' in chart else 0
        if ot < 3.0: fails.append(f"{pn}/{mode} 其他灰槽 {ot:.2f} < 3.0")
        print(f" | 顺序单调 {'✓' if mono else '✗'} | 序数近端 {od:4.2f} | 其他灰 {ot:4.2f}")
print("  注：分类 8 色的 CVD 间距（OKLab ΔE）与明度带由 dataviz 校验器负责，见 references/chart-audit.md")

print(f"\n{'='*50}")
if fails:
    print(f"FAIL {len(fails)} 项:")
    for f in fails: print("  ✗", f)
else:
    print("全部通过")
sys.exit(1 if fails else 0)
