# ui-unify 视觉规范

风格基调：Linear 暗色精致风。近黑画布、炭灰卡片、1px 边框分层、无阴影、单一强调色。

## 1. 色板

### 表面（深色默认 / 浅色）
| token | 深色 | 浅色 | 用途 |
|---|---|---|---|
| --bg | #0e0e10 | #fafafa | 页面画布 |
| --surface | #151518 | #ffffff | 卡片、顶栏 |
| --surface-2 | #1c1c1f | #f4f4f5 | 弹层、hover 背景 |
| --border | #26262a | #e5e5e8 | 全部边框与分割线 |

### 文字
| token | 深色 | 浅色 | 用途 |
|---|---|---|---|
| --text | #f7f8f8 | #18181b | 主文字 |
| --text-2 | #8a8f98 | #71717a | 次要文字、表头 |
| --text-3 | #62666d | #a1a1aa | 占位符、弱化信息 |

### 强调色（两主题共用）
- --accent #3ecf8e：主按钮底色、链接、选中态边框、进行中状态
- --accent-hover #34b27b；--accent-ring rgba(62,207,142,.22)（focus ring）
- --accent-contrast #0e0e10：实心绿按钮上的文字永远用深色
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
- 层次：1px 边框 + surface 色阶；平面元素禁止 box-shadow（focus ring 除外）
- **浮层例外**：命令面板 / 弹层 / toast 可用 `--shadow-overlay` 柔和投影表达悬浮层级；仅限脱离文档流的浮层，卡片/表格等平面元素仍禁用
- 密度：表格行高 36px（--row-h）、控件高 32px、顶栏高 48px

## 3.5 组件清单（base.css 提供的 class）
- 布局外壳：`.ui-shell` `.ui-sidebar`（`.brand`/`.mark`）`.ui-nav-label` `.ui-nav-item`（`.icon`/`.count`/`.active`）`.ui-content`
- 顶栏与导航：`.ui-topbar` · `.ui-search`+`.ui-kbd`（⌘K 触发器）· `.ui-tabs`/`.ui-tab` · `.ui-crumb`（面包屑）
- 反馈与进度：`.ui-progress`（`.warn`/`.danger`/`.indeterminate`）· `.ui-tip`（纯 CSS tooltip，`data-tip`）· `.ui-alert`（`.info`/`.ok`/`.warn`/`.danger`）
- 基础控件：`.ui-btn`（`.primary`/`.danger`/`:disabled`）`.ui-input`/`.ui-select`/`.ui-textarea` `.ui-card`
- 选择控件：`.ui-switch`（开关）`.ui-check`（checkbox / radio 通用，绿选中）
- 数据展示：`.ui-table`（`.num`）`.ui-badge`（`.ok`/`.warn`/`.danger`/`.running`+`.ui-dot`）`.ui-pagination`/`.ui-page-btn`
- 浮层与反馈：`.ui-overlay`+`.ui-command`（命令面板）· `.ui-menu`（下拉菜单，`.item`/`.sep`/`.label`/`.item.danger`）· `.ui-drawer`（抽屉，`.left` 变体 + head/body/foot）· `.ui-empty`（空状态）· `.ui-toast-stack`/`.ui-toast`（`.ok`/`.warn`/`.danger`/`.info`）
- 文本：`.ui-link` `.ui-muted` `.ui-mono`
- 借鉴来源：sidebar / ⌘K / tabs / pagination / 命令面板 参考 shadcn-admin，落地时坚持绿强调 + Linear 克制圆角，未照搬其中性 primary 与 10px 圆角

## 4. 主题机制
- 默认深色；`@media (prefers-color-scheme: light)` 自动浅色
- `:root[data-theme="dark"|"light"]` 手动覆盖，优先于系统偏好
- 所有颜色必须来自 token 变量，组件内禁止硬编码色值

## 5. 反例（迁移时要消灭的东西）
- 硬编码色值（#4361ee、#0071e3 等旧主色）
- box-shadow 卡片投影 → 换 1px 边框
- 用强调绿表达「成功」语义 → 用 --ok
