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

# THE BEST WAY TO DO IT

from collections import defaultdict

word_counts = defaultdict(int)
for word in document:
    word_counts[word] += 1

print(dict(word_counts))