# 论文选读

从图纸到实物，一块板要经过原理图设计、元件布局、铜线布线和工程审查。下面按任务列出论文、研究方法和可取得的资料。

## 原理图理解与生成

- [OmniSch](https://arxiv.org/abs/2604.00270 "OmniSch: A Multimodal PCB Schematic Benchmark For Structured Diagram Visual Reasoning")（ECCV 2026）— 用 1,854 张原理图测试模型能否找到器件、认出连线，并把图转成网表。网表记录每个引脚连接到哪里。评分分别衡量定位、连接和几何关系。[项目与数据](https://www.omnisch.com/)
- [PCBnet](https://arxiv.org/abs/2608.27923 "PCBnet: A Dataset and Automatic Construction of SPICE Netlists from Schematic Images")（ICLAD 2026）— 把原理图图片转换成 SPICE 电路仿真网表。作者报告的器件检测平均精度为 94.54%，端到端连接准确率为 84.47%。作者仓库提供 300 个展示样本，完整代码受知识产权限制。[作者仓库](https://github.com/ECNUACRush/PCBnet)
- [SchGen](https://arxiv.org/abs/2605.30345 "SchGen: PCB Schematic Generation with Semantic-Grounded Code Representations")（2026）— 从文字需求生成可编辑的 KiCad 原理图。模型用引脚名称指定连接，用相对位置放置符号。作者发布了模型适配器、训练数据和导出原理图的示例。[代码与模型](https://github.com/microsoft/SchGen)
- [PCBSchemaGen](https://arxiv.org/abs/2602.00510 "PCBSchemaGen: Reward-Guided LLM Code Synthesis for Printed Circuit Boards (PCB) Schematic Design with Structured Verification")（2026）— 从器件手册提取封装和引脚信息，用五层验证器检查设计，再把错误定位到具体引脚供模型修改。两套基准共有 227 道题，衡量设计满足指定结构规则的能力。[验证器与题库](https://github.com/HZou9/PCBSchemaGen_v2)
- [HWE-Bench](https://arxiv.org/abs/2603.18102 "HWE-Bench: Can Language Models Perform Board-level Schematic Designs?")（2026）— 作者用 300 道板级原理图任务研究模型能否根据需求和器件手册生成连接方案。评测先检查静态电气规则，再用 LTspice 仿真检查电路行为。公开仓库提供浴室排风扇样例。[评测代码](https://github.com/EDI-Systems/HWE-Bench)
- [PCB 原理图符号生成](https://doi.org/10.1145/3670474.3685944 "An ML-aided Approach to Automatically Generate Schematic Symbols in PCB EDA Tools")（MLCAD 2024）— 从器件封装图识别引脚的位置与方向，把引脚编号和名称配对，再生成两侧或四侧带引脚的原理图符号。这项工作处理的是元件库中的单个符号。[会议议程](https://mlcad.org/symposium/2024/wp-content/uploads/2024/07/MLCAD-Program-2024.pdf#page=1)
- [功率变换器原理图综合](https://arxiv.org/abs/2610.38201 "From Natural Language to Real Schematics: An Automated Workflow for Power Electronics Schematic Synthesis")（2026 预印本）— 从供电规格出发，查器件手册选型，用 ngspice 检查瞬态行为，再导出可编辑的 KiCad 原理图。论文用降压变换器和隔离式双有源桥各做一次端到端验证，分别检查仿真结果和重新导出的网表。

## 元件布局

- [RL_PCB](https://past.date-conference.com/proceedings-archive/2024/DATA/1040_pdf_upload.pdf "Learning Circuit Placement Techniques Through Reinforcement Learning with Adaptive Rewards")（DATE 2024）— 让模型反复移动元件，用完成布线后的走线长度比较布局。实验只有 9 个基础电路，每个含 3 至 12 个元件，其中 6 个用于训练、3 个用于测试。[代码与电路](https://github.com/LukeVassallo/RL_PCB)
- [Cypress](https://www.csl.cornell.edu/~zhiruz/pdfs/cypress-ispd2025.pdf "Cypress: VLSI-Inspired PCB Placement with GPU Acceleration")（ISPD 2025）— Cypress 用 GPU 求解元件位置，重点处理非关键元件。公开基准由商业设计合成。可把它作为解析布局基线，与学习方法比较布局耗时、能否完成布线和实际走线长度。[代码与基准](https://github.com/NVlabs/Cypress)
- [强化学习辅助模拟退火布局](https://ieeexplore.ieee.org/document/10652635 "Reinforcement Learning-Based Placement Method for Printed Circuit Board")（ICCCAS 2024）— 用强化学习帮助模拟退火算法挑选元件布局，研究能否缩短求解时间。作者报告，相比原模拟退火算法，在其测试中保持了相当的布局质量，运行时间减少了一半以上。

## 板级布线

- [FanoutNet](https://doi.org/10.1609/aaai.v37i7.26030 "FanoutNet: A Neuralized PCB Fanout Automation Method Using Deep Reinforcement Learning")（AAAI 2023）— 研究扇出，即怎样从密集的焊盘周围引出第一段走线，为后续布线留出空间。模型读取布局和网表选择扇出方式，再把结果交给布线器。作者在工业板样例上比较了走线长度。[摘要与索引](https://mlanthology.org/aaai/2023/li2023aaai-fanoutnet/)
- [PCBench](https://61dac.conference-program.com/presentation/?id=RESEARCH617&sess=sess237 "PCBench: A Dataset for Printed Circuit Board Routing")（DAC 2024 工作进展海报）— 从开源板文件抽取布线问题与已有解，用 JSON 描述板框、网络、规则和走线。仓库有数据增强脚本和强化学习环境。不同版本的板数见[数据集说明](data.md#pcbench)。[数据与脚本](https://github.com/PCBench/PCBench)
- [PCBWorld](https://arxiv.org/abs/2607.05915 "PCBWorld: A Benchmark Environment for Engine-Grounded PCB Design Automation")（2026）— 让智能体操作 KiCad 的布线引擎，使用工具反馈选择下一步动作。作者提供合成板生成器和 679 块来自开源项目的板设计。最终板文件按统一指标评分，其中包括网络连接和设计规则检查。[环境与评测代码](https://github.com/LGAI-Research/PCBWorld)
- [PCBRouteAgent](https://arxiv.org/abs/2611.08175 "PCBRouteAgent: How Close Are LLM Agents to Becoming PCB Routing Engineers?")（2026）— 模型决定布线顺序、走线区域和换层位置，KiCad 根据这些指令生成铜线。Opus 5.5 配置在 99 块小板中有 94 块全部接通且无错误级违规。中型和大型双层板各测试 10 块，分别通过 10 块和 4 块。[作者仓库](https://github.com/chip-ai-agent/PCBRouteAgent)
- [CADET](https://arxiv.org/abs/2611.16913 "CADET: Construction of PCB Routing Instances with Executable Demonstrations")（2026）— 先让模型模仿布线示范，再用强化学习训练。作者报告生成 10 万块合成训练板，并在独立选出的 141 块中型双层板上评测。在这批板上，单次布线的整板通过率平均为 67.2%。[生成与回放代码](https://github.com/LGAI-Research/CADET) · [141 块测试板清单](https://github.com/LGAI-Research/CADET/blob/main/cadet/configs/splits/boards_d3b_test.txt)
- [TRouter](https://www.cse.cuhk.edu.hk/~byu/papers/J94-TCAD2023-TRouter.pdf "TRouter: Thermal-Driven PCB Routing via Nonlocal Crisscross Attention Networks")（IEEE TCAD 2023）— 用元件、焊盘、过孔和走线预测板上的温度分布，再据此调整走线绕行和过孔位置。论文用热仿真核对结果。作者的公开仓库提供四份尚未布线的 KiCad 板文件。[测试板](https://github.com/plutochen1990/TRouterBM)

## 设计理解与工程审查

- [PCB-Bench](https://proceedings.iclr.cc/paper_files/paper/2026/hash/051f3997af1dd65da8e14397b6a72f8e-Abstract-Conference.html "PCB-Bench: Benchmarking LLMs for Printed Circuit Board Placement and Routing")（ICLR 2026）— 用文字题、看图题和 170 多个完整工程检查模型能否理解设计。例如，模型要解释元件的作用，或根据板图判断走线关系。题目主要按回答质量评分。[项目与题库](https://github.com/digailab/PCB-Bench)
- [DRCY](https://arxiv.org/abs/2603.15672 "DRCY: Agentic Hardware Design Reviews")（2026）— 用元件手册逐个核对原理图引脚，把发现的问题写成审查意见。例如，它会检查稳压器的反馈电阻能否产生目标输出电压。论文给出 AllSpice Hub 的实际使用流程和审查示例。

## 实板制作与测量

- [JARVIS](https://arxiv.org/abs/2611.26503 "JARVIS: An Agent That Designs, Builds, and Tests Circuit Boards on Its Own")（2026，预印本）— 实验人员确认方案后，系统驱动设备打印、贴装并测试一块 60 Hz 陷波滤波器板。作者报告实板在 60 Hz 的衰减为 50.6 dB。系统根据测量结果在 KiCad 中修改设计，并在数字模型里预演了第二版。
