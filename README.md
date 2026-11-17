# Vaccine and Immune Response Simulator

### A Computational Model of Primary Immune Response, Booster Vaccination and Immune Memory Formation

## 1. Project Overview

The Vaccine and Immune Response Simulator is a Python-based computational application designed to simulate selected aspects of the human immune response following vaccination.

The application uses mathematical modelling and numerical integration of ordinary differential equations (ODEs) to represent antigen clearance, immune-cell activation, antibody production and immune memory formation.

An interactive dashboard developed using Streamlit allows users to explore simulated immune responses under different vaccine parameter assumptions and vaccination schedules.

## 2. Project Objectives

- Simulate primary immune responses following vaccination.
- Model IgM and IgG antibody production.
- Represent immune memory B-cell formation.
- Simulate booster vaccination and secondary immune responses.
- Compare illustrative vaccine parameter profiles.
- Investigate the influence of model parameters through sensitivity analysis.
- Calculate quantitative immune response metrics.

## 3. Technologies Used

| Technology | Application |
|---|---|
| Python | Core programming |
| NumPy | Numerical calculations |
| Pandas | Data handling |
| SciPy | ODE integration |
| Streamlit | Interactive dashboard |
| Plotly | Interactive visualisation |

## 4. Vaccine Profiles

The application contains three illustrative vaccine profiles:

1. mRNA-1273 (Moderna-like)
2. BNT162b2 (Pfizer-like)
3. Recombinant Protein (Novavax-like)

**Important:** The numerical parameters are hypothetical modelling assumptions. They are not experimentally measured or clinically validated vaccine-specific parameters. Comparisons represent model behaviour under these assumptions, not actual clinical vaccine effectiveness.

## 5. Project Modules

### Module 1: Vaccine Data Management

File: `modules/data_manager.py`

Stores vaccine profile information and illustrative immune-response parameters.

### Module 2: Primary Immune Response

File: `modules/primary_response.py`

Models:
- Antigen concentration
- Activated B-cell/plasma-cell compartment
- IgM antibody production
- IgG antibody production

The model uses ordinary differential equations and numerical integration.

### Module 3: Immune Memory and Booster Response

File: `modules/memory_booster.py`

Models:
- Naive B-cell dynamics
- Memory B-cell formation
- Plasma-cell response
- IgG production following booster vaccination

### Module 4: Interactive Dashboard

File: `app.py`

Provides:
- Vaccine profile selection
- Primary and booster simulation
- Comparative vaccine analysis
- One-at-a-time sensitivity analysis
- Immune response metrics
- CSV result export

## 6. Mathematical Modelling

The primary immune response is represented using a simplified compartmental ODE model.

Let:

- A = Antigen concentration
- P = Combined activated B-cell/plasma-cell compartment
- IgM = IgM antibody level
- IgG = IgG antibody level

The governing equations are:

**Antigen clearance**

dA/dt = -δA × A

**Immune-cell activation**

dP/dt = βB × A - δP × P

**IgM production**

dIgM/dt = pM × P - δM × IgM

**IgG production**

dIgG/dt = pG × P - δG × IgG

The booster model additionally includes naive B cells and memory B cells to represent a simplified secondary immune response.

## 7. Immune Response Metrics

The application calculates:

- Peak IgM level
- Peak IgG level
- Time to peak IgG
- IgG area under the curve (AUC)
- Final IgG level

These metrics describe the simulated antibody response over the selected time interval.

## 8. Installation and Execution

### Prerequisites

- Python 3.10 or later
- Visual Studio Code (recommended)

### Step 1: Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
```

### Step 2: Navigate into the project folder

```bash
cd vacc
```

### Step 3: Install dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Launch the application

```bash
streamlit run app.py
```

### Step 5: Validate the simulation

```bash
python validate_model.py
```

## 9. Validation

The project includes a validation script that checks:

- Finite numerical outputs
- Non-negative values within a defined numerical tolerance
- Antigen clearance
- IgG production
- Memory B-cell formation
- Booster simulation functionality

The current validation tests passed for all three primary vaccine profiles and the booster simulation.

## 10. Model Assumptions and Limitations

This project is an educational computational simulation and not a clinical prediction system.

The model has several limitations:

- Immune responses are represented using simplified compartments.
- Vaccine parameters are illustrative assumptions.
- Germinal-centre reactions are not explicitly modelled.
- T-cell responses are not included.
- Antibody affinity maturation is not represented.
- Individual differences, infection history and pre-existing immunity are not considered.
- The model has not been validated against experimental or clinical datasets.

Therefore, simulated antibody levels must not be interpreted as actual patient antibody measurements or vaccine effectiveness.

## 11. Future Enhancements

- Calibration using published experimental datasets.
- Inclusion of T-cell-mediated immune responses.
- More detailed germinal-centre and affinity maturation models.
- Parameter estimation and uncertainty analysis.
- Comparison with experimentally observed immune-response profiles.
- Extended immune memory modelling.

## 12. Conclusion

The Vaccine and Immune Response Simulator demonstrates how computational modelling, numerical integration and interactive visualisation can be combined to explore selected mechanisms of vaccination-induced immune responses.

The application provides a foundation for further development of computational immunology models.

---

**Project Category:** Computational Biology / Immunoinformatics / Mathematical Modelling

**Programming Language:** Python