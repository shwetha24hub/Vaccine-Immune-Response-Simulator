"""Module 4: Streamlit interactive interface."""
import numpy as np
import streamlit as st
import plotly.graph_objects as go
from modules.data_manager import VACCINE_DATABASE, get_vaccine_data
from modules.primary_response import simulate_primary_response
from modules.memory_booster import simulate_full_schedule

st.set_page_config(page_title="Vaccine & Immune Memory Simulator", layout="wide")

st.title("Interactive Vaccine Response & Immune Memory System")
st.markdown("Simulation engine tracking primary antigen clearance, clonal expansion, and booster kinetics.")

# Sidebar Configuration
st.sidebar.header("Vaccine & Regimen Controls")
selected_vaccine_name = st.sidebar.selectbox("Select Vaccine Formulation", list(VACCINE_DATABASE.keys()))
profile = get_vaccine_data(selected_vaccine_name)

st.sidebar.markdown(f"**Modality:** `{profile.modality}`")

prime_dose = st.sidebar.slider("Primary Dose (Arbitrary Units)", 25.0, 200.0, 100.0, 5.0)
include_booster = st.sidebar.checkbox("Administer Booster Dose", value=True)

if include_booster:
    booster_day = st.sidebar.slider("Booster Interval (Days)", 14, 60, profile.recommended_booster_day)
    booster_dose = st.sidebar.slider("Booster Dose (AU)", 25.0, 200.0, 100.0, 5.0)
    total_days = st.sidebar.slider("Simulation Timeline (Days)", 60, 180, 90)
else:
    booster_day = None
    total_days = 40

# Execute Calculations
if not include_booster:
    df_primary = simulate_primary_response(profile, dose_units=prime_dose, days=total_days)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df_primary["Day"], y=df_primary["Antigen"], name="Antigen Load", line=dict(color="orange", dash="dash")))
    fig.add_trace(go.Scatter(x=df_primary["Day"], y=df_primary["IgM_Titer"], name="IgM (Early Response)", line=dict(color="royalblue")))
    fig.add_trace(go.Scatter(x=df_primary["Day"], y=df_primary["IgG_Titer"], name="IgG (High-Affinity)", line=dict(color="forestgreen", width=3)))

    fig.update_layout(title="Primary Dose Kinetics", xaxis_title="Days Post-Vaccination", yaxis_title="Concentration (AU)")
    st.plotly_chart(fig, use_container_width=True)

else:
    df_sim = simulate_full_schedule(profile, prime_dose, booster_dose, booster_day, total_days)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df_sim["Day"], y=df_sim["Antigen"], name="Antigen", line=dict(color="gray", dash="dot")))
    fig.add_trace(go.Scatter(x=df_sim["Day"], y=df_sim["Memory_B_Cells"], name="Memory B Cells", line=dict(color="darkorchid")))
    fig.add_trace(go.Scatter(x=df_sim["Day"], y=df_sim["IgG_Antibody_Titer"], name="Total IgG Titer", line=dict(color="firebrick", width=3)))

    # Mark Booster Timing
    fig.add_vline(x=booster_day, line_width=2, line_dash="dash", line_color="black", annotation_text=f"Booster (Day {booster_day})")

    fig.update_layout(
        title=f"Comparative Primary vs. Secondary Booster Response ({profile.name})",
        xaxis_title="Days Post-Initial Vaccination",
        yaxis_title="Arbitrary Units / Titers",
        hovermode="x unified"
    )
    st.plotly_chart(fig, use_container_width=True)

    # Key Metrics
    c1, c2, c3 = st.columns(3)
    primary_peak = df_sim[df_sim["Day"] < booster_day]["IgG_Antibody_Titer"].max()
    secondary_peak = df_sim[df_sim["Day"] >= booster_day]["IgG_Antibody_Titer"].max()
    fold_increase = secondary_peak / max(primary_peak, 1e-3)

    c1.metric("Peak Primary IgG", f"{primary_peak:.1f} AU")
    c2.metric("Peak Secondary IgG", f"{secondary_peak:.1f} AU")
    c3.metric("Booster Fold Amplification", f"{fold_increase:.2f}x")
    # ==========================================
# FEATURE 1: COMPARATIVE VACCINE ANALYSIS
# ==========================================

st.divider()

st.header("Comparative Vaccine Analysis")

st.write(
    "Compare simulated primary IgG antibody responses "
    "across different vaccine formulations."
)

comparison_days = st.slider(
    "Comparison Duration (Days)",
    min_value=30,
    max_value=90,
    value=60
)

comparison_fig = go.Figure()

