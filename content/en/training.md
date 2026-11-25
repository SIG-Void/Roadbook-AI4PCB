Start with a CPU exercise using real board statistics from CADET. Fit a model on board area and predict net counts for 29 held-out boards. Then follow PCBWorld’s routing example from board selection through a trained policy and a separate design rule check. [CADET data](https://github.com/LGAI-Research/CADET/blob/7bea0d51d3ee96bacf2915fd0d3e119fa4404cc5/cadet/configs/fit_params/d3b_fit_half.json) · [PCBWorld training script](https://github.com/LGAI-Research/PCBWorld/blob/57738250415db0d409f44aca36dd43af25432971/tools/quickstart/train_rl.sh)

## CPU exercise: can board area predict the number of nets?

CADET generates synthetic boards for policy training. Its authors start with 142 D3-B reference boards. After filtering on area and net count, their parameter file contains 141 board rows. Each row reports the bounding-box area in `area_cm2`. The `n_nets` field counts nets with at least two pads. Can area predict that count more accurately than a constant guess? [Author’s extraction code](https://github.com/LGAI-Research/CADET/blob/7bea0d51d3ee96bacf2915fd0d3e119fa4404cc5/cadet/stats/fit_board_params.py) · [Reference list](https://github.com/LGAI-Research/CADET/blob/7bea0d51d3ee96bacf2915fd0d3e119fa4404cc5/cadet/configs/splits/boards_d3b_fit.txt)

Download the JSON file. Use Python 3.10 or later and the standard library. We used Python 3.13.7. Save the code as `fit.py` beside the JSON file. Run `python3 fit.py`.

```sh
curl -fL -o d3b_fit_half.json \
  https://raw.githubusercontent.com/LGAI-Research/CADET/7bea0d51d3ee96bacf2915fd0d3e119fa4404cc5/cadet/configs/fit_params/d3b_fit_half.json
```

```python
import hashlib, json, math, statistics as st
from pathlib import Path

rows = json.loads(Path("d3b_fit_half.json").read_text())["boards"]
rows.sort(key=lambda r: hashlib.sha256(r["id"].encode()).digest())
check, train = rows[::5], [r for i, r in enumerate(rows) if i % 5]
def features(row):
    return math.log(row["area_cm2"]), math.log(row["n_nets"])
x, y = zip(*(features(r) for r in train))
slope, offset = st.linear_regression(x, y)
baseline = st.median(r["n_nets"] for r in train)
def prediction(row):
    return math.exp(offset + slope * math.log(row["area_cm2"]))
def mae(predict):
    return st.mean(abs(predict(r) - r["n_nets"]) for r in check)
print(len(train), len(check), round(slope, 3), round(offset, 3))
print(round(mae(prediction), 2), round(mae(lambda r: baseline), 2))
```

The script sorts board IDs by their SHA-256 hash and reserves every fifth row. It fits log net count against log area on the other 112 boards. The comparison always predicts 18 nets, the training median. Mean absolute error measures the average difference in nets per board across the same 29 held-out boards.

| Our reproduced output | Meaning |
| --- | --- |
| `112 29 0.129 2.473` | Training boards, held-out boards, slope, and intercept |
| `5.72 6.0` | Area model: 5.72 nets of error per board. Constant prediction: 6.00. |

For `0340_kitspace_Brk40p`, the recorded area is 9.805 cm². The model estimates 15.9 nets. The board has 41. Similar board sizes can accommodate very different connection requirements. This Roadbook regression exercise uses published reference rows. CADET has a separate 141-board D3-B test list. [Board records](https://github.com/LGAI-Research/CADET/blob/7bea0d51d3ee96bacf2915fd0d3e119fa4404cc5/cadet/configs/fit_params/d3b_fit_half.json) · [Official test list](https://github.com/LGAI-Research/CADET/blob/7bea0d51d3ee96bacf2915fd0d3e119fa4404cc5/cadet/configs/splits/boards_d3b_test.txt)

## Routing policy: follow the author’s PPO example

The CPU exercise produces two regression coefficients. For routed copper, use an environment that executes routing actions. PCBWorld’s example trains a policy with proximal policy optimization (PPO). The inputs are two-layer boards with pads and target nets. The KiCad router executes the policy’s actions. We checked the pinned script and output paths. The configuration below comes from the authors. [Setup](https://github.com/LGAI-Research/PCBWorld/blob/57738250415db0d409f44aca36dd43af25432971/README.md#quick-start) · [Environment and actions](https://github.com/LGAI-Research/PCBWorld/blob/57738250415db0d409f44aca36dd43af25432971/docs/ENVIRONMENT.md)

Install the documented system dependencies first. Linux x86_64 is the primary platform. The setup script uses conda’s libmamba solver or mamba. Select training hardware and drivers using the versioned setup notes. Use a new data directory because the script reuses an existing `train/` directory.

```sh
git clone https://github.com/LGAI-Research/PCBWorld.git
cd PCBWorld
git checkout 57738250415db0d409f44aca36dd43af25432971
git submodule update --init --recursive
bash tools/setup/setup_all.sh
conda activate pcbworld
export PYTHONPATH=build_rl/pcbnew/python/rl:.
export PCBWORLD_DATA_ROOT="$PWD/var/datasets"
bash tools/quickstart/train_rl.sh \
  --data-dir var/datasets/synthetic/roadbook_2L \
  --boards 200 --iterations 5 --seed 42
```

- **Check the inputs.** In a fresh directory, expect `split.json` to list 200 training boards, 20 validation boards, and 20 test boards. The policy trains for five iterations with seed 42.
- **Check the weights.** The script looks for `var/outputs/quickstart/rl/ppo_per_step/checkpoints/policy_last.pt`. It evaluates the last checkpoint from this short run.
- **Check the results.** Evaluation uses seed 5600 and five rollouts per test board, with selection after DRC. Inspect `per_boards_summary.csv` and its two companion CSV files under `var/results/quickstart/rl/`. Match the test boards and attempt counts when comparing policies. [Script stages](https://github.com/LGAI-Research/PCBWorld/blob/57738250415db0d409f44aca36dd43af25432971/tools/quickstart/train_rl.sh) · [Reading a routing success rate](routing-scores.md)

## Trace the AP2112K power nets in a SchGen schematic

The SchGen authors published a 3.3 V regulator example with eight calls to `connect_pins`. Does U1’s enable pin connect to the input or the output? Download the pinned source file. Save the Python snippet as `check_pins.py`. Run `python3 check_pins.py` in the same directory. The script reads the connection arguments using the Python standard library. [Published connection code](https://github.com/microsoft/SchGen/blob/dbfdec5930da0c675961601acfbb0fe702309d58/dataset_construction/sch_sketch/test_L1.py)

```sh
curl -fL -o test_L1.py \
  https://raw.githubusercontent.com/microsoft/SchGen/dbfdec5930da0c675961601acfbb0fe702309d58/dataset_construction/sch_sketch/test_L1.py
```

```python
import ast
from pathlib import Path

source = ast.parse(Path("test_L1.py").read_text(encoding="utf-8"))
for statement in source.body:
    call = getattr(statement, "value", None)
    if not isinstance(call, ast.Call) or not isinstance(call.func, ast.Name):
        continue
    if call.func.id == "connect_pins":
        a, p, b, q = map(ast.literal_eval, call.args)
        print(f"{a}.{p}  {b}.{q}")
```

The script printed eight lines. The line `#PWR1.+5V  U1.EN` connects the enable pin directly to the +5 V input. Follow `C1.1  U1.VIN` back to C1’s supply connection to verify that VIN shares this net. We also checked the symbol positions, pin locations, and wire endpoints in the published schematic. Here, `U1.3` means pin 3 on U1. [Schematic](https://github.com/microsoft/SchGen/blob/dbfdec5930da0c675961601acfbb0fe702309d58/dataset_construction/sch_sketch/test.kicad_sch) · [Device pin table](https://www.diodes.com/datasheet/download/AP2112.pdf)

| Net | Pins connected in the schematic |
| --- | --- |
| +5 V input | U1.1 (VIN), U1.3 (EN), C1.1 |
| +3.3 V output | U1.5 (VOUT), C2.1 |
| GND | U1.2 (GND), C1.2, C2.2 |

This exercise starts with the published example and ends with the pin check. We did not run inference with the 20B base model. A direct export of this schematic with KiCad 10.0.7 produced an XML netlist with zero components and zero nets. The table records the connections we verified in the published files.

## What should you inspect for other tasks?

| Task | First output to inspect |
| --- | --- |
| Schematic generation | Generate SchGen’s AP2112K schematic. Inspect the supply, ground, and output pins. The authors specify KiCad 8.0.9. [SchGen example](https://github.com/microsoft/SchGen#example-generate-a-33v-voltage-regulator-based-on-ap2112k) |
| Component placement | Inspect footprint positions, overlap, and wirelength in RL_PCB. The paper checks placement quality again using routed wirelength. [RL_PCB](https://github.com/LukeVassallo/RL_PCB) · [DATE paper](https://past.date-conference.com/proceedings-archive/2024/DATA/1040_pdf_upload.pdf) |
| Learning from routing demonstrations | CADET’s small configuration uses 200 training boards, 16 validation boards, and a 300-second limit per board. Replay a demonstration in a fresh engine before behavior cloning. [Generation and replay](https://github.com/LGAI-Research/CADET/blob/7bea0d51d3ee96bacf2915fd0d3e119fa4404cc5/README.md#2-routedemos-generation-and-replay-verification) |
