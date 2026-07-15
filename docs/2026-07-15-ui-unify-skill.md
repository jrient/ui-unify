# ui-unify Skill Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 构建全局 Claude Code skill `ui-unify`（Linear 暗色 + Supabase 绿、双主题 design token），供各后台项目调用执行 UI 统一升级。

**Architecture:** skill 位于 `~/.claude/skills/ui-unify/`，由 SKILL.md（迁移工作流指令）、assets（tokens.css / base.css，迁移时复制进目标项目）、references（style-guide.md / migration.md）组成。无运行时依赖、无构建步骤；验证方式是用 demo 页面在深/浅两主题下人工走查。

**Tech Stack:** 纯 CSS（CSS 变量 + prefers-color-scheme + data-theme 覆盖）、Markdown。

**Spec:** `/data/projects/tmp/docs/superpowers/specs/2026-07-15-ui-unify-skill-design.md`

**注意:** `~/.claude/skills/` 不一定是 git 仓库；若不是，跳过所有 commit 步骤（先用 `git -C ~/.claude rev-parse 2>/dev/null` 检查一次即可）。

---

### Task 1: tokens.css — 设计变量（双主题）

**Files:**
- Create: `~/.claude/skills/ui-unify/assets/tokens.css`

- [ ] **Step 1: 创建目录并写入 tokens.css**

```css
/* ui-unify design tokens — Linear dark + Supabase green, dual theme.
 * 深色为默认；浅色经 prefers-color-scheme 自动跟随；
 * :root[data-theme="dark"|"light"] 手动覆盖优先于系统偏好。 */
:root {
  /* surfaces */
  --bg: #0e0e10;
  --surface: #151518;
  --surface-2: #1c1c1f;
  --border: #26262a;
  /* text */
  --text: #f7f8f8;
  --text-2: #8a8f98;
  --text-3: #62666d;
  /* accent (shared across themes) */
  --accent: #3ecf8e;
  --accent-hover: #34b27b;
  --accent-ring: rgba(62, 207, 142, 0.22);
  --accent-contrast: #0e0e10; /* text on solid accent */
  /* semantic status — 与强调绿刻意错开 */
  --ok: #2f9e6e;
  --warn: #f5a623;
  --danger: #fb7185;
  --idle: #8a8f98;
  /* typography */
  --font-sans: Inter, -apple-system, "PingFang SC", "Microsoft YaHei", system-ui, sans-serif;
  --font-mono: "JetBrains Mono", ui-monospace, SFMono-Regular, Menlo, monospace;
  /* shape & density */
  --radius: 6px;       /* controls */
  --radius-lg: 8px;    /* cards */
  --row-h: 36px;       /* table row height */
  color-scheme: dark;
}

@media (prefers-color-scheme: light) {
  :root {
    --bg: #fafafa;
    --surface: #ffffff;
    --surface-2: #ffffff;
    --border: #e5e5e8;
    --text: #18181b;
    --text-2: #71717a;
    --text-3: #a1a1aa;
    --danger: #e11d48; /* 浅底上加深以保对比度 */
    color-scheme: light;
  }
}

/* 手动覆盖：data-theme 优先于系统偏好 */
:root[data-theme="dark"] {
  --bg: #0e0e10;
  --surface: #151518;
  --surface-2: #1c1c1f;
  --border: #26262a;
  --text: #f7f8f8;
  --text-2: #8a8f98;
  --text-3: #62666d;
  --danger: #fb7185;
  color-scheme: dark;
}

:root[data-theme="light"] {
  --bg: #fafafa;
  --surface: #ffffff;
  --surface-2: #ffffff;
  --border: #e5e5e8;
  --text: #18181b;
  --text-2: #71717a;
  --text-3: #a1a1aa;
  --danger: #e11d48;
  color-scheme: light;
}
```

- [ ] **Step 2: 验证文件落盘**

Run: `ls -la ~/.claude/skills/ui-unify/assets/tokens.css`
Expected: 文件存在且非空。

- [ ] **Step 3: Commit（若 ~/.claude 是 git 仓库）**

```bash
git -C ~/.claude add skills/ui-unify/assets/tokens.css && git -C ~/.claude commit -m "feat(ui-unify): add design tokens (dual theme)"
```

---

