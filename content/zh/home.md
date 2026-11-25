Roadbook AI4PCB 持续整理 **AI 辅助印制电路板（PCB）设计**的论文、开源工具、数据集和评测。硬件工程师可以按原理图、布局、布线和设计审查查找方法。AI 研究者可以找到板文件、训练样本，以及检查设计结果的程序。

## AI × PCB 论文精选

- [SchGen](https://arxiv.org/abs/2605.30345)（2026）从文字需求生成可在 KiCad 中编辑的原理图。模型用器件符号表示元件，按引脚名称写出连接。论文用连线准确率等指标检查结果。
- [PCBWorld](https://arxiv.org/abs/2607.05915)（2026）让不同布线方法操作同一个 KiCad 布线引擎。用同一批板卡和设计规则，可以比较哪些网络接通了、留下多少违规。
- [CADET / RouteDemos](https://arxiv.org/abs/2611.16913)（2026）作者报告为 10 万块合成训练板生成了布线示范。用公开的生成器可以创建样本，再用回放程序逐步重现铜线怎样接通。

[查看全部论文 →](papers.md)

## 从哪里开始

| 背景 / 需求 | 建议先看 | 后续阅读 |
| --- | --- | --- |
| 刚接触 PCB，想知道一块板是怎样画出来的 | [PCB 绘制流程](workflow.md)，从器件选型、原理图看到布局、布线和检查 | 对照[公开板卡](boards.md)，在工程里找到对应的文件 |
| 熟悉硬件，想了解 AI 已经能做哪些工作 | [论文精选](papers.md)，按原理图、布局、布线和设计审查选读 | 看[评测基准](benchmarks.md)采用什么输入和验收条件 |
| 想训练模型，需要原理图、板文件或操作轨迹 | [数据集](data.md)，先看数据包含哪些设计阶段 | 用[设计工具](tools.md)打开样本，核对网络与几何信息 |
| 想比较头部模型的评测成绩 | 先看 [ALE 两道 KiCad 题](benchmarks.md#ale)要求怎样交付 | 再比较[布局题](benchmarks.md#omnilayout)和[接线恢复题](benchmarks.md#benchcad-t6)分别量什么 |
| 想让 AI 帮忙检查或修改一份 KiCad 工程 | [KiCad 智能体与插件](agents.md)，按读图、改图或布线选工具 | 看一份[设计检查实例](design-checks.md)，对照哪些要求已经验证 |
| 想在本地运行一道 PCB 评测题 | [Harbor 环境示例](harbor.md)，打开 ALE 的 Mini Encabulator 原理图 | 下载题包，用 ALE 的评分程序检查板文件 |

## 阅读路线

### 在原理图和板图中找到同一个连接器

先读《PCB 绘制流程》中的[原理图编译](workflow.md#原理图编译)。再打开[Antmicro 载板](boards.md#多接口载板)的接口原理图，找到位号为 `J3` 的网口。在板图中搜索同一位号，检查 2、3 号焊盘分别接到哪个网络。

### 从论文读到可复现的实验

先读 [PCBWorld](https://arxiv.org/abs/2607.05915) 的任务定义，了解模型可以调用哪些布线操作。再按 [CADET 仓库](https://github.com/LGAI-Research/CADET)的 RouteDemos 小规模示例生成一组板，再回放布线动作。最后对照[布线评测实例](routing-scores.md)，检查报告给出的是网络接通率、设计规则违规数，还是所有网络接通且无违规的整板比例。

## 工程博客

可以从[追踪 RP2040 电源网](rp2040-power.md)、[核对贴片原点](assembly-origin.md)或[按板族划分训练集](board-family-split.md)开始。[查看全部工程博客 →](blog.md)

我们建了一个 AI × PCB 交流群，欢迎研究员和工程师来聊画板和模型评测。[加微信进群 →](about.md#collaborate)
