---
name: ui-unify
description: Use when the user asks to 统一UI/升级UI/迁移UI风格 for a backend tool project — applies the unified Linear-dark + Supabase-green design system (dual theme) by copying design tokens into the project and migrating its styles per the stack-specific handbook.
---

# ui-unify — 后台工具统一 UI 升级

把当前项目的 UI 迁移到统一设计体系：Linear 暗色精致风、强调色 Supabase 绿 #3ecf8e、深色为主 + 浅色自动跟随（双主题）。

## 工作流

1. **盘点**：识别本项目 UI 技术栈（原生 HTML/Flask、React+Tailwind、Vue+Element Plus）与 UI 入口文件；grep 列出全部硬编码颜色/box-shadow/字体/圆角。
2. **确认范围**：向用户展示盘点结果和将要改动的文件清单；若项目是 manju-bar（或用户表达过保留个性），询问「全量迁移」还是「仅对齐间距/圆角/字体、保留自有配色」。
3. **复制资产**：把本 skill 的 `assets/tokens.css`、`assets/base.css` 复制进项目静态目录（原生项目如 `web/ui/`，React 项目 `src/styles/`）。已存在则覆盖更新；若项目内的副本已被定制修改，先 diff 给用户确认再覆盖。
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
