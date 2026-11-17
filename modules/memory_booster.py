"""Module 3: Memory formation and booster dose kinetics."""

import numpy as np
import pandas as pd
from scipy.integrate import odeint
from modules.data_manager import VaccineProfile

def dual_dose_ode_system(y, t, profile: VaccineProfile, booster_day: float, booster_dose: float):
    # Variables: Antigen (A), Naive B (Bn), Memory B (Bm), Plasma (P), IgG
    A, Bn, Bm, P, IgG = y

    delta_Ab = np.log(2) / profile.antibody_half_life_days

    # Naive vs memory differentiation rates
    activation_from_naive = profile.b_activation_rate * A * (Bn / (100.0 + Bn))
    activation_from_memory = (profile.b_activation_rate * 3.5) * A * (Bm / (100.0 + Bm))

    dA_dt = -profile.antigen_decay_rate * A
    dBn_dt = -activation_from_naive
    dBm_dt = 0.15 * activation_from_naive + 0.25 * activation_from_memory - 0.005 * Bm
    dP_dt = (activation_from_naive + activation_from_memory) - profile.plasma_decay_rate * P
    dIgG_dt = profile.igg_secretion_rate * P - delta_Ab * IgG

    return [dA_dt, dBn_dt, dBm_dt, dP_dt, dIgG_dt]

def simulate_full_schedule(profile: VaccineProfile,
                           prime_dose: float = 100.0,
                           booster_dose: float = 100.0,
                           booster_day: int = 28,
                           total_days: int = 90) -> pd.DataFrame:
    # Phase 1: Day 0 to Booster Day
    t1 = np.linspace(0, booster_day, booster_day * 4)
    y0_phase1 = [prime_dose, 100.0, 5.0, 0.0, 0.0]
    sol1 = odeint(dual_dose_ode_system, y0_phase1, t1, args=(profile, booster_day, booster_dose))

    # Phase 2: Inject Booster Antigen at booster_day
    y0_phase2 = sol1[-1].copy()
    y0_phase2[0] += booster_dose  # Introduce antigen bolus
    
    t2 = np.linspace(booster_day, total_days, (total_days - booster_day) * 4)
    sol2 = odeint(dual_dose_ode_system, y0_phase2, t2, args=(profile, booster_day, booster_dose))

    # Combine time series
    t_full = np.concatenate([t1, t2[1:]])
    sol_full = np.vstack([sol1, sol2[1:]])

    return pd.DataFrame({
        "Day": t_full,
        "Antigen": sol_full[:, 0],
        "Memory_B_Cells": sol_full[:, 2],
        "Plasma_Cells": sol_full[:, 3],
        "IgG_Antibody_Titer": sol_full[:, 4],
    })