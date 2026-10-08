# ui-unify 视觉规范

风格基调：Linear 暗色精致风。近黑画布、炭灰卡片、1px 边框分层、无阴影、单一强调色。

## 1. 色板

### 表面（深色默认 / 浅色）—— 分层提亮做纵深：canvas < surface < elevated
| token | 深色 | 浅色 | 用途 |
|---|---|---|---|
| --bg | #151517 | #f2f1ec | 页面画布（深色最深压底；浅色为护眼暖灰底） |
| --surface | #232324 | #faf9f6 | 卡片、侧栏、顶栏（浅色为柔米白卡片，全程不出现纯白） |
| --surface-2 | #2c2c2e | #e8e6df | hover 背景、inset、分段轨道 |
| --elevated | #353638 | #fdfcfa | 浮层：命令面板/菜单/抽屉/toast（浅色靠暖调投影拉开悬浮感） |

黑白配色：**暗色画布 #151517、卡片逐层提亮**；**浅色护眼方案——暖灰画布 #f2f1ec + 柔米白卡片 #faf9f6**，统一遵循 canvas < surface < elevated 逐层提亮模型，大面积卡片与表格也不出现纯白，消除刺眼感。
| --border-subtle | rgba(255,255,255,.06) | rgba(0,0,0,.06) | 表格行分隔线、菜单分割线 |
| --border | rgba(255,255,255,.09) | rgba(0,0,0,.11) | 默认边框（卡片/按钮/badge） |
| --border-strong | rgba(0,0,0,.16)⁻¹ | rgba(0,0,0,.18) | 可输入控件（input/select/switch/checkbox），提示可交互 |

边框原则（借鉴 platform.deepseek.com）：**边框一律用半透明黑/白而非实色**，叠在任意背景层上都自然，无需为每层单独配边框色；按「分隔线 < 默认 < 输入控件」三档递进。（⁻¹ 深色为 rgba(255,255,255,.16)）

纵深原则（依据现代暗色 UI 实践）：**暗色靠"逐层提亮 3–6%"而非阴影**——阴影在暗底上是最差的深度信号。三级层：画布 → 卡片 → 浮层。卡片用 `--card-shadow`（暗色=1px 顶部内高光 bevel `inset 0 1px 0 rgba(255,255,255,.035)`；浅色=柔和投影）与画布拉开；浮层再叠 `--elevated` 更亮背景 + `--shadow-overlay`。

### 文字
| token | 深色 | 浅色 | 用途 |
|---|---|---|---|
| --text | #f7f8f8 | #191816 | 主文字（浅色采用暖炭黑） |
| --text-2 | #8a8f98 | #5f5e58 | 次要文字、表头（浅色加深至 #5f5e58 过 AA） |
| --text-3 | #62666d | #8e8c84 | 占位符、弱化信息 |


### 主题色系（data-palette）
本设计系统采用三轴正交的多色系机制：`data-theme` (明暗)、`data-palette` (主题色系)、`data-accent` (强调色)。
- 默认无属性即为经典的“护眼暖灰/柔米白”方案。
- 共 12 套，均脱胎于业界成熟配色方案，因分层方向与对比度约束做过最小幅度改编。

**护眼低调向**（大面积久看不累）：
  - `solarized` (日光)：Ethan Schoonover 的 Solarized，用 CIELAB 精确控制明度关系、刻意压低对比度，暖黄纸配深青蓝，长时间注视不累。
  - `everforest` (森林)：sainnhe 的 Everforest，低饱和绿调，以「久看不累」为设计目标，适合阅读与编码类工具。
  - `nord` (北欧)：arcticicestudio 的 Nord，北极极夜意象的冷蓝灰，理性克制，适合数据密集型后台与仪表盘。
  - `catppuccin` (粉彩)：Catppuccin 的 Latte / Mocha，柔和粉彩与统一色相骨架，观感现代亲和。
  - `rose-pine` (玫瑰)：Rosé Pine 的 Dawn / Main，玫瑰灰紫，本身的 base < surface < overlay 分层与本体系天然一致。

**深色向**（气质深沉、夜间感强）：
  - `dracula` (德古拉)：Dracula，开发者圈最知名的紫粉调夜间方案，暗色画布用原作 `#282a36`。
  - `tokyo-night` (东京夜)：folke 的 Tokyo Night Storm，霓虹街头感的深冷蓝。
  - `one-dark` (经典深)：Atom / One Dark，代码编辑器里最稳重的蓝灰深色标准。