### Task 2: base.css — 基础组件样式

**Files:**
- Create: `~/.claude/skills/ui-unify/assets/base.css`

- [ ] **Step 1: 写入 base.css**

```css
/* ui-unify base components — depends on tokens.css being loaded first. */
* { box-sizing: border-box; }

body.ui {
  margin: 0;
  background: var(--bg);
  color: var(--text);
  font-family: var(--font-sans);
  font-size: 14px;
  line-height: 1.5;
}

/* ---------- top bar ---------- */
.ui-topbar {
  display: flex;
  align-items: center;
  gap: 16px;
  height: 48px;
  padding: 0 16px;
  background: var(--surface);
  border-bottom: 1px solid var(--border);
  position: sticky;
  top: 0;
  z-index: 10;
}
.ui-topbar .brand { font-weight: 600; color: var(--text); }
.ui-topbar nav a {
  color: var(--text-2);
  text-decoration: none;
  padding: 6px 10px;
  border-radius: var(--radius);
  font-size: 13px;
}
.ui-topbar nav a:hover { color: var(--text); background: var(--surface-2); }
.ui-topbar nav a.active { color: var(--text); background: var(--surface-2); }

/* ---------- card ---------- */
.ui-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 16px;
}
.ui-card h3 { margin: 0 0 8px; font-size: 14px; font-weight: 600; }

/* ---------- buttons ---------- */
.ui-btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  height: 32px;
  padding: 0 14px;
  border-radius: var(--radius);
  border: 1px solid var(--border);
  background: var(--surface);
  color: var(--text);
  font-size: 13px;
  font-family: inherit;
  cursor: pointer;
}
.ui-btn:hover { background: var(--surface-2); }
.ui-btn:focus-visible { outline: none; box-shadow: 0 0 0 3px var(--accent-ring); border-color: var(--accent); }
.ui-btn.primary {
  background: var(--accent);
  border-color: var(--accent);
  color: var(--accent-contrast);
  font-weight: 600;
}
.ui-btn.primary:hover { background: var(--accent-hover); border-color: var(--accent-hover); }
.ui-btn.danger { color: var(--danger); border-color: var(--danger); background: transparent; }
.ui-btn:disabled { opacity: 0.5; cursor: not-allowed; }

/* ---------- inputs ---------- */
.ui-input, .ui-select, .ui-textarea {
  height: 32px;
  padding: 0 10px;
  border-radius: var(--radius);
  border: 1px solid var(--border);
  background: var(--bg);
  color: var(--text);
  font-size: 13px;
  font-family: inherit;
}
.ui-textarea { height: auto; padding: 8px 10px; }
.ui-input:focus, .ui-select:focus, .ui-textarea:focus {
  outline: none;
  border-color: var(--accent);
  box-shadow: 0 0 0 3px var(--accent-ring);
}
.ui-input::placeholder { color: var(--text-3); }

/* ---------- table ---------- */
.ui-table { width: 100%; border-collapse: collapse; font-size: 13px; }
.ui-table th {
  text-align: left;
  color: var(--text-2);
  font-weight: 500;
  padding: 0 12px;
  height: var(--row-h);
  border-bottom: 1px solid var(--border);
}
.ui-table td {
  padding: 0 12px;
  height: var(--row-h);
  border-bottom: 1px solid var(--border);
  color: var(--text);
}
.ui-table tbody tr:hover td { background: var(--surface-2); }
.ui-table .num { font-family: var(--font-mono); font-variant-numeric: tabular-nums; }

/* ---------- badges & status ---------- */
.ui-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 2px 8px;
  border-radius: 999px;
  font-size: 12px;
  border: 1px solid var(--border);
  color: var(--text-2);
}
.ui-badge.ok { color: var(--ok); border-color: var(--ok); }
.ui-badge.warn { color: var(--warn); border-color: var(--warn); }
.ui-badge.danger { color: var(--danger); border-color: var(--danger); }
.ui-badge.running { color: var(--accent); border-color: var(--accent); }
.ui-dot { width: 8px; height: 8px; border-radius: 50%; background: currentColor; }
.ui-badge.running .ui-dot { animation: ui-pulse 1.6s ease-in-out infinite; }
@keyframes ui-pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.35; } }

/* ---------- misc ---------- */
.ui-link { color: var(--accent); text-decoration: none; }
.ui-link:hover { text-decoration: underline; }
.ui-muted { color: var(--text-2); }
.ui-mono { font-family: var(--font-mono); }
```

