先跑一个能在 CPU 上完成的实验：用 CADET 作者公布的板级数据，拟合板面积与网络数的关系，再让模型预测留出的 29 块板。然后进入 PCBWorld 的布线训练，对照板清单、策略权重和独立的规则检查结果。[CADET 数据文件](https://github.com/LGAI-Research/CADET/blob/7bea0d51d3ee96bacf2915fd0d3e119fa4404cc5/cadet/configs/fit_params/d3b_fit_half.json) · [PCBWorld 训练脚本](https://github.com/LGAI-Research/PCBWorld/blob/57738250415db0d409f44aca36dd43af25432971/tools/quickstart/train_rl.sh)

## CPU 实验：板面积能预测多少条网络？

CADET 需要生成与真实板相似的训练样本。作者从 D3-B 的 142 块参考板开始，按面积和网络数筛选后，在公布的参数文件中保留 141 行。每行的 `area_cm2` 是板框包围盒面积，`n_nets` 统计至少有两个焊盘的网络。我们用这两个字段做一个小实验：已知板面积时，网络数的预测能比一个固定数值准多少？[作者的筛选与统计代码](https://github.com/LGAI-Research/CADET/blob/7bea0d51d3ee96bacf2915fd0d3e119fa4404cc5/cadet/stats/fit_board_params.py) · [参考板清单](https://github.com/LGAI-Research/CADET/blob/7bea0d51d3ee96bacf2915fd0d3e119fa4404cc5/cadet/configs/splits/boards_d3b_fit.txt)

下载这一份 JSON 即可，使用 Python 3.10 或更新版本，只需标准库。我们在 Python 3.13.7 上运行。将以下代码保存为同一目录里的 `fit.py`，再运行 `python3 fit.py`。

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

脚本先按板 ID 的 SHA-256 排序，每五行取一块作内部留出。模型在其他 112 块板上拟合 `log(网络数) = 截距 + 斜率 × log(面积)`。对照方法始终猜训练集网络数的中位数，即 18 条。两种方法都按相同的 29 块板计算平均绝对误差，单位是每块板差多少条网络。

| 我们复跑得到的输出 | 读法 |
| --- | --- |
| `112 29 0.129 2.473` | 拟合板数、内部留出板数、斜率、截距 |
| `5.72 6.0` | 用面积预测，平均差 5.72 条；固定猜 18 条，平均差 6.00 条 |

例如，`0340_kitspace_Brk40p` 的面积为 9.805 cm²，模型估计 15.9 条，原记录是 41 条。面积相近的板也可能有很不相同的连接需求。这是本站对公开参考行做的回归练习。CADET 另有 141 块 D3-B 正式测试板，以上代码只读取参考数据。[原始逐板记录](https://github.com/LGAI-Research/CADET/blob/7bea0d51d3ee96bacf2915fd0d3e119fa4404cc5/cadet/configs/fit_params/d3b_fit_half.json) · [作者的测试清单](https://github.com/LGAI-Research/CADET/blob/7bea0d51d3ee96bacf2915fd0d3e119fa4404cc5/cadet/configs/splits/boards_d3b_test.txt)

## 布线策略：按作者流程跑通一次 PPO

上面的 CPU 实验输出两个回归系数。要生成实际走线，需要能执行布线动作的环境。PCBWorld 的示例用 PPO（近端策略优化）训练策略，输入是带有焊盘和目标网络的双层板，动作交给 KiCad 布线引擎执行。下面给出作者脚本的固定版本。本站核对了脚本和输出路径，此处的运行配置来自作者。[环境和安装要求](https://github.com/LGAI-Research/PCBWorld/blob/57738250415db0d409f44aca36dd43af25432971/README.md#quick-start) · [状态与动作](https://github.com/LGAI-Research/PCBWorld/blob/57738250415db0d409f44aca36dd43af25432971/docs/ENVIRONMENT.md)

为这次小实验准备独立的数据目录，并先完成仓库列出的系统依赖。作者主要支持 Linux x86_64，安装脚本依赖 conda 的 libmamba 求解器或 mamba；训练设备与驱动要求按该版本的安装说明选择。脚本发现已有 `train/` 目录时会沿用其中的板。

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

- **核对输入。** 在新目录中，预期 `split.json` 包含 200 块训练板、20 块验证板和 20 块测试板。训练使用种子 42，迭代 5 次。
- **核对权重。** 脚本检查 `var/outputs/quickstart/rl/ppo_per_step/checkpoints/policy_last.pt`。短跑用最后一次保存的权重进入测试。
- **核对输出。** 评估阶段另用种子 5600，每块测试板运行 5 次，再按事后 DRC 选择结果。查看 `var/results/quickstart/rl/` 下的 `per_boards_summary.csv` 和另外两份 CSV。比较两个策略前，核对测试板和每板尝试次数。[脚本的生成、训练和测试步骤](https://github.com/LGAI-Research/PCBWorld/blob/57738250415db0d409f44aca36dd43af25432971/tools/quickstart/train_rl.sh) · [怎样读整板通过率](routing-scores.md)

## 沿着 SchGen 原理图里的 AP2112K 引脚找三条电源网络

SchGen 作者公布的 `test_L1.py` 用八条 `connect_pins` 描述了一组 3.3 V 稳压电路。可以先问一个具体问题：U1 的使能脚 EN 接在输入侧还是输出侧？下载固定版本的连接代码，把下一段保存为 `check_pins.py`，在同一目录运行 `python3 check_pins.py`。脚本使用 Python 标准库，只读取源代码中的连接参数。[作者的连接代码](https://github.com/microsoft/SchGen/blob/dbfdec5930da0c675961601acfbb0fe702309d58/dataset_construction/sch_sketch/test_L1.py)

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

实际输出有八行。其中 `#PWR1.+5V  U1.EN` 给出了答案：使能脚直接接 +5 V 输入。沿 `C1.1  U1.VIN` 再回看 C1 的另一条连接，可以确认 VIN 和 EN 接在同一网络。我们还按作者原理图里的符号位置、引脚位置和导线端点核对了三条网络。表中的点号连接位号和引脚号，例如 `U1.3` 表示 U1 的 3 脚。[原理图](https://github.com/microsoft/SchGen/blob/dbfdec5930da0c675961601acfbb0fe702309d58/dataset_construction/sch_sketch/test.kicad_sch) · [器件引脚表](https://www.diodes.com/datasheet/download/AP2112.pdf)

| 网络 | 原理图中接在一起的引脚 |
| --- | --- |
| +5 V 输入 | U1.1（VIN）、U1.3（EN）、C1.1 |
| +3.3 V 输出 | U1.5（VOUT）、C2.1 |
| GND | U1.2（GND）、C1.2、C2.2 |

本次复现从作者已发布的样例开始，完成到引脚连接核对，未运行 20B 基础模型推理。用本机 KiCad 10.0.7 直接导出这份原图时，XML 网表中的元件数和网络数都是 0。上表记录的是从公开文件核对出的连接。

## 换任务时，先找哪份输入？

| 要复现的对象 | 第一项能核对的输出 |
| --- | --- |
| 原理图生成 | 用 SchGen 的 AP2112K 示例生成 KiCad 原理图，打开电源、地和输出引脚。作者指定 KiCad 8.0.9。[SchGen 示例](https://github.com/microsoft/SchGen#example-generate-a-33v-voltage-regulator-based-on-ap2112k) |
| 元件布局 | 在 RL_PCB 的基准里核对落位的封装、重叠量和线长。论文用布线后的实际线长复查布局结果。[RL_PCB](https://github.com/LukeVassallo/RL_PCB) · [DATE 论文](https://past.date-conference.com/proceedings-archive/2024/DATA/1040_pdf_upload.pdf) |
| 从布线示范学习 | CADET 的小配置指定 200 块训练板、16 块验证板和单板 300 秒上限。在新的引擎实例中回放示范，先检查走线能否重建，再交给行为克隆训练。[生成与回放](https://github.com/LGAI-Research/CADET/blob/7bea0d51d3ee96bacf2915fd0d3e119fa4404cc5/README.md#2-routedemos-generation-and-replay-verification) |
