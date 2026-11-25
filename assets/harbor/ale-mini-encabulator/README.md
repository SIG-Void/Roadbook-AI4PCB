# Mini Encabulator PCB layout

This package adapts the [Agents’ Last Exam v1.1 task](https://github.com/rdi-berkeley/agents-last-exam/tree/2e91edd3cd26baa35a38127c90c8e5241dfbe62f/tasks/engineering/pcb_layout_kicad_1) for Harbor. The official task uses a Windows desktop. This example runs KiCad 10.0.0 command-line tools in Linux containers.

## Run the verifier

Install Harbor 0.25.0. Start Docker with Linux AMD64 containers or AMD64 emulation. Extract the ZIP. Run each command from the directory that contains `ale-mini-encabulator/`.

```sh
harbor run -p ./ale-mini-encabulator -a oracle
harbor run -p ./ale-mini-encabulator -a nop
```

The first command replays the published DeepSeek V4.1 Flash submission from SIGVoid’s ALE run. The second submits an empty output directory. Each trial saves `reward.txt` and `checks.json` under `verifier/`. A completed KiCad check also produces `drc.json`.

## Inspect a design

Open `environment/input/mini_encabulator.kicad_sch` in desktop KiCad to inspect the circuit and footprint assignments. Open `solution/sample/mini_encabulator.kicad_pcb` to inspect the submitted layout. To score your own board, replace the sample in an extracted copy and run the first command again.

The agent and verifier use separate containers. Only the submitted board crosses the boundary. The verifier copies it to a clean directory, runs KiCad DRC, and passes the resulting JSON and board text to the original ALE scorer.

| Score | Condition |
| --- | --- |
| 1 | DRC reports zero violations and zero unconnected items. All structural checks pass. |
| 0.5 | DRC passes. At least one structural check fails. |
| 0 | The board is missing, DRC is unavailable, or DRC reports violations or unconnected items. |

The command-line replay checks a submitted artifact. ALE leaderboard runs also include the original agent and Windows environment.

## Files and attribution

| Path | Origin |
| --- | --- |
| `upstream/task_card.json` | ALE task card, including the original Windows instructions |
| `environment/input/mini_encabulator.kicad_sch` | Published ALE v1.1 input schematic |
| `tests/score_outputs.py` | Original ALE scorer, unchanged |
| `solution/sample/mini_encabulator.kicad_pcb` | Model submission from SIGVoid’s published run |
| `tests/verify.py` and the Dockerfiles | Roadbook’s Harbor integration |

UC Berkeley RDI and RDI Foundation released the benchmark data under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Roadbook adapted paths and runtime instructions. The upstream license texts are in `licenses/`.

[Original task and scorer](https://github.com/rdi-berkeley/agents-last-exam/tree/2e91edd3cd26baa35a38127c90c8e5241dfbe62f/tasks/engineering/pcb_layout_kicad_1) · [Original input schematic](https://huggingface.co/datasets/agents-last-exam/agents-last-exam-data/blob/e9a2674a62f7d8069f136e642c10e8d8e9979dbf/tasks/engineering/pcb_layout_kicad_1/base/input/mini_encabulator.kicad_sch) · [Published model submission and action trace](https://sig-void.github.io/Roadbook-AI4PCB/assets/runs/ale-mini-deepseek.zip)
