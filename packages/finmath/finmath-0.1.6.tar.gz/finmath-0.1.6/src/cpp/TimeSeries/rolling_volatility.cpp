#include "finmath/TimeSeries/rolling_volatility.h"

#include <algorithm>
#include <cmath>
#include <iostream>
#include <numeric>
#include <vector>

// Function to compute the logarithmic returns
std::vector<double> compute_log_returns(const std::vector<double>& prices) {
    std::vector<double> log_returns;
    for (size_t i = 1; i < prices.size(); ++i) {
        log_returns.push_back(std::log(prices[i] / prices[i - 1]));
    }
    return log_returns;
}

// Function to compute the standard deviation of a vector
double compute_std(const std::vector<double>& data) {
    double mean = std::accumulate(data.begin(), data.end(), 0.0) / data.size();
    double sq_sum = std::inner_product(data.begin(), data.end(), data.begin(), 0.0);
    return std::sqrt(sq_sum / data.size() - mean * mean);
}

// Function to compute rolling volatility
std::vector<double> rolling_volatility(const std::vector<double>& prices, size_t window_size) {
    std::vector<double> volatilities;

    // Compute log returns
    std::vector<double> log_returns = compute_log_returns(prices);

    // Rolling window calculation
    for (size_t i = 0; i <= log_returns.size() - window_size; ++i) {
        // Get the window of log returns
        std::vector<double> window(log_returns.begin() + i, log_returns.begin() + i + window_size);

        // Compute the standard deviation
        double std_dev = compute_std(window);

        // Annualize the standard deviation (multiply by sqrt(252))
        double annualized_vol = std_dev * std::sqrt(252);

        // Store the result
        volatilities.push_back(annualized_vol);
    }

    return volatilities;
}