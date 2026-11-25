Roadbook AI4PCB is a guide to **AI for printed circuit board (PCB) design**. Browse research on drawing schematics, placing components, routing traces, and checking layouts. Where authors share them, entries link to board files, training data, and evaluation code.

## Selected AI × PCB papers

- [SchGen](https://arxiv.org/abs/2605.30345) (2026) generates editable KiCad schematics from written requirements. It places component symbols and connects their pins by name. The paper measures the accuracy of the resulting connections.
- [PCBWorld](https://arxiv.org/abs/2607.05915) (2026) gives routing methods access to the same KiCad engine. Compare the connections and rule violations on the same boards under the same constraints.
- [CADET / RouteDemos](https://arxiv.org/abs/2611.16913) (2026) reports routing demonstrations for 100,000 synthetic training boards. The authors provide code to generate samples and replay the routing actions.

[Browse all papers →](papers.md)

## Where to start

| Background or goal | Start here | Read next |
| --- | --- | --- |
| Learn how engineers design a board | [PCB design workflow](workflow.md), from part selection to final checks | Open a [reference board](boards.md) and find the files from each stage |
| Find AI methods for a hardware project | [Selected papers](papers.md) on schematics, placement, routing, and review | Compare inputs and acceptance criteria in [benchmarks](benchmarks.md) |
| Find training examples | [Datasets](data.md) with schematic files, layouts, or routing actions | Inspect a sample with the [design tools](tools.md) |
| Compare frontier model results | Start with the [two KiCad tasks](benchmarks.md#ale) and their submission rules | Compare [placement](benchmarks.md#omnilayout) with [connectivity recovery](benchmarks.md#benchcad-t6) |
| Use an agent on a KiCad project | [KiCad agents and plugins](agents.md) for review, editing, and routing | Compare the checks in the [hole-spacing example](design-checks.md) |
| Run a PCB benchmark task | Open the [Harbor example](harbor.md) to inspect the ALE Mini Encabulator schematic | Download the task and check a board with the ALE scorer |

## Reading guide

### Follow one connector

Read how to [check the schematic](workflow.md#check-the-schematic). Open the interface schematic for the [Antmicro baseboard](boards.md#a-carrier-board-with-multiple-interfaces). Find the Ethernet jack marked `J3`. Search for the same reference in the board editor. Check which nets connect to pads 2 and 3.

### Reproduce a routing experiment

Read the task definition in [PCBWorld](https://arxiv.org/abs/2607.05915) to see which routing operations a model can use. Follow the small RouteDemos example in the [CADET repository](https://github.com/LGAI-Research/CADET) to generate a small set of boards and replay the routing actions. Read the [routing results](routing-scores.md) for the difference between connected nets, rule violations, and fully connected boards with zero violations.

## Engineering blog

[Trace the RP2040 power rails](rp2040-power.md), [check a placement origin](assembly-origin.md), or [separate board families for training](board-family-split.md). [Read all engineering notes →](blog.md)

PCB specialists can help define benchmarks and review model submissions. Contact SIGVoid about joint research or custom training data. [Partnerships and WeChat →](about.md#collaborate)
