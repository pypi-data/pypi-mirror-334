#include <cmath> 
#include "finmath/OptionPricing/black_scholes.h"
#include "finmath/Helper/helper.h"

double black_scholes(OptionType type, double strike, double price, double time, double rate, double volatility){
    double d1 = (std::log(price / strike) + ((rate + volatility*volatility/2) * time)) / (volatility * std::sqrt(time));
    double d2 = d1 - (volatility * std::sqrt(time));

    if (type == OptionType::CALL) {
        return price * normal_cdf(d1) - std::exp(-rate * time) * strike * normal_cdf(d2);
    } else {
        return strike * std::exp(-rate * time) * normal_cdf(-d2) - price * normal_cdf(-d1);
    }
}
