# ui-unify 对比度实测（WCAG AA）

tokens.css v1.1.0 的关键前景/背景组合实测比值（WCAG 2.x 相对亮度公式）。
正文/控件文字目标 **≥4.5:1**，大号/非文字目标 ≥3:1。**每次改动色值后重跑下方脚本回归。**

## 深色主题（bg #151517 / surface #232324 / elevated #353638）

| 组合 | 比值 | 判定 |
|---|---|---|
| text `#f7f8f8` on bg | 17.14 | ✅ AA |
| text-2 `#8a8f98` on bg | 5.61 | ✅ AA |
| text-2 `#8a8f98` on surface | 4.83 | ✅ AA |
| accent-text `#3ecf8e` on bg | 9.14 | ✅ AA |
| accent-text `#3ecf8e` on surface | 7.87 | ✅ AA |
| ok `#2f9e6e` on bg | 5.42 | ✅ AA |
| warn `#f5a623` on bg | 9.00 | ✅ AA |
| danger `#fb7185` on bg | 6.78 | ✅ AA |
| accent-contrast `#0e0e10` on accent(实心绿按钮) | 9.66 | ✅ AA |
| **text-3 `#62666d` on bg / surface** | 3.16 / 2.72 | ⚠️ 弱化档，低于 AA |

## 浅色主题（bg #fff / surface #f5f6f7）

| 组合 | 比值 | 判定 |
|---|---|---|
| text `#18181b` on bg | 17.72 | ✅ AA |
| text-2 `#67676f` on bg | 5.61 | ✅ AA |
| text-2 `#67676f` on surface | 5.18 | ✅ AA |
| accent `#16825d` as link on bg | 4.79 | ✅ AA |
| accent-text `#157a54` on bg | 5.32 | ✅ AA |
| ok `#1e7f56` on bg | 4.97 | ✅ AA |
| warn `#b45309` on bg | 5.02 | ✅ AA |
| danger `#e11d48` on bg | 4.70 | ✅ AA |
| accent-contrast `#fff` on accent(实心绿按钮) | 4.79 | ✅ AA |
| **text-3 `#a1a1aa` on bg / surface** | 2.56 / 2.37 | ⚠️ 弱化档，低于 AA |

## 关于 --text-3

`--text-3` 是刻意保留的最faint「弱化/占位档」，对照 DeepSeek 后台校准，**低于 AA（约 2.4–3.2:1）**。
仅用于：占位符、分隔符、与主信息重复的辅助计数（如导航项数字）。**勿承载必要正文**——若某处文字是唯一信息来源，改用 `--text-2`。
若目标项目要求 text-3 也过 3:1（UI 组件最低档），可上调：暗色 `#71757e`（3.4–3.95）、浅色 `#88888f`（3.25–3.52）。

## 重跑脚本

```python
def lin(c):
    c/=255
    return c/12.92 if c<=0.03928 else ((c+0.055)/1.055)**2.4
def L(h):
    h=h.lstrip('#'); r,g,b=int(h[0:2],16),int(h[2:4],16),int(h[4:6],16)
    return 0.2126*lin(r)+0.7152*lin(g)+0.0722*lin(b)
def ratio(a,b):
    la,lb=L(a),L(b); hi,lo=max(la,lb),min(la,lb); return (hi+0.05)/(lo+0.05)

pairs = [  # (名称, 前景, 背景, 目标)
    ("dark text-2 / surface", "#8a8f98", "#232324", 4.5),
    ("dark accent-text / surface", "#3ecf8e", "#232324", 4.5),
    ("light text-2 / surface", "#67676f", "#f5f6f7", 4.5),
    ("light accent-text / bg", "#157a54", "#ffffff", 4.5),
    ("light link accent / bg", "#16825d", "#ffffff", 4.5),
]
for name, fg, bg, aa in pairs:
    r = ratio(fg, bg)
    print(f"{'OK ' if r>=aa else 'FAIL'} {r:5.2f}:1  {name}")
```
