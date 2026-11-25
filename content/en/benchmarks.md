# Benchmarks

Model scores and submissions for two KiCad tasks in ALE, component placement in OmniLayout, and connectivity recovery in BenchCAD T6.

| Benchmark | What the model does | Selected result |
| --- | --- | --- |
| [Agents’ Last Exam (ALE)](#ale) | Lay out a board or repair a KiCad project. | Board layout, out of 1. DeepSeek V4.1 Flash scored **1**. Qwen4-Max-Preview scored **0**. [Team submissions ↓](#team-runs) |
| [OmniLayout](#omnilayout) | Place components and test whether a router can connect them. | GPT-5.5 passed **15.23%** of cases in one attempt. With a schematic it passed **42.83%**. |
| [BenchCAD 2.0 T6](#benchcad-t6) | Recover the connections between pins from board images. | Mean across 12 boards, out of 1. GPT-6 Astra scored **0.4222** after correction. Claude Opus 5.5 scored **0.3983**. [SIGVoid practice traces ↓](#public-t6) |

<h2 id="ale">Agents’ Last Exam (ALE) · Two KiCad tasks</h2>

<h3 id="team-runs">Four runs by SIGVoid</h3>

| Model | Board layout · out of 1 | Navigation switch repair · out of 1 |
| --- | ---: | ---: |
| DeepSeek V4.1 Flash | <strong>1</strong> · <a download href="../../assets/runs/ale-mini-deepseek.zip" aria-label="Download DeepSeek board layout trace and submission">Trace and files ↓</a> | <strong>0</strong> · <a download href="../../assets/runs/ale-navswitch-deepseek.zip" aria-label="Download DeepSeek switch repair trace and submission">Trace and files ↓</a> |
| Qwen4-Max-Preview | <strong>0</strong> · <a download href="../../assets/runs/ale-mini-qwen4.zip" aria-label="Download Qwen4 board layout trace and submission">Trace and files ↓</a> | <strong>0</strong> · <a download href="../../assets/runs/ale-navswitch-qwen4.zip" aria-label="Download Qwen4 switch repair trace and submission">Trace and files ↓</a> |

On November 14, 2026, SIGVoid ran each model once per task in the ALE v1.1 Windows 10 environment. DeepSeek used max effort and Qwen used xhigh. Each ZIP contains the KiCad submission, observed tool calls in `operations.csv`, and the recorded score in `eval_result.json`.

<details class="run-trace">
<summary>Inspect the tool results from both layout runs</summary>
<p><strong>DeepSeek</strong> · At step 106, KiCad reported seven violations and 27 unconnected items. Both counts reached zero at step 274, with 34 differences between the schematic and the board. All three counts reached zero at step 314.</p>
<p><strong>Qwen</strong> · The same counts were 14, 1, and 34 at step 170. All three reached zero at steps 235 and 265. The archived evaluator score was zero. Its DRC report is unavailable, so the cause of that score remains open.</p>
<p>Both layout runs called Python routing scripts. Use the <code>result_step</code> column in <code>operations.csv</code> to find the tool results.</p>
</details>

**Why did both switch repairs score zero?** Both models restored U4. DeepSeek submitted `.rpt` reports. The grader found no `erc.json`, `drc.json`, `project.net`, or `board.d356`. Qwen supplied both JSON reports, used different names for four other files, and omitted the separate `drill/` directory. Both submissions failed the required-file check.

<h3 id="ale-layout">Board layout · Fit the SN25 enclosure</h3>

**The submission is a routed KiCad board.** The model must open the Mini Encabulator schematic in KiCad, import its footprints, place the components, and route the connections. Four M3 mounting holes must form a rectangle measuring 1.575 × 1.26 inches between centers. Ground vias must connect the copper pours on both sides. [Task and input file](https://github.com/rdi-berkeley/agents-last-exam/blob/2e91edd3cd26baa35a38127c90c8e5241dfbe62f/tasks/engineering/pcb_layout_kicad_1/task_card.json)

**The grader runs a fresh design rule check (DRC).** A missing or invalid report, a violation, or an unconnected item scores **0**. A clean DRC scores **0.5** if a structural check fails. These checks cover the board outline, hole spacing, ground pours, and other features. Passing all checks scores **1**. [Grading code](https://github.com/rdi-berkeley/agents-last-exam/blob/2e91edd3cd26baa35a38127c90c8e5241dfbe62f/tasks/engineering/pcb_layout_kicad_1/scripts/score_outputs.py) · [Run this task in Harbor](harbor.md)

<h3 id="ale-navswitch">Project repair · Restore U4 on the navigation switch board</h3>

**U4 has a broken footprint assignment.** The model must restore the project-local footprint for U4 (PCA9554) in the KiCad desktop interface, then update the PCB from the schematic. The task prohibits direct edits to KiCad source text. Deliverables include the repaired project, local libraries, netlist, reports, Gerbers, and drill files. [Task and deliverables](https://github.com/rdi-berkeley/agents-last-exam/blob/2e91edd3cd26baa35a38127c90c8e5241dfbe62f/tasks/engineering/kicad_navswitch_library_integration_release_002/task_card.json)

**The grader checks U4 in both designs and verifies the required files.** Failure on any mandatory check scores **0**. After these checks pass, matching U4’s reference pin connections earns **0.20 points**. Matching the Gerber file list earns **0.10 points**. [Grading code](https://github.com/rdi-berkeley/agents-last-exam/blob/2e91edd3cd26baa35a38127c90c8e5241dfbe62f/tasks/engineering/kicad_navswitch_library_integration_release_002/scripts/score_outputs.py)

<h3 id="ale-results">Official results · Windows group</h3>

The ALE v1.1 leaderboard includes both KiCad tasks among 36 Windows tasks. It publishes platform and suite totals. Individual GPT-6.2 Astra scores for the two KiCad tasks are unavailable in that table. [Official leaderboard, November 18, 2026](https://agents-last-exam.org/api/demo/leaderboard/v1.1) · [Official replays](https://agents-last-exam.org/traces)

| Model and configuration | Windows tasks passed | All tasks passed |
| --- | ---: | ---: |
| Qwen 4 · Codex, xhigh | 16 / 36 | 57 / 122 |
| Kimi 3.1 Pro · Kimi Code, max | 15 / 36 | 53 / 122 |
| GPT-6.2 Astra · Codex, xhigh | 15 / 36 | 58 / 122 |

<h2 id="omnilayout"><span id="omnilayout-2">OmniLayout · Component placement</span></h2>

The model receives a board outline, a netlist, and component dimensions. It submits each component’s position, orientation, and board side. The evaluator checks for overlaps and boundary violations, then runs Freerouting. [Evaluation protocol](https://arxiv.org/html/2607.03261v3#S4.SS1) · [Sample layouts](https://www.omnieda.com/)

| Model | Basic inputs | With a schematic image |
| --- | ---: | ---: |
| GPT-5.5 | 15.23% | 42.83% |
| Qwen3.6-35B-A3B | 5.31% | 24.45% |

The metric is the end-to-end pass rate for one submission. The authors also report runs where models revise placements after inspecting the layout, overlap checks, and routing feedback. As of November 25, 2026, the authors list no placement scores for GPT-6.2, Claude Fable 5.2, or GLM-5.4. [One-pass results, Table 2](https://arxiv.org/html/2607.03261v3#S5.T2) · [Tool-assisted results, Table 3](https://arxiv.org/html/2607.03261v3#S5.T3) · [Authors’ leaderboard](https://www.omnieda.com/#leaderboard)

<h2 id="benchcad-t6"><span id="benchcad-2-0-t6">BenchCAD 2.0 T6 · Connectivity recovery</span></h2>

The public example has six board images. Each side has one straight view and two oblique views. Multilayer boards also have an image of each inner copper layer so the model can follow a trace through a via. The model can crop and enlarge images with Python offline. Its answer lists component positions in the top view, their terminals, and their nets. The grader matches components by position and checks the connections. [Six images from the public example](https://github.com/BenchCAD-org/benchcad-2-main/tree/v2.0-core1/examples/task6/cases/case1/input/views) · [Task and answer format](https://github.com/BenchCAD-org/benchcad-2-main/blob/v2.0-core1/envs/t6_pcb2schematic/TASK_position.md)

**The 2.0 T6 test** contains 12 boards. Each model ran each board once at max effort. GPT-6 Astra originally averaged 0.4639. One case received credit without an explicit submission. Under the authors’ corrected rule, that case scores zero and Astra averages **0.4222**. Claude Opus 5.5 averaged **0.3983**. [Task scores](https://github.com/BenchCAD-org/benchcad-2-main/blob/main/results/core_reference.json) · [Submission rule correction](https://github.com/BenchCAD-org/benchcad-2-main#readme)

**The full 2.1 suite** has 100 cases across six tasks. With customized harnesses at max effort, Claude Fable 5.2 with Claude Code scored **0.835**. GPT-6.2 Astra with Codex scored **0.825**. The leaderboard omits separate T6 scores for these two configurations. [Official 2.1 leaderboard](https://benchcad.com/leaderboard)

<h3 id="public-t6">SIGVoid runs on nine Public practice boards</h3>

Each batch used the same nine cases, with one attempt per case. We used the 2.1 T6 scorer with no per-case limit on turns or output tokens. Missing submissions scored zero. The official Core result covers 12 different boards.

| Model and effort | Batch 1 mean | Batch 2 mean |
| --- | ---: | ---: |
| DeepSeek V4.1 Flash · max | 0.1295 | 0.1200 |
| Qwen4-Max-Preview · xhigh | 0.0839 | 0.1389 |
| Qwen3.8-Max · xhigh | 0.0768 | Not tested |

**Action traces by case.** The 45 attempts contain 1,432 recorded events. The models submitted 41 wiring graphs. Filter the CSV by model, batch, and case to see the actions, exit codes, and final score. Image operation tags identify calls in the code for that turn.

- Qwen4-Max-Preview, batch 2, `case009`. The code in turn 3 included an image crop. The model submitted a wiring graph in turn 6 and scored 0.6667.
- Qwen3.8-Max, batch 1, `case004`. The program failed with exit code 1. The model then requested submission. The submission program also failed. The run produced no answer and scored zero.

<a href="../../assets/runs/benchcad-public-t6-traces.csv" download>Download per-case action traces (CSV) ↓</a> · <a href="../../assets/runs/benchcad-public-t6.csv" download>Download scores for all five batches (CSV) ↓</a> · [Public dataset terms](https://huggingface.co/datasets/BenchCAD/benchcad-2.0-public#evaluation-terms)
