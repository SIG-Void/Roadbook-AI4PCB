投板前，对照器件手册核对焊盘编号，在板图上检查铜线和安装位置，再用制造文件复查钻孔和贴片位号。

<h2 id="footprints">器件手册与封装</h2>

**先核对编号。** onsemi BAT54SLT1G 的一个 SOT23 封装中串联了两只二极管。1 脚是第一只的阳极，2 脚是第二只的阴极，3 脚是公共点。在原理图中找出这三个脚连接的网络，再打开封装，按编号依次点选三个焊盘。若图上公共点接对了、封装的 3 号盘却落在另一个物理引脚上，板子会把这个网络引到错误位置。[BAT54SLT1G 引脚表](https://www.onsemi.com/pdf/datasheet/bat54slt1-d.pdf) · [KiCad SOT-23 库文件](https://gitlab.com/kicad/libraries/kicad-footprints/-/blob/master/Package_TO_SOT_SMD.pretty/SOT-23.kicad_mod)

**再核对尺寸。** 先按所选料号的数据手册核对器件外形。作为工艺对照，NXP 的 SOT23 封装图分别给出回流焊和波峰焊的推荐焊盘。用计划采用的焊接工艺选取尺寸图，在封装编辑器中量焊盘间距和长宽。检查装配图层的外形、丝印标记和元件占用边界，最后记录手册版本与库文件版本。[封装尺寸图](https://www.nxp.com/docs/en/package-information/SOT23.pdf) · [KiCad 封装图层约定](https://gitlab.com/kicad/libraries/klc/-/tree/6e8cbad9556359879d2b91f904d6df82517d97d1/content/footprint/F5)

<h2 id="layout">元件位置与实际电流路径</h2>

**先确定哪些东西必须固定。** 接口连接器受机壳开口约束，安装孔受螺柱约束。把板框和关键器件带入机械装配，检验插头能否插入、螺丝能否安装。Framework 提供了同一款扩展卡的电气模板和机械文件，适合练习这一步。[Framework 电气模板](https://github.com/FrameworkComputer/ExpansionCards/tree/main/Electrical/KiCad_templates) · [机械设计文件](https://github.com/FrameworkComputer/ExpansionCards/tree/main/Mechanical)

**沿回路摆电源器件。** 在降压转换器中，先分别画出开关导通和关断时的电流路径，找出电流变化最大的那一段。再在 PCB 上定位输入电容和开关器件，看它们之间的铜线围成了多大面积。Analog Devices 的 AN-139 把两种开关状态与实际布局放在了一起。[开关状态与布局图](https://www.analog.com/en/resources/app-notes/an-139.html)

**让高速约束对应具体接口。** 选一对差分网络，从连接器追到接收端，标出每次换层和参考平面的变化。把接口指南中适用于当前层叠的线距、阻抗和长度要求交给板编辑器。调长后，再看增加的线段位于哪里、回流参考是否连续。[TI 高速接口布局指南](https://www.ti.com/lit/an/spraar7j/spraar7j.pdf) · [KiCad 差分布线](https://docs.kicad.org/10.0/en/pcbnew/pcbnew.html#routing-differential-pairs)

<h2 id="fabrication">板厂与贴片厂各收到什么</h2>

| 交付物 | 在导出文件上做的检查 | 可定位的问题 |
| --- | --- | --- |
| 板框、铜层与钻孔 | 在独立查看器中叠加板框、外层铜、金属化孔和非金属化孔。放大一个通孔连接器。 | 原点错位、孔文件遗漏、轮廓来自另一版板。 |
| 物料清单（BOM） | 从一组共用物料的位号取一个，核对制造商料号、封装和本次是否装配。 | 同封装用了不同规格，或未装器件进了采购清单。 |
| 贴片坐标（CPL） | 对一个有方向的器件核对位号、单位、板面、旋转方向和引脚 1。 | 底面坐标镜像、原点不一致、器件旋转错误。 |

打开 Olimex 的 ESP32-PoE M2 目录，原工程位于 M2 目录内，随附的 Gerber 文件名使用 Rev_M。仅凭文件名无法判断铜层对应的修订版。一次可复核的交付应从选定工程导出整套文件，并保留版本和导出设置。[M2 工程](https://github.com/OLIMEX/ESP32-POE/tree/master/HARDWARE/ESP32-PoE-hardware-revision-M2) · [随附 Gerber](https://github.com/OLIMEX/ESP32-POE/tree/master/HARDWARE/ESP32-PoE-hardware-revision-M2/Gerbers) · [Ucamco 查看器](https://www.ucamco.com/en/gerber/reference-gerber-viewer)

装配端用位号把 BOM 和 CPL 连起来。一个位号能在板图上找到，还要核实该器件是否应进入这次贴装。可以用 [JLCPCB 的 BOM 与坐标示例](https://jlcpcb.com/help/article/how-to-generate-the-bom-and-centroid-file-from-kicad)熟悉字段，再用[一块实际的双面板](assembly-origin.md)检查更换坐标原点后的结果。
