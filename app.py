import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from src.sdg_model import evaluate_sdg_progress

st.set_page_config(page_title="Malaysia SDG Progress Tracker", layout="wide")
st.title("SDG PROGRESS TRACKER (TABLE 5.1)")
st.caption("Monitoring Malaysia's Progress Across All 17 UN Sustainable Development Goals")

scores, goal_summary, counts = evaluate_sdg_progress()
df_scores = pd.DataFrame([s.model_dump() for s in scores])

k1, k2, k3 = st.columns(3)
k1.metric("Improving Indicators", str(counts["Improving"]))
k2.metric("Stagnant Indicators", str(counts["Stagnant"]))
k3.metric("Lagging / Regressing Indicators", str(counts["Lagging / Regressing"]))

fig = go.Figure()
fig.add_trace(go.Bar(name="Improving", x=goal_summary["sdg_goal"], y=goal_summary["improving"], marker_color="#1D4ED8"))
fig.add_trace(go.Bar(name="Stagnant", x=goal_summary["sdg_goal"], y=goal_summary["stagnant"], marker_color="#EAB308"))
fig.add_trace(go.Bar(name="Lagging", x=goal_summary["sdg_goal"], y=goal_summary["lagging"], marker_color="#D92B2B"))
fig.update_layout(barmode="stack", title="SDG Indicator Progress by Goal", paper_bgcolor="#FFFFFF")
st.plotly_chart(fig, use_container_width=True)

st.subheader("Flagged Lagging / Regressing Indicators")
st.dataframe(df_scores[df_scores["status"] == "Lagging / Regressing"], use_container_width=True)
st.subheader("Goal Health Summary")
st.dataframe(goal_summary, use_container_width=True)
