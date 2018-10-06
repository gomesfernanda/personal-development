import random
from collections import Counter

num_friends = []

for i in range(300):
    randint = random.randint(0,300)
    num_friends.append(randint)

print(num_friends)

def mean(x):
    return sum(x) / len(x)


def median(v):
    """finds the 'middle-most' value of v"""
    n = len(v)
    sorted_v = sorted(v)
    midpoint = n // 2

    if n % 2 == 1:
        # if odd, return the middle value
        return sorted_v[midpoint]
    else:
        # if even, return the average of the middle values
        lo = midpoint - 1
        hi = midpoint
        return (sorted_v[lo] + sorted_v[hi]) / 2

def quantile(x, p):
    """returns the p-th percentile value in x"""
    p_index = int(p * len(x))
    return sorted(x)[p_index]

def mode(x):
    """returns a list, might be more than one mode"""
    counts = Counter(x)
    max_count = max(counts.values())
    return [(x_i, count) for x_i in counts.keys()
            for count in counts.values()
            if count == max_count]

######################
#                    #
#     DISPERSION     #
#                    #
######################

def dot(v, w):
    """v_w * w_1 + v_2 * w_2 + ... + v_n * w_n"""
    return sum(v_i * w_i for v_i, w_i in zip(v, w))

def sum_of_squares(v):
    """v_w * v_1 + v_2 * v_2 + ... + v_n * v_n"""
    return dot(v, v)

def data_range(x):
    return max(x) - min(x)

def de_mean(x):
    """translate x by subtracting its mean(so the result has mean 0)"""
    x_bar = mean(x)
    return [x_i - x_bar for x_i in x]

def variance(x):
    """assumes x has at least two elements"""
    n = len(x)
    deviations = de_mean(x)
    return sum_of_squares(deviations) / (n-1)