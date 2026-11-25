# 开源与公开数据集

要训练模型读原理图，可以从带引脚和网络标注的图开始。要训练布线，先找能打开的板文件或能重放的动作。拿到板文件后，可以对照[原始 PCB 数据质量](data-procurement.md)检查版本和连接。

## 原理图与网表

- [SchGen_dataset](https://huggingface.co/datasets/microsoft/SchGen_dataset)（2026）— 将设计要求与生成 KiCad 原理图的代码配对。公开训练集有 8,420 条增强样本，同一设计可以对应多个样本。Hugging Face 数据卡标注 MIT，文件页提供 JSONL 和 KiCad 原理图。[生成与转换代码](https://github.com/microsoft/SchGen)
- [OmniSch](https://www.omnisch.com/)（2026）— 论文报告 1,854 张真实原理图，标注器件位置、文字和网络连接。官网的公开样例包包含 5 个设计，例如 Adafruit FunHouse，适合对照原图和 JSON 标注。[论文](https://arxiv.org/abs/2604.00270) · [样例包](https://drive.google.com/file/d/1GRPNowJNRixrFIWvS7YSkhp_k7erUV6y/view)
- [BenchPCNP](https://github.com/MrBade/BenchPCNP)（2026）— 50 套电路的网表配有 54 类功能模块标签，可用来研究哪些器件共同完成一项功能。公开材料包含网表、图数据和构建代码。[数据论文](https://www.nature.com/articles/s41597-026-06818-y)

## 板文件与布线过程

- [PCBench](https://github.com/PCBench/PCBench)（DAC 2024 工作进展海报）— README 介绍了 164 块板，仓库主清单列出 1,194 个设计、846 个来源仓库。可从单个样例对照原始与清理后的 KiCad 板文件，并查看 JSON 中的布线规则和参考走线。[主清单](https://raw.githubusercontent.com/PCBench/PCBench/main/PCBs/master_metadata.json) · [降压电源板样例](https://github.com/PCBench/PCBench/tree/main/PCBs/C-BISCUIT_buck-reg-5v)
- [pcb-corpus](https://github.com/punkfab/pcb-corpus) — 从 170 个开源硬件仓库整理出 235 块 KiCad 板。每块板都有原设计和去除布线后的副本，保留项目规则，方便比较自动布线与原设计。每块板的 `SOURCE.json` 记录上游仓库、提交和处理过程，使用时可逐板核对随附许可。[来源与许可说明](https://github.com/punkfab/pcb-corpus#licences)
- [CADET / RouteDemos](https://github.com/LGAI-Research/CADET)（2026）— 从合成板生成可重放的布线动作。论文报告了 10 万块合成训练板，代码提供生成器和重放检查，可验证一串操作能否在布线引擎中产生有效结果。仓库给出生成步骤，代码和预训练权重分别列明许可。[论文](https://arxiv.org/abs/2611.16913)
- [tscircuit autorouting-dataset-01](https://github.com/tscircuit/autorouting-dataset-01) — 200 个自动布线问题，用 TypeScript 描述元件和连接关系。仓库提供预览入口，可以先看题目怎样摆放元件，再检查需要连接哪些引脚。

## 制造与外观检测

- [DeepPCB](https://github.com/tangsanli5201/DeepPCB) — 1,500 对已对齐的裸板扫描图，每对包含无缺陷模板和待测图像。标注覆盖开路、短路、针孔等六类缺陷。作者在待测图像上额外添加了人工缺陷，数据集说明限定为研究用途。
