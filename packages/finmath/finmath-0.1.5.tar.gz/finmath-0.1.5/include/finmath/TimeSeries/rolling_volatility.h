#ifndef ROLLING_VOLATILITY_H
#define ROLLING_VOLATILITY_H

#include <vector>

// Function to compute the logarithmic returns from prices
std::vector<double> compute_log_returns(const std::vector<double>& prices);

// Function to compute the standard deviation of a vector
double compute_std(const std::vector<double>& data);

// Function to compute the rolling volatility from a time series of prices
std::vector<double> rolling_volatility(const std::vector<double>& prices, size_t window_size);

#endif // ROLLING_VOLATILITY_H
