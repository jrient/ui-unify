# ui-unify

Claude Code skill：后台工具统一 UI 升级——Linear 暗色 + Supabase 绿设计体系，双主题 design tokens 一键迁移。

给多个后台小工具做 UI 统一时用：Claude Code 读取本 skill，把统一的 design token 和基础组件样式复制进目标项目，再按技术栈手册完成样式迁移。**只换皮不动骨架**——不改布局、不改逻辑、不换组件库。

## 设计体系速览

- **风格**：Linear 暗色精致风，强调色 Supabase 绿 `#3ecf8e`
- **双主题**：深色为主，浅色自动跟随系统（也可用 `data-theme` 手动指定）
- **配色校准**：黑白灰对照 DeepSeek 开放平台——暗色画布 `#151517` + 卡片逐层提亮；浅色为白画布 + 浅灰卡片；边框半透明黑/白分三档（subtle / 默认 / strong）；强调绿亮暗双值（暗底 `#3ecf8e`、浅底 `#16825d`）
- 具体数值以 [`assets/tokens.css`](assets/tokens.css) 为准

想直观看效果：**在线 demo → <https://jrient.github.io/ui-unify/>**（push 到 main 后由 GitHub Actions 自动部署）；也可以浏览器直接打开 [`assets/demo.standalone.html`](assets/demo.standalone.html)（零依赖单文件），或用 `deploy/nginx.conf` 自行部署。

## 安装

克隆到 Claude Code 的个人 skill 目录即可，对本机所有项目生效：

```bash
git clone git@github.com:jrient/ui-unify.git ~/.claude/skills/ui-unify
```

更新：

```bash
git -C ~/.claude/skills/ui-unify pull
```

也可以放进单个项目的 `.claude/skills/ui-unify/`，随项目仓库分发、仅对该项目生效。

## 使用

在目标项目里对 Claude Code 说「统一UI」「升级UI」「迁移UI风格」之类的话即可触发。Claude 会按以下流程执行：

1. **盘点**——识别技术栈（原生 HTML/Flask、React+Tailwind、Vue+Element Plus）与全部硬编码样式
2. **确认范围**——展示将改动的文件清单，等你确认
3. **复制资产**——把 `tokens.css`、`base.css` 复制进项目静态目录
4. **迁移**——按 `references/migration.md` 对应技术栈章节执行
5. **验收**——深/浅两主题逐页走查验收清单并汇报

## 仓库结构

```
SKILL.md                        skill 入口（Claude Code 自动发现）
assets/
  tokens.css                    design token（双主题 CSS 变量），复制进目标项目
  base.css                      基础组件 class（ui-btn / ui-card / ui-table / ui-badge …）
  demo.html                     完整应用外壳示例（侧栏 + 顶栏 ⌘K + 表格分页 + 命令面板 + toast）
  demo.standalone.html          单文件版 demo，浏览器直接打开预览
references/
  style-guide.md                完整视觉规范（色板 / 排版 / 形态 / 反例）
  migration.md                  分技术栈迁移手册 + 验收清单
deploy/nginx.conf               demo 页面的 nginx 部署配置
docs/                           skill 设计过程文档
```

## 不适用范围

- 纯后端 / CLI 项目
- 无源码的打包产物（如 MediaCrawler webui）
