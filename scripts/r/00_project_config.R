get_script_dir <- function() {
  args <- commandArgs(trailingOnly = FALSE)
  file_arg <- "--file="
  script_path <- sub(file_arg, "", args[grep(file_arg, args)])
  if (length(script_path) == 0) {
    return(getwd())
  }
  normalizePath(dirname(script_path))
}

project_root <- normalizePath(file.path(get_script_dir(), "..", ".."), mustWork = FALSE)

data_dir <- file.path(project_root, "data")
raw_dir <- file.path(data_dir, "raw")
processed_dir <- file.path(data_dir, "processed")
outputs_dir <- file.path(project_root, "outputs")
reports_dir <- file.path(outputs_dir, "reports")
models_dir <- file.path(outputs_dir, "models")
figures_dir <- file.path(project_root, "figures")

covariates <- c(
  "body_mass_change_kg",
  "sex",
  "weight_class",
  "time_between_tests_hours",
  "training_status"
)

timepoint_map <- c(T0 = 0, T1 = 1)

# Modeling notes:
# - lme4::lmer for linear mixed-effects
# - lmerTest for p-values
# - brms for Bayesian extensions
