## 接口与外形

- [Framework Expansion Cards](https://github.com/FrameworkComputer/ExpansionCards) 发布笔记本扩展卡的电路与机械设计资料。打开 KiCad 模板，对照机械图检查连接器的位置、板框和外壳空间。[KiCad 模板](https://github.com/FrameworkComputer/ExpansionCards/tree/main/Electrical/KiCad_templates) · [机械图](https://github.com/FrameworkComputer/ExpansionCards/tree/main/Mechanical)

## 供电与网络

- [Olimex ESP32-PoE](https://github.com/OLIMEX/ESP32-POE) 支持通过网线供电。打开 M2 版原理图，从网口沿供电网络找到相关器件，再用器件位号在同版 KiCad 板图中查找它们。[M2 版原理图与板文件](https://github.com/OLIMEX/ESP32-POE/tree/master/HARDWARE/ESP32-PoE-hardware-revision-M2)

## 多接口载板

- [Antmicro Jetson Nano Baseboard](https://github.com/antmicro/jetson-nano-baseboard) 从 1.5 版起提供 KiCad 工程。根目录里的 `supply.kicad_sch`、`interfaces.kicad_sch` 和 `csi.kicad_sch` 分别对应供电、外设接口和相机接口。打开接口原理图，找到网口 `J3`。在同版本的板图中，`J3` 的 2、3 号焊盘分别连接 `ENET_TRD0_P` 和 `ENET_TRD0_N`。高亮其中一个网络，就能沿着铜线检查它的去向。[接口原理图](https://github.com/antmicro/jetson-nano-baseboard/blob/d8d0b2d71ab4cc4bcdb204a09f78be40d4c8cda3/interfaces.kicad_sch) · [对应板文件](https://github.com/antmicro/jetson-nano-baseboard/blob/d8d0b2d71ab4cc4bcdb204a09f78be40d4c8cda3/jetson-nano-baseboard.kicad_pcb)

第一次打开 KiCad 工程，可以跟着[官方入门教程](https://docs.kicad.org/10.0/zh/getting_started_in_kicad/getting_started_in_kicad.html)看一遍从原理图更新 PCB、放置器件和运行设计规则检查的过程。

## 微控制器的最小系统

[Raspberry Pi RP2040 Minimal Viable Board](https://pip.raspberrypi.com/documents/RP-008296-DS) 的 R3-S1 包含原理图、板图、物料表和同版 PDF。先在芯片 U3 找 45 脚，再在板图中高亮 `+1V1`。这个工程适合练习从芯片内部稳压器的输出追到数字内核供电脚。官方另行发布 Pico 和 Pico W 的 Allegro 设计文件。[官方文件目录](https://pip.raspberrypi.com/categories/814-rp2040) · [跟做一次网表核对](rp2040-power.md)
