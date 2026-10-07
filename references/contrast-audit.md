# ui-unify 对比度实测（WCAG AA）

tokens.css v1.4.0 的关键前景/背景组合实测比值（WCAG 2.x 相对亮度公式）。
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

## 浅色主题（bg #f2f1ec / surface #faf9f6 / elevated #fdfcfa）

| 组合 | 比值 | 判定 |
|---|---|---|
| text `#191816` on bg | 15.69 | ✅ AA |
| text-2 `#5f5e58` on bg | 5.75 | ✅ AA |
| text-2 `#5f5e58` on surface | 6.18 | ✅ AA |
| accent `#157a54` as link on bg | 4.71 | ✅ AA |
| accent-text `#157a54` on bg | 4.71 | ✅ AA |
| ok `#19734d` on bg | 5.16 | ✅ AA |
| warn `#a34a06` on bg | 5.25 | ✅ AA |
| danger `#cb1840` on bg | 4.96 | ✅ AA |
| accent-contrast `#ffffff` on accent(实心绿按钮) | 5.32 | ✅ AA |
| **text-3 `#8e8c84` on bg / surface** | 2.98 / 3.20 | ⚠️ 弱化档，低于 AA |

> 注：浅色下所有前景色叠在柔米白 `--surface`（#faf9f6）上的对比度均高于 `--bg`（text 16.85、text-2 6.18、accent 5.06、ok 5.54、warn 5.64、danger 5.33），双表面均稳定达标 ≥4.5:1。


## 强调色系变体实测 (v1.4.0 新增)

所有新增色系的明暗双主题 accent 均与共有中性色底色实测 ≥ 4.5:1。

| 色系 | 模式 | accent / bg | accent / surface | accent-text / bg | accent-text / surface | contrast / accent | 判定 |
|---|---|---|---|---|---|---|---|
| **Blue** | Light | `#0055cc` 5.86 | 6.30 | 5.86 | 6.30 | 6.62 | ✅ AA |
| | Dark | `#78a9ff` 7.74 | 6.67 | 7.74 | 6.67 | 8.19 | ✅ AA |
| **Violet** | Light | `#6d28d9` 6.28 | 6.75 | 6.28 | 6.75 | 7.10 | ✅ AA |
| | Dark | `#a78bfa` 6.70 | 5.77 | 6.70 | 5.77 | 7.09 | ✅ AA |
| **Teal** | Light | `#0d7680` 4.74 | 5.09 | 4.74 | 5.09 | 5.36 | ✅ AA |
| | Dark | `#2dd4bf` 9.80 | 8.44 | 9.80 | 8.44 | 10.36 | ✅ AA |
| **Amber** | Light | `#7a6200` 5.19 | 5.58 | 5.19 | 5.58 | 5.87 | ✅ AA |
| | Dark | `#f5db5c` 13.17 | 11.34 | 13.17 | 11.34 | 13.93 | ✅ AA |
| **Graphite** | Light | `#4f4d46` 7.48 | 8.03 | 7.48 | 8.03 | 8.46 | ✅ AA |
| | Dark | `#a6a9b2` 7.76 | 6.68 | 7.76 | 6.68 | 8.21 | ✅ AA |

## 关于 --text-3

`--text-3` 是刻意保留的最faint「弱化/占位档」，对照 DeepSeek 后台校准，**低于 AA（约 2.4–3.4:1）**。
仅用于：占位符、分隔符、与主信息重复的辅助计数（如导航项数字）。**勿承载必要正文**——若某处文字是唯一信息来源，改用 `--text-2`。
若目标项目要求 text-3 也过 3:1（UI 组件最低档），可上调：暗色 `#71757e`（3.4–3.95）、浅色 `#7d7b73`（3.4–3.8）。

## 主题色系实测（v1.7.0）

每个色系内部的中性色文字对比度实测。要求：text / text-2 ≥ 4.5:1；text-3 是刻意弱化档 ≥ 2.4:1；三档必须严格递减且各拉开 ≥1.0。