**彩色向**（色彩更浓、个性更强）：
  - `monokai` (莫诺凯)：Sublime Text 时代风靡的高对比方案，暗色画布用原作 `#272822`。
  - `gruvbox` (复古)：morhetz 的 Gruvbox，标志性褐黄复古调，浅色画布直接用原作 `#fbf1c7`。
  - `ayu` (柔光)：Ayu Mirage，色彩平衡优雅，暖调高级灰。

> 这些方案的原作浅色多为纯白或接近纯白（One Light / Ayu Light 都是 `#fafafa`），违反本体系的护眼底线，
> 因此除 Gruvbox 外，浅色侧都是按原作标志性色相另行设计的搭档色，不是原作值。
- **硬性约束**：`data-palette` 仅改变画面的基础中性色（背景、文字、边框）与阴影底色。**绝对不碰强调色和语义状态色**，确保更换底色的同时，不破坏品牌按钮、链接以及状态高亮色的独立语义和对比度。


### 强调色（data-accent）
本设计系统引入正交的多色系支持（`data-accent`），每个色系覆盖 5 个 accent token。中性色（底色、文字、边框）与语义状态色完全不变，确保换色不破坏对比度与暗色质感。

色系名单与场景（默认为绿色，即不加属性）：
- `blue` (蓝)：最通用的后台色，稳重可靠
- `violet` (紫)：创意、高级、差异化场景
- `teal` (青)：清爽、数据、科技感（与 --ok 的纯绿明确错开）
- `amber` (琥珀)：暖调、活泼；刻意压成金黄调（色相约 48°），与 --warn 的橙褐（约 26–37°）在色相与明度上双重错开，避免主按钮被误读成警告
- `graphite` (灰)：近无彩色（浅色暖灰 / 暗色微蓝灰，跟随各自主题的中性调），极度克制、内容绝对优先的场合

### 强调色（亮暗双值——暗底提亮、浅底加深，借鉴 DeepSeek 品牌蓝手法）
- --accent 深 #3ecf8e / 浅 #157a54：主按钮底色、链接、选中态边框、进行中状态
- --accent-hover 深 #34b27b / 浅 #126748；--accent-ring 深 rgba(62,207,142,.22) / 浅 rgba(21,122,84,.2)（focus ring）
- --accent-contrast 深 #0e0e10 / 浅 #ffffff：实心绿按钮上的文字（暗底亮绿配深字、浅底深绿配白字）
- --accent-text 深 #3ecf8e / 浅 #157a54：绿色作文字/图标时使用

### 语义状态色（与强调绿刻意错开）
- 成功 --ok #2f9e6e（浅色主题下 #19734d；比强调绿暗且灰，勿混用）
- 警告 --warn #f5a623（浅色主题下 #a34a06） ｜ 失败 --danger #fb7185（浅色主题下 #cb1840）
- 进行中：--accent + 脉冲动画 ｜ 排队/闲置 --idle #8a8f98（浅色主题下 #6e6c65）

## 2. 排版
- 正文 --font-sans: Inter, -apple-system, "PingFang SC", "Microsoft YaHei", system-ui；不引外网字体
- 数字/ID/代码 --font-mono: "JetBrains Mono", ui-monospace + tabular-nums
- 字号：正文 14px、表格与控件 13px、辅助 12px；标题靠字重（600）不靠字号跳跃

## 3. 形态与密度
- 圆角：**嵌套子元素 4px（--radius-sm）**、控件 6px（--radius）、卡片 8px（--radius-lg）、徽章 999px
- **嵌套圆角规则**：紧贴容器内壁的子元素用 `inner = outer − 内边距`——控件 6−2、卡片 8−4 均得 4px，故菜单/命令项、kbd、分段按钮、行内代码等一律 `--radius-sm`，避免内外弧线在角上打架（对照 killaislop #21）
- 层次：1px 边框 + surface 色阶 + 分层提亮（canvas/surface/elevated）
- **卡片纵深**：`.ui-card` 用 `--card-shadow`（暗色=极轻顶部内高光 bevel，浅色=柔和投影）与画布拉开；这是唯一允许的平面阴影，其余平面元素（表格/输入等）仍禁 box-shadow（focus ring 除外）
- **浮层例外**：命令面板 / 菜单 / 抽屉 / toast 用 `--elevated` 更亮背景 + `--shadow-overlay` 表达悬浮层级
- **阴影准则**（对照 killaislop #20）：`--shadow-overlay` 为两层——`0 1px 2px` 接触影落地 + `0 16px 32px -12px` 收敛环境影（负 spread 收紧扩散），拒绝「小元素投巨大柔影、无高度逻辑」的浮影
- 密度：表格行高 36px（--row-h）、控件高 32px、顶栏高 48px

