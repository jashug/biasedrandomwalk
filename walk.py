# Author: Jasper Hugunin
# On a biased random walk

# Setup:
# Consider a random walk on the integers starting at n, ending at x <= 0.
# With equal probability, take two steps left or one step right.
# What is the expected length of the walk?

# l(n): random variable giving the length of a walk starting at n
# p(n): random variable giving the probability of ending at -1 rather than 0
# P(n): event that a walk starting at n ends at -1
# We have l(n) = 2 n + 2 p(n), p(n) = l(n) / 2 - n
# E[p(n)] = Pr[P(n)]

# E[l(-1)] = E[l(0)] = 0
# E[l(n)] = 1 + 1/2 E[l(n-2)] + 1/2 E[l(n+1)] for n >= 1

# E[p(-1)] = 1, E[p(0)] = 0
# E[p(n)] = 1/2 E[p(n-2)] + 1/2 E[p(n+1)] for n >= 1

# TODO: adjust indexing to make most sense

# We mostly work in the field Q[phi], phi = (1 + sqrt(5)) / 2
from phinum import PhiNum, phi, sqrt5
from fractions import Fraction
from math import sqrt

# p(n) = Pr[P(n)]
def p(n):
    return (2 - phi) * (1 - (1 - phi) ** n)

assert p(0) == 0
assert p(-1) == 1
for i in range(-100, 100):
    assert p(i) == (p(i - 2) + p(i + 1)) / 2
for i in range(-1, 50):
    assert 0 <= float(p(i)) <= 1

def l(n):
    ansa = (4 - 2 * phi) + (-4 + 2 * phi) * (1 - phi) ** n + 2 * n
    return ansa

assert l(-1) == l(0) == 0
for i in range(-100, 100):
    assert l(i) == 1 + (l(i - 2) + l(i + 1)) / 2

# approximate versions, avoiding catastrophic cancellation with float(p(n))
def approx_p(n):
    return (3 - sqrt(5)) / 2 * (1 - ((1 - sqrt(5)) / 2) ** n)
def approx_l(n):
    # 1 - phi = - 1 / phi = (1 - sqrt(5)) / 2
    return 2 * ((3 - sqrt(5)) / 2 * (1 - ((1 - sqrt(5)) / 2) ** n) + n)


# p -> 2 - phi ~ 0.381966
# l -> 2 n + (4 - 2 phi) ~ 2 n + 0.763932