- [ ] **Step 2: 验证文件落盘**

Run: `ls -la ~/.claude/skills/ui-unify/assets/base.css`
Expected: 文件存在且非空。

- [ ] **Step 3: Commit（若为 git 仓库）**

```bash
git -C ~/.claude add skills/ui-unify/assets/base.css && git -C ~/.claude commit -m "feat(ui-unify): add base component styles"
```

---

### Task 3: demo.html — 视觉验证页

**Files:**
- Create: `~/.claude/skills/ui-unify/assets/demo.html`

- [ ] **Step 1: 写入 demo.html（覆盖全部组件与三种主题模式）**

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>ui-unify demo</title>
<link rel="stylesheet" href="tokens.css">
<link rel="stylesheet" href="base.css">
</head>
<body class="ui">
<header class="ui-topbar">
  <span class="brand">工具台</span>
  <nav>
    <a class="active" href="#">任务</a>
    <a href="#">账号</a>
    <a href="#">设置</a>
  </nav>
  <div style="margin-left:auto;display:flex;gap:8px">
    <button class="ui-btn" onclick="setTheme('light')">浅色</button>
    <button class="ui-btn" onclick="setTheme('dark')">深色</button>
    <button class="ui-btn" onclick="setTheme(null)">跟随系统</button>
  </div>
</header>
<main style="max-width:960px;margin:24px auto;padding:0 16px;display:grid;gap:16px">
  <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:16px">
    <div class="ui-card"><h3 class="ui-muted">今日任务</h3><div class="ui-mono" style="font-size:24px;font-weight:700">128</div></div>
    <div class="ui-card"><h3 class="ui-muted">进行中</h3><div class="ui-mono" style="font-size:24px;font-weight:700;color:var(--accent)">12</div></div>
    <div class="ui-card"><h3 class="ui-muted">失败</h3><div class="ui-mono" style="font-size:24px;font-weight:700;color:var(--danger)">3</div></div>
  </div>
  <div class="ui-card">
    <div style="display:flex;gap:8px;margin-bottom:12px">
      <button class="ui-btn primary">新建任务</button>
      <button class="ui-btn">导出</button>
      <button class="ui-btn danger">删除</button>
      <button class="ui-btn" disabled>禁用态</button>
      <input class="ui-input" placeholder="搜索任务…" style="margin-left:auto">
    </div>
    <table class="ui-table">
      <thead><tr><th>ID</th><th>名称</th><th>状态</th><th>耗时</th></tr></thead>
      <tbody>
        <tr><td class="num">#1024</td><td>视频切分 batch-07</td><td><span class="ui-badge running"><span class="ui-dot"></span>进行中</span></td><td class="num">02:14</td></tr>
        <tr><td class="num">#1023</td><td>台词翻译 ep12</td><td><span class="ui-badge ok"><span class="ui-dot"></span>成功</span></td><td class="num">00:41</td></tr>
        <tr><td class="num">#1022</td><td>合并导出 final</td><td><span class="ui-badge danger"><span class="ui-dot"></span>失败</span></td><td class="num">01:03</td></tr>
        <tr><td class="num">#1021</td><td>素材抓取</td><td><span class="ui-badge warn"><span class="ui-dot"></span>重试中</span></td><td class="num">00:12</td></tr>
        <tr><td class="num">#1020</td><td>排队任务</td><td><span class="ui-badge"><span class="ui-dot"></span>排队</span></td><td class="num">--</td></tr>
      </tbody>
    </table>
    <p style="margin:12px 0 0"><a class="ui-link" href="#">查看全部 →</a></p>
  </div>
