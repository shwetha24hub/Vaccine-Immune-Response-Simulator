"""Module 1: Structured dataset containing vaccine details and immune parameters."""

from dataclasses import dataclass
from typing import Dict

@dataclass(frozen=True)
class VaccineProfile:
    name: str
    modality: str
    antigen_decay_rate: float      # delta_A (1/days)
    b_activation_rate: float       # beta_B
    plasma_decay_rate: float       # delta_P (1/days)
    igm_secretion_rate: float      # p_M
    igg_secretion_rate: float      # p_G
    antibody_half_life_days: float # IgG clearance parameter
    recommended_booster_day: int

VACCINE_DATABASE: Dict[str, VaccineProfile] = {
    "mRNA-1273 (Moderna-like)": VaccineProfile(
        name="mRNA-1273",
        modality="mRNA / Lipid Nanoparticle",
        antigen_decay_rate=0.45,
        b_activation_rate=0.08,
        plasma_decay_rate=0.05,
        igm_secretion_rate=1.8,
        igg_secretion_rate=4.2,
        antibody_half_life_days=25.0,
        recommended_booster_day=28,
    ),
    "BNT162b2 (Pfizer-like)": VaccineProfile(
        name="BNT162b2",
        modality="mRNA / Lipid Nanoparticle",
        antigen_decay_rate=0.50,
        b_activation_rate=0.075,
        plasma_decay_rate=0.055,
        igm_secretion_rate=1.6,
        igg_secretion_rate=3.9,
        antibody_half_life_days=23.0,
        recommended_booster_day=21,
    ),
    "Recombinant Protein (Novavax-like)": VaccineProfile(
        name="NVX-CoV2373",
        modality="Subunit + Saponin Adjuvant",
        antigen_decay_rate=0.25,
        b_activation_rate=0.06,
        plasma_decay_rate=0.04,
        igm_secretion_rate=1.2,
        igg_secretion_rate=3.5,
        antibody_half_life_days=28.0,
        recommended_booster_day=21,
    ),
}

def get_vaccine_data(vaccine_key: str) -> VaccineProfile:
    return VACCINE_DATABASE.get(vaccine_key, VACCINE_DATABASE["mRNA-1273 (Moderna-like)"])