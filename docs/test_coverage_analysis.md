# Test Coverage Analysis

**Generated:** 2026-01-23
**Branch:** claude/analyze-test-coverage-5OQOt

## Executive Summary

The codebase currently has **zero test coverage**. No test files, test infrastructure, or testing dependencies exist. This represents a critical gap for a scientific research project where data integrity and reproducibility are paramount.

## Current State

### Existing Code Structure

The project contains two Python modules:

1. **`scripts/python/00_project_config.py`** (53 lines)
   - Path configuration constants
   - Logging setup function
   - Directory creation utility
   - Covariate definitions
   - Timepoint mappings

2. **`scripts/python/01_ingest_qc.py`** (156 lines)
   - Data loading (CSV, Parquet)
   - QC checks: missingness, duplicates, range validation
   - Required column validation
   - Timepoint validation
   - Report generation

### Testing Infrastructure

- **Test files:** 0
- **Test configuration:** None (no pytest.ini, .coveragerc, or pyproject.toml)
- **Testing dependencies:** Not included in environment.yml
- **CI/CD testing:** Not configured

## Critical Areas Requiring Test Coverage

### 1. Data Loading Functions (`01_ingest_qc.py`)

**Priority: HIGH**

The `load_data()` function is a critical entry point that handles multiple file formats:

```python
def load_data(path: Path) -> pd.DataFrame:
    # Lines 44-52
```

**Required tests:**
- ✗ Valid CSV file loading
- ✗ Valid Parquet file loading
- ✗ FileNotFoundError handling
- ✗ Unsupported file type handling (.xlsx, .json, etc.)
- ✗ Corrupted file handling
- ✗ Empty file handling
- ✗ Large file handling (memory constraints)
- ✗ Case-insensitive suffix matching (.CSV, .Parquet)

**Risk:** Incorrect data loading could invalidate entire analysis pipeline.

### 2. QC Validation Functions (`01_ingest_qc.py`)

**Priority: HIGH**

Multiple QC functions lack any validation:

#### `qc_missingness()` (lines 55-56)
**Required tests:**
- ✗ DataFrame with no missing values
- ✗ DataFrame with partial missingness
- ✗ DataFrame with complete missingness (all NaN column)
- ✗ Empty DataFrame
- ✗ Correct sorting (descending by missingness)

#### `qc_duplicates()` (lines 59-60)
**Required tests:**
- ✗ DataFrame with no duplicates
- ✗ DataFrame with exact duplicates
- ✗ DataFrame with multiple duplicate groups
- ✗ Empty DataFrame

#### `qc_range_checks()` (lines 63-70)
**Required tests:**
- ✗ All values within range
- ✗ Values below minimum
- ✗ Values above maximum
- ✗ Missing columns (should skip gracefully)
- ✗ Non-numeric values (coercion with errors='coerce')
- ✗ Edge cases (exactly at boundaries)
- ✗ NaN values after coercion

**Risk:** False negatives could allow invalid data into analysis; false positives could reject valid data.

#### `qc_required_columns()` (lines 73-74)
**Required tests:**
- ✗ All required columns present
- ✗ Some required columns missing
- ✗ All required columns missing
- ✗ Extra columns present (should not affect check)

#### `qc_timepoints()` (lines 77-83)
**Required tests:**
- ✗ All valid timepoints (T0, T1, 0, 1)
- ✗ Invalid timepoints (T2, "baseline", etc.)
- ✗ Mixed valid and invalid
- ✗ Missing timepoint column
- ✗ NaN timepoint values

### 3. Report Generation (`01_ingest_qc.py`)

**Priority: MEDIUM**

The `write_report()` function (lines 86-132) formats and writes QC results:

**Required tests:**
- ✗ Report file creation
- ✗ Parent directory creation
- ✗ Markdown formatting correctness
- ✗ Numeric formatting (thousands separators, percentages)
- ✗ Empty result sets
- ✗ Unicode handling in column names
- ✗ Report content validation (contains expected sections)

### 4. Configuration Module (`00_project_config.py`)

**Priority: MEDIUM**

#### Path Configuration (lines 6-16)
**Required tests:**
- ✗ Path resolution relative to project root
- ✗ Paths are absolute (not relative)
- ✗ PROJECT_ROOT points to correct location

#### `ensure_project_dirs()` (lines 40-52)
**Required tests:**
- ✗ Creates missing directories
- ✗ Handles existing directories (idempotent)
- ✗ Creates nested directory structure
- ✗ Handles permission errors (if applicable)

#### `setup_logging()` (lines 30-34)
**Required tests:**
- ✗ Default INFO level configuration
- ✗ Custom log level
- ✗ Log format validation
- ✗ Multiple invocations (reconfiguration behavior)

### 5. Argument Parsing (`01_ingest_qc.py`)

**Priority: LOW**

The `parse_args()` function (lines 25-41):

**Required tests:**
- ✗ Default arguments
- ✗ Custom input path
- ✗ Custom output path
- ✗ Invalid path formats
- ✗ Help message generation

