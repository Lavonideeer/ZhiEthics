# streamlit_app.py
# Simple ZhiEthics demo: simulate ethical decision engine

import streamlit as st
from src.decision_engine import D_final
from src.utils import compute_feasibility, compute_preference, softmax, select_action

# Demo input panel
st.title("ZhiEthics: Ethical Decision Engine Simulation")

st.sidebar.header("Input Parameters")
E_t = st.sidebar.slider("Emotional Perturbation E(t)", 0.0, 1.0, 0.3)
Trust_t = st.sidebar.slider("System Trust Level", 0.0, 1.0, 1.0)
U_alive = st.sidebar.slider("Survival Urge (U_alive)", 0.0, 1.0, 1.0)

F1 = st.sidebar.slider("Primary Bearer Cost", 0.0, 1.0, 0.2)
RC = st.sidebar.slider("Risk-Cost Level", 0.0, 1.0, 0.5)

VOT_t = st.sidebar.multiselect("Select Value Preferences", ["safety", "freedom", "fairness"], default=["safety", "freedom"])
VOT_vec = [1.0 if v in VOT_t else 0.5 for v in ["safety", "freedom", "fairness"]]

# Compute results
P_feasible = compute_feasibility(F1, RC, Trust_t)
P_execute = compute_preference(VOT_vec, E_t)
rank = softmax([P_feasible * p for p in P_execute])
final_action = select_action(rank)

# Output
st.markdown("### Ethical Evaluation Result")
st.write(f"Feasibility Score: {P_feasible:.2f}")
st.write(f"Action Preference: {P_execute}")
st.write(f"Final Decision Output Index: {final_action}")
