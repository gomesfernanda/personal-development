from sklearn.naive_bayes import MultinomialNB, BernoulliNB
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import precision_score, recall_score, accuracy_score


####### On this file, we used the SMS Spam dataset available on: https://data.world/lylepratt/sms-spam

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

X_train, X_test, y_train, y_test = train_test_split(X, target, test_size=.4, random_state=42)

print("Using Multinomial Naive Bayes\n")

mnb = MultinomialNB()

y_pred_mnb = mnb.fit(X_train, y_train).predict(X_test)

accuracy_mnb = round(accuracy_score(y_test, y_pred_mnb), 4)
precision_mnb = round(precision_score(y_test, y_pred_mnb), 4)
recall_mnb = round(recall_score(y_test, y_pred_mnb), 4)

print("Accuracy:", accuracy_mnb)
print("Precision:", precision_mnb)
print("Recall:", recall_mnb)

print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")

print("Using Bernoulli Naive Bayes\n")

bnb = BernoulliNB()

y_pred_bnb = bnb.fit(X_train, y_train).predict(X_test)

accuracy_bnb = round(accuracy_score(y_test, y_pred_bnb), 4)
precision_bnb = round(precision_score(y_test, y_pred_bnb), 4)
recall_bnb = round(recall_score(y_test, y_pred_bnb), 4)

print("Accuracy:", accuracy_bnb)
print("Precision:", precision_bnb)
print("Recall:", recall_bnb)