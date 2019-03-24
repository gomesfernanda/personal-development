import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
import requests
import re
from collections import defaultdict, Counter
import random

##################
#                #
#   WORD CLOUD   #
#                #
##################

def plot_resumes(data):
    def text_size(total):
        """equals 8 if total is 0, 28 if total is 200"""
        return 8 + total / 200 * 20

    for word, job_popularity, resume_popularity in data:
        plt.text(job_popularity, resume_popularity, word, ha='center', va='center',
                 size=text_size(job_popularity + resume_popularity))

    plt.xlabel("Popularity on Job Postings")
    plt.ylabel("Popularity on Resumes")
    plt.axis([0, 100, 0, 100])
    plt.xticks([])
    plt.yticks([])
    plt.show()


###################
#                 #
#     N-GRAMS     #
#                 #
###################


def fix_unicode(text):
    return text.replace(u"\u2019", "'")

def get_document():
    url = "http://radar.oreilly.com/2010/06/what-is-data-science.html"
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'html5lib')

    content_ = soup.find("div", "article-body")
    regex = r"[\w']+|[\.]"

    document = []

    for paragraph in content_("p"):
        words = re.findall(regex, fix_unicode(paragraph.text))
        document.extend(words)

    return document

def get_bigrams_transitions(document):
    bigrams = zip(document, document[1:])
    transitions = defaultdict(list)
    for prev, current in bigrams:
        transitions[prev].append(current)
    return transitions

def generate_using_bigrams(transitions):
    current = "."           # this means the next word will start a sequence
    result = []
    while True:
        next_word_candidates = transitions[current]         # bigrams (current, )
        current = random.choice(next_word_candidates)       # choose one at random
        result.append(current)                              # append it to the results
        if current == ".": return " ".join(result)          # if "." we're done

def get_trigrams_transitions(document):
    trigrams = zip(document, document[1:], document[2:])
    trigrams_transitions = defaultdict(list)
    starts = []
    for prev, current, next in trigrams:
        if prev == ".":
            starts.append(current)
        trigrams_transitions[(prev, current)].append(next)
    return starts, trigrams_transitions

def generate_using_trigrams(starts, trigram_transitions):
    current = random.choice(starts)    # choose a random starting word
    prev = "."                         # and precede it with a '.'
    result = [current]
    while True:

        next_word_candidates = trigram_transitions[(prev, current)]
        next = random.choice(next_word_candidates)
        prev, current = current, next
        result.append(current)
        if current == ".":
            return " ".join(result)


###################
#                 #
#     GRAMMAR     #
#                 #
###################

def is_terminal(token):
    return token[0] != "_"

def expand(grammar, tokens):
    for i, token in enumerate(tokens):

        # skip over terminals
        if is_terminal(token): continue

        # if we get here, we found a non-terminal token
        # so we need to choose a replacement at random
        replacement = random.choice(grammar[token])

        if is_terminal(replacement):
            tokens[i] = replacement
        else:
            tokens = tokens[:i] + replacement.split() + tokens[(i+1):]

        # now call expand on the new list of tokens
        return expand(grammar, tokens)

    # if we get here we had all terminals and are done
    return " ".join(tokens)

def generate_sentence(grammar):
    return expand(grammar, ["_S"])

######################
#                    #
#   GIBBS SAMPLING   #
#                    #
######################

def roll_a_die():
    return random.choice([1, 2, 3, 4, 5, 6])

def direct_sample():
    d1 = roll_a_die()
    d2 = roll_a_die()
    return d1, d1 + d2

def random_y_given_x(x):
    """equally likely to be a x + 1, x + 2, x + 3, ... , x + 6"""
    return x + roll_a_die()

def random_x_given_y(y):
    if y <= 7:
        # if the total is 7 or less, the first die is equally likely to be
        # 1, 2, ..., (total - 1)
        return random.randrange(1, y)
    else:
        # if the total is 7 or more, the first die is equally likely to be
        # (total - 6), (total - 5), ..., 6
        return random.randrange(y - 6, 7)

def gibbs_sample(num_iters=100):
    x, y = 1, 2         # doesn't really matter
    for _ in range(num_iters):
        x = random_x_given_y(y)
        y = random_y_given_x(x)
    return x, y

def compare_samples(num_iters=100):
    counts = defaultdict(lambda: [0, 0])
    for _ in range(num_iters):
        counts[gibbs_sample()][0] += 1
        counts[direct_sample()][1] += 1
    return counts


######################
#                    #
#   TOPIC MODELING   #
#                    #
######################

def sample_from(weights):
    """ returns i with the probability weights[i] / sum(weights) """
    total = sum(weights)
    rnd = total * random.random()           # uniform between 0 and total
    for i, w in enumerate(weights):
        rnd -= w                            # return the smallest i such that
        if rnd <= 0: return i               # weights[0] + ... + weights[i] >= rnd

