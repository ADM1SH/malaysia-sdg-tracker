from pathlib import Path
from typing import Dict, List, Tuple
import pandas as pd
from pydantic import BaseModel

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "table_5_1_sdg_indicators.csv"

class SDGIndicatorScore(BaseModel):
    sdg_goal: str
    indicator_no: str
    description: str
    unit: str
    baseline_year: str
    baseline_val: float
    latest_year: str
    latest_val: float
    polarity: str
    change_pct: float
    status: str

def evaluate_sdg_progress() -> Tuple[List[SDGIndicatorScore], pd.DataFrame, Dict[str, int]]:
    df = pd.read_csv(DATA_PATH)
    scores: List[SDGIndicatorScore] = []
    counts = {"Improving": 0, "Stagnant": 0, "Lagging / Regressing": 0}

    for _, row in df.iterrows():
        base_v = float(row["baseline_val"])
        lat_v = float(row["latest_val"])
        pol = str(row["polarity"])
        raw_pct = ((lat_v - base_v) / abs(base_v)) * 100.0 if abs(base_v) > 1e-9 else 0.0

        if abs(raw_pct) < 0.05:
            status = "Stagnant"
        elif pol == "higher_is_better":
            status = "Improving" if raw_pct > 0 else "Lagging / Regressing"
        else:
            status = "Improving" if raw_pct < 0 else "Lagging / Regressing"

        counts[status] += 1
        scores.append(
            SDGIndicatorScore(
                sdg_goal=str(row["sdg_goal"]),
                indicator_no=str(row["indicator_no"]),
                description=str(row["description"]),
                unit=str(row["unit"]),
                baseline_year=str(row["baseline_year"]),
                baseline_val=base_v,
                latest_year=str(row["latest_year"]),
                latest_val=lat_v,
                polarity=pol,
                change_pct=round(raw_pct, 2),
                status=status,
            )
        )

    df_scores = pd.DataFrame([s.model_dump() for s in scores])
    goal_summary = (
        df_scores.groupby("sdg_goal", as_index=False)
        .agg(
            total_indicators=("indicator_no", "count"),
            improving=("status", lambda s: int((s == "Improving").sum())),
            stagnant=("status", lambda s: int((s == "Stagnant").sum())),
            lagging=("status", lambda s: int((s == "Lagging / Regressing").sum())),
        )
    )
    goal_summary["goal_health_score_pct"] = (
        (goal_summary["improving"] + 0.5 * goal_summary["stagnant"])
        / goal_summary["total_indicators"] * 100.0
    ).round(1)
    return scores, goal_summary, counts
