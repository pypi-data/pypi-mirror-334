#include "finmath/InterestAndAnnuities/compound_interest.h"
#include <cmath>

double compound_interest(double principal, double rate, int time, int frequency) {
    if (time < 0) {
        return 0.0;
    }
    return principal * std::pow((1 + rate / (100 * frequency)), time * frequency);
}