def p_topic_given_document(topic, d, alpha=0.1):
    """the fraction of words in document _d_
    that are assigned to _topic_ (plus some smoothing)"""

    return ((document_topic_counts[d][topic] + alpha) / (document_lengths[d] + K * alpha))

def p_word_given_topic(word, topic, beta=0.1):
    """the fraction of words assigned to _topic_
    that equal _word_ (plus some smoothing)"""
    return ((topic_word_counts[topic][word] + beta) / (topic_counts[topic] + W * beta))

def topic_weight(d, word, k):
    """given a document and a word in that document,
    return the weight for the kth topic"""
    return p_word_given_topic(word, k) * p_topic_given_document(k, d)

def choose_new_topic(d, word):
    return sample_from([topic_weight(d, word, k) for k in range(K)])


if __name__ == '__main__':

    data = [ ("big data", 100, 15), ("Hadoop", 95, 25), ("Python", 75, 50),
             ("R", 50, 40), ("machine learning", 80, 20), ("statistics", 20, 60),
             ("data science", 60, 70), ("analytics", 90, 3),
             ("team player", 85, 85), ("dynamic", 2, 90), ("synergies", 70, 0),
             ("actionable insights", 40, 30), ("think out of the box", 45, 10),
             ("self-starter", 30, 50), ("customer focus", 65, 15),
             ("thought leadership", 35, 35)]

    run_wordcloud = 0
    run_bigram = 0
    run_trigram = 0
    run_grammar = 0
    run_topic_modeling = 1

    if run_wordcloud == 1:
        plot_resumes(data)

    if run_bigram == 1:
        document_list = get_document()
        bigram_transitions = get_bigrams_transitions(document_list)
        generated_document_bigram = generate_using_bigrams(bigram_transitions)
        print(generated_document_bigram)

    if run_trigram == 1:
        document_list = get_document()
        starts, trigram_transitions = get_trigrams_transitions(document_list)
        generated_document_trigram = generate_using_trigrams(starts, trigram_transitions)
        print(generated_document_trigram)

    if run_grammar == 1:
        grammar = {
            "_S"  : ["_NP _VP"],
            "_NP" : ["_N",
                     "_A _NP _P _A _N"],
            "_VP" : ["_V _NP",
                     "_V _NP"],
            "_N"  : ["data science", "Python", "regression", "NLP", "matrix", "machine learning", "clustering", "Hadoop", "Tensorflow"],
            "_A"  : ["big", "linear", "logistic", "dense", "sparse", "accurate", "advanced"],
            "_P"  : ["about", "near", "with", "before"],
            "_V"  : ["learns", "trains", "tests", "is", "grows", "sets", "expands", "validate", "results"]
        }

        sentence = generate_sentence(grammar)
        print(sentence)

    if run_topic_modeling == 1:
        documents = [
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

        K = 4

        # a list of Counters, one for each document // how many times each topic is assigned to each document
        document_topic_counts = [Counter() for _ in documents]

        # a list of Counters, one for each topic // how many times each word is assigned to each topic
        topic_word_counts = [Counter() for _ in range(K)]

        # a list of numbers, one for each topic // the total number of words assigned to each topic
        topic_counts = [0 for _ in range(K)]

        # a list of numbers, one for each document // the total number of words contained in each document
        document_lengths = [len(d) for d in documents]

        # the number of distinct words
        distinct_words = set(word for document in documents for word in document)
        W = len(distinct_words)

        # the number of documents
        D = len(documents)

        random.seed(0)
        document_topics = [[random.randrange(K) for word in document] for document in documents]

        for d in range(D):
            for word, topic in zip(documents[d], document_topics[d]):
                document_topic_counts[d][topic] += 1
                topic_word_counts[topic][word] += 1
                topic_counts[topic] += 1

        for iter in range(1000):
            for d in range(D):
                for i, (tord, topic) in enumerate(zip(documents[d], document_topics[d])):

                    # remove this word / topic from the counts
                    # so that it doesn't influence the weights
                    document_topic_counts[d][topic] -= 1
                    topic_word_counts[topic][word] -= 1
                    topic_counts[topic] -= 1
                    document_lengths[d] -= 1

                    # choose a new topic based on the weights
                    new_topic = choose_new_topic(d, word)
                    document_topics[d][i] = new_topic

                    # and now add it back to the counts
                    document_topic_counts[d][new_topic] += 1
                    topic_word_counts[new_topic][word] += 1
                    topic_counts[new_topic] += 1
                    document_lengths[d] += 1

        for k, word_counts in enumerate(topic_word_counts):
            for word, count in word_counts.most_common():
                if count > 0: print(k, word, count)
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

        topic_names = ["Big Data and programming languages",
                       "databases",
                       "machine learning",
                       "statistics"]

        for document, topic_counts in zip(documents, document_topic_counts):
            current_topic_counts = topic_counts.most_common()
            for topic, count in current_topic_counts:
                if count > 0:
                    print(topic_names[topic], count)
            print()
