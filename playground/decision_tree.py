from sklearn import datasets, tree, ensemble
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score

digits = datasets.load_digits()
X = digits.data
Y = digits.target
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=.4, random_state=42)

########################
#                      #
#    DECISION TREES    #
#                      #
########################

print("\n\n======================== DECISION TREES ========================\n")

clf_dt = tree.DecisionTreeClassifier()

clf_fit_dt = clf_dt.fit(X_train, Y_train)
Y_pred_dt = clf_fit_dt.predict(X_test)

accuracy_dt = accuracy_score(Y_test, Y_pred_dt)
precision_dt = precision_score(Y_test, Y_pred_dt, average="macro")
recall_dt = recall_score(Y_test, Y_pred_dt, average="macro")

print("Accuracy using Decision Trees:", round(accuracy_dt, 4))
print("Precision using Decition Trees:", round(precision_dt,4))
print("Recall using Decision Trees", round(recall_dt,4))


########################
#                      #
#     RANDOM FOREST    #
#                      #
########################

print("\n\n======================== RANDOM FOREST ========================\n")

clf_rf = ensemble.RandomForestClassifier()
clf_fit_rf = clf_rf.fit(X_train, Y_train)
Y_pred_rf = clf_fit_rf.predict(X_test)

accuracy_rf = accuracy_score(Y_test, Y_pred_rf)
precision_rf = precision_score(Y_test, Y_pred_rf, average="macro")
recall_rf = recall_score(Y_test, Y_pred_rf, average="macro")

print("Accuracy using Random Forest:", round(accuracy_rf,4))
print("Precision using Random Forest:", round(precision_rf,4))
print("Recall using Random Forest:",round(recall_rf,4))