## 3.5 组件清单（base.css 提供的 class）
- 布局外壳：`.ui-shell` `.ui-sidebar`（`.brand`/`.mark`）`.ui-nav-label` `.ui-nav-item`（`.icon`/`.count`/`.active`）`.ui-content`
- 顶栏与导航：`.ui-topbar` · `.ui-search`+`.ui-kbd`（⌘K 触发器）· `.ui-tabs`/`.ui-tab` · `.ui-crumb`（面包屑）
- 反馈与进度：`.ui-progress`（`.warn`/`.danger`/`.indeterminate`）· `.ui-tip`（纯 CSS tooltip，`data-tip`）· `.ui-alert`（`.info`/`.ok`/`.warn`/`.danger`）
- 基础控件：`.ui-btn`（`.primary`/`.danger`/`:disabled`）`.ui-input`/`.ui-select`/`.ui-textarea` `.ui-card`
- 选择控件：`.ui-switch`（开关）`.ui-check`（checkbox / radio 通用，绿选中）`.ui-seg`（分段控件）`.ui-stepper`（数字步进器）`.ui-dropzone`（文件拖拽区，`.dragover` 态）
- 键值展示：`.ui-desc`（dt/dd 描述列表）
- 数据展示：`.ui-table`（`.num`）`.ui-badge`（`.ok`/`.warn`/`.danger`/`.running`+`.ui-dot`）`.ui-pagination`/`.ui-page-btn`
- 浮层与反馈：`.ui-overlay`+`.ui-command`（命令面板）· `.ui-menu`（下拉菜单，`.item`/`.sep`/`.label`/`.item.danger`）· `.ui-drawer`（抽屉，`.left` 变体 + head/body/foot）· `.ui-empty`（空状态）· `.ui-toast-stack`/`.ui-toast`（`.ok`/`.warn`/`.danger`/`.info`）
- 展示与状态：`.ui-tag`（`.accent`，可含 `.x` 删除）· `.ui-avatar`（`.sm`/`.lg`/`.accent` + `.ui-avatar-group` 叠加）· `.ui-timeline`（节点 `.ok`/`.danger`/`.active`）· `.ui-skeleton`（`.line`/`.circle` 加载态）
- 数据/代码：`.ui-tree`（树形，`.node.active`）· `.ui-code`（日志/代码块，`.c-accent`/`.c-warn`/`.c-danger` 语义高亮）+ `code.ui-inline`（行内代码）· `.ui-trend`（`.up`/`.down`/`.flat` 涨跌）· `.ui-spark`（纯 CSS 迷你柱图）
- 浮层进阶：`dialog.ui-dialog`（原生 `<dialog>` 居中模态，`.head`/`.body`/`.foot`，`::backdrop` 遮罩——自带焦点陷阱 / Esc 关闭 / 背景 inert）
- 加载与折叠：`.ui-spinner`（`.lg`，必要动效，reduced-motion 下仍旋转）· `.ui-accordion`（原生 `<details>`/`<summary>` 折叠面板，`.body`/`.count`）
- 数据与工具条：`.ui-stat`（KPI 卡片，`.label`/`.value`/`.foot`）· `.ui-btn-group`（相邻按钮拼接工具条）· `.ui-divider`（分隔线，`.v` 垂直 / `.label` 带文字）
- 图表：`.ui-chart`（`-head`/`-title`/`-sub`/`-tools`/`-body`/`-foot`）· 事件 `.ui-chart-event` · 小倍数 `.ui-multiples` · 占比条 `.ui-meter` · 子弹图 `.ui-bullet`· 系列槽 `.ui-s1…8`（分类）/`.ui-cok`·`.ui-cwarn`·`.ui-cdanger`·`.ui-cidle`（状态）/`.ui-q1…7`（顺序）/`.ui-o1…4`（序数）/`.ui-dn2…dp2`（发散）· 标记 `.ui-chart-line`/`-area`/`-band`/`-dot`（`.before`/`.after`）/`-dumbbell-rail`/`-bar`/`-seg`/`-cell`/`-ring` · 变化标注 `.ui-chart-delta` · chrome `.ui-chart-grid`/`-axis`/`-tick`/`-label` · `.ui-chart-legend`/`-legend-item`/`.ui-chart-scale` · hover 层 `.ui-chart-hit`（`.box`/`.cross`/`.tip`/`.peak`，纯 CSS 零 JS）· `.ui-chart-rule`/`-rule-label`（阈值/目标参考线）· `.ui-chart-empty`（空态）/`.ui-chart-skeleton`（加载占位）· `.ui-chart-a11y`（`<details>` 展开成 `.ui-table`）· `.ui-chart-tex`（纹理第二编码）
- 文本：`.ui-link` `.ui-muted` `.ui-mono`
- 借鉴来源：sidebar / ⌘K / tabs / pagination / 命令面板 参考 shadcn-admin，落地时坚持绿强调 + Linear 克制圆角，未照搬其中性 primary 与 10px 圆角
- 可访问性：`.ui-btn`/`.ui-tab`/`.ui-page-btn`/`.ui-switch`/`.ui-check` 用原生表单/按钮元素，键盘可达；模态用原生 `<dialog>`（`showModal()` 自动焦点陷阱与 Esc），折叠用原生 `<details>`；`.ui-menu .item`、`.ui-command .item`、`.ui-tree .node` 是纯样式 `div`，集成时需自行补 `role`/`tabindex`/键盘事件
- 全局 a11y 兜底（base.css 末尾）：`prefers-reduced-motion` 关无限动画（保留 spinner/状态可辨识）；`prefers-contrast: more` 加深边框与弱化文字；`forced-colors`（Windows 高对比）给半透明边框补系统色；所有焦点态用「透明实线 outline + 强调色」双保险，高对比模式不丢焦点框

