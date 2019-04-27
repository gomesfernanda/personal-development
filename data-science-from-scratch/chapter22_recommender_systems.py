from collections import Counter, defaultdict
from chapter04_linearalgebra import dot
import math

users_interests = [
    ["Hadoop", "Big Data", "HBase", "Java", "Spark", "Storm", "Cassandra"],
    ["NoSQL", "MongoDB", "Cassandra", "HBase", "Postgres"],
    ["Python", "scikit-learn", "scipy", "numpy", "statsmodels", "pandas"],
    ["R", "Python", "statistics", "regression", "probability"],
    ["machine learning", "regression", "decision trees", "libsvm"],
    ["Python", "R", "Java", "C++", "Haskell", "programming languages"],
    ["statistics", "probability", "mathematics", "theory"],
    ["machine learning", "scikit-learn", "Mahout", "neural networks"],
    ["neural networks", "deep learning", "Big Data", "artificial intelligence"],
    ["Hadoop", "Java", "MapReduce", "Big Data"],
    ["statistics", "R", "statsmodels"],
    ["C++", "deep learning", "artificial intelligence", "probability"],
    ["pandas", "R", "Python"],
    ["databases", "HBase", "Postgres", "MySQL", "MongoDB"],
    ["libsvm", "regression", "support vector machines"]
]


#####################
#                   #
#  MANUAL CURATION  #
#                   #
#####################

popular_interests = Counter(interest
                            for user_interests in users_interests
                            for interest in user_interests).most_common()

def most_popular_new_interests(user_interests, max_results=5):
    suggestions = [(interest, frequency)
                   for interest, frequency in popular_interests
                   if interest not in user_interests]
    return suggestions[:max_results]


########################################
#                                      #
#  USER-BASED COLLABORATIVE FILTERING  #
#                                      #
########################################

def cosine_similarity(v, w):
    return dot(v, w) / math.sqrt(dot(v, v) * dot(w, w))


def make_user_interest_vector(user_interests):
    """ given a list of interests, produce a vector whose ith element iss 1
    if unique_interests[i] is in the list, 0 otherwise """
    return [1 if interest in user_interests else 0
            for interest in unique_interests]

def most_similar_user_to(user_id):
    pairs = [(other_user_id, similarity)                            # find other
             for other_user_id, similarity in                       # users with
                enumerate(user_similarities[user_id])               # nonzero
             if user_id != other_user_id and similarity > 0]        # similarity
    return sorted(pairs,                                            # sort them
                  key=lambda pair: pair[-1],
                  reverse=True)          # most similar first

def user_based_suggestions(user_id, include_current_interests=False):
    # sum up the similarities
    suggestions = defaultdict(float)
    for other_user_id, similarity in most_similar_user_to(user_id):
        for interest in users_interests[other_user_id]:
            suggestions[interest] += similarity

    # convert them to a sorted list
    suggestions = sorted(suggestions.items(),
                         key=lambda pair: pair[1],
                         reverse=True)

    # and maybe exclude already-interests
    if include_current_interests:
        return suggestions
    else:
        return [(suggestion, weight) for suggestion, weight in suggestions if suggestion not in users_interests[user_id]]


########################################
#                                      #
#  ITEM-BASED COLLABORATIVE FILTERING  #
#                                      #
########################################


def most_similar_interests_to(interest_id):
    similarities = interest_similarities[interest_id]
    pairs = [(unique_interests[other_interest_id], similarity)
             for other_interest_id, similarity in enumerate(similarities)
             if interest_id != other_interest_id and similarity > 0]
    return sorted(pairs,
                  key=lambda pair: pair[1],
                  reverse=True)


def item_based_suggestions(user_id, include_current_interests=False):
    suggestions = defaultdict(float)
    user_interest_vector = user_interest_matrix[user_id]
    for interest_id, is_interested in enumerate(user_interest_vector):
        if is_interested == 1:
            similar_interests = most_similar_interests_to(interest_id)
            for interest, similarity in similar_interests:
                suggestions[interest] += similarity

    suggestions = sorted(suggestions.items(),
                         key=lambda pair: pair[1],
                         reverse=True)

    if include_current_interests:
        return suggestions
    else:
        return [(suggestion, weight)
                for suggestion, weight in suggestions
                if suggestion not in users_interests[user_id]]


if __name__ == '__main__':

    print("Let's recommend interests for user 0 according to...\n")
    # POPULARITY / MANUAL CURATION

    user_0_popularity_suggestion = users_interests[0]

    print("(A) Overall popularity:")
    for i, item in enumerate(user_0_popularity_suggestion):
        print(i+1,"-", item)

    unique_interests = sorted(list({ interest
                                     for user_interests in users_interests
                                     for interest in user_interests }))

    # USER-BASED COLLABORATIVE FILTERING

    user_interest_matrix = list(map(make_user_interest_vector, users_interests))

    user_similarities = [[round(cosine_similarity(interest_vector_i, interest_vector_j),4)
                          for interest_vector_j in user_interest_matrix]
                         for interest_vector_i in user_interest_matrix]

    user_0_user_suggestion = user_based_suggestions(0)

    print("\n(B) Users with common interests:")
    for i, item in enumerate(user_0_user_suggestion):
        print(i + 1, "-", item[0], "(", item[1], ")")

    # print(user_0_user_suggestion)

    # ITEM COLLABORATIVE FILTERING

    interest_user_matrix = [[user_interest_vector[j]
                             for user_interest_vector in user_interest_matrix]
                            for j, _ in enumerate(unique_interests)]

    interest_similarities = [[round(cosine_similarity(user_vector_i, user_vector_j),4)
                              for user_vector_j in interest_user_matrix]
                             for user_vector_i in interest_user_matrix]

    user_0_item_suggestion = item_based_suggestions(0)

    print("\n(C) Similar interests:")
    for i, item in enumerate(user_0_item_suggestion):
        print(i + 1, "-", item[0], "(", item[1], ")")