### 6. Integration Tests

**Priority: HIGH**

End-to-end workflow tests:

**Required tests:**
- ✗ Complete QC pipeline with valid data
- ✗ Pipeline with data containing QC violations
- ✗ Pipeline with missing files
- ✗ Generated report accuracy
- ✗ Idempotency (running twice produces same results)

## Recommended Testing Infrastructure

### 1. Test Framework Setup

Add to `environment.yml`:
```yaml
dependencies:
  # ... existing dependencies
  - pytest>=7.4
  - pytest-cov>=4.1
  - pytest-mock>=3.12
```

### 2. Test Directory Structure

```
tests/
├── __init__.py
├── conftest.py                    # Shared fixtures
├── test_project_config.py         # Config module tests
├── test_ingest_qc.py              # QC module tests
├── integration/
│   ├── __init__.py
│   └── test_qc_pipeline.py        # End-to-end tests
└── fixtures/
    ├── valid_data.csv
    ├── valid_data.parquet
    ├── missing_data.csv
    ├── out_of_range_data.csv
    └── invalid_timepoints.csv
```

### 3. Testing Configuration Files

**pytest.ini:**
```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts =
    --verbose
    --cov=scripts/python
    --cov-report=html
    --cov-report=term-missing
    --cov-fail-under=80
```

**.coveragerc:**
```ini
[run]
source = scripts/python
omit =
    */tests/*
    */test_*.py

[report]
precision = 2
show_missing = True
skip_covered = False

[html]
directory = outputs/coverage_html
```

### 4. CI/CD Integration

Create `.github/workflows/tests.yml`:
```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: conda-incubator/setup-miniconda@v2
        with:
          environment-file: environment.yml
      - name: Run tests
        run: |
          conda activate sport_science_muay_thai
          pytest
```

## Test Coverage Targets

| Component | Priority | Target Coverage | Estimated Tests |
|-----------|----------|-----------------|-----------------|
| Data loading | HIGH | 95%+ | 8-10 tests |
| QC functions | HIGH | 90%+ | 25-30 tests |
| Report generation | MEDIUM | 80%+ | 7-10 tests |
| Configuration | MEDIUM | 85%+ | 8-12 tests |
| Argument parsing | LOW | 70%+ | 5-7 tests |
| Integration | HIGH | End-to-end coverage | 5-8 tests |
| **TOTAL** | | **85%+ overall** | **58-77 tests** |

## Implementation Phases

### Phase 1: Foundation (Priority 1)
1. Add testing dependencies to environment.yml
2. Create test directory structure
3. Set up pytest.ini and .coveragerc
4. Create conftest.py with shared fixtures
5. Generate test data fixtures

### Phase 2: Critical Path (Priority 2)
1. Test data loading functions (test_load_data_*)
2. Test QC validation functions (test_qc_*)
3. Basic integration tests

### Phase 3: Comprehensive (Priority 3)
1. Test report generation
2. Test configuration module
3. Test argument parsing
4. Advanced integration tests
5. Edge case coverage

### Phase 4: Infrastructure (Priority 4)
1. CI/CD pipeline setup
2. Pre-commit hooks
3. Coverage reporting
4. Documentation

## Risk Assessment

### Critical Risks (Current State)

1. **Data Integrity Risk:** No validation that QC functions correctly identify invalid data
2. **Regression Risk:** Code changes may break existing functionality without detection
3. **Scientific Validity Risk:** Errors in data processing could invalidate research findings
4. **Reproducibility Risk:** Cannot verify consistent behavior across environments

### Mitigation Through Testing

- Unit tests → Validate individual function correctness
- Integration tests → Verify end-to-end pipeline
- Fixture-based tests → Ensure consistent test data
- CI/CD → Catch regressions before merge

## Immediate Action Items

1. **Install testing infrastructure** (Phase 1)
2. **Create test fixtures** with known-good and known-bad data samples
3. **Implement high-priority tests** for data loading and QC functions
4. **Set up coverage reporting** to track progress
5. **Establish testing policy** (e.g., "all new functions require tests")

## Long-term Recommendations

1. **Achieve 80%+ coverage** before adding new features
2. **Require tests for all PRs** as part of code review
3. **Run tests in CI/CD** on every commit
4. **Generate coverage reports** and track trends
5. **Document testing patterns** for contributors
6. **Add property-based testing** with hypothesis for QC functions
7. **Performance testing** for large dataset handling
8. **Add type checking** with mypy or pyright

## Conclusion

The complete absence of tests represents a significant risk for a scientific research project. The good news is the codebase is small (209 lines) and well-structured, making it feasible to achieve high coverage quickly. Prioritizing tests for data loading and QC validation functions will provide the most immediate value for ensuring research validity and reproducibility.

**Recommended immediate next step:** Implement Phase 1 (Foundation) and Phase 2 (Critical Path) testing infrastructure and tests within the next sprint.
