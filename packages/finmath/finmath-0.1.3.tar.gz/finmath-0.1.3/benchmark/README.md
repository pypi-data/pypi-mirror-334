# Benchmarking Utilities for Financial Mathematics Functions

This directory contains Python modules for benchmarking financial mathematics functions. It provides an organized framework to benchmark functions for calculating rolling metrics (like Simple Moving Average and Relative Strength Index), as well as other financial and statistical indicators. Results are saved as JSON files with detailed environment information and performance metrics.

## File Descriptions

### `benchmark.py`

The main script to run comprehensive tests for various financial metrics using different implementations. The results are saved in a timestamped JSON file in the `results` directory.

- **Main Function**: `run_exhaustive_test()`
  - Runs a series of tests comparing functions from different libraries (`gs_quant` and `finmath`) for performance.
  - Tests metrics such as:
    - Simple Moving Average (SMA)
    - Relative Strength Index (RSI)
    - Volatility
  - Saves results including environment information, mean execution time, and standard deviation.

### `bench_helper.py`

This module provides helper functions and utilities for testing and benchmarking.

- **Functions**:
  - `get_environment_info()`: Gathers system information, including OS, CPU, RAM, and Python version.
  - `test_function()`: Benchmarks a given function multiple times, calculating mean and standard deviation of runtimes.
  - `test_generic()`: Generalized function for testing any callable function with various inputs and configurations.
  - `test_rolling_window()`: Specifically benchmarks rolling-window functions, such as SMA or RSI, by generating large data arrays and passing a specified window size.

## Requirements

```bash
pip3 install -r requirements.txt
```

- Python 3.7+
- `gs_quant` for `moving_average`, `relative_strength_index`, and `volatility` functions.
- `finmath` for alternative financial calculations.
- `cpuinfo` and `psutil` for environment info.
- `pandas` for data manipulation.

## How to Use

1. Run `run_exhaustive_test.py` to conduct all predefined benchmarks.
2. Review results in the `results` directory. Each result file is timestamped and contains environment details, test configuration, mean execution time, and standard deviation.

## Example Usage

To run the benchmarks:

```bash
python benchmark.py
```
