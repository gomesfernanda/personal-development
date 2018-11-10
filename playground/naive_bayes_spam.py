from sklearn.naive_bayes import MultinomialNB, BernoulliNB
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import precision_score, recall_score, accuracy_score


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

mnb = MultinomialNB()

y_pred = mnb.fit(X_train, y_train).predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)

print("Accuracy:", accuracy)
print("Precision:", precision)
print("Recall:", recall)