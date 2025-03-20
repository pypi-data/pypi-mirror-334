# Interest And Annuities Documentation

This document provides documentation for functions available in InterestAndAnnuities in the `FinMath` library, organized by category. Each function includes its description, syntax, parameters, return values, and usage examples.

---

## Table of Contents

- [Interest Functions](#interest-functions)
  - [compound_interest](#compound_interest)
  - [simple_interest](#simple_interest)
- [Annuity Functions](#annuity-functions)


---

## Interest Functions

### `compound_interest`

#### Description

Calculates the future value based on compound interest, given an initial principal, rate, time period, and compounding frequency.

#### Syntax

```cpp
double compound_interest(double principal, double rate, int time, int frequency);
```

#### Parameters
- **principal** (`double`): The initial amount of money invested or loaned.
- **rate** (`double`): The interest rate per period (expressed as a decimal, e.g., 0.05 for 5%).
- **time** (`int`): The total time in years that the money is invested or borrowed for.
- **frequency** (`int`): The number of times interest is compounded per year.

#### Returns
- **double**: The future value after applying compound interest.

---

### `simple_interest`

#### Description

Calculates the future value based on simple interest, given an initial principal, rate, and time period.

#### Syntax

```cpp
double simple_interest(double principal, double rate, double time);
```

#### Parameters
- **principal** (`double`): The initial amount of money invested or loaned.
- **rate** (`double`): The interest rate per period (expressed as a decimal, e.g., 0.05 for 5%).
- **time** (`double`): The total time in years that the money is invested or borrowed for.

#### Returns
- **double**: The future value after applying simple interest.
