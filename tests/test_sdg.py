from src.sdg_model import evaluate_sdg_progress

def test_sdg():
    scores, goal_summary, counts = evaluate_sdg_progress()
    assert len(scores) >= 35
    assert len(goal_summary) == 17
    assert counts["Lagging / Regressing"] > 0