## 3.6 图表（data viz）

图表色板是**第四个正交轴**：`data-palette` 换中性底色、`data-accent` 换强调色，图表色都不跟着变——
同一份数据在任何主题下颜色含义恒定。色值与实测见 `references/chart-audit.md`。

### 四类颜色，各有各的活

| 用途 | token | 规矩 |
|---|---|---|
| 分类（身份） | `--chart-1…8` | 固定顺序取用，**不循环**；第 9 个系列并入「其他」或改小倍数图 |
| 顺序（连续量级） | `--chart-seq-1…7` | 单色相蓝，离画布越远＝值越大 |
| 序数（离散有序） | `--chart-ord-1…4` | 比连续渐变收窄，近画布一端仍 ≥2:1 |
| 发散（有极性） | `--chart-div-neg-2…pos-2` | 蓝↔红两极 + **中性灰中点**（中点绝不用色相） |
| 长尾「其他」 | `--chart-other` | 中性灰，**不是第 9 个色相**；色相到 8 为止 |
| 状态 | `--ok`/`--warn`/`--danger`/`--idle` | 不占分类槽；永远配图标或文字，不靠颜色单跑 |

chrome 一律走已有 token：网格 `--chart-grid`（= `--border-subtle`）、基线 `--chart-axis`（= `--border`）、
文字 `--chart-ink`/`--chart-ink-muted`（= `--text-2`/`--text-3`）。**文字永远不穿系列色。**

### 硬规矩（违反是画错，不是风格问题）

1. **单 Y 轴，永不双轴**。量纲不同就拆两张图，或归一化到同一基准。
2. **颜色跟实体走，不跟排名走**：筛掉几个系列后，活下来的系列不许重新上色。
3. **≥2 系列必有图例**；≤4 系列同时做末端直接标注；单系列不配图例（标题已经说了是什么）。
4. **只圆远离基线的一端**（`--chart-mark-r: 4px`），柱脚直角贴基线；相邻色块之间留
   `--chart-gap: 2px` 卡片底色的缝。
5. **图表画在卡片面 `--surface` 上**，不要画在 `--elevated` 浮层上——部分色系浮层过亮，实测掉出 3:1。
6. **每张图都要能展开成表格**（`.ui-chart-a11y` 包 `.ui-table`）：这是浅底上弱色系列的兜底义务，
   不是可选装饰。
7. **hover 层默认有**：`.ui-chart-hit` 用透明 hitbox 接鼠标（细折线不好点），准星 + tooltip 纯 CSS
   显隐；hitbox 带 `tabindex` 与 `aria-label`，键盘也能逐点读数。
