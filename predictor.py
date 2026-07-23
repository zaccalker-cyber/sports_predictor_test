import sqlite3
import pandas as pd
from sklearn.preprocessing import LabelEncoder

# Connect to the SQLite database and read the events table into a DataFrame
conn = sqlite3.connect("sports_events.db")

df = pd.read_sql_query(
    "SELECT * FROM events ORDER BY event_date",
    conn
)

conn.close()

# Encode categorical variables (home_team and away_team) using LabelEncoder
encoder = LabelEncoder()

all_teams = pd.concat([
    df['home_team'],
    df['away_team']
])

encoder.fit(all_teams)

df["home_team"] = encoder.transform(df["home_team"])
df["away_team"] = encoder.transform(df["away_team"])

# Prepare the features (X) and target variable (y)
X = df[
    [
        "home_team",
        "away_team",
        "round"
    ]
]

y = df["winner"]

# Split the dataset into training and testing sets
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# Train a Random Forest Classifier model
from sklearn.ensemble import RandomForestClassifier

model = RandomForestClassifier(
    n_estimators=200,
    random_state=42
)

model.fit(X_train, y_train)

# Evaluate the model's accuracy on the test set
from sklearn.metrics import accuracy_score

predictions = model.predict(X_test)

accuracy = accuracy_score(y_test, predictions)

print(f"Accuracy: {accuracy:.2%}")

game = pd.DataFrame({
    "home_team": [7],
    "away_team": [11],
    "round": [18]
})

prediction = model.predict(game)

print(f"Prediction: {prediction[0]}")