# 模型与权重

想看 AI 实际做过什么板，可以看 Claude 和 GPT 的原型记录。想在自己的电脑上运行模型，可以从 SchGen 的原理图示例、Micius-Flash 的完整权重，或 PCBWorld 的布线策略开始。[各模型在公开任务上的成绩](benchmarks.md)

## 头部厂商的通用模型

- [Claude Fable 5.2](https://www.anthropic.com/research/claude-electronics-design) — **三款实物原型。** Anthropic 和 Diode 给模型简短的产品要求。模型设计了 USB-C 会议扬声器、语音助手主机和掌上电子宠物的电路板、外壳与固件。Diode 工程师制作并测试了原型。Anthropic 对三款电路的原话是“worked without any fixes to their circuitry”，即电路均未返修便可工作。研究仍待完成天线调谐、热测试和认证。双方还披露，从 Sonnet 4.5 起，训练任务包括让 Claude 依据芯片手册设计外围参考电路，再按电气要求检查生成结果。[模型发布稿](https://www.anthropic.com/claude-fable-and-mythos-5-2) · [Diode 参与的训练方法](https://claude.com/resources/articles/making-claude-a-better-electrical-engineer)
- [GPT-6 Astra](https://openai.com/index/gpt-6-astra/) — **KiCad 布局布线与手持设备。** OpenAI 首发演示从已有原理图出发，在 KiCad 中摆放元件、绘制铜线。后续项目从“手持设备能与 Codex 对话”的要求出发，由 Astra 选器件、设计电路板和外壳。两名团队成员参与项目，代工厂生产了一小批样机。OpenAI 对交付规模的原话是“a small batch of prototypes”。制造前经过多轮评审，重点包括公差和装配细节。首发稿提到面向专业软件的训练，PCB 训练集和配方尚未披露。[手持设备实物记录](https://openai.com/index/accelerating-engineering-for-the-physical-world/)
- [GPT-6.2 Astra 与 Sol](https://openai.com/index/introducing-gpt-6-2-astra-sol/) — **新版本的公开证据。** 6.2 发布稿列出 BenchCAD 2.1 工程评测。上面的 KiCad 视频和手持样机使用的是 GPT-6 Astra。复现实验时，应分别记录模型版本和推理设置。OpenAI 将 Ultra 定义为可调用多个子智能体分工的推理模式。[模型与推理设置](https://learn.chatgpt.com/docs/models)
- [GLM-5.4](https://www.zhipuai.cn/zh/research/164) — **机械设计与三维演示。** 智谱首发展示了六轴机械臂。模型在 FreeCAD 中建模，再用 Blender 编排抓取动作。独立测试者 TOKRACE 另行公开了掌机的 Blender 工程，拆解视图里能看到电路板外形。该工程提供三维网格和渲染图。这两份资料均未给出 PCB 原理图、铜线连接或板级专项训练细节。11 月 23 日发布时，GLM Coding Plan 已提供访问，智谱计划随后公开权重。11 月 24 日核对时，智谱的 Hugging Face 账号仍未列出 5.4 权重。[掌机工程与生成脚本](https://www.tokrace.com/en/guides/glm-5-4#handheld) · [智谱模型库](https://huggingface.co/zai-org/models?search=GLM-5.4)

## PCB 专项模型与工程模型

### 可下载的权重

- [Micius-Flash（墨子）](https://huggingface.co/zhiman-ai/Micius-Flash) — **知满的 27B 多模态工程模型，提供完整权重。** 在论文的一个案例中，输入是空白原理图和固定的板框。模型通过 Micius Harness 操作 KiCad，生成了 5 V 自锁开关电路和含 9 个封装的双层板，并检查网表和铜线连接。团队披露了半导体领域训练和经工具执行验证的样本。模型库提供 11 个 BF16 权重分片，合计约 54.7 GB，权重许可适用于非商业研究。复现 KiCad 案例还需要单独配置 Harness 和工具。[权重文件](https://huggingface.co/zhiman-ai/Micius-Flash/tree/main) · [论文案例](https://arxiv.org/html/2611.10015v1#S6.p5) · [工具回放与 API](https://zhiman.cn/zh/models/micius)
- [SchGen](https://huggingface.co/microsoft/SchGen) — **生成可编辑原理图的 LoRA 适配器。** 适配器是一组加在基础模型上的训练参数。微软团队公开了适用于 `openai/gpt-oss-20b` 的权重。示例要求用 AP2112K 设计 3.3 V 稳压电源。模型生成 Python 代码，导出程序再生成 KiCad 原理图。[适配器配置](https://huggingface.co/microsoft/SchGen/blob/main/adapter_config.json) · [运行与导出示例](https://github.com/microsoft/SchGen)
- [AI KiCad PCB Architectural Planner](https://github.com/Ssbullock/pcb-layout-llm) — **布局布线前的规划适配器。** 作者用 KiCad 设计样本微调 Qwen2.5-Coder-32B-Instruct。模型读取网表和封装几何摘要，输出两份 JSON 文件，分别描述哪些器件应靠近，以及怎样给电源线定宽、给总线留通道。下游布局器和布线器据此计算坐标并绘制走线。仓库提供训练脚本，模型库单独发布 LoRA 参数。[适配器文件](https://huggingface.co/Simonssb/qwen2.5-coder-32b-pcb-grpo/tree/main)
- [PCBWorld](https://huggingface.co/LG-AI-Research/PCBWorld) — **逐步布线的策略权重。** 策略读取当前布线状态，选择下一步动作，由 KiCad 引擎执行。模型库把规则网格训练的策略放在 D1 目录，把无网格合成板训练的策略放在 D2 目录。两组权重均供研究和教育使用。[权重目录](https://huggingface.co/LG-AI-Research/PCBWorld/tree/main) · [运行环境](https://github.com/LGAI-Research/PCBWorld)
- [CADET](https://huggingface.co/LG-AI-Research/CADET) — **六份可加载的布线策略权重。** 在同一块未布线的板上，可比较 `cadet_bc.pt` 和 `cadet.pt`。前者从布线动作示范中学习，后者在此基础上经强化学习微调。两者都通过 PCBWorld 执行动作，交付的板文件可用 KiCad 检查。权重供研究和教育使用。[权重文件](https://huggingface.co/LG-AI-Research/CADET/tree/main) · [运行与检查](https://github.com/LGAI-Research/CADET)

### 托管布局布线服务

- [Quilter](https://www.quilter.ai/product) — **在线布局布线服务。** 上传原理图和带板框、安装孔及固定元件的板文件，服务返回可编辑的候选布局。团队称其用合成板和物理约束训练布局系统。Project Speedrun 公布了 Linux 计算机两块板的多个版本，可对照自动生成的布局与工程师整理后的生产文件。[输入要求](https://docs.quilter.ai/get-started/quickstart) · [样板设计文件](https://www.quilter.ai/project-speedrun/download)

如需从头训练布局策略，可跟着 RL_PCB 的例子操作。若要给已有原理图评分，可直接运行 PCBSchemaGen 的引脚检查程序。[训练与复现](training.md) · [PCBSchemaGen 检查程序](https://github.com/HZou9/PCBSchemaGen_v2/blob/main/framework/score_design.py)
