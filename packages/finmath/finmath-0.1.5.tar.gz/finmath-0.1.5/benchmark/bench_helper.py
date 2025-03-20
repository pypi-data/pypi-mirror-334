"""
This module provides utilities for benchmarking

Functions:
- get_environment_info: Fetches environment info including OS, CPU, RAM, and Python version
- test_function: Tests and benchmarks the function $num_iter times.
"""

from typing import Dict, Tuple, Callable
import platform
import sys
import psutil
import cpuinfo
import time
import statistics
import random
import pandas as pd

def get_environment_info() -> Dict:
    """
    Fetches environment info including OS, CPU, RAM, and Python version
    
    Returns:
        Dict: environment information

    """
    # System and Python version info
    env_info = {
        "OS": platform.system(),
        "OS Version": platform.version(),
        "Machine": platform.machine(),
        "Python Version": sys.version,
        "Python Implementation": platform.python_implementation()
    }

    # CPU info
    cpu_info = cpuinfo.get_cpu_info()
    env_info.update({
        "CPU Brand": cpu_info.get("brand_raw", "Unknown"),
        "CPU Cores (Logical)": psutil.cpu_count(logical=True),
        "CPU Cores (Physical)": psutil.cpu_count(logical=False),
        "CPU Frequency (Max)": psutil.cpu_freq().max
    })

    # Memory info
    memory_info = psutil.virtual_memory()
    env_info["Total RAM (GB)"] = round(memory_info.total / (1024 ** 3), 2)

    return env_info

def test_function(test_func: Callable, num_iter: int, *args) -> Tuple[int, int]: 
    """
    Tests and benchmarks the function $num_iter times.

    Parameters:
        test_func (Callable): the function to benchmark
        num_iter (int): number of times to benchmark
        *args: the arguments that will be passed to test_func

    Returns:
        Tuple[int, int]: the mean and the standard deviation of runtimes in seconds
    """
    times = []
    # Warm-up
    for _ in range(3):
        test_func(*args)
    
    for _ in range(num_iter):
        start = time.perf_counter()
        result = test_func(*args)
        end = time.perf_counter()
        times.append(end - start)

    return statistics.mean(times), statistics.stdev(times)

def test_generic(test_func: Callable, *args, num_iter: int = 3, return_test_config: bool = False,
                 input_size: int = 1, test_name: str = "test_generic"):
    """
    Generalized testing and benchmarking function for arbitrary functions.

    Args:
        test_func (Callable): The function to test. Accepts any function as long as its arguments match those passed through `*args`.
        *args: Arguments to pass to `test_func`.
        num_iter (int, optional): Number of iterations to run the test. Defaults to 3.
        return_test_config (bool, optional): If True, returns the configuration and benchmark statistics (mean, stdev).
            Defaults to False.
        input_size (int, optional): Represents the size of the input data or its parameterization. Defaults to 1.
        test_name (str, optional): Name of the test, used in the configuration output. Defaults to "test_generic".

    Returns:
        Union[Tuple[float, float, Dict], Tuple[float, float]]
            mean (float): The mean execution time across iterations.
            stdev (float): The standard deviation of execution times across iterations.
            - If `return_test_config` is True, also returns:
                test_config (dict): Dictionary with test configuration and statistics.
    """
    
    test_config = {
        "test_name": test_name,
        "test_func": f"{test_func.__module__}.{test_func.__name__}",
        "num_iter": num_iter,
        "input_size": input_size
    }

    if return_test_config:
       mean, stdev = test_function(test_func, num_iter, *args)
       test_config = { **test_config, "mean": mean, "stdev": stdev }
       return mean, stdev, test_config
    
    return test_function(test_func, num_iter, *args)

def test_rolling_window(test_func: Callable, num_iter: int = 3, num_elem: int = int(1e4),
                        window_size: int = 10, return_test_config: bool = False, input_type = list,
                        test_name: str = "test_rolling_window", *args):
    """
    Tests and benchmarks for rolling-window type of functions such as simple moving average or relative strength index

    Args:
        test_func (Callable): The function to test. Must accept a list and a window-size as its argument
        num_iter (int, optional): Number of iterations to run the test. Defaults to 3
        num_elem (int, optional): Number of elements in the generated data array. Defaults to 10^4.
        window_size (int, optional): Size of the rolling window to use in the test function. Defaults to 10.
        return_test_config (bool, optional): If True, returns the configuration and benchmark statistics (mean, stdev).
            Defaults to False.
        input_type (type, optional): Data type for the input array, either `list` or `pd.Series`. Defaults to `list`.
        test_name (str, optional): Name of the test, used in the configuration output. Defaults to "test_rolling_window".
        *args: Additional arguments to pass to the test function.

    Returns:
        Union[Tuple[float, float, Dict], Tuple[float, float]]
            mean (float): The mean execution time across iterations.
            stdev (float): The standard deviation of execution times across iterations.
            - If `return_test_config` is True, also returns:
                test_config (dict): Dictionary with test configuration and statistics.
    """
    test_config = {
        "test_name": test_name,
        "test_func": f"{test_func.__module__}.{test_func.__name__}",
        "num_iter": num_iter,
        "num_elem": num_elem,
        "window_size": window_size,
        "input_type": input_type.__name__
    }

    random.seed(0)
    random_list = [random.randint(1, 1 << 30) for _ in range(num_elem)]
    if input_type == pd.Series:
        random_list = pd.Series(random_list)
    
    if return_test_config:
        mean, stdev = test_function(test_func, num_iter, random_list, window_size)
        test_config = { **test_config, "mean": mean, "stdev": stdev }
        return mean, stdev, test_config
    
    return test_function(test_func, num_iter, random_list, window_size)