comparison_results = {}

for vaccine_key, vaccine_profile in VACCINE_DATABASE.items():

    df = simulate_primary_response(
        vaccine_profile,
        dose_units=prime_dose,
        days=comparison_days
    )

    comparison_results[vaccine_profile.name] = df

    comparison_fig.add_trace(
        go.Scatter(
            x=df["Day"],
            y=df["IgG_Titer"],
            mode="lines",
            name=vaccine_profile.name
        )
    )

comparison_fig.update_layout(
    title="Comparative IgG Antibody Response",
    xaxis_title="Days After Vaccination",
    yaxis_title="IgG Antibody Titer (AU)",
    hovermode="x unified",
    template="plotly_white"
)

st.plotly_chart(
    comparison_fig,
    use_container_width=True
)

st.success(
    "Comparative vaccine simulation completed successfully."
)
# ==========================================
# FEATURE 2: SENSITIVITY ANALYSIS
# ==========================================

st.divider()

st.header("Sensitivity Analysis")

st.write(
    "Investigate how changes in biological parameters "
    "influence the simulated IgG antibody response."
)

sensitivity_parameter = st.selectbox(
    "Select Parameter to Investigate",
    [
        "Antigen Decay Rate",
        "B-cell Activation Rate",
        "Antibody Half-Life"
    ]
)

parameter_values = st.slider(
    "Parameter Variation (%)",
    min_value=50,
    max_value=150,
    value=(75, 125),
    step=5
)

sensitivity_fig = go.Figure()

for variation in range(
    parameter_values[0],
    parameter_values[1] + 1,
    25
):

    modified_profile = profile
    factor = variation / 100

    if sensitivity_parameter == "Antigen Decay Rate":
        modified_profile = __import__("dataclasses").replace(
            profile,
            antigen_decay_rate=profile.antigen_decay_rate * factor
        )

    elif sensitivity_parameter == "B-cell Activation Rate":
        modified_profile = __import__("dataclasses").replace(
            profile,
            b_activation_rate=profile.b_activation_rate * factor
        )

    else:
        modified_profile = __import__("dataclasses").replace(
            profile,
            antibody_half_life_days=profile.antibody_half_life_days * factor
        )

    sensitivity_df = simulate_primary_response(
        modified_profile,
        dose_units=prime_dose,
        days=40
    )

    sensitivity_fig.add_trace(
        go.Scatter(
            x=sensitivity_df["Day"],
            y=sensitivity_df["IgG_Titer"],
            mode="lines",
            name=f"{variation}% of baseline"
        )
    )

sensitivity_fig.update_layout(
    title=f"Effect of {sensitivity_parameter} on IgG Response",
    xaxis_title="Days After Vaccination",
    yaxis_title="IgG Antibody Titer (AU)",
    hovermode="x unified",
    template="plotly_white"
)

st.plotly_chart(
    sensitivity_fig,
    use_container_width=True
)
# ==========================================
# FEATURE 3: IMMUNE RESPONSE METRICS
# ==========================================

st.divider()

st.header("Immune Response Metrics")

st.write(
    "Quantitative analysis of simulated antibody "
    "production and immune response characteristics."
)

# Simulate primary immune response
metrics_df = simulate_primary_response(
    profile,
    dose_units=prime_dose,
    days=40
)

# Calculate metrics
peak_igm = metrics_df["IgM_Titer"].max()

peak_igg = metrics_df["IgG_Titer"].max()

time_to_peak = metrics_df.loc[
    metrics_df["IgG_Titer"].idxmax(), "Day"
]

igg_auc = np.trapezoid(
    metrics_df["IgG_Titer"],
    metrics_df["Day"]
)

final_igg = metrics_df["IgG_Titer"].iloc[-1]

# Display metrics
m1, m2, m3 = st.columns(3)

m1.metric("Peak IgM", f"{peak_igm:.2f} AU")
m2.metric("Peak IgG", f"{peak_igg:.2f} AU")
m3.metric("Time to Peak IgG", f"{time_to_peak:.2f} Days")

m4, m5 = st.columns(2)

m4.metric("IgG AUC", f"{igg_auc:.2f} AU-days")
m5.metric("Final IgG", f"{final_igg:.2f} AU")

# Display detailed results
st.subheader("Detailed Immune Response Data")

st.dataframe(
    metrics_df.round(3),
    use_container_width=True
)

# Download simulation results
csv_data = metrics_df.to_csv(index=False)

st.download_button(
    label="Download Immune Response Data (CSV)",
    data=csv_data,
    file_name="immune_response_results.csv",
    mime="text/csv"
)