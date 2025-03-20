import finmath

print(dir(finmath))
print(finmath.__file__)

# Example: Calculate compound interest
principal = 1000
rate = 5
time = 10
frequency = 4
result = finmath.compound_interest(principal, rate, time, frequency)
print(f"Compound Interest: {result}")

