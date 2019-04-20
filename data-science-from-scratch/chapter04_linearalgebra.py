from functools import partial, reduce
import math

###################
#                 #
#     VECTORS     #
#                 #
###################

def vector_add(v, w):
    """adds corresponding elements"""
    return [v_i + w_i for v_i, w_i in zip(v, w)]

def vector_subtract(v, w):
    """subtracts corresponding elements"""
    return [v_i - w_i for v_i, w_i in zip(v, w)]

def vector_sum(vectors):
    """sums all corresponding elements"""
    result = vectors[0]                         # start with the first vector
    for vector in vectors[1:]:                  # then loop over the others
        result = vector_add(result, vector)     # and add them to the result
    return result

# ANOTHER WAY OF WRITING ABOVE FUNCTION IS USING `REDUCE`:
def vector_sum(vectors):
    return reduce(vector_add, vectors)

# OR EVEN
vector_sum = partial(reduce, vector_add)

def scalar_multiply(c, v):
    """c is a number, v is a vector"""
    return [c * v_i for v_i in v]

def vector_mean(vectors):
    """compute the vector whose ith element is the mean of the
    ith elements of the input vectors"""
    n = len(vectors)
    return scalar_multiply(1/n, vector_sum(vectors))

def dot(v, w):
    """v_w * w_1 + v_2 * w_2 + ... + v_n * w_n"""
    return sum(v_i * w_i for v_i, w_i in zip(v, w))

def sum_of_squares(v):
    """v_w * v_1 + v_2 * v_2 + ... + v_n * v_n"""
    return dot(v, v)

def magnitude(v):
    return math.sqrt(sum_of_squares(v))

# Now we have the pieces to compute the distance between two vectors:
def squared_distances(v, w):
    """(v_1 - w_1) ** 2 + ... + (v_n - w_n) ** 2"""
    return sum_of_squares(vector_subtract(v, w))

def distance(v, w):
    return math.sqrt(squared_distances(v, w))

# Which is possibly clearer if we do:

def distance(v, w):
    return magnitude(vector_subtract(v, w))



###################
#                 #
#     MATRICES    #
#                 #
###################

# We will represent matrices as a lists of lists

A = [[1, 2, 3],     # A has 2 rows and 3 columns
     [4, 5, 6]]

B = [[1, 2],        # B has 3 rows and 2 columns
     [3, 4],
     [5, 6]]


def shape(A):
    num_rows = len(A)
    num_cols = len(A[0]) if A else 0      # number of elements in first row
    return num_rows, num_cols

def get_row(A, i):
    return A[i]     # A[i] is already the ith row

def get_column(A, j):
    return [A_i[j] for A_i in A]        # jth element of row A_i for each row A_i

def make_matrix(num_rows, num_cols, entry_fn):
    """returns a num_rows x num_cols matrix
    whose (i,j)-th entry is entry_fn(i, j)"""
    return [[entry_fn(i, j) for j in range(num_cols)]
            for i in range(num_rows)]

def is_diagonal(i, j):
    """1's on the 'diagonal', 0's everywhere else"""
    return 1 if i == j else 0

identify_matrix = make_matrix(5, 5, is_diagonal)