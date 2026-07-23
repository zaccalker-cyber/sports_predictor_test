import sqlite3
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "data" / "sports_events_test.db"

# Connect to the SQLite database and read the events table into a DataFrame
conn = sqlite3.connect(DB_PATH)

df = pd.read_sql_query(
    "SELECT * FROM events ORDER BY event_date, event_time",
    conn
)

conn.close()

# Keep track of team history for feature engineering
team_history = {}


def get_team_stats(team):

    games = team_history.get(team, [])

    if len(games) == 0:
        return {
            "wins": 0,
            "avg_for": 0,
            "avg_against": 0
        }

    last5 = games[-5:]

    return {
        "wins": sum(g["won"] for g in last5),
        "avg_for": sum(g["points_for"] for g in last5) / len(last5),
        "avg_against": sum(g["points_against"] for g in last5) / len(last5)
    }

feature_rows = []

def extract_features(df):
    for _, match in df.iterrows():

        home = match["home_team"]
        away = match["away_team"]

        home_stats = get_team_stats(home)
        away_stats = get_team_stats(away)

        feature_rows.append({

            "round": match["round"],

            "home_team": home,
            "away_team": away,

            "home_last5_wins": home_stats["wins"],
            "away_last5_wins": away_stats["wins"],

            "home_avg_points": home_stats["avg_for"],
            "away_avg_points": away_stats["avg_for"],

            "home_avg_against": home_stats["avg_against"],
            "away_avg_against": away_stats["avg_against"],

            "winner": match["winner"]

        })

        # AFTER creating the feature row, update history

        if home not in team_history:
            team_history[home] = []

        if away not in team_history:
            team_history[away] = []

        team_history[home].append({
            "points_for": match["home_score"],
            "points_against": match["away_score"],
            "won": 1 if match["winner"] == 1 else 0
        })

        team_history[away].append({
            "points_for": match["away_score"],
            "points_against": match["home_score"],
            "won": 1 if match["winner"] == 0 else 0
        })

    features = pd.DataFrame(feature_rows)

    # Remove rows where winner is NaN (incomplete games)
    features = features.dropna(subset=['winner'])
#features.to_csv("features.csv", index=False)
    # Prepare the features (X) and target variable (y)
    X = features[
        [
            "home_last5_wins",
            "away_last5_wins",
            "home_avg_points",
            "away_avg_points",
            "home_avg_against",
            "away_avg_against",
            "round"
        ]
    ]

    y = features["winner"]


    return X, y

# Split the dataset into training and testing sets
# split=int(len(features) * 0.8)
# X_train, X_test, y_train, y_test = X.iloc[:split], X.iloc[split:], y.iloc[:split], y.iloc[split:]

def train_model(X, y):
    # Train a Random Forest Classifier model
    from sklearn.ensemble import RandomForestClassifier

    model = RandomForestClassifier(
        n_estimators=300,
        random_state=42,
        max_depth=8
    )

    model.fit(X, y)

    # Save model
    import joblib
    joblib.dump(model, "models\\nrl_model.pkl")

# Evaluate the model's accuracy on the test set
#from sklearn.metrics import accuracy_score
# predictions = model.predict(X_test)

# accuracy = accuracy_score(y_test, predictions)

# print(f"Accuracy: {accuracy:.2%}")

# results = X_test.copy()

# results["Actual"] = y_test.values
# results["Prediction"] = predictions

# print(results.head(20))

# # View feature importance
# importance = (
#     pd.DataFrame({
#         "Feature": X.columns,
#         "Importance": model.feature_importances_
#     })
#     .sort_values("Importance", ascending=False)
# )

# print(importance)



#print(features.head())