8. **纹理只在需要时开**（`data-chart-texture="on"`、打印、`forced-colors`），45°/135° 两向，
   它是第二编码不是装饰。
9. **脚注里提到的阈值就要画出来**：`.ui-chart-rule` 虚线 + `.ui-chart-rule-label`，比基线弱，
   不抢数据；标尺要包得住阈值，否则说明标尺选错了。
10. **加载和空态要占同样的高度**：`.ui-chart-skeleton` / `.ui-chart-empty` 与真图等高，数据回来时页面不跳；
   空态要说清为什么空、下一步做什么，不要拿空坐标系冒充有数据。
11. **图例联动零 JS**：图例项与标记挂同一个 `data-s` 值，`:has()` 负责把其余系列淡到 .25。
12. **打印能看**：`@media print` 自动收起准星/tooltip、顶上纹理、摊开数据表格、卡片不跨页断裂。

### 字号与缩放（和现有字号阶梯对齐：卡片标题 14 > 正文 13 > 次要 12）

- SVG 图按宽度铺满、高度随 viewBox 比例走；主体写 `style="--vbw:<viewBox 宽>"`，缩放被夹在 **0.92×–1.04×**。
  低于下限时在卡片内横向滚动（和宽表格同一做法），高于上限时居中留白——字号永远不会比卡片标题大。
- **汉字不进 mono、不小于 12px**：类目名、阈值/事件标签一律 sans 13 单位（缩放后 12–13.5px）；
  mono 11 单位只给数字、时间、技术 ID（`node-01` 用 `.ui-chart-tick.id`）。
- 标签自带卡片底色衬底（`paint-order: stroke`），压在网格线或标记上也读得清。
- viewBox 宽度按目标卡片的典型宽度定（一栏 ≈312、2/3 栏 ≈680、半栏 ≈500），否则会被夹住后大面积留白。
- 超宽屏的剩余留白是「零 JS + 固定字号」的代价；接入方要铺满就在运行时按容器宽重算 viewBox。

### 诚实规则（借鉴 diagram-design）

- **值轴必含 0**，刻度取 1/2/2.5/5×10ⁿ 整齐步长；全零数据给 0–1 兜底跨度，标记落在基线上。
  阈值/目标线要纳入值域。生成器里统一用 `nice_domain()`，并对四种符号情形（正/负/跨零/全零）测过。
- **0 值不画**：不给 0 画 1px 色块冒充「有一点」；堆叠缝只留在段与段之间，最底段贴基线。
- **印出来的数字必须从数据算**：图例当前值、脚注峰值/均值、`aria-label`、数据表格全部由同一份数据生成，
  不手填——手填的统计会在数据改动后悄悄变成错的（本仓库就发生过 3 处）。
- **趋势色跟好坏走，不跟方向走**：失败数、耗时这类「降为好」的指标给 `.ui-trend` 加 `.inverse`。
- **多系列只有主系列铺面积**：两层半透明面积叠在一起会混色，还会被读成堆叠。

### 组件补充

| 组件 | 用途 | 要点 |
|---|---|---|
| `.ui-chart-event` | 时序图上的「时刻」（发版、告警、扩容） | 竖直实线＋顶部标签，和水平虚线的阈值区分开；每图 ≤3 个 |
| `.ui-multiples` | 系列 >4 时拆成一格一个 | **共用同一纵轴**（脚注写明范围）；同一颜色，身份由格子标题承担 |
| `.ui-meter` | 100% 占比条，可直接放进 `.ui-table` 单元格 | 段用 `flex-grow:原始数值`，0 值不渲染；与 `.ui-progress`（界面状态、强调色、胶囊形）分工 |
| `.ui-bullet` | 实际 vs 目标/配额 | 四列：名称／轨道／数字／徽章；超出用 `.ui-badge` 说明，不靠变色 |
| 哑铃图 `.ui-chart-dumbbell-rail` + `.ui-chart-dot.before/.after` | 同一批类目的前后对比（优化前后、两期） | 「前」空心 `--chart-other` 灰、「后」实心 `.ui-s1`；按业务顺序排，不按变化量重排；变慢的项如实画；变化写在右侧固定列（`.ui-chart-delta.good/.bad/.flat`，按好坏不按正负，减号用 `−`），不贴着点放 |
| 分位区间带 `.ui-chart-band` | 延迟/耗时的分布（P10–P90 + P50） | 带只是背景，中位线 `.ui-chart-line` 才是主角；tooltip 让开中位线；值轴照样含 0 |
| `.ui-stat` + `.ui-spark` | KPI 数字卡 | 大数字用 `--text`，状态用 `.ui-dot`+文字；sparkline 默认 `--chart-1`，不跟强调色 |

