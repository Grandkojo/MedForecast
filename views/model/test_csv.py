import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
import joblib

data = pd.read_csv('views/model/Training.csv')

# print(dir(data))
columns = data.columns[ :-1]
columns = [column.replace('_', ' ') for column in columns]
print(columns)
X = data.iloc[:, :-1]
y = data['prognosis']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

model = DecisionTreeClassifier()
model.fit(X_train, y_train)

joblib.dump(model, 'decision_tree_model.pkl')