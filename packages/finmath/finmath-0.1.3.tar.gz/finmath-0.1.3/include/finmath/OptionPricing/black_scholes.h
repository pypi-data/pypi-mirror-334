#ifndef BLACK_SCHOLES_H
#define BLACK_SCHOLES_H

#include "options_pricing_types.h"

double black_scholes(OptionType type, double strike, double price, double time, double rate, double volatility);

#endif //BLACK_SCHOLES_H
