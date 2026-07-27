import pandas as pd
import joblib

future_games_features = pd.read_csv("data\\features.csv")
future_games_features = future_games_features[future_games_features["winner"].isna()]
print(future_games_features)

future_games_features_x = future_games_features.drop(columns=["winner", "home_team", "away_team"])

model = joblib.load("model\\nrl_model.pkl")
prediction = model.predict(future_games_features_x)
probability = model.predict_proba(future_games_features_x)
print(f"Data type of prediction: {type(probability)}")

j = 0

for i in future_games_features.index:
    outcome = {}
    home_team = future_games_features.loc[i, "home_team"]
    away_team = future_games_features.loc[i, "away_team"]
    outcome[j] = "Home Win" if prediction[j] == 1 else "Away Win" if prediction[j] == 0 else "Draw"
    print(f"Index: {i}, Home Team: {home_team}, Away Team: {away_team}, Prediction: {outcome[j]}, Home Probability: {(probability[j][0]) * 100:.2f}%, Away Probability: {(probability[j][1]) * 100:.2f}%")
    j += 1


print(range(len(prediction)))
#print(probability)