### 校验（规则写成检查器，不靠肉眼）

- `python3 deploy/verify-charts.py`：两份 demo × 6 个断点，实测页面溢出、缩放区间、汉字字号与字体、文字越界、
  文字重叠、文字压标记，以及**正交**（12 色系 × 6 强调色 × 明暗下所有数据标记颜色不变）。
- `python3 deploy/verify-charts.py --self-test`：跑 `deploy/fixtures/verify-charts-bad.html` 里的反例，
  确认每条规则真能报错——只测「好的会通过」不够。
- 改 demo 图表只改 `deploy/gen-demo-charts.py` 再重建，不要直接编辑 HTML 里的 `<svg>`。

### 反例

- 双 Y 轴 · 彩虹色顺序渐变 · 发散中点用色相
- 药丸柱（四角全圆、柱体浮离基线）· 面积图渐变到纯黑
- 用系列色写坐标轴/标题/数值 · 每个点都标数字 · 网格线比数据还重
- 8 条折线挤一张图（面条图）· 切 8 块的实心饼图 · 语义色拿去当「系列 4」
- 汉字塞进 9px mono 刻度 · 大数字染成状态色 · 「失败 ▼」标红 · 脚注里写着没有数据依据的「周环比」
- 小倍数各格各自缩放纵轴 · 0 值画成 1px 色块 · 两层面积叠成泥色

## 4. 主题机制（tokens.css v1.4.0：light-dark() 单份定义）
- 颜色用 `light-dark(浅色值, 深色值)` **只写一次**，主题由 `color-scheme` 驱动：`:root { color-scheme: light dark }` 跟随系统；`:root[data-theme="light"|"dark"]` 手动覆盖只需切 `color-scheme`（不再重列整套变量）
- **阴影不是颜色**，`light-dark()` 不接受 → `--shadow-overlay`/`--card-shadow` 仍保留极小的 `@media`+`data-theme` 覆盖块（这是唯一的重复，诚实对待边界）
- 浏览器要求：`light-dark()` 需 Chrome/Edge 123、Safari 17.5、Firefox 120（Baseline 2024）；若目标项目须兼容更老浏览器，退回旧的四块 `@media`+`data-theme` 写法
- 所有颜色必须来自 token 变量，组件内禁止硬编码色值

## 5. 反例（迁移时要消灭的东西）
- 硬编码色值（#4361ee、#0071e3 等旧主色）
- 重实心投影卡片（如 `0 4px 12px rgba(0,0,0,.3)`）→ 换 1px 边框 + `--card-shadow` 的极轻 bevel/投影
- 用强调绿表达「成功」语义 → 用 --ok

## 6. 反 AI-slop 自检（对照 killaislop.com 33 tells，迁移完成后过一遍）
本体系天然规避多数「机器味」，落地时守住这些，别把它们又请回来：
- **先减后加**：一个元素若解释不出存在理由，删掉——slop 是堆出来的
- **单一强调色**：只有 Supabase 绿一个强调色；渐变文字 / 氛围光晕 / 玻璃态一律不用
- **层次靠尺度与留白**，不靠「换字体」或「加灰度」；标题用字号+字重+间距，不用彩色/描边
- **间距按 4/8/16/24 小阶跳变，按语义不均匀施加**：相关元素间距紧、无关区块间距松；避免整页 `gap:16px` 一个值到底
- **过渡只给会变的属性**（bg/border/opacity），120–200ms 标准缓动；禁止 `hover:scale` 弹跳、`transition:all`
- **圆角一处 token、嵌套用 inner=outer−gap**（见 §3）；边框与圆角放同一元素，让描边自动包住圆角
- **装饰须承载信息**：badge/pill/图标底片不滥用；状态用「扁平小圆点+文字」，脉冲只留给「进行中」这类真活动态
- **callout 稀用**（每屏 1–2 个真旁注）：`.ui-alert` 的左色条别变成「每行都重要」的通用装饰
- **具体优于热情**：文案用真实数字与专有名词，别堆 emoji 和「一键告别 X」式空话
