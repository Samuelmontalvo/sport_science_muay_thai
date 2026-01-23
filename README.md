# Muay Thai Weight-Cut (Dehydration) Effects on Force-Plate Vertical Jump Performance

This project studies repeated-measures force-plate vertical jump performance in world-level Muay Thai fighters. Athletes completed vertical jumps at (T0) baseline a few days pre-competition and again at (T1) immediately post weigh-in (after acute weight cut/dehydration and before full rehydration). The goal is to quantify the acute effect of weigh-in-associated dehydration on jump kinematic and kinetic metrics while modeling relevant covariates.

**Project Context (verbatim)**
- Domain: Muay Thai (world-level competition)
- Data source: Force plate vertical jump testing from the VALD system (ForceDecks / related export). Data include kinematic and kinetic parameters (e.g., CMJ/SJ outcomes).
- Study design: repeated measures. Fighters performed vertical jumps at (T0) baseline a few days pre-competition, and again at (T1) immediately post weigh-in (after acute weight cut / dehydration and before full rehydration). Goal is to quantify the acute effect of weigh-in–associated dehydration on jump kinematic/kinetic metrics, while modeling relevant covariates (e.g., body mass change, sex, weight class, time between tests, training status, etc.; keep covariates as a configurable list).
- Competition context to include in README: This project references competition media for a bout featuring Laura Burgos vs Michelle Viljoen at Rajadamnern World Series (RWS) 173 (Rajadamnern Stadium, Thailand) on December 20, 2025.

## Data source
Data come from force plate vertical jump testing exported from the VALD system (ForceDecks or related formats). Measures include CMJ/SJ outcomes with kinematic and kinetic features.

## Competition context
This project references competition media for a bout featuring Laura Burgos vs Michelle Viljoen at Rajadamnern World Series (RWS) 173 at Rajadamnern Stadium in Thailand on December 20, 2025.

## Primary aims and example outcomes
- Quantify T0 to T1 changes in vertical jump performance after acute weight cut/dehydration.
- Evaluate key outcomes such as jump height, peak force, impulse, rate of force development (RFD), peak power, eccentric/concentric phase metrics, and asymmetry indices if present.
- Model covariates (configurable list) including body mass change, sex, weight class, time between tests, and training status.

## Analysis plan (sketch)
- EDA and QC: check missingness, duplicates, range checks, and trial validity.
- Primary model: linear mixed-effects with random intercept for athlete, fixed effect for timepoint (T0 vs T1), covariates, and optional interactions.
- Sensitivity analyses: percent change models, robust regression, and exclusion of failed trials.

## Reproducibility
- Create the Python environment: `conda env create -f environment.yml`
- Run QC: `python scripts/python/01_ingest_qc.py --input data/processed/<file>`
- Outputs are written to `outputs/reports/` (QC) and `outputs/models/` (model artifacts).

## Directory map
- `data/` raw (not committed), processed, external, private
- `scripts/` analysis utilities (Python, R)
- `figures/` exploratory and final figures
- `outputs/` model outputs and reports (not committed)
- `manuscript/` journal draft, tables, references
- `notebooks/` exploratory work
- `docs/` project documentation
