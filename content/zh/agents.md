手上有一份 KiCad 工程，可以让 AI 读取板文件、修改原理图，或者把待布线的板交给外部布线器。

## 先读懂已有设计

- [KiCad Happy](https://github.com/aklofas/kicad-happy)（MIT）提供可以单独运行的 Python 分析脚本。板图分析器读取 `.kicad_pcb`，原理图分析器读取 `.kicad_sch`。作者公开了一份机器人控制板的审查报告。打开报告的电源部分，可以看到程序怎样沿着网络找到稳压器，再用反馈电阻估算输出电压。[控制板报告](https://github.com/aklofas/kicad-happy/blob/main/example-report-1.md)
- [Backplane](https://github.com/BackplaneWorks/Backplane)（主程序 MIT）把 AI 对话、原理图、板图和三维视图放在同一工作台。打开已有工程，在原理图中点选连接器的某个引脚，再到板图中看同一网络的焊盘。评审一次改版时，可以按图纸或铜层对照修改前后的设计。[工程审查说明](https://github.com/BackplaneWorks/Backplane/blob/main/docs/design-review.md)

## 修改原理图，核对工程记录

- [Copper](https://github.com/claynicholson/copper-kicad-mcp)（MIT）让支持模型上下文协议（MCP）的 AI 客户端调用 KiCad 10。设计者可以按位号和引脚名指定一条连接，交给 KiCad 运行电气规则检查，再导出图纸。语言模型由客户端提供。作者提供安装包、工具说明，以及宏键盘等示例的渲染图。[发布包](https://github.com/claynicholson/copper-kicad-mcp/releases/latest)
- [Copperhead](https://github.com/copperheadhq/copperhead)（Apache-2.0）把设计需求、KiCad 文件和检查结果放进同一份 Git 工程。作者提供一个 USB-C 电源转接板的需求样例。可以先读需求，查看生成流程怎样调用 KiCad 检查，再核对元件值和物料清单。作者已用离线测试覆盖检查流程，调用模型完成整套设计的验收仍待验证。[USB-C 需求文件](https://github.com/copperheadhq/copperhead/blob/main/examples/simple/usb-c-breakout.md)

## 把板交给布线器

- [DeepPCB KiCad 插件](https://github.com/instadeepai/deeppcb-kicad-plugin)（插件 Apache-2.0）从 KiCad 板编辑器提交布线任务，完成后把结果下载回工程。布线在 DeepPCB 云端运行，使用者需要账户、API 密钥和服务点数。想在本地比较两种走线结果，可以把下载的板与原板并排打开，核对未接通项和规则违规。[插件发布包](https://github.com/instadeepai/deeppcb-kicad-plugin/releases)

## 用本站的教学板试一次

下载[原板](../../assets/examples/hole-spacing/reference.kicad_pcb)和[移孔后的板](../../assets/examples/hole-spacing/shifted.kicad_pcb)，放在 KiCad Happy 仓库的根目录。从该目录分别运行：

```sh
python3 skills/kicad/scripts/analyze_pcb.py reference.kicad_pcb --full -o reference-analysis.json
python3 skills/kicad/scripts/analyze_pcb.py shifted.kicad_pcb --full -o shifted-analysis.json
```

我们用同一版脚本读取了这两份文件。两次输出的板框都是 40 × 20 mm，`SENSE` 网络的铜线都长 10 mm。在 `footprints` 里找到 H2，横坐标由 85 mm 变为 84 mm。结合[教学板的孔距要求](design-checks.md)，就能判断这次改动影响了哪项验收。[本次使用的脚本版本](https://github.com/aklofas/kicad-happy/blob/6b9767e19979cdef91631573753b1547efdbeab9/skills/kicad/scripts/analyze_pcb.py)

这些项目来自 whut09 维护的[工程智能体清单](https://github.com/whut09/Awesome-AI-Engineering-Agents/blob/main/README_CN.md)。上面的示例、使用条件和许可均可在各项目仓库核对。
