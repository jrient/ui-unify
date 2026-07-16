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
