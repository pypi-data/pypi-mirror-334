#include <cmath>
#include "finmath/Helper/helper.h"


// Standard normal cumulative distribution function
double normal_cdf(double x) {
    return 0.5 * std::erfc(-x / std::sqrt(2));
}

// Standard normal probability density function
double normal_pdf(double x) {
    return std::exp(-0.5 * x * x) / std::sqrt(2 * M_PI);
}

long long combinations(long n, long k) {
    // Ensure k <= n - k to minimize operations
    if (k > n - k) {
        k = n - k;
    }

    long long result = 1;  // Use long long to handle large numbers

    // Efficiently compute the binomial coefficient
    for (long i = 0; i < k; ++i) {
        result *= (n - i);    // Multiply by (n - i)
        result /= (i + 1);    // Divide by (i + 1)
    }

    return result;
}