</main>
<script>
function setTheme(t) {
  if (t) document.documentElement.dataset.theme = t;
  else delete document.documentElement.dataset.theme;
}
</script>
</body>
</html>
```

- [ ] **Step 2: 视觉走查（人工验收点）**

Run: `python3 -m http.server 8899 --directory ~/.claude/skills/ui-unify/assets` （后台运行），浏览器打开 `http://<host>:8899/demo.html`。
Expected 检查清单：
1. 深色默认：#0e0e10 画布、卡片有 1px 边框、无阴影
2. 点「浅色」全部翻转且文字对比度正常
3. 「进行中」徽章绿色脉冲，与「成功」徽章的绿肉眼可区分
4. 主按钮绿底深字；focus 时出现绿色 focus ring（Tab 键验证）
5. 「跟随系统」按钮能恢复系统偏好

- [ ] **Step 3: 走查通过后停掉 http.server 并 Commit（若为 git 仓库）**

```bash
git -C ~/.claude add skills/ui-unify/assets/demo.html && git -C ~/.claude commit -m "feat(ui-unify): add demo page for visual verification"
```

---

### Task 4: references/style-guide.md — 视觉规范手册

**Files:**
- Create: `~/.claude/skills/ui-unify/references/style-guide.md`

- [ ] **Step 1: 写入 style-guide.md**

内容为 spec 第 1 节的展开版，必须包含以下全部小节（每节含具体值和用法示例，不得留 TBD）：

```markdown
# ui-unify 视觉规范

风格基调：Linear 暗色精致风。近黑画布、炭灰卡片、1px 边框分层、无阴影、单一强调色。

## 1. 色板

### 表面（深色默认 / 浅色）
| token | 深色 | 浅色 | 用途 |
|---|---|---|---|
| --bg | #0e0e10 | #fafafa | 页面画布 |
| --surface | #151518 | #ffffff | 卡片、顶栏 |
| --surface-2 | #1c1c1f | #ffffff | 弹层、hover 背景 |
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

### 语义状态色（与强调绿刻意错开）
- 成功 --ok #2f9e6e（比强调绿暗且灰，勿混用）
- 警告 --warn #f5a623 ｜ 失败 --danger #fb7185（浅色主题下 #e11d48）
- 进行中：--accent + 脉冲动画 ｜ 排队/闲置 --idle #8a8f98

## 2. 排版
- 正文 --font-sans: Inter, -apple-system, "PingFang SC", system-ui；不引外网字体
- 数字/ID/代码 --font-mono: "JetBrains Mono", ui-monospace + tabular-nums
- 字号：正文 14px、表格与控件 13px、辅助 12px；标题靠字重（600）不靠字号跳跃

## 3. 形态与密度
- 圆角：控件 6px（--radius）、卡片 8px（--radius-lg）、徽章 999px
- 层次：1px 边框 + surface 色阶；禁止 box-shadow（focus ring 除外）
- 密度：表格行高 36px（--row-h）、控件高 32px、顶栏高 48px

## 4. 主题机制
- 默认深色；`@media (prefers-color-scheme: light)` 自动浅色
- `:root[data-theme="dark"|"light"]` 手动覆盖，优先于系统偏好
- 所有颜色必须来自 token 变量，组件内禁止硬编码色值

## 5. 反例（迁移时要消灭的东西）
- 硬编码色值（#4361ee、#0071e3 等旧主色）
- box-shadow 卡片投影 → 换 1px 边框
- 用强调绿表达「成功」语义 → 用 --ok
```

- [ ] **Step 2: Commit（若为 git 仓库）**

```bash
git -C ~/.claude add skills/ui-unify/references/style-guide.md && git -C ~/.claude commit -m "docs(ui-unify): add style guide"
```

---

### Task 5: references/migration.md — 分技术栈迁移手册

**Files:**
- Create: `~/.claude/skills/ui-unify/references/migration.md`

- [ ] **Step 1: 写入 migration.md**

```markdown
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
   `colors: { bg: 'var(--bg)', surface: 'var(--surface)', 'surface-2': 'var(--surface-2)', border: 'var(--border)', text: 'var(--text)', 'text-2': 'var(--text-2)', accent: 'var(--accent)', ok: 'var(--ok)', warn: 'var(--warn)', danger: 'var(--danger)' }`
   Tailwind 4：在 index.css 用 `@theme { --color-bg: var(--bg); --color-surface: var(--surface); ... }` 同名映射
3. 逐组件把 bg-[#...]、text-[#...]、bg-gray-50 等硬编码/默认灰替换为语义类（bg-bg、bg-surface、text-text-2、bg-accent…）
4. drama-auto 已有 theme.css 变量体系：将其变量值改指向 tokens（--accent: var(--accent) 式桥接或直接替换值），保留其组件结构
5. 状态色对齐：done→--ok、queued→--idle、failed→--danger、running→--accent

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
- [ ] 无 box-shadow 投影残留；卡片用 1px 边框
- [ ] 功能无回归：原有按钮/表单/表格交互全部正常
```

