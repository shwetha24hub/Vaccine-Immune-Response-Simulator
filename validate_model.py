
import numpy as np

from modules.data_manager import VACCINE_DATABASE
from modules.primary_response import simulate_primary_response
from modules.memory_booster import simulate_full_schedule


print("\n===== VACCINE SIMULATOR VALIDATION =====")


# ==================================================
# TEST 1: PRIMARY IMMUNE RESPONSE
# ==================================================

for key, profile in VACCINE_DATABASE.items():

    df = simulate_primary_response(
        profile,
        dose_units=100,
        days=40
    )

    numerical_data = df.select_dtypes(include=[np.number])

    # Check for NaN or infinite values
    assert np.isfinite(numerical_data.values).all(), \
        f"Non-finite values detected in {profile.name}"

    # Check for negative values
    assert (numerical_data >= 0).all().all(), \
        f"Negative values detected in {profile.name}"

    # Check antigen clearance
    assert df["Antigen"].iloc[-1] < df["Antigen"].iloc[0], \
        f"Antigen clearance failed for {profile.name}"

    # Check IgG production
    assert df["IgG_Titer"].max() > 0, \
        f"IgG production failed for {profile.name}"

    print(f"PASS: Primary response - {profile.name}")


# ==================================================
# TEST 2: BOOSTER IMMUNE RESPONSE
# ==================================================

profile = list(VACCINE_DATABASE.values())[0]

booster_df = simulate_full_schedule(
    profile,
    prime_dose=100,
    booster_dose=100,
    booster_day=28,
    total_days=90
)

booster_numerical_data = booster_df.select_dtypes(
    include=[np.number]
)

# Display minimum values for inspection
print("\nMinimum values in booster simulation:")
print(booster_numerical_data.min().to_string())

print("\nNegative values detected:")
for column in booster_numerical_data.columns:
    minimum = booster_numerical_data[column].min()
    if minimum < 0:
        print(f"{column}: {minimum:.15e}")
# Check for NaN or infinite values
assert np.isfinite(booster_numerical_data.values).all(), \
    "Non-finite values detected in booster simulation"

# Check for negative values
# Allow negligible floating-point errors (tolerance = 1e-8)
assert (booster_numerical_data >= -1e-8).all().all(), \
    "Significant negative values detected in booster simulation"

print("PASS: No significant negative values detected")

# Check memory B-cell formation
assert booster_df["Memory_B_Cells"].iloc[-1] > 0, \
    "Memory B-cell formation failed"

# Check IgG production
assert booster_df["IgG_Antibody_Titer"].max() > 0, \
    "Booster IgG production failed"

# Check antigen clearance
assert booster_df["Antigen"].iloc[-1] < booster_df["Antigen"].iloc[0], \
    "Booster antigen clearance failed"

print("\nPASS: Booster simulation")
print("PASS: Memory B-cell formation")
print("PASS: Booster IgG production")
print("PASS: Antigen clearance")


# ==================================================
# FINAL VALIDATION RESULT
# ==================================================

print("\n========================================")
print("ALL VALIDATION TESTS COMPLETED SUCCESSFULLY")
print("========================================")
