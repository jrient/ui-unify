# ui-unify

Claude Code skill：后台工具统一 UI 升级——Linear 暗色 + Supabase 绿设计体系，双主题 design tokens 一键迁移。

给多个后台小工具做 UI 统一时用：Claude Code 读取本 skill，把统一的 design token 和基础组件样式复制进目标项目，再按技术栈手册完成样式迁移。**只换皮不动骨架**——不改布局、不改逻辑、不换组件库。

## 设计体系速览

- **风格**：Linear 暗色精致风，强调色 Supabase 绿 `#3ecf8e`
- **三轴正交的多色系支持**：`data-theme` 控制明暗；`data-palette` 切换整套底色基调（12 套：默认暖纸，护眼低调向 Solarized / Everforest / Nord / Catppuccin / Rosé Pine，深色向 Dracula / Tokyo Night / One Dark，彩色向 Monokai / Gruvbox / Ayu）；`data-accent` 切换强调色（绿、蓝、紫等 6 种）。三者独立组合，互不干扰。
- **配色校准**：深色为暗色画布 `#151517` + 卡片逐层提亮；浅色为护眼暖灰画布 `#f2f1ec` + 柔米白卡片 `#faf9f6`（消除白屏刺眼感，深浅两主题统一保持逐层提亮纵深）；边框半透明黑/白分三档（subtle / 默认 / strong）；强调绿亮暗双值（暗底 `#3ecf8e`、浅底 `#157a54`）
- **图表体系**（v1.8.0 新增）：第四个正交轴——分类 8 槽固定顺序 + 顺序/序数/发散渐变 + 状态色复用，切色系/强调色都不变；纯 CSS + 内联 SVG 组件（折线/面积/柱/条/堆叠/环形/热力/发散），带零 JS 的 hover 准星/tooltip 与图例联动、阈值线与事件标记、小倍数、占比条、子弹图、加载骨架与空态、可展开的数据表格兜底、CVD 纹理通道与打印样式；几何与正交规则由 `deploy/verify-charts.py` 实测校验（含反例自测）。CVD 间距与对比度实测见 [`references/chart-audit.md`](references/chart-audit.md)
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
  demo.html                     完整应用外壳示例（侧栏 + 顶栏 ⌘K + 图表分区 + 表格分页 + 命令面板 + toast）
  demo.standalone.html          单文件版 demo，浏览器直接打开预览
references/
  style-guide.md                完整视觉规范（色板 / 排版 / 形态 / 反例）
  migration.md                  分技术栈迁移手册 + 升级已接入项目 + 验收清单
  contrast-audit.md             WCAG AA 对比度实测表 + 可复现回归脚本
  chart-audit.md                图表色板实测（CVD 间距 / 明度带 / 12 色系对比度）
  audit.py                      八项校验回归脚本：python3 references/audit.py
deploy/nginx.conf               demo 页面的 nginx 部署配置
deploy/gen-demo-charts.py       demo 图表分区生成器（SVG 几何由数据计算）
deploy/verify-charts.py         图表几何/字号/正交校验（--self-test 跑反例）
docs/                           skill 设计过程文档
```

## 不适用范围

- 纯后端 / CLI 项目
- 无源码的打包产物（如 MediaCrawler webui）