- [ ] **Step 2: Commit（若为 git 仓库）**

```bash
git -C ~/.claude add skills/ui-unify/references/migration.md && git -C ~/.claude commit -m "docs(ui-unify): add migration handbook"
```

---

### Task 6: SKILL.md — skill 入口

**Files:**
- Create: `~/.claude/skills/ui-unify/SKILL.md`

- [ ] **Step 1: 写入 SKILL.md**

```markdown
---
name: ui-unify
description: Use when the user asks to 统一UI/升级UI/迁移UI风格 for a backend tool project — applies the unified Linear-dark + Supabase-green design system (dual theme) by copying design tokens into the project and migrating its styles per the stack-specific handbook.
---

# ui-unify — 后台工具统一 UI 升级

把当前项目的 UI 迁移到统一设计体系：Linear 暗色精致风、强调色 Supabase 绿 #3ecf8e、深色为主 + 浅色自动跟随（双主题）。

## 工作流

1. **盘点**：识别本项目 UI 技术栈（原生 HTML/Flask、React+Tailwind、Vue+Element Plus）与 UI 入口文件；grep 列出全部硬编码颜色/box-shadow/字体/圆角。
2. **确认范围**：向用户展示盘点结果和将要改动的文件清单；若项目是 manju-bar（或用户表达过保留个性），询问「全量迁移」还是「仅对齐间距/圆角/字体、保留自有配色」。
3. **复制资产**：把本 skill 的 `assets/tokens.css`、`assets/base.css` 复制进项目静态目录（原生项目如 `web/ui/`，React 项目 `src/styles/`）。已存在则覆盖更新。
4. **迁移**：读取 `references/migration.md`，按对应技术栈章节执行；视觉规范细节查 `references/style-guide.md`。核心约束：**只换皮不动骨架**——不改布局、不改逻辑、不换组件库；所有颜色必须来自 token 变量。
5. **验收**：启动项目（或用 demo 数据打开页面），深/浅两主题逐页走查 migration.md 文末的验收清单；把结果报告给用户。

## 资源
- `assets/tokens.css` — design token（双主题 CSS 变量），复制进项目
- `assets/base.css` — 基础组件 class（ui-btn/ui-card/ui-table/ui-badge…），复制进项目
- `assets/demo.html` — 组件全览示例，可对照最终效果
- `references/style-guide.md` — 完整视觉规范（色板/排版/形态/反例）
- `references/migration.md` — 分技术栈迁移手册 + 验收清单

## 例外
- MediaCrawler webui（打包产物无源码）：跳过
- 纯后端/CLI 项目：本 skill 不适用
```

- [ ] **Step 2: Commit（若为 git 仓库）**

```bash
git -C ~/.claude add skills/ui-unify/SKILL.md && git -C ~/.claude commit -m "feat(ui-unify): add skill entry point"
```

---

### Task 7: 端到端验证

- [ ] **Step 1: 校验 skill 目录完整**

Run: `find ~/.claude/skills/ui-unify -type f | sort`
Expected 输出恰好 6 个文件：SKILL.md、assets/base.css、assets/demo.html、assets/tokens.css、references/migration.md、references/style-guide.md。

- [ ] **Step 2: 校验 frontmatter 可被识别**

Run: `head -5 ~/.claude/skills/ui-unify/SKILL.md`
Expected: 输出以 `---` 开头，含 `name: ui-unify` 与 `description:` 行。

- [ ] **Step 3: 新会话冒烟测试（人工）**

在任一项目目录新开 Claude Code 会话，输入 `/ui-unify`（或「统一这个项目的 UI」），确认 skill 被列出并可调用、指令内容完整加载。

- [ ] **Step 4: 试点迁移建议（不在本计划内执行）**

建议首个试点选 **merge-video**（UI 最小、原生 HTML，风险最低），验证 skill 流程后再推广到其余项目。
