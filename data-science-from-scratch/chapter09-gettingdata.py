import csv
import json

# egrep.py
import sys, re

# sys.argv is the list of command line arguments
# sys.argv[0] is the name of the program itself
# sys.argv[1] will be the regex specified at the command line

regex = sys.argv[1]

# for every line passed into the script
for line in sys.stdin:
    # if it matches the regex, write it to stdout
    if re.search(regex, line):
        sys.stdout.write(line)



# line_count.py
import sys

count = 0
for line in sys.stdin:
    count += 1

# print goes to stdout
print(count)



# most_common_words.py
import sys
from collections import Counter

# pass in number of wprds as first argument
try:
    num_words = int(sys.argv[1])
except:
    print("usage: most_common_words.py num_words")
    sys.exit(1)         # non-zero exit code indicates error

counter = Counter(word.lower()                          # lowercase words
                  for line in sys.stdin                 #
                  for word in line.strip().split()      # split on spaces
                  if word)                              # skip smpty "words"

for word, counter in counter.most_common(num_words):
    sys.stdout.write(str(count))
    sys.stdout.write("\t")
    sys.stdout.write(word)
    sys.stdout("\n")


###########################
#                         #
#      READING FILES      #
#                         #
###########################

# 'r' means read-only
file_for_reading = open('reading_file.txt', 'r')

# 'w' is write -- will destroy the file if it already exists!
file_for_writing = open('writing_file.txt', 'w')

# 'a' is append -- for adding to the end of the file
file_for_appending = open('appending_file.txt', 'a')

# don'' forget to close your files when you're done
file_for_writing.close()

# using a 'with' block, your files will close automatically:

with open('filename.txt', 'r') as f:
    data = function_that_gets_data_from_f(f)

# imagine you want to generate a histogram of domains from a file full of email addresses.

def get_domain(email_address):
    """split on '@' and return the last piece"""
    return email_address.lower().split('@')[-1]

with open('email_addresses.txt', 'r') as f:
    domain_counts = Counter(get_domain(line.strip())
                            for line in f
                            if "@" in line)

with open('colon_delimited_stock_prices.txt', 'rb') as f:
    reader = csv.DictReader(f, delimiter=',')
    for row in reader:
        date = row['date']
        symbol = row['symbol']
        closing_price = float(row['closing_price'])
        process(date, symbol, closing_price)


###########################
#                         #
#    SCRAPING THE WEB     #
#                         #
###########################

from bs4 import BeautifulSoup
import requests
html = requests.get('http://www.example.com').text
soup = BeautifulSoup(html, 'htmlparser')

first_paragraph = soup.find('p')        # or just soup.p
first_paragraph_text = soup.p.text
first_paragraph_words = soup.p.text.split()
first_paragraph_id = soup.p['id']
first_paragraph_id2 = soup.p.get('id')
all_paragraphs = soup.find_all('p')     # or just soup('p')
paragraphs_with_ids = [p for p in soup('p') if p.get('id')]

important_paragraphs = soup('p', {'class' : 'important'})
important_paragraphs2 = soup('p', 'important')
important_paragraphs3 = [p for p in soup('p')
                         if 'important' in p.get('class', [])]