# ui-unify 视觉规范

风格基调：Linear 暗色精致风。近黑画布、炭灰卡片、1px 边框分层、无阴影、单一强调色。

## 1. 色板

### 表面（深色默认 / 浅色）—— 分层提亮做纵深：canvas < surface < elevated
| token | 深色 | 浅色 | 用途 |
|---|---|---|---|
| --bg | #151517 | #ffffff | 页面画布（深色最深压底；浅色为纯白） |
| --surface | #232324 | #f5f6f7 | 卡片、侧栏、顶栏 |
| --surface-2 | #2c2c2e | #ebeef2 | hover 背景、inset、分段轨道 |
| --elevated | #353638 | #ffffff | 浮层：命令面板/菜单/抽屉/toast（比卡片更亮） |

黑白配色（对照 DeepSeek 后台截图校准）：**暗色画布 #151517、卡片逐层提亮**；**浅色反过来——白画布 + 浅灰卡片**（不是灰画布 + 白卡片），卡片主要靠填充差区分层次。
| --border-subtle | rgba(255,255,255,.06) | rgba(0,0,0,.05) | 表格行分隔线、菜单分割线 |
| --border | rgba(255,255,255,.09) | rgba(0,0,0,.10) | 默认边框（卡片/按钮/badge） |
| --border-strong | rgba(0,0,0,.16)⁻¹ | rgba(0,0,0,.16) | 可输入控件（input/select/switch/checkbox），提示可交互 |

边框原则（借鉴 platform.deepseek.com）：**边框一律用半透明黑/白而非实色**，叠在任意背景层上都自然，无需为每层单独配边框色；按「分隔线 < 默认 < 输入控件」三档递进。（⁻¹ 深色为 rgba(255,255,255,.16)）

纵深原则（依据现代暗色 UI 实践）：**暗色靠"逐层提亮 3–6%"而非阴影**——阴影在暗底上是最差的深度信号。三级层：画布 → 卡片 → 浮层。卡片用 `--card-shadow`（暗色=1px 顶部内高光 bevel `inset 0 1px 0 rgba(255,255,255,.035)`；浅色=柔和投影）与画布拉开；浮层再叠 `--elevated` 更亮背景 + `--shadow-overlay`。

### 文字
| token | 深色 | 浅色 | 用途 |
|---|---|---|---|
| --text | #f7f8f8 | #18181b | 主文字 |
| --text-2 | #8a8f98 | #71717a | 次要文字、表头 |
| --text-3 | #62666d | #a1a1aa | 占位符、弱化信息 |

### 强调色（亮暗双值——暗底提亮、浅底加深，借鉴 DeepSeek 品牌蓝手法）
- --accent 深 #3ecf8e / 浅 #16825d：主按钮底色、链接、选中态边框、进行中状态
- --accent-hover 深 #34b27b / 浅 #136e4e；--accent-ring 深 rgba(62,207,142,.22) / 浅 rgba(22,130,93,.2)（focus ring）
- --accent-contrast 深 #0e0e10 / 浅 #ffffff：实心绿按钮上的文字（暗底亮绿配深字、浅底深绿配白字）
- --accent-text 深 #3ecf8e / 浅 #158f5e：绿色作文字/图标时使用

### 语义状态色（与强调绿刻意错开）
- 成功 --ok #2f9e6e（浅色主题下 #1e7f56；比强调绿暗且灰，勿混用）
- 警告 --warn #f5a623（浅色主题下 #b45309） ｜ 失败 --danger #fb7185（浅色主题下 #e11d48）
- 进行中：--accent + 脉冲动画 ｜ 排队/闲置 --idle #8a8f98（浅色主题下 #71717a）

## 2. 排版
- 正文 --font-sans: Inter, -apple-system, "PingFang SC", "Microsoft YaHei", system-ui；不引外网字体
- 数字/ID/代码 --font-mono: "JetBrains Mono", ui-monospace + tabular-nums
- 字号：正文 14px、表格与控件 13px、辅助 12px；标题靠字重（600）不靠字号跳跃

## 3. 形态与密度
- 圆角：控件 6px（--radius）、卡片 8px（--radius-lg）、徽章 999px
- 层次：1px 边框 + surface 色阶 + 分层提亮（canvas/surface/elevated）
- **卡片纵深**：`.ui-card` 用 `--card-shadow`（暗色=极轻顶部内高光 bevel，浅色=柔和投影）与画布拉开；这是唯一允许的平面阴影，其余平面元素（表格/输入等）仍禁 box-shadow（focus ring 除外）
- **浮层例外**：命令面板 / 菜单 / 抽屉 / toast 用 `--elevated` 更亮背景 + `--shadow-overlay` 表达悬浮层级
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
- 文本：`.ui-link` `.ui-muted` `.ui-mono`
- 借鉴来源：sidebar / ⌘K / tabs / pagination / 命令面板 参考 shadcn-admin，落地时坚持绿强调 + Linear 克制圆角，未照搬其中性 primary 与 10px 圆角
- 可访问性：`.ui-btn`/`.ui-tab`/`.ui-page-btn`/`.ui-switch`/`.ui-check` 用原生表单/按钮元素，键盘可达；模态用原生 `<dialog>`（`showModal()` 自动焦点陷阱与 Esc），折叠用原生 `<details>`；`.ui-menu .item`、`.ui-command .item`、`.ui-tree .node` 是纯样式 `div`，集成时需自行补 `role`/`tabindex`/键盘事件
- 全局 a11y 兜底（base.css 末尾）：`prefers-reduced-motion` 关无限动画（保留 spinner/状态可辨识）；`prefers-contrast: more` 加深边框与弱化文字；`forced-colors`（Windows 高对比）给半透明边框补系统色；所有焦点态用「透明实线 outline + 强调色」双保险，高对比模式不丢焦点框

## 4. 主题机制（tokens.css v1.1.0：light-dark() 单份定义）
- 颜色用 `light-dark(浅色值, 深色值)` **只写一次**，主题由 `color-scheme` 驱动：`:root { color-scheme: light dark }` 跟随系统；`:root[data-theme="light"|"dark"]` 手动覆盖只需切 `color-scheme`（不再重列整套变量）
- **阴影不是颜色**，`light-dark()` 不接受 → `--shadow-overlay`/`--card-shadow` 仍保留极小的 `@media`+`data-theme` 覆盖块（这是唯一的重复，诚实对待边界）
- 浏览器要求：`light-dark()` 需 Chrome/Edge 123、Safari 17.5、Firefox 120（Baseline 2024）；若目标项目须兼容更老浏览器，退回旧的四块 `@media`+`data-theme` 写法
- 所有颜色必须来自 token 变量，组件内禁止硬编码色值

## 5. 反例（迁移时要消灭的东西）
- 硬编码色值（#4361ee、#0071e3 等旧主色）
- 重实心投影卡片（如 `0 4px 12px rgba(0,0,0,.3)`）→ 换 1px 边框 + `--card-shadow` 的极轻 bevel/投影
- 用强调绿表达「成功」语义 → 用 --ok
