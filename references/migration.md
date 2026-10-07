# ui-unify 迁移手册

总原则：**只换皮不动骨架**——不改布局结构、不改交互逻辑、不换组件库。所有颜色/圆角/字体最终必须来自 tokens.css 变量。

## 通用流程
1. 把 skill 的 assets/tokens.css、assets/base.css 复制到目标项目静态目录（如 web/ui/ 或 src/styles/）
2. 全局搜索硬编码样式：`grep -rniE '#[0-9a-f]{3,8}|box-shadow|border-radius|font-family' <ui目录> --include='*.css' --include='*.html' --include='*.vue' --include='*.tsx' --include='*.jsx' --include='*.ts' --include='*.js'`
3. 按下述对应栈的做法替换
4. 深/浅两主题逐页截图走查（验收清单见文末）

## A. 原生 HTML / Flask 模板
适用：Video2Script、Video2ScriptEn、merge-video、video-splitter、tencent-media-process
1. 在每个页面（或 base.html）`<head>` 引入：
   `<link rel="stylesheet" href="ui/tokens.css"><link rel="stylesheet" href="ui/base.css">`，`<body>` 加 class `ui`
2. 项目自有 CSS 里的色值逐个替换为 var(--xxx)；旧主色（#4361ee/#0071e3/#2563eb 等）→ var(--accent)
3. 按钮/输入框/表格/徽章的 class 改为或叠加 ui-btn / ui-input / ui-table / ui-badge
4. 删除 box-shadow 卡片投影，卡片容器改用 ui-card
5. 项目残余的自有 CSS 只保留布局（宽度、grid、间距），不保留颜色

## B. React + Tailwind
适用：drama-auto、seedance2.0、jimeng-sd-sec-dev（Tailwind 3）、script-dialogue-translate（Tailwind 4）
1. tokens.css 复制到 src/styles/ 并在入口（main.tsx / index.css）最先导入
2. Tailwind 3：tailwind.config 的 theme.extend.colors 映射为变量，例如
   `colors: { bg: 'var(--bg)', surface: 'var(--surface)', 'surface-2': 'var(--surface-2)', border: 'var(--border)', 'border-subtle': 'var(--border-subtle)', 'border-strong': 'var(--border-strong)', text: 'var(--text)', 'text-2': 'var(--text-2)', accent: 'var(--accent)', 'accent-text': 'var(--accent-text)', ok: 'var(--ok)', warn: 'var(--warn)', danger: 'var(--danger)' }`
   Tailwind 4：在 index.css 用 `@theme { --color-bg: var(--bg); --color-surface: var(--surface); ... }` 同名映射
