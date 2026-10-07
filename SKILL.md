---
name: ui-unify
description: Use when the user asks to 统一UI/升级UI/迁移UI风格 for a backend tool project — applies the unified Linear-dark + Supabase-green design system (dual theme) by copying design tokens into the project and migrating its styles per the stack-specific handbook.
---

# ui-unify — 后台工具统一 UI 升级

把当前项目的 UI 迁移到统一设计体系：Linear 暗色精致风、强调色 Supabase 绿 #3ecf8e、深色为主 + 浅色自动跟随（双主题），支持多色系。

深色为暗色画布 #151517 + 卡片逐层提亮；浅色为护眼暖灰画布 #f2f1ec + 柔米白卡片 #faf9f6（消除白屏刺眼感，深浅两主题统一遵循逐层提亮纵深）；边框一律半透明黑/白分三档（subtle/默认/strong）；强调绿亮暗双值（暗底亮绿 #3ecf8e、浅底深绿 #157a54）。采用三轴正交的多色系机制：`data-theme` 切换明暗，`data-palette` 改变整体中性底色基调（共 12 套，改编自 Solarized / Everforest / Nord / Catppuccin / Rosé Pine / Dracula / Tokyo Night / One Dark / Monokai / Gruvbox / Ayu，分护眼低调、深色、彩色三类，绝不改变强调色），`data-accent` 改变按钮/高亮强调色（提供蓝、紫等 6 种）。图表色板是**第四个正交轴**：分类 8 槽 + 顺序/序数/发散渐变，不跟色系与强调色变化。具体值以 `assets/tokens.css` 为准。

## 工作流

1. **盘点**：识别本项目 UI 技术栈（原生 HTML/Flask、React+Tailwind、Vue+Element Plus）与 UI 入口文件；grep 列出全部硬编码颜色/box-shadow/字体/圆角。
2. **确认范围**：向用户展示盘点结果和将要改动的文件清单；若项目是 manju-bar（或用户表达过保留个性），询问「全量迁移」还是「仅对齐间距/圆角/字体、保留自有配色」。
3. **复制资产**：把本 skill 的 `assets/tokens.css`、`assets/base.css` 复制进项目静态目录（原生项目如 `web/ui/`，React 项目 `src/styles/`）。已存在则覆盖更新；若项目内的副本已被定制修改，先 diff 给用户确认再覆盖。
4. **迁移**：读取 `references/migration.md`，按对应技术栈章节执行；视觉规范细节查 `references/style-guide.md`。核心约束：**只换皮不动骨架**——不改布局、不改逻辑、不换组件库；所有颜色必须来自 token 变量。
5. **图表（若项目有图表）**：读 `references/style-guide.md` §3.6 与 `references/chart-audit.md`；颜色只用 `--chart-*`，接图表库时按 migration.md「图表库怎么接」运行时读 CSS 变量，不硬抄 hex。
6. **验收**：启动项目（或用 demo 数据打开页面），深/浅两主题逐页走查 migration.md 文末的验收清单；改过色值则跑 `python3 references/audit.py`；把结果报告给用户。

## 资源
- `assets/tokens.css` — design token（双主题 CSS 变量），复制进项目
- `assets/base.css` — 基础组件 class（ui-btn/ui-card/ui-table/ui-badge…），复制进项目
- `assets/demo.html` — 完整应用外壳示例（侧栏导航 + 顶栏 ⌘K 搜索 + 标签页 + 统计卡片 + 图表分区 + 数据表格分页 + 表单 + 空状态 + 命令面板 + toast），双主题分段切换，可对照最终效果
- `references/style-guide.md` — 完整视觉规范（色板/排版/形态/反例）
- `references/migration.md` — 分技术栈迁移手册 + 升级已接入项目 + 验收清单
- `references/contrast-audit.md` — WCAG AA 对比度实测表 + 可复现回归脚本
- `references/chart-audit.md` — 图表色板（分类/顺序/序数/发散）实测：CVD 间距、明度带、12 色系对比度
- `references/audit.py` — 一条命令跑完八项校验：`python3 references/audit.py`
- `deploy/verify-charts.py` — 图表渲染实测：溢出、缩放、汉字字号、文字重叠/越界、主题正交（`--self-test` 验证反例能被抓到）

## 例外
- MediaCrawler webui（打包产物无源码）：跳过
- 纯后端/CLI 项目：本 skill 不适用
