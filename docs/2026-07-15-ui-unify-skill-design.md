# ui-unify Skill 设计文档

日期：2026-07-15
状态：已由用户在头脑风暴中确认

## 目标

为 /data/projects/ 下的 11 个带 Web UI 的后台工具建立统一视觉风格，并把风格规范与迁移流程固化为一个全局 Claude Code skill（`ui-unify`）。用户在任意项目中调用该 skill，即可对该项目执行 UI 升级；各项目之间零依赖耦合。

## 已确认的决策

| 决策项 | 结论 |
|---|---|
| 风格方向 | Linear 暗色精致风（近黑画布 + 炭灰卡片 + 细边框分层，无阴影） |
| 强调色 | Supabase 绿 `#3ecf8e` |
| 主题策略 | 深色为主 + 浅色自动跟随系统（双主题，同一组 CSS 变量极性翻转） |
| 落地方式 | 全局 skill（`~/.claude/skills/ui-unify/`），token 文件复制进各项目，不做共享依赖 |

## 1. 视觉规范

### 1.1 色板（CSS 变量，深色为默认值）

深色主题：

- 画布 `--bg: #0e0e10`；卡片 `--surface: #151518`；浮层/弹层 `--surface-2: #1c1c1f`
- 边框 `--border: #26262a`；分割线同边框
- 文字：主 `--text: #f7f8f8`；次 `--text-2: #8a8f98`；弱 `--text-3: #62666d`

浅色主题（`@media (prefers-color-scheme: light)` 自动生效；`:root[data-theme="dark"|"light"]` 手动覆盖优先）：

- 画布 `#fafafa`；卡片 `#ffffff`；浮层 `#ffffff`
- 边框 `#e5e5e8`
- 文字：主 `#18181b`；次 `#71717a`；弱 `#a1a1aa`

强调色（两主题共用）：

- `--accent: #3ecf8e`；hover `--accent-hover: #34b27b`；焦点环 `--accent-ring: rgba(62,207,142,.22)`
- 深色底上，实心绿按钮的文字用深色（`#0e0e10`）；浅色底上用白字需先验对比度，默认仍用深字

语义状态色（刻意与强调绿错开）：

- 成功 `--ok: #2f9e6e`（比强调绿更暗更灰）
- 警告 `--warn: #f5a623`
- 失败/错误 `--danger: #fb7185`
- 进行中：强调绿 + 脉冲动画
- 排队/闲置：中性灰 `#8a8f98`

### 1.1.1 实现期评审补充（质量审查后新增/调整）

- 浅色主题 `--surface-2: #f4f4f5`（否则 hover 态不可见）
- 新增 `--accent-text`：深色 `#3ecf8e` / 浅色 `#158f5e`——强调绿作为**文字/图标色**时必须用它（浅底上原绿对比度不足）；按钮底色仍用 `--accent`
- 浅色主题状态色加深：`--warn #b45309`、`--ok #1e7f56`、`--danger #e11d48`、`--idle #71717a`
- base.css 的 box-sizing reset 作用域收敛为 `.ui, .ui *`，不污染宿主项目

### 1.2 排版与形态

- 字体：正文 `Inter, -apple-system, "PingFang SC", system-ui, sans-serif`；数字/代码/ID 用 `"JetBrains Mono", ui-monospace, monospace`。均走本地 fallback，不引外网字体（内网工具不依赖 Google Fonts）
- 圆角：控件 6px、卡片 8px
- 层次表达：1px 边框 + surface 色阶，不用 box-shadow
- 密度：中等偏高（表格行高 ~36px，工具类后台以信息效率优先）

## 2. Skill 结构

位置：`~/.claude/skills/ui-unify/`（全局 skill，所有项目可调用）

```
ui-unify/
├── SKILL.md          # 触发条件 + 迁移工作流指令（见第 3 节）
├── assets/
│   ├── tokens.css    # 全部 CSS 变量，含深浅双主题与 data-theme 覆盖
│   └── base.css      # 基础组件 class：按钮/卡片/表格/徽章/输入框/顶栏/状态点
└── references/
    ├── style-guide.md   # 完整视觉规范（本文档第 1 节的展开版，含用法示例）
    └── migration.md     # 分技术栈迁移手册（本文档第 3 节的展开版）
```

分发模型：迁移时把 `tokens.css` / `base.css` **复制**进目标项目（如 `web/ui/` 或 `src/styles/`）。不做 git submodule、不做 CDN。规范升级时在各项目重新调用 skill 覆盖更新；单项目微调直接改本地副本。

## 3. 迁移工作流（SKILL.md 核心指令）

在目标项目中调用 `/ui-unify` 时：

1. **盘点**：识别该项目的 UI 技术栈与入口文件，列出所有硬编码颜色/字体/圆角/阴影
2. **迁移**：按技术栈选择手册执行
   - 原生 HTML / Flask 模板（Video2Script、Video2ScriptEn、merge-video、video-splitter、tencent-media-process）：`<link>` 引入 tokens.css + base.css；手写颜色替换为变量；控件 class 对齐 base.css
   - React + Tailwind（drama-auto、seedance2.0、jimeng-sd-sec-dev、script-dialogue-translate）：引入 tokens.css；tailwind config 的语义色映射到 CSS 变量；逐组件替换硬编码色值。Tailwind 4 项目（script-dialogue-translate）用 `@theme` 变量方式
   - Vue + Element Plus（dreamina-cli-manager）：用 `--el-color-primary` 等 Element Plus CSS 变量覆盖对齐 token；启用 Element Plus 暗色模式并默认深色
3. **约束**：只换皮不动骨架——不改布局结构、不改交互逻辑、不更换组件库
4. **验收**：逐页面在深色与浅色两主题下截图走查，确认无残留硬编码色、无对比度问题

## 4. 边界与例外

- **MediaCrawler**：webui 为打包产物、无源码，跳过迁移（文档站可选对齐）
- **manju-bar**：琥珀四原色为刻意的产品个性。默认纳入迁移范围，但 SKILL.md 标注「个性豁免」选项——可仅对齐间距/圆角/字体而保留自有配色，调用时由用户决定
- 纯后端/CLI 项目（df、dy-download、gamas、llm-provider、manju-mini、ssh、translate-srt）不在范围内

## 5. 验收标准

- skill 安装后，在任一目标项目中调用 `/ui-unify` 能完成迁移且不破坏功能
- 任一迁移后的项目：深/浅两主题下界面色彩全部来自 token 变量；强调绿与语义成功色可肉眼区分
- 各项目间无共享运行时依赖
