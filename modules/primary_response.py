"""Module 2: Primary immune response modeling via Runge-Kutta integration."""

import numpy as np
import pandas as pd
from scipy.integrate import odeint
from modules.data_manager import VaccineProfile

def primary_ode_system(y, t, profile: VaccineProfile):
    # State variables: Antigen (A), Activated B/Plasma (P), IgM, IgG
    A, P, IgM, IgG = y

    delta_Ab = np.log(2) / profile.antibody_half_life_days

    dA_dt = -profile.antigen_decay_rate * A
    dP_dt = profile.b_activation_rate * A - profile.plasma_decay_rate * P
    dIgM_dt = profile.igm_secretion_rate * P - 0.20 * IgM  # IgM short half-life (~3-5 days)
    dIgG_dt = profile.igg_secretion_rate * P - delta_Ab * IgG

    return [dA_dt, dP_dt, dIgM_dt, dIgG_dt]

def simulate_primary_response(profile: VaccineProfile, dose_units: float = 100.0, days: int = 40) -> pd.DataFrame:
    t = np.linspace(0, days, days * 4)
    y0 = [dose_units, 0.0, 0.0, 0.0]

    solution = odeint(primary_ode_system, y0, t, args=(profile,))

    return pd.DataFrame({
        "Day": t,
        "Antigen": solution[:, 0],
        "Effector_Cells": solution[:, 1],
        "IgM_Titer": solution[:, 2],
        "IgG_Titer": solution[:, 3],
    })