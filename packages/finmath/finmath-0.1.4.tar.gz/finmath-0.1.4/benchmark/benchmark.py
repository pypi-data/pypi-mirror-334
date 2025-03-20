import sys
sys.path.append("../build")

import finmath
import bench_helper as bh
import gs_quant.timeseries as ts
import pandas as pd
from datetime import datetime
import json

def run_exhaustive_test():
    current_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    benchmark_result = {}
    benchmark_result["environment_info"] = bh.get_environment_info()


    # Test 1: SMA
    mean_gs, _, test_config_gs = bh.test_rolling_window(ts.moving_average, num_elem=int(1e4), return_test_config=True,
                                                        input_type=pd.Series, test_name="SMA_GS")
    mean_finmath, _, test_config_finmath = bh.test_rolling_window(finmath.simple_moving_average, num_elem=int(1e4), 
                                                                  return_test_config=True, test_name="SMA_FINMATH")
    benchmark_result["SMA"] = {
        "GS_MEAN": mean_gs,
        "FINMATH_MEAN": mean_finmath,
        "PERFORMANCE_IMPROVEMENT": mean_gs / mean_finmath,
        "SMA_GS": test_config_gs,
        "SMA_FINMATH": test_config_finmath
    }
    
    # Test 2: RSI
    mean_gs, _, test_config_gs = bh.test_rolling_window(ts.relative_strength_index, num_elem=int(1e4), return_test_config=True,
                                                        input_type=pd.Series, test_name="RSI_GS")
    mean_finmath, _, test_config_finmath = bh.test_rolling_window(finmath.rsi, num_elem=int(1e4), return_test_config=True,
                                                             test_name="RSI_FINMATH")
    benchmark_result["RSI"] = {
        "GS_MEAN": mean_gs,
        "FINMATH_MEAN": mean_finmath,
        "PERFORMANCE_IMPROVEMENT": mean_gs / mean_finmath,
        "SMA_GS": test_config_gs,
        "SMA_FINMATH": test_config_finmath
    }
    
    # Test 3: Volatility
    mean_gs, _, test_config_gs = bh.test_generic(ts.volatility, ts.generate_series(int(1e4)), 20, return_test_config=True, input_size=int(1e4), 
                                                        test_name="Volatility_GS")
    mean_finmath, _, test_config_finmath = bh.test_rolling_window(finmath.rolling_volatility, num_elem=int(1e4), return_test_config=True,
                                                                    test_name="Volatility_FINMATH")
    benchmark_result["ROLLING_VOLATILITY"] = {
        "GS_MEAN": mean_gs,
        "FINMATH_MEAN": mean_finmath,
        "PERFORMANCE_IMPROVEMENT": mean_gs / mean_finmath,
        "SMA_GS": test_config_gs,
        "SMA_FINMATH": test_config_finmath
    }

    with open(f"results/{current_timestamp}.json", "w") as file:
        json.dump(benchmark_result, file, indent=4)
    
run_exhaustive_test()