3. 逐组件把 bg-[#...]、text-[#...]、bg-gray-50 等硬编码/默认灰替换为语义类（bg-bg、bg-surface、text-text-2、bg-accent…）
4. drama-auto 已有 theme.css 变量体系：将其变量值改指向 tokens（--accent: var(--accent) 式桥接或直接替换值），保留其组件结构
5. 状态色对齐：done→--ok、queued→--idle、failed→--danger、running→--accent；绿色作文字/图标用 --accent-text

## C. Vue + Element Plus
适用：dreamina-cli-manager
1. tokens.css 导入 main.js/main.ts
2. 引入 Element Plus 暗色变量：`import 'element-plus/theme-chalk/dark/css-vars.css'`；默认给 `<html>` 加 class `dark`，并写一个跟随 prefers-color-scheme / data-theme 的小段 JS 同步该 class
3. 新建 element-bridge.css 覆盖 EP 变量对齐 token：
   `:root, :root.dark { --el-color-primary: var(--accent); --el-color-success: var(--ok); --el-color-warning: var(--warn); --el-color-danger: var(--danger); --el-bg-color: var(--surface); --el-bg-color-page: var(--bg); --el-border-color: var(--border); --el-text-color-primary: var(--text); --el-text-color-regular: var(--text-2); --el-border-radius-base: var(--radius); --el-font-family: var(--font-sans); }`
4. 页面级自有样式按 A 节方式替换


## 如何为目标项目选主题色系与强调色
ui-unify 引入了**三轴正交的多色系机制**：
1. `data-theme`：明暗主题（light/dark/跟随系统）。
2. `data-palette`：主题色系，共 12 套。护眼低调向 solarized / everforest / nord / catppuccin / rose-pine；深色向 dracula / tokyo-night / one-dark；彩色向 monokai / gruvbox / ayu。**只改变中性底色**，提供不同冷暖基调。
3. `data-accent`：强调色（blue 蓝、violet 紫、teal 青、amber 琥珀、graphite 灰、默认绿）。**只改变按钮和高亮部件**。

**使用方法**：
在引入 `tokens.css` 的页面 `<html data-palette="solarized" data-accent="blue">`（或动态设置 `document.documentElement.dataset.palette = 'solarized'`）即可生效。不设属性即为默认的暖灰/米白中性底色 + 绿色强调。

**选色建议**：
请根据目标项目的品牌调性或具体场景选择合适的色系与强调色。例如长文本阅读可选 `everforest` 或 `solarized`，数据密集后台可选 `nord` 配 `blue`。所有颜色仍必须走 token 变量（如 `var(--bg)`、`var(--accent)`），**绝对不要为了迎合色系硬编码新色**。语义色（如 --ok, --warn）永远独立，不随任何色系变化。

## 升级已接入项目（防"复制即分叉"漂移）
tokens.css 是**复制**进各项目的，skill 后续更新不会自动回流，须主动升级：
1. 看目标项目里 `tokens.css` 顶部的版本号（如 `v1.1.0`）与本 skill 比对，判断是否过期
2. 升级前先 `diff` 目标副本与 skill 版本；若下游有本地魔改，逐条确认保留/覆盖再替换
3. base.css 同理；升级后按下方验收清单双主题回归
4. **浏览器要求**：v1.1.0 起 tokens.css 用 `light-dark()`（Baseline 2024：Chrome/Edge 123、Safari 17.5、Firefox 120）。目标项目若须兼容更老浏览器，改用旧的四块 `@media`+`data-theme` 写法（git 历史里有）

## 图表库怎么接（ECharts / Chart.js / Recharts）

图表色板是 CSS 变量，图表库要的是 JS 字符串——取值别硬抄 hex，运行时读，主题切换才跟得上：

```js
const css = getComputedStyle(document.documentElement);
const v = n => css.getPropertyValue(n).trim();
const series = [1,2,3,4,5,6,7,8].map(i => v(`--chart-${i}`));   // 按顺序取，用几个取几个
const ink = { label: v('--chart-ink'), muted: v('--chart-ink-muted'),
              grid: v('--chart-grid'), axis: v('--chart-axis') };
```

- `light-dark()` 由 `color-scheme` 决定，`getComputedStyle` 拿到的已经是当前主题下的实际色值。
- 主题/色系切换后要**重新取值并 `setOption`/重绘**（监听 `data-theme` 的 MutationObserver，
  或 `matchMedia('(prefers-color-scheme: dark)')` 的 change 事件）。
- 库的默认色板一律关掉（ECharts 的 `color`、Chart.js 的 `backgroundColor` 循环），
  否则第 9 个系列会被自动生成一个新色相——那正是本体系禁止的。
- 库自带的双 Y 轴、饼图默认标签、彩虹渐变都关掉，理由见 style-guide §3.6。

## 例外
- MediaCrawler webui：打包产物无源码，跳过（文档站可选对齐）
- manju-bar：个性豁免候选——调用时先问用户「全量迁移」还是「仅对齐间距/圆角/字体、保留琥珀配色」

## 验收清单（每项目迁移完成时逐条核对）
- [ ] 深色默认正确；浅色跟随系统正确；data-theme 手动覆盖生效
- [ ] grep 无残留硬编码色值（布局用的透明/黑白遮罩除外）
- [ ] 强调绿与 --ok 成功色肉眼可区分
- [ ] 无重实心投影残留；卡片=1px 边框 + --card-shadow 极轻 bevel，浮层=--elevated + --shadow-overlay，其余平面元素禁阴影
- [ ] 纵深分层正确：画布(--bg) < 卡片(--surface) < 浮层(--elevated) 肉眼可辨
- [ ] 功能无回归：原有按钮/表单/表格交互全部正常
- [ ] a11y：键盘 Tab 走查每个可交互元素焦点框清晰可见；开系统「减少动态」后无限动画停止但加载/状态仍可辨
- [ ] 对比度：主/次文字、链接绿、状态色实测 ≥ WCAG AA 4.5:1（实测表见 references/contrast-audit.md）；--text-3 是低于 AA 的弱化档，勿承载必要正文
- [ ] 图表（若有）：颜色全部来自 --chart-* token，不跟随 accent 变化；单 Y 轴；分类色按 1→8 固定顺序不循环（第 9 个并入 --chart-other 灰）；≥2 系列有图例；每张图可展开成数据表格；有加载态与空态且与真图等高；脚注提到的阈值在图上画出来；图表画在 --surface 上（实测见 references/chart-audit.md）
- [ ] 图表文字：汉字 ≥12px 且不用 mono；值轴从 0 起；图例/脚注里的统计数字由数据计算而非手填；「降为好」的趋势用 .ui-trend.inverse
