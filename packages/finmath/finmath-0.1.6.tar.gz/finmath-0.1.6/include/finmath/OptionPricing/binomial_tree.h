#ifndef BINOMIAL_TREE_H
#define BINOMIAL_TREE_H

#include "options_pricing_types.h"

double binomial_option_pricing(OptionType type, double S0, double K, double T, double r, double sigma, long N);

#endif
