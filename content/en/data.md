# Open and public datasets

For schematic recognition, look for labeled pins and connections. For routing, look for editable boards or actions you can replay. For board files, see [how to check revisions and connections](data-procurement.md).

## Schematics and netlists

- [SchGen_dataset](https://huggingface.co/datasets/microsoft/SchGen_dataset) (2026) — Pairs design requests with code that generates KiCad schematics. The training set contains 8,420 augmented examples. A single design can appear in several examples. The dataset card lists MIT. The release includes JSONL and KiCad schematics. [Generation and conversion code](https://github.com/microsoft/SchGen)
- [OmniSch](https://www.omnisch.com/) (2026) — The paper reports 1,854 schematics with labels for component positions, text, and connections. The public sample archive contains five designs, including Adafruit FunHouse, with images and JSON annotations. [Paper](https://arxiv.org/abs/2604.00270) · [Sample archive](https://drive.google.com/file/d/1GRPNowJNRixrFIWvS7YSkhp_k7erUV6y/view)
- [BenchPCNP](https://github.com/MrBade/BenchPCNP) (2026) — Netlists from 50 circuits carry labels for 54 types of functional modules. The release includes netlists, graph data, and construction code for studying which components work together. [Data paper](https://www.nature.com/articles/s41597-026-06818-y)

## Board files and routing traces

- [PCBench](https://github.com/PCBench/PCBench) (DAC 2024 work-in-progress poster) — The README describes 164 boards. The repository inventory lists 1,194 designs from 846 repositories. The buck regulator example includes original and cleaned KiCad files, routing rules, and reference traces in JSON. [Inventory](https://raw.githubusercontent.com/PCBench/PCBench/main/PCBs/master_metadata.json) · [Example board](https://github.com/PCBench/PCBench/tree/main/PCBs/C-BISCUIT_buck-reg-5v)
- [pcb-corpus](https://github.com/punkfab/pcb-corpus) — Collects 235 KiCad boards from 170 open hardware repositories. Each entry pairs the original design with an unrouted copy and its project rules for comparison. Each board includes its upstream license. Its `SOURCE.json` identifies the source repository, commit, and changes. [Provenance and licenses](https://github.com/punkfab/pcb-corpus#licences)
- [CADET / RouteDemos](https://github.com/LGAI-Research/CADET) (2026) — Generates synthetic boards and routing actions that can run in the engine. The paper reports 100,000 synthetic training boards. The repository includes a generator and an independent replay check. The authors list separate licenses for code and trained weights. [Paper](https://arxiv.org/abs/2611.16913)
- [tscircuit autorouting-dataset-01](https://github.com/tscircuit/autorouting-dataset-01) — Contains 200 routing problems with components and connections described in TypeScript. The repository links to a preview for inspecting placement and the pins each route must connect.

## Manufacturing and visual inspection

- [DeepPCB](https://github.com/tangsanli5201/DeepPCB) — Each of 1,500 aligned image pairs contains a defect-free template and a bare-board scan. The dataset labels six defect types, including opens, shorts, and pinholes. The authors added artificial defects to the test images and specify research use only.
