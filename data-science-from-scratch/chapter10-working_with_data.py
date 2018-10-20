import math
import matplotlib.pyplot as plt
from collections import Counter
import random
from chapter06_probability import inverse_normal_cdf

###########################
#                         #
#   EXPLORING YOUR DATA   #
#                         #
###########################

def bucketize(point, bucket_size):
    """floor the point to the next lower multiple of bucket_size"""
    return bucket_size * math.floor(point / bucket_size)

def make_histogram(points, bucket_size):
    """buckets the points and counts how many in each bucket"""
    return Counter(bucketize(point, bucket_size) for point in points)

def plot_histogram(points, bucket_size, title=""):
    histogram = make_histogram(points, bucket_size)
    plt.bar(list(histogram.keys()), list(histogram.values()), width=bucket_size)
    plt.title(title)
    plt.show()

def compare_two_distributions():

    random.seed(0)

    uniform = [random.randrange(-100,101) for _ in range(200)]
    normal = [57 * inverse_normal_cdf(random.random())
              for _ in range(200)]

    plot_histogram(uniform, 10, "Uniform Histogram")
    plot_histogram(normal, 10, "Normal Histogram")

def random_normal():
    """returns a random draw from a standard normal distribution"""
    return inverse_normal_cdf(random.random())

xs = [random_normal() for _ in range(1000)]
ys1 = [ x + random_normal() / 2 for x in xs]
ys2 = [ -x + random_normal() / 2 for x in xs]

plt.scatter(xs, ys1, marker='.', color='black', label="ys1")
plt.scatter(xs, ys2, marker='.', color='gray', label="ys2")
plt.xlabel("xs")
plt.ylabel("ys")
plt.legend(loc=9)
plt.title("Very different joint distributions")
plt.show()