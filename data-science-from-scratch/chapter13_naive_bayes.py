import re, glob, os
from collections import defaultdict, Counter
from math import log, exp
import random
from chapter11_machine_learning import split_data, accuracy, precision, recall




def tokenize(message):
    message = message.lower()
    all_words = re.findall("[a-z0-9']+", message)
    return set(all_words)

def count_words(training_set):
    """training set consist of pairs (message, is_spam)
    returns a dictionary whose keys are the words and values are two-element lists [spam_count, non_spam_count]"""
    counts = defaultdict(lambda: [0, 0])
    for message, is_spam in training_set:
        for word in tokenize(message):
            counts[word][0 if is_spam else 1] += 1
    return counts

def word_probabilities(counts, total_spams, total_non_spams, k=0.5):
    """turn the word_counts into a list of triplets
    w, p(w | spam), p(w | ~spam)"""
    return [(w,
             (spam + k) / (total_spams + 2 * k),
             (non_spam + k) / (total_non_spams + 2 * k))
            for w, (spam, non_spam) in counts.items()]

def spam_probabilities(word_probs, message):
    message_words = tokenize(message)
    log_prob_if_spam = log_prob_if_not_spam = 0.0

    # iterate through each word in our vocabulary
    for word, prob_if_spam, prob_if_not_spam in word_probs:
        # if *word* appears in the message
        if word in message_words:
            log_prob_if_spam += log(prob_if_spam)
            log_prob_if_not_spam += log(prob_if_not_spam)

        # if *word* DOESN'T appear in the message
        # add the log probability of not seeing it
        # which is log(1 - prob of seeing it)
        else:
            log_prob_if_spam  += log(1.0 - prob_if_spam)
            log_prob_if_not_spam += log(1.0 - prob_if_not_spam)

    prob_if_spam = exp(log_prob_if_spam)
    prob_if_not_spam = exp(log_prob_if_not_spam)

    return prob_if_spam / (prob_if_spam + prob_if_not_spam)


class NaiveBayesClassifier:

    def __init__(self, k=0.5):
        self.k = k
        self.word_probs = []

    def train(self, training_set):

        # count spam and non spam messages
        num_spams = len([is_spam
                         for message, is_spam in training_set
                         if is_spam])
        num_non_spams = len(training_set) - num_spams

        # run training data through our pipeline
        word_counts = count_words(training_set)
        self.word_probs = word_probabilities(word_counts,
                                             num_spams,
                                             num_non_spams,
                                             self.k)

    def classify(self, message):
        return spam_probabilities(self.word_probs, message)



def get_subject_data(path):

    data = []

    # regex for stripping out the leading "Subject:" and any spaces after it
    subject_regex = re.compile(r"^Subject:\s+")

    # glob.glob returns every filename that matches the wildcarded path
    for fn in glob.glob(path):
        is_spam = "ham" not in fn

        with open(fn,'r',encoding='ISO-8859-1') as file:
            for line in file:
                if line.startswith("Subject:"):
                    subject = subject_regex.sub("", line).strip()
                    data.append((subject, is_spam))
    return data

def p_spam_given_word(word_prob):
    """uses baye's theorem to compute p(spam | message contains word)"""

    # word_prob is one of the triplets produced by word_probabilities
    word, prob_if_spam, prob_if_no_spam = word_prob
    return prob_if_spam / (prob_if_spam + prob_if_no_spam)


def train_and_test_classifier(path):
    # we will first split the data into training and test sets
    data = get_subject_data(path)

    random.seed(0)
    train_data, test_data = split_data(data, 0.75)

    # create the "classifier" object
    classifier = NaiveBayesClassifier()
    classifier.train(train_data)

    # triplets (subject, actual is_spam, predicted spam probability)
    classified = [( subject, is_spam, classifier.classify(subject))
                  for subject, is_spam in test_data]

    # assume that spam_probability > 0.5 corresponds to spam prediction
    # and count the combinations of (actual is_spam, predicted is_spam)

    counts = Counter((is_spam, spam_probability > 0.5)
                     for _, is_spam, spam_probability in classified)
    print(counts)
    tp = counts[(True, True)]
    fp = counts[(True, False)]
    fn = counts[(False, True)]
    tn = counts[(False, False)]
    # sort by spam_probability from smallest to largest
    classified.sort(key=lambda row: row[2])

    # the highest predicted spam probabilities among the non-spams
    spammiest_hams = list(filter(lambda row: not row[1], classified))[-5:]

    # the lowest predicted spam probabilities among the actual spams
    hammiest_spams = list(filter(lambda row: row[1], classified))[:5]

    print("spammiest_hams", spammiest_hams)
    print("hammiest_spams", hammiest_spams)

    # let'' look at the spammiest words



    words = sorted(classifier.word_probs, key=p_spam_given_word)

    spammiest_words = words[-5:]
    hammiest_words = words[:5]
    print("spammiest words", spammiest_words)
    print("hammiest words", hammiest_words)

    print("accuracy: ", round(accuracy(tp, fp, fn, tn),2))
    print("precision: ", round(precision(tp, fp, fn, tn), 2))
    print("recall: ", round(recall(tp, fp, fn, tn), 2))

# path = os.getcwd() + "/*/*"
# train_and_test_classifier(path)


#### TOTALLY off-book, but I decided to play with SMS Spam dataset available at https://data.world/lylepratt/sms-spam

def get_data_sms(filename):
    data_sms = []
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            is_spam = "ham" not in line
            if is_spam == True:
                line = line.replace("spam	","")
            else:
                line = line.replace("ham	", "")
            data_sms.append((line.rstrip(), is_spam))
    return data_sms

def train_and_test_classifier_sms(data_file):
    # we will first split the data into training and test sets
    data = data_file

    random.seed(0)
    train_data, test_data = split_data(data, 0.75)

    # create the "classifier" object
    classifier = NaiveBayesClassifier()
    classifier.train(train_data)

    # triplets (subject, actual is_spam, predicted spam probability)
    classified = [( subject, is_spam, classifier.classify(subject))
                  for subject, is_spam in test_data]

    # assume that spam_probability > 0.5 corresponds to spam prediction
    # and count the combinations of (actual is_spam, predicted is_spam)

    counts = Counter((is_spam, spam_probability > 0.5)
                     for _, is_spam, spam_probability in classified)
    print(counts)
    tp = counts[(True, True)]
    fp = counts[(True, False)]
    fn = counts[(False, True)]
    tn = counts[(False, False)]

    # sort by spam_probability from smallest to largest
    classified.sort(key=lambda row: row[2])

    # the highest predicted spam probabilities among the non-spams
    spammiest_hams = list(filter(lambda row: not row[1], classified))[-5:]

    # the lowest predicted spam probabilities among the actual spams
    hammiest_spams = list(filter(lambda row: row[1], classified))[:5]

    print("spammiest_hams", spammiest_hams)
    print("hammiest_spams", hammiest_spams)

    # let's look at the spammiest words
    words = sorted(classifier.word_probs, key=p_spam_given_word)

    spammiest_words = words[-5:]
    hammiest_words = words[:5]
    print("spammiest words", spammiest_words)
    print("hammiest words", hammiest_words)

    print("accuracy: ", round(accuracy(tp, fp, fn, tn),2))
    print("precision: ", round(precision(tp, fp, fn, tn), 2))
    print("recall: ", round(recall(tp, fp, fn, tn), 2))


file = "SMSSpamCollection.txt"
data_sms = get_data_sms(file)
train_and_test_classifier_sms(data_sms)