# 评测基准

ALE 的两道 KiCad 工程题、OmniLayout 元件布局、BenchCAD T6 接线恢复，以及各模型的实测成绩与答卷。

| 基准 | 考查能力 | 模型成绩示例 |
| --- | --- | --- |
| [Agents’ Last Exam（ALE）](#ale) | 用 KiCad 做整板布局，或修复已有工程 | 整板题满分 1。DeepSeek V4.1 Flash 得 **1**，Qwen4-Max-Preview 得 **0**。[团队答卷 ↓](#team-runs) |
| [OmniLayout](#omnilayout) | 摆放元件，再检验能否完成布线 | GPT-5.5 一次提交的端到端通过率为 **15.23%**，增加原理图后为 **42.83%**。 |
| [BenchCAD 2.0 T6](#benchcad-t6) | 从板图恢复器件引脚之间的连接 | 12 块板的均分，满分 1。GPT-6 Astra **0.4222**（修正后），Claude Opus 5.5 **0.3983**。 [SIGVoid 练习题轨迹 ↓](#public-t6) |

<h2 id="ale">Agents’ Last Exam（ALE）· 两道 KiCad 工程题</h2>

<h3 id="team-runs">SIGVoid 的四次模型实测</h3>

| 模型 | 整板布局 · 满分 1 | 导航开关修复 · 满分 1 |
| --- | ---: | ---: |
| DeepSeek V4.1 Flash | <strong>1</strong> · <a download href="../../assets/runs/ale-mini-deepseek.zip" aria-label="下载 DeepSeek 整板布局的操作轨迹与答卷">轨迹与答卷 ↓</a> | <strong>0</strong> · <a download href="../../assets/runs/ale-navswitch-deepseek.zip" aria-label="下载 DeepSeek 导航开关的操作轨迹与答卷">轨迹与答卷 ↓</a> |
| Qwen4-Max-Preview | <strong>0</strong> · <a download href="../../assets/runs/ale-mini-qwen4.zip" aria-label="下载 Qwen4 整板布局的操作轨迹与答卷">轨迹与答卷 ↓</a> | <strong>0</strong> · <a download href="../../assets/runs/ale-navswitch-qwen4.zip" aria-label="下载 Qwen4 导航开关的操作轨迹与答卷">轨迹与答卷 ↓</a> |

2026 年 11 月 14 日，两个模型在 ALE v1.1 的 Windows 10 环境中各做两题，每题一次。DeepSeek 使用 max，Qwen 使用 xhigh。每个 ZIP 都含可在 KiCad 打开的答卷、逐次工具调用表 `operations.csv` 和当次评分 `eval_result.json`。

<details class="run-trace">
<summary>展开查看两次整板布局的操作记录</summary>
<p><strong>DeepSeek</strong> · 在第 106 步的工具返回中，KiCad 报告 7 处违规、27 个未连接项。第 274 步，两项均已归零，原理图与板图仍有 34 项不一致。到第 314 步，三项均为零。</p>
<p><strong>Qwen</strong> · 第 170 步对应的三项计数为 14、1、34，第 235 步与第 265 步均为 0、0、0。归档的评分结果为 0。此次评分器的 DRC 报告未保存，现有记录不足以确定零分的具体原因。</p>
<p>两次布局运行都调用过 Python 布线脚本。下载后，在 <code>operations.csv</code> 的 <code>result_step</code> 列可以定位这些工具返回。</p>
</details>

**两份导航开关答卷为什么都是零分？** 两个模型都修复了 U4。DeepSeek 提交了 `.rpt` 检查报告，评分器要求的 `erc.json`、`drc.json`、`project.net` 和 `board.d356` 均缺失。Qwen 的两个 JSON 报告齐全，另外四个文件的名称与清单不符，还缺少独立的 `drill/` 目录。两份交付都未通过必交文件检查。

<h3 id="ale-layout">整板布局 · 装进 SN25 外壳</h3>

**交付物**是完成布线的 KiCad 板文件。模型须在 KiCad 打开给定的 Mini Encabulator 原理图，导入封装，完成布局和布线。四个 M3 安装孔的中心构成 1.575 × 1.26 英寸的矩形。板的正反面都要铺地铜，并用接地过孔连接。[原题与输入说明](https://github.com/rdi-berkeley/agents-last-exam/blob/2e91edd3cd26baa35a38127c90c8e5241dfbe62f/tasks/engineering/pcb_layout_kicad_1/task_card.json)

**评分器重新运行设计规则检查（DRC）。** 检查报错、仍有未连通项，或评分器无法取得有效报告，均得 **0 分**。DRC 通过后，如果孔距、板框、地铜等结构检查仍有一项失败，得 **0.5 分**。全部通过得 **1 分**。[评分代码](https://github.com/rdi-berkeley/agents-last-exam/blob/2e91edd3cd26baa35a38127c90c8e5241dfbe62f/tasks/engineering/pcb_layout_kicad_1/scripts/score_outputs.py) · [在 Harbor 中运行这道题](harbor.md)

<h3 id="ale-navswitch">工程修复 · 给导航开关板恢复 U4</h3>

**故障在 U4 的封装关联。** 模型须在 KiCad 桌面界面为 U4（PCA9554）选回工程自带的封装，再从原理图更新 PCB。原题禁止直接改写 KiCad 源文件文本。交付物包括修复后的工程、本地库、网表、检查报告、Gerber 和钻孔文件。[原题与交付清单](https://github.com/rdi-berkeley/agents-last-exam/blob/2e91edd3cd26baa35a38127c90c8e5241dfbe62f/tasks/engineering/kicad_navswitch_library_integration_release_002/task_card.json)

**评分器先核对原理图和 PCB 上的 U4，再检查必交文件。** 任一硬性条件失败即得 **0 分**。通过后按项计分，例如 U4 各引脚的网络与参考网表一致占 **0.20 分**，Gerber 文件清单匹配占 **0.10 分**。[评分代码](https://github.com/rdi-berkeley/agents-last-exam/blob/2e91edd3cd26baa35a38127c90c8e5241dfbe62f/tasks/engineering/kicad_navswitch_library_integration_release_002/scripts/score_outputs.py)

<h3 id="ale-results">官方成绩 · Windows 组</h3>

ALE v1.1 官方榜单统计 36 道 Windows 题，两道 KiCad 题也在其中。榜单只公布各组和全套任务的汇总成绩。GPT-6.2 Astra 在这两道 KiCad 题上各得多少分，表中未列出。[官方榜单，2026 年 11 月 18 日](https://agents-last-exam.org/api/demo/leaderboard/v1.1) · [官方运行回放](https://agents-last-exam.org/traces)

| 模型与运行配置 | Windows 组通过题数 | 全套通过题数 |
| --- | ---: | ---: |
| Qwen 4 · Codex，xhigh | 16 / 36 | 57 / 122 |
| Kimi 3.1 Pro · Kimi Code，max | 15 / 36 | 53 / 122 |
| GPT-6.2 Astra · Codex，xhigh | 15 / 36 | 58 / 122 |

<h2 id="omnilayout"><span id="omnilayout-2">OmniLayout · 元件布局</span></h2>

模型读取板框、网表和元件尺寸，提交每个元件的坐标、旋转角和所在板面。评测器检查元件重叠和越界，再用 Freerouting 尝试布线。[任务定义与评测方法](https://arxiv.org/html/2607.03261v3#S4.SS1) · [公开布局样例](https://www.omnieda.com/)

| 模型 | 基础输入 | 另附原理图 |
| --- | ---: | ---: |
| GPT-5.5 | 15.23% | 42.83% |
| Qwen3.6-35B-A3B | 5.31% | 24.45% |

指标为一次提交的端到端通过率（E2E Pass）。论文另测了模型查看布局图、重叠检查和布线反馈后多轮修改的成绩。截至 2026 年 11 月 25 日，作者榜单尚未列出 GPT-6.2、Claude Fable 5.2 或 GLM-5.4 的布局成绩。[一次提交，表 2](https://arxiv.org/html/2607.03261v3#S5.T2) · [多轮修改，表 3](https://arxiv.org/html/2607.03261v3#S5.T3) · [作者榜单](https://www.omnieda.com/#leaderboard)

<h2 id="benchcad-t6"><span id="benchcad-2-0-t6">BenchCAD 2.0 T6 · 从板图恢复接线</span></h2>

作者公开的样例有六张板图：正面、背面各一张，两面各有两张斜视图。多层板另给每个内层的铜图，可沿过孔继续追线。模型可以用离线 Python 放大、裁剪图像。答卷列出器件在顶视图中的位置、各端子和所属网络。评分器按位置匹配器件，再核对接线。[样例的六张板图](https://github.com/BenchCAD-org/benchcad-2-main/tree/v2.0-core1/examples/task6/cases/case1/input/views) · [题目要求与答卷格式](https://github.com/BenchCAD-org/benchcad-2-main/blob/v2.0-core1/envs/t6_pcb2schematic/TASK_position.md)

**2.0 的 T6 分项**含 12 块板，每个模型每块板运行一次，推理强度为 max。GPT-6 Astra 原始均分为 0.4639，其中一题在模型未正式提交时获得了分数。按作者修正的规则，该题计零，T6 均分为 **0.4222**。Claude Opus 5.5 均分为 **0.3983**。[分项成绩](https://github.com/BenchCAD-org/benchcad-2-main/blob/main/results/core_reference.json) · [提交规则修订](https://github.com/BenchCAD-org/benchcad-2-main#readme)

**2.1 全套**含六类任务、共 100 题。在自定义运行环境和 max 推理强度下，Claude Fable 5.2 配 Claude Code 得 **0.835**，GPT-6.2 Astra 配 Codex 得 **0.825**。该榜单尚未单列两者的 T6 成绩。[2.1 官方榜单](https://benchcad.com/leaderboard)

<h3 id="public-t6">SIGVoid 实测 · 9 道 Public 练习题</h3>

每个模型每批做同样的 9 道题，每题一次。我们用 2.1 版 T6 评分器评分，单题未设轮数上限和输出 token 上限，缺卷按零分计入均值。官方 Core 分项使用另外 12 块板。

| 模型与推理强度 | 第一批均分 | 第二批均分 |
| --- | ---: | ---: |
| DeepSeek V4.1 Flash · max | 0.1295 | 0.1200 |
| Qwen4-Max-Preview · xhigh | 0.0839 | 0.1389 |
| Qwen3.8-Max · xhigh | 0.0768 | 未测试 |

**逐题操作轨迹。** 45 次作答共记录 1,432 条操作，41 次交回了接线答卷。按模型、批次和题号筛选 CSV，可以查看每轮的动作、程序退出码和该题的最终得分。图像操作标签来自该轮代码。

- Qwen4-Max-Preview，第二批 `case009`。第 3 轮的代码包含裁剪图像的操作，第 6 轮提交接线答卷，得 0.6667 分。
- Qwen3.8-Max，第一批 `case004`。程序运行失败（退出码 1）。模型随后请求提交，提交程序也运行失败。这次没有生成答卷，得 0 分。

<a href="../../assets/runs/benchcad-public-t6-traces.csv" download>下载逐题操作轨迹 CSV ↓</a> · <a href="../../assets/runs/benchcad-public-t6.csv" download>下载五批成绩 CSV ↓</a> · [Public 数据使用条款](https://huggingface.co/datasets/BenchCAD/benchcad-2.0-public#evaluation-terms)