| 色系 | 模式 | 画布 | text/bg | text/surface | text-2/bg | text-2/surface | text-3/bg | 判定 |
|---|---|---|---|---|---|---|---|---|
| **default (暖纸)** | 浅色 | `#f2f1ec` | 15.69 | 16.85 | 5.75 | 6.18 | 2.98 | ✅ AA |
| **default (暖纸)** | 暗色 | `#151517` | 17.14 | 14.76 | 5.61 | 4.83 | 3.16 | ✅ AA |
| **日光 · Solarized** | 浅色 | `#fdf6e3` | 13.92 | 14.74 | 4.55 | 4.82 | 2.48 | ✅ AA |
| **日光 · Solarized** | 暗色 | `#002b36` | 13.92 | 12.05 | 5.61 | 4.86 | 2.79 | ✅ AA |
| **森林 · Everforest** | 浅色 | `#eef3e3` | 8.02 | 8.63 | 4.94 | 5.31 | 2.44 | ✅ AA |
| **森林 · Everforest** | 暗色 | `#232a2e` | 8.62 | 7.38 | 5.97 | 5.12 | 4.49 | ✅ AA |
| **北欧 · Nord** | 浅色 | `#e7eef7` | 10.69 | 11.74 | 6.31 | 6.93 | 2.63 | ✅ AA |
| **北欧 · Nord** | 暗色 | `#1a2432` | 13.57 | 10.84 | 11.58 | 9.25 | 5.81 | ✅ AA |
| **粉彩 · Catppuccin** | 浅色 | `#eff1f5` | 7.06 | 7.45 | 4.62 | 4.88 | 2.41 | ✅ AA |
| **粉彩 · Catppuccin** | 暗色 | `#201c32` | 11.40 | 10.22 | 7.41 | 6.64 | 4.46 | ✅ AA |
| **玫瑰 · Rosé Pine** | 浅色 | `#faf4ed` | 16.17 | 17.00 | 4.58 | 4.81 | 2.73 | ✅ AA |
| **玫瑰 · Rosé Pine** | 暗色 | `#191724` | 13.39 | 12.50 | 5.48 | 5.12 | 3.42 | ✅ AA |
| **德古拉 · Dracula** | 浅色 | `#f6e9fc` | 12.19 | 13.06 | 7.33 | 7.85 | 4.07 | ✅ AA |
| **德古拉 · Dracula** | 暗色 | `#282a36` | 13.25 | 12.15 | 5.13 | 4.70 | 3.00 | ✅ AA |
| **东京夜 · Tokyo Night** | 浅色 | `#e6eeff` | 12.63 | 13.46 | 5.59 | 5.96 | 2.80 | ✅ AA |
| **东京夜 · Tokyo Night** | 暗色 | `#24283e` | 8.98 | 8.25 | 5.13 | 4.71 | 2.49 | ✅ AA |
| **经典深 · One Dark** | 浅色 | `#e4f6fb` | 12.60 | 13.25 | 5.58 | 5.87 | 2.80 | ✅ AA |
| **经典深 · One Dark** | 暗色 | `#283234` | 8.40 | 7.83 | 5.60 | 5.22 | 2.80 | ✅ AA |
| **莫诺凯 · Monokai** | 浅色 | `#f5fbe4` | 14.03 | 14.33 | 5.60 | 5.72 | 2.81 | ✅ AA |
| **莫诺凯 · Monokai** | 暗色 | `#272822` | 13.83 | 12.40 | 5.24 | 4.70 | 2.99 | ✅ AA |
| **复古 · Gruvbox** | 浅色 | `#fbf1c7` | 10.25 | 10.44 | 4.74 | 4.83 | 3.24 | ✅ AA |
| **复古 · Gruvbox** | 暗色 | `#2b282a` | 10.63 | 9.65 | 5.26 | 4.77 | 2.50 | ✅ AA |
| **柔光 · Ayu** | 浅色 | `#fbece4` | 7.50 | 8.02 | 5.61 | 6.00 | 2.80 | ✅ AA |
| **柔光 · Ayu** | 暗色 | `#202c36` | 9.87 | 8.96 | 5.35 | 4.86 | 2.47 | ✅ AA |

