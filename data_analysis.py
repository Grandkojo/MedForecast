import pandas as pd
import numpy as np
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split
import pickle



df = pd.read_csv('notebook/Training.csv')


# Split the dataset into features and target
X = df.iloc[:, :-1]  # All columns except the last one
y = df.iloc[:, -1]   # The last column (prognosis)

# Split into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a Gradient Boosting Classifier
model = GradientBoostingClassifier()
model.fit(X_train, y_train)

# Get feature importances
importances = model.feature_importances_
indices = np.argsort(importances)[::-1]

# Print the top 10 important features
top_features = X.columns[indices[:20]].tolist()
print("Top 10 features:", top_features)


