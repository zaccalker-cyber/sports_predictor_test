import pandas as pd
import joblib

# Read features from csv and prepare for prediction
future_games_features = pd.read_csv("data\\features.csv")
future_games_features = future_games_features[future_games_features["winner"].isna()]
future_games_features_x = future_games_features.drop(columns=["winner", "home_team", "away_team"])

# Load model and make predictions
model = joblib.load("model\\nrl_model.pkl")
prediction = model.predict(future_games_features_x)
probability = model.predict_proba(future_games_features_x)
print(f"Probability: {probability}")
predicted_winner_series = future_games_features.reset_index()

# Add predicted winner and probailities to the DataFrame
j = 0
for i in predicted_winner_series.index:
    predicted_winner_series.loc[i, "predicted_winner"] = prediction[j]
    predicted_winner_series.loc[i, "home_probability"] = probability[j][0]
    predicted_winner_series.loc[i, "away_probability"] = probability[j][1]
    j += 1
predicted_winner_series.drop(columns=["winner", "index"], inplace=True)
predicted_winner_series.to_csv("data\\predictions.csv", index=False)
