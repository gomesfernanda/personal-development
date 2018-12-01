import math
from collections import Counter, defaultdict
from functools import partial

def entropy(class_probabilities):
    """given a list of class probabilities, compute the entropy"""
    return sum(-p * math.log(p, 2)
               for p in class_probabilities
               if p)                # ignore zero probabilities

def class_probabilities(labels):
    total_count = len(labels)
    return [count / total_count for count in Counter(labels).values()]

def data_entropy(labeled_data):
    labels = [label for _, label in labeled_data]
    probabilities = class_probabilities(labels)
    return entropy(probabilities)

def partition_entropy(subsets):
    """find the entropy from this partition of data into subsets
    subsets is a list of lists of labaled data"""

    total_count = sum(len(subset) for subset in subsets)
    return sum( data_entropy(subset) * len(subset) / total_count
                for subset in subsets)

def partition_by(inputs, attribute):
    """each input is a pair of (attribute_dict, label).
    returns a dict : attribute_value -> inputs"""
    groups = defaultdict(list)
    for input in inputs:
        key = input[0][attribute]           # get the value of the specified attribute
        groups[key].append(input)           # then add this input to the correct list
    return groups

def partition_entropy_by(inputs, attribute):
    """computes the entropy corresponding to the given partition"""
    partitions = partition_by(inputs, attribute)
    return partition_entropy(partitions.values())

def classify(tree, input):
    """classify the input using the given decision tree"""

    # if this is a leaf node, return its value
    if tree in [True, False]:
        return tree
    # otherwise this tree consists of an attribute to split on
    # and a dictionary whose keys are values of that attribute
    # and whose values of are subtrees to consider next
    attribute, subtree_dict = tree

    subtree_key = input.get(attribute)         # None if input is missing attribute
    if subtree_key not in subtree_dict:
        subtree_key = None

    subtree = subtree_dict[subtree_key]
    return classify(subtree, input)

def build_tree_id3(inputs, split_candidates=None):

    # if this is our first oass,
    # all keys of the first input are split candidates

    if split_candidates is None:
        split_candidates = inputs[0][0].keys()

    # count Trues and Falses in the inputs
    num_inputs = len(inputs)
    num_trues = len([label for item, label in inputs if label])
    num_falses = num_inputs - num_trues

    if num_trues == 0: return False
    if num_falses == 0: return True

    if not split_candidates:
        return num_trues >= num_falses

    # otherwise, split on the best attribute
    best_attribute = min(split_candidates, key=partial(partition_entropy_by, inputs))

    partitions = partition_by(inputs, best_attribute)
    new_candidates = [a for a in split_candidates
                      if a != best_attribute]

    # recursively building subtrees

    subtrees = { attribute_value : build_tree_id3(subset, new_candidates)
                for attribute_value, subset in partitions.items()}

    subtrees[None] = num_trues >= num_falses

    return (best_attribute, subtrees)

if __name__ == "__main__":

    inputs = [
        ({'level':'Senior','lang':'Java','tweets':'no','phd':'no'},   False),
        ({'level':'Senior','lang':'Java','tweets':'no','phd':'yes'},  False),
        ({'level':'Mid','lang':'Python','tweets':'no','phd':'no'},     True),
        ({'level':'Junior','lang':'Python','tweets':'no','phd':'no'},  True),
        ({'level':'Junior','lang':'R','tweets':'yes','phd':'no'},      True),
        ({'level':'Junior','lang':'R','tweets':'yes','phd':'yes'},    False),
        ({'level':'Mid','lang':'R','tweets':'yes','phd':'yes'},        True),
        ({'level':'Senior','lang':'Python','tweets':'no','phd':'no'}, False),
        ({'level':'Senior','lang':'R','tweets':'yes','phd':'no'},      True),
        ({'level':'Junior','lang':'Python','tweets':'yes','phd':'no'}, True),
        ({'level':'Senior','lang':'Python','tweets':'yes','phd':'yes'},True),
        ({'level':'Mid','lang':'Python','tweets':'no','phd':'yes'},    True),
        ({'level':'Mid','lang':'Java','tweets':'yes','phd':'no'},      True),
        ({'level':'Junior','lang':'Python','tweets':'no','phd':'yes'},False)
    ]

    # Finding the partition entropy for the whole dataset:

    print("## Finding the partition entropy for the whole dataset:")

    for key in ['level', 'lang', 'tweets', 'phd']:
        print(key, partition_entropy_by(inputs, key))

    print("\n\n## Finding the partition entropy for the seniority level Senior:")
    senior_inputs = [(input, label) for input, label in inputs if input['level'] == "Senior"]

    for key in ['lang', 'tweets', 'phd']:
        print(key, partition_entropy_by(senior_inputs, key))

    print("\n\n## Finding the partition entropy for the seniority level Junior:")
    junior_inputs = [(input, label) for input, label in inputs if input['level'] == "Junior"]

    for key in ['lang', 'tweets', 'phd']:
        print(key, partition_entropy_by(junior_inputs, key))

    # BUILDING THE TREE FROM OUR TRAINING DATA

    tree = build_tree_id3(inputs)
    print("\n\n## BUILDING THE TREE FROM OUR TRAINING DATA")
    print(tree)

    # TESTING OUR MODEL

    print("\n\n## TESTING OUR MODEL")

    candidate_1 = {'level': 'Junior',
                    'lang': 'Java',
                    'tweets': 'yes',
                    'phd': 'no'}
    print("Candidate 1: ", candidate_1)
    print("Should we hire candidate 1?", classify(tree, candidate_1))

    candidate_2 = {'level': 'Junior',
                    'lang': 'Java',
                    'tweets': 'yes',
                    'phd': 'yes'}

    print("\nCandidate 2: ", candidate_2)
    print("Should we hire candidate 2?", classify(tree, candidate_2))

    candidate_3 = {'level' : 'Intern'}

    print("\nCandidate 3: ", candidate_3)
    print("Should we hire candidate 3?", classify(tree, candidate_3))

    candidate_4 = {'level': 'Senior'}

    print("\nCandidate 4: ", candidate_4)
    print("Should we hire candidate 4?", classify(tree, candidate_4))
