# Parcel Delivery Unit Tests

This is my C339 CA1 Project 07. I used pytest to check the two supplied functions against the Parcel Delivery System specification. The supplied source files are unchanged.

## Project Files

```text
07_parcel_delivery/
├── .github/workflows/tests.yml
├── src/
│   ├── parcel_fee.py
│   └── parcel_acceptance.py
├── tests/
│   ├── test_parcel_fee.py
│   └── test_parcel_acceptance.py
├── .gitignore
├── requirements.txt
└── README.md
```

## What the Tests Check

- `delivery_fee(weight_grams)`: weights from 1 to 1000 grams cost 500 cents, and weights from 1001 to 20000 grams cost 1000 cents. The return value must be an integer. Integer weights outside 1 to 20000 must raise `ValueError`.
- `is_parcel_accepted(weight_grams, length_cm)`: return `True` only when the weight is 1 to 20000 grams and the length is 1 to 200 cm, including both limits. Zero or measurements above these limits return `False`. Negative measurements raise `ValueError`. The return value must be a Boolean.
- Both functions must raise `TypeError` for invalid input types, including strings, floats, `None`, Booleans, lists and dictionaries.

I used normal values, boundary values and invalid inputs. The tests use the Arrange–Act–Assert pattern, `pytest.mark.parametrize` for multiple inputs, and `pytest.raises` for exceptions. For parcel acceptance, I tested each parameter separately with the other one valid, as well as combinations of measurements.

## How to Run

Use Python 3.14.4 and open a terminal in the `07_parcel_delivery` folder. Install the dependencies:

```bash
python -m pip install -r requirements.txt
```

Run all tests:

```bash
python -m pytest tests -v
```

Run the tests with a shorter failure report and statement coverage:

```bash
python -m pytest tests -v --tb=short --cov=src --cov-report=term-missing
```

The dependencies are pytest 9.0.2 and pytest-cov 7.1.0.

## Test Results and Defect Analysis

Local results checked on 19 November 2026 using Windows and Python 3.14.4:

| Test file | Total | Passed | Failed |
|---|---:|---:|---:|
| `test_parcel_fee.py` | 20 | 19 | 1 |
| `test_parcel_acceptance.py` | 38 | 35 | 3 |
| **Total** | **58** | **54** | **4** |

All 21 `TypeError` cases and all 6 `ValueError` cases passed. The pass rate is about 93.1%.

### Failed Cases

Weights are in grams, lengths are in cm, and fees are in Singapore cents.

| Function call | Expected | Actual | Defect |
|---|---|---|---|
| `delivery_fee(1000)` | `500` | `1000` | D1 |
| `is_parcel_accepted(500, 200)` | `True` | `False` | D2 |
| `is_parcel_accepted(1, 200)` | `True` | `False` | D2 |
| `is_parcel_accepted(20000, 200)` | `True` | `False` | D2 |

**D1: Incorrect fee at 1000 grams.** Section 3.1 of the specification includes 1000 grams in the 500-cent band. The source uses `weight_grams < 1000`, so it charges 1000 cents at this boundary. The suggested correction is `weight_grams <= 1000`.

**D2: Parcels with a length of 200 cm are rejected.** Section 3.2 includes 200 cm in the accepted range. The source uses `length_cm < 200`, which rejects this boundary even when the weight is valid. The suggested correction is `length_cm <= 200`.

These four failed cases identify two source-code defects. The suggested corrections have not been applied. The test expectations follow the specification and have been kept unchanged.

### Coverage

| Source file | Statements | Missed | Statement coverage |
|---|---:|---:|---:|
| `src/parcel_fee.py` | 8 | 0 | 100% |
| `src/parcel_acceptance.py` | 6 | 0 | 100% |
| **Total** | **14** | **0** | **100%** |

100% statement coverage means that every measured executable statement ran during the tests. It does not mean that all tests passed or that the code has no defects.

## GitHub Actions

The workflow is in `.github/workflows/tests.yml`. It uses Ubuntu 24.04 and Python 3.14.4. It checks out the code, sets up Python, installs the dependencies, and runs pytest with coverage.

The [GitHub Actions run on 18 November 2026](https://github.com/25028784-zjiaxun/07_parcel_delivery/actions/runs/44217499861) also reported 54 passed and 4 failed, with 100% statement coverage. The workflow is marked as failed because pytest returns exit code 1 when tests fail. The environment setup completed successfully in this run.

### Workflow Enhancement

I added a `paths` filter so a push triggers the tests when it changes:

- `src/**`
- `tests/**`
- `requirements.txt`
- `.github/workflows/tests.yml`

This avoids unnecessary test runs for changes only to unrelated files, such as this README, while still testing changes to the code, tests, dependencies or workflow. The workflow also supports manual runs through `workflow_dispatch`.

I verified the `paths` filter with two pushes to `main`. Commit `492d4c5` changed `.github/workflows/tests.yml` and triggered [the test run](https://github.com/25028784-zjiaxun/07_parcel_delivery/actions/runs/44217499861). The next [commit, `1b2b3b7`](https://github.com/25028784-zjiaxun/07_parcel_delivery/commit/1b2b3b7c1fb53814d35748ba2000b1052321e9c7), changed only `README.md`. The GitHub Actions API reported zero runs of this workflow for that commit SHA, confirming that the filter skipped the README-only push.
