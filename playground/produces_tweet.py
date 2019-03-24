import re
from collections import defaultdict
import random
import tweepy


def get_words(text):
    regex = r"[\w]+|[.,#!$%^&*;:{}=_'~]+|\B@[a-z0-9_-]+"
    document = []
    words = re.findall(regex, text)
    document.extend(words)
    return document


def get_tweets(username, number_of_tweets):
    """replace the credentials below with yours; you can get them on https://developer.twitter.com/en/apps/create"""
    consumer_key = "[CONSUMER_KEY]"
    consumer_secret = "[CONSUMER_SECRET]"
    access_token = "[ACCESS_TOKEN]"
    access_token_secret = "[ACCESS_TOKEN_SECRET]"

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    tweets_word_list = []

    for tweet in tweepy.Cursor(api.user_timeline, screen_name=username, tweet_mode='extended').items(number_of_tweets):
        words_in_tweet = get_words(tweet.full_text)
        tweets_word_list.extend(words_in_tweet)
    return tweets_word_list


def get_bigrams_transitions(document):
    bigrams = zip(document, document[1:])
    transitions = defaultdict(list)
    for prev, current in bigrams:
        transitions[prev].append(current)
    return transitions

def generate_using_bigrams(transitions):
    current = "."           # this means the next word will start a sequence
    result = []
    for _ in range(40):
        next_word_candidates = transitions[current]         # bigrams (current, )
        current = random.choice(next_word_candidates)       # choose one at random
        result.append(current)                              # append it to the results
    return " ".join(result)                                 # if "." we're done

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
    for _ in range(40):
        next_word_candidates = trigram_transitions[(prev, current)]
        next = random.choice(next_word_candidates)
        prev, current = current, next
        result.append(current)
    return " ".join(result)

if __name__ == '__main__':

    twitter_handle = "liamgallagher"
    num_past_tweets = 2000
    tweets = get_tweets(twitter_handle, num_past_tweets)
    print(tweets)

    run_bigram = 1
    run_trigram = 1

    if run_bigram == 1:
        bigram_transitions = get_bigrams_transitions(tweets)
        generated_document_bigram = generate_using_bigrams(bigram_transitions)
        print("\nBRIGRAM:")
        print(generated_document_bigram)

    if run_trigram == 1:
        starts, trigram_transitions = get_trigrams_transitions(tweets)
        generated_document_trigram = generate_using_trigrams(starts, trigram_transitions)
        print("\nTRIGRAM:")
        print(generated_document_trigram)
