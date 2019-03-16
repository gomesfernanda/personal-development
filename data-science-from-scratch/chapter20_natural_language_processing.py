import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
import requests
import re
from collections import defaultdict
import random

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

if __name__ == '__main__':

    data = [ ("big data", 100, 15), ("Hadoop", 95, 25), ("Python", 75, 50),
             ("R", 50, 40), ("machine learning", 80, 20), ("statistics", 20, 60),
             ("data science", 60, 70), ("analytics", 90, 3),
             ("team player", 85, 85), ("dynamic", 2, 90), ("synergies", 70, 0),
             ("actionable insights", 40, 30), ("think out of the box", 45, 10),
             ("self-starter", 30, 50), ("customer focus", 65, 15),
             ("thought leadership", 35, 35)]

    plot_resumes(data)

    document_list = get_document()

    run_bigram = 0
    run_trigram = 1

    if run_bigram == 1:
        bigram_transitions = get_bigrams_transitions(document_list)
        generated_document_bigram = generate_using_bigrams(bigram_transitions)
        print(generated_document_bigram)

    if run_trigram == 1:
        starts, trigram_transitions = get_trigrams_transitions(document_list)
        generated_document_trigram = generate_using_trigrams(starts, trigram_transitions)
        print(generated_document_trigram)
