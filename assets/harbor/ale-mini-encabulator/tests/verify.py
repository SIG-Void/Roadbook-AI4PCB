"""Run KiCad DRC in a clean directory and pass its report to the ALE scorer."""
import json
import shutil
import subprocess
import tempfile
from pathlib import Path

from score_outputs import score_from_text

BOARD = Path("/app/output/mini_encabulator.kicad_pcb")
LOGS = Path("/logs/verifier")


def evaluate():
    if not BOARD.is_file():
        return {"score": 0.0, "reason": "missing_output"}

    with tempfile.TemporaryDirectory() as folder:
        board = Path(folder) / "submission.kicad_pcb"
        report = Path(folder) / "drc.json"
        shutil.copyfile(BOARD, board)
        run = subprocess.run(
            ["kicad-cli", "pcb", "drc", "--format", "json", "--severity-all",
             "--severity-exclusions", "--output", str(report), str(board)],
            capture_output=True, text=True,
        )
        drc = None
        reason = None
        if run.returncode == 0 and report.is_file():
            drc = report.read_text(encoding="utf-8")
            (LOGS / "drc.json").write_text(drc, encoding="utf-8")
        else:
            reason = run.stderr.strip() or f"DRC report unavailable (KiCad exit {run.returncode})"
        return score_from_text(
            board.read_text(encoding="utf-8", errors="replace"),
            drc_json_text=drc,
            drc_unavailable_reason=reason,
            allow_structural_fallback=False,
        )


if __name__ == "__main__":
    LOGS.mkdir(parents=True, exist_ok=True)
    result = evaluate()
    (LOGS / "checks.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    (LOGS / "reward.txt").write_text(str(result["score"]) + "\n", encoding="utf-8")
