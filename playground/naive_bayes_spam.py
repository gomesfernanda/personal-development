from sklearn.naive_bayes import MultinomialNB, BernoulliNB
import re
from sklearn.feature_extraction.text import CountVectorizer


def tokenize(message):
    message = message.lower()
    all_words = re.findall("[a-z0-9']+", message)
    return list(set(all_words))

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

file = "SMSSpamCollection.txt"
data_sms = get_data_sms(file)
target = []
features = []
for i in range(len(data_sms)):
    features.append(data_sms[i][0])
    target.append(data_sms[i][1])

vectorizer = CountVectorizer()
X = vectorizer.fit_transform(features)

mnb = MultinomialNB()

y_pred = mnb.fit(X, target).predict(X)

count = 0
true_positive = 0
pred_positives = 0
false_negative = 0

for i in range(len(y_pred)):
    if y_pred[i] != target[i]:
        count += 1
    # Let's count the numbers to calculate precision:
    if y_pred[i] == True:
        pred_positives += 1
        if y_pred[i] == target[i]:
            true_positive +=1
    # Let's count the numbers to calculate recall:
    if target[i] == True and y_pred[i] == False:
        false_negative += 1


fraction = count / len(y_pred)
accuracy = 1 - fraction
precision = true_positive / pred_positives
recall = true_positive / (true_positive + false_negative)
print("Accuracy:", accuracy)
print("Precision:", precision)
print("Recall:", recall)