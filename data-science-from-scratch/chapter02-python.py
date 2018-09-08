##################
#                #
#     LAMBDA     #
#                #
##################

def double(x):
    return x * 2

def apply_to_one(f):
    return f(1)

my_double = double
x = apply_to_one(my_double)

print(x)

y = apply_to_one(lambda x: x + 4)

print(y)

##################
#                #
#     LISTS      #
#                #
##################

# It's convenient to unpack lists if you know how many elements they contain:
a = [1, 2]
x, y = a
print(x)
print(y)

# You can use underscore if you want to throw away an element; in this example, I'm throwing the first element away.

_, y = [1, 2]
print(y)

##################
#                #
#  DICTIONARIES  #
#                #
##################

### There are many ways to count the words in a document


docstring = """One morning, when Gregor Samsa woke from troubled dreams, he found himself transformed in his bed
            into a horrible vermin. He lay on his armour-like back, and if he lifted his head a little he could
            see his brown belly, slightly domed and divided by arches into stiff sections."""
document = docstring.split()

# WAY 1:

word_counts = {}
for word in document:
    if word in word_counts:
        word_counts[word] += 1
    else:
        word_counts[word] = 1

print(word_counts)

# WAY 2:

word_counts = {}
for word in document:
    previous_count = word_counts.get(word, 0)
    word_counts[word] = previous_count + 1

print(word_counts)

# WAY 3: USING defaultdict

from collections import defaultdict

word_counts = defaultdict(int)
for word in document:
    word_counts[word] += 1

print(word_counts)

# WAY 4: USING Counter

from collections import Counter

word_counts = Counter(document)
print(word_counts)

## A Counter instance has `most_common` method that is frquently useful; let's see the first 10 most common words in the document

for word, count in word_counts.most_common(10):
    print(word, count)

########################
#                      #
#  LIST COMPREHENSION  #
#                      #
########################

even_numbers = [x for x in range(10) if x % 2 ==0]
print(even_numbers)

squares = [x * x for x in range(5)]
print(squares)

even_squares = [x * x for x in even_numbers]
print(even_squares)

# If you don't need the value from the list, it'' conventional to use an underscore as the variable

zeroes = [0 for _ in even_numbers]
print(zeroes)

# Multiple 'for's

pairs = [(x, y)
         for x in range(10)
         for y in range(10)]

print(pairs)

########################
#                      #
#   FUNCTIONAL TOOLS   #
#                      #
########################

from functools import partial, reduce

def double(x):
    return x * 2

xs = [1, 2, 3, 4]
twice_xs = [double(x) for x in xs]       # [2, 4, 6, 8]
twice_xs = map(double, xs)               # same as above
list_doubler = partial(map, double)      # *function* that doubles a list
twice_xs = list_doubler(xs)

# You can use `map` with multiple argument function

def multiply(x, y) : return x * y

products = map(multiply, [1, 2], [4, 5])

# FILTER does the work of a list comprehension`if`

def is_even(x):
    return x % 2 == 0

x_evens = [x for x in xs if is_even(x)]   # [2, 4]
x_evens = filter(is_even, xs)             # same as above
list_evener = partial(filter, is_even)    # *function* that filters a list
x_evens = list_evener(xs)                 # again, [2, 4]

# REDUCE combine the first two elements of a list, then that result with the thirst, and so on, producing a single result:

x_product = reduce(multiply, xs)            # = 1 * 2 * 3 * 4 = 24
list_product = partial(reduce, multiply)    # *function* that reduces a list
x_product  = list_product(xs)               # again = 24

########################
#                      #
#       ENUMERATE      #
#                      #
########################


documents = ["doc 1", "doc 2", "doc n"]

# NOT PYTHONIC
for i in range(len(documents)):
    document  = documents[i]
    # do_something_with(i, document)

# ALSO NOT PYTHONIC
i = 0
for document in documents:
    # do_something_with(i, document)
    i += 1

# PYTHONIC
for i, document in enumerate(documents):
    # do_something_with(i, document
    i



#########################
#                       #
#   ZIP AND UNPACKING   #
#                       #
#########################

# zip transforms multiple lists into a single list of tuples of corresponding elements:

list1 = ['a', 'b', 'c']
list2 = [1, 2, 3]
ziplists = zip(list1, list2)

# to "unzip"
pairs = [('a', 1), ('b', 2), ('c', 3)]
letters, numbers = zip(*pairs)