## 色系 × 强调色交叉矩阵（v1.7.0）

**12 色系 × 6 强调色 × 2 模式 × 2 表面 = 288 组**逐一实测。下表给出每个色系每种模式下**最低**的那个比值。

| 色系 | 浅色最低 | 出现于 | 暗色最低 | 出现于 |
|---|---|---|---|---|
| **default (暖纸)** | 4.71 | `green accent/bg` | 5.77 | `violet accent/surface` |
| **日光 · Solarized** | 4.94 | `green accent/bg` | 4.78 | `violet accent/surface` |
| **森林 · Everforest** | 4.71 | `green accent/bg` | 4.58 | `violet accent/surface` |
| **北欧 · Nord** | 4.56 | `green accent/bg` | 4.59 | `violet accent/surface` |
| **粉彩 · Catppuccin** | 4.71 | `green accent/bg` | 5.43 | `violet accent/surface` |
| **玫瑰 · Rosé Pine** | 4.88 | `green accent/bg` | 6.06 | `violet accent/surface` |
| **德古拉 · Dracula** | 4.56 | `green accent/bg` | 4.80 | `violet accent/surface` |
| **东京夜 · Tokyo Night** | 4.57 | `green accent/bg` | 4.90 | `violet accent/surface` |
| **经典深 · One Dark** | 4.79 | `green accent/bg` | 4.51 | `violet accent/surface` |
| **莫诺凯 · Monokai** | 5.02 | `green accent/bg` | 4.90 | `violet accent/surface` |
| **复古 · Gruvbox** | 4.69 | `green accent/bg` | 4.86 | `violet accent/surface` |
| **柔光 · Ayu** | 4.62 | `green accent/bg` | 4.75 | `violet accent/surface` |

全矩阵最低值 **4.51:1**（经典深 · One Dark 暗色 violet accent/surface），仍在 AA 4.5:1 之上。
规律：浅色下最先触底的永远是绿强调色 `#157a54`，暗色下是紫强调色 `#a78bfa`，新增色系时先拿这两个卡边界最省事。

语义状态色（ok / warn / danger）叠在各色系画布上的最低值：

| 色系 | 浅色最低 | 暗色最低 |
|---|---|---|
| **default (暖纸)** | 4.96 | 6.49 |
| **日光 · Solarized** | 5.20 | 5.34 |
| **森林 · Everforest** | 4.96 | 5.18 |
| **北欧 · Nord** | 4.80 | 5.57 |
| **粉彩 · Catppuccin** | 4.96 | 5.87 |
| **玫瑰 · Rosé Pine** | 5.14 | 6.29 |
| **德古拉 · Dracula** | 4.80 | 5.07 |
| **东京夜 · Tokyo Night** | 4.82 | 5.16 |
| **经典深 · One Dark** | 5.04 | 4.68 |
| **莫诺凯 · Monokai** | 5.29 | 5.29 |
| **复古 · Gruvbox** | 4.94 | 5.19 |
| **柔光 · Ayu** | 4.87 | 5.07 |

> 暗色侧 `--ok` 为兼容各色系偏亮的暗色画布，由 `#2f9e6e` 提亮至 `#34ae79`；浅色侧与 warn / danger 未变。

## 重跑脚本

改动任何色值后，在仓库根目录跑：

```bash
python3 references/audit.py
```

脚本直接解析 `assets/tokens.css`，不会与源文件脱节。校验八件事：

1. 色系内部文字对比度
2. 画布明度带（浅色不许过亮、暗色在 8–19.5%）
3. 强调色交叉矩阵
4. 语义色交叉矩阵
5. 色系之间的互辨识度（任意两色系画布 RGB 通道差 ≥ 8）
6. 浅色侧不得出现纯白
7. 色阶方向（浅色 surface-2 下陷、暗色逐层提亮）与文字三档层级
8. 图表色板 × 全部色系卡片面：分类色对比度、顺序渐变单调性、序数渐变近端门槛、「其他」灰槽 ≥3:1（CVD 间距见 references/chart-audit.md）

任何一项不达标会打印 ✗ 并以非零码退出。
