改引脚连接时，打开原理图，再把改动同步到板文件。查钻孔偏移时，把发给板厂的钻孔文件与板框叠在一起看。

## 打开并编辑原工程

- [KiCad](https://www.kicad.org/discover/) — 打开项目的 `.kicad_pro`，在原理图中选中连接器，再在 PCB 编辑器中定位同一位号。复查别人的结果时一起保存项目规则、符号库和封装库。开源，可本地运行。
- [LibrePCB](https://librepcb.org/docs/user-manual/project-editor/output-jobs/) — 用项目中的 Output Jobs 定义要生成的板图、钻孔和装配文件。图形界面和命令行可以使用同一套输出设置，适合一份设计需要多次发布的场景。[命令行入口](https://librepcb.org/docs/cli/open-project/)
- [嘉立创 EDA 专业版（EasyEDA Pro）](https://prodocs.easyeda.com/en/quick-start.html) — 在同一工程中编辑原理图与 PCB，分别导出制板 Gerber、物料清单和贴片坐标。让板厂做贴装时，可先用位号核对物料表和坐标表。[制板导出](https://prodocs.easyeda.com/en/pcb/export-pcb-fabrication-file-gerber/index.html) · [坐标导出](https://prodocs.easyeda.com/en/pcb/export-pick-and-place-file/)
- [Altium Designer](https://www.altium.com/documentation/altium-designer/preparing-for-manufacture/output-jobs) — 交接 Altium 项目时找 `.PrjPcb` 和 `.OutJob`。后者记录哪些设计文件用来生成哪些输出，也能包含验证报告。重做一个发布包时，先查它选中了哪块板和哪个装配变体。
- [Cadence Allegro X](https://www.cadence.com/en_US/home/tools/pcb-design-and-analysis/allegro-x-design-platform.html) — 如果源工程使用 Allegro，先查 Constraint Manager 中网络或网络类继承的间距、电气和物理约束。与其他布局结果比较前，核对两次使用的规则集。[约束对象与继承](https://community.cadence.com/cadence_blogs_8/b/pcb/posts/leverage-object-hierarchy-for-effective-constraint-management)

## 写电路、验证电气行为

- [SKiDL](https://github.com/devbisme/skidl) — 用 Python 声明器件、引脚和网络，生成网表。用它生成重复通道时，可从导出的网表里各取一条电源网和一条信号网，核对通道之间的连接。
- [atopile](https://github.com/atopile/atopile) — 用 `.ato` 描述可复用电路模块，构建时检查连接和约束，更新 KiCad 板文件。在 KiCad 中检查封装和器件位置，保留源模块以便下次修改。
- [ngspice](https://ngspice.sourceforge.io/) — 将电路网表、器件模型和分析指令放在同一个输入文件中。做 RC 滤波器实验时，扫频读取增益和相位，另做瞬态分析读取阶跃响应。
- [LTspice](https://www.analog.com/en/resources/design-tools-and-calculators/LTspice-simulator.html) — 在图形编辑器里搭电路，使用厂商的器件模型运行仿真，在波形窗口选择节点。与另一种工具对照时，记录所用模型、信号源参数和输出节点。
- [Siemens HyperLynx SI](https://www.siemens.com/en-us/products/pcb/hyperlynx/signal-integrity/) — 用于板级信号完整性分析。布局后分析需要实际互连及层叠，数字接口还可能需要驱动器和接收器模型。读报告时检查其使用的模型、数据速率和拓扑。

## 放元件、接铜线、检查外壳

- [Cypress](https://github.com/NVlabs/Cypress) — 以板框、元件和网络为输入，用解析优化求元件位置。与学习方法比较时，保持锁定元件的位置相同，分别记录重叠和线长，再检验可布线性。
- [Freerouting](https://github.com/freerouting/freerouting) — 从板编辑器导出 Specctra DSN，用外部布线器生成 SES 会话文件，再将走线导回原工程。用原工程的约束重新运行设计规则检查。
- [PCBWorld](https://github.com/LGAI-Research/PCBWorld) — 在固定布局上，程序逐步调用 KiCad 布线引擎。需要观察每一步动作或训练策略时，使用它提供的环境、板生成器和评测入口。[训练与复现](training.md)
- [KiCad StepUp](https://www.kicad.org/external-tools/stepup/) — 在 FreeCAD 与 KiCad 之间交换板外形和三维模型。用机壳装配定位安装孔、板边接口与有高度限制的器件；缺少三维模型的位置需要另查机械尺寸。

## 自动检查、制板和装配

- [KiCad CLI](https://docs.kicad.org/10.0/en/cli/cli.html) — 对原理图运行 `sch erc`，对板运行 `pcb drc`。自动化任务若要在发现违规时失败，需按命令文档使用 `--exit-code-violations`。两份报告回答不同的问题。[检查实例](design-checks.md)
- [KiCad IPC API](https://dev-docs.kicad.org/en/apis-and-binding/ipc-api/for-addon-developers/index.html) — 当脚本要读取和修改编辑器中的对象时使用。在 KiCad 9 和 10 中，运行中的图形编辑器提供此接口。脚本只需检查或导出磁盘文件时，可直接使用 CLI。
- [KiBot](https://kibot.readthedocs.io/en/master/) — 通过版本控制中的配置运行检查、导出和打包。把配置与项目一同提交，使另一台机器能用同一份定义生成输出。
- [Ucamco Reference Gerber Viewer](https://www.ucamco.com/en/gerber/reference-gerber-viewer) — 用独立查看器打开实际交付的 Gerber 与钻孔文件。叠加板框、外层铜和孔，从一个通孔连接器检查对齐。
- [InteractiveHtmlBom](https://github.com/openscopeproject/InteractiveHtmlBom) — 从板文件生成可点选的装配图。点击某个物料组，就能定位这批位号在板的哪一面。
- [PcbDraw](https://github.com/yaqwsx/PcbDraw) — 从 KiCad 板文件生成 SVG 板图。用 Populate 分步画出要装的元件，适合制作手工装配说明。

需要判断一套文件能否交付，可按[设计审查与交付](design-review.md)逐项对照设计要求、工程文件和最终导出物。
