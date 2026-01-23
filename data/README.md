# Data directory

This directory stores raw and processed data for the project. Raw data are not committed to git.

## Naming convention
Use a consistent schema for data files:
`<participant_id>_<timepoint>_<trial>_<date>_<units>.<ext>`

Examples:
- `athlete001_T0_trial01_2025-12-17_metric.csv`
- `athlete001_T1_trial01_2025-12-20_metric.csv`

Timepoints:
- `T0`: baseline (pre-competition)
- `T1`: post weigh-in (acute dehydration)

Raw data are not committed. Place unmodified exports in `data/raw/` and use `data/processed/` for analysis-ready files.
