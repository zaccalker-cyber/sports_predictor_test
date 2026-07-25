import sys
import unittest
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import feature_engineering
from feature_engineering import extract_features

class FeatureEngineeringTests(unittest.TestCase):
    def setUp(self):
        feature_engineering.team_history = {}
        feature_engineering.feature_rows = []
        

    def test_future_games_without_winner_are_ignored_in_history(self):
        df = pd.DataFrame([
            {
                "round": 1,
                "home_team": "A",
                "away_team": "B",
                "home_score": 1,
                "away_score": 0,
                "winner": 1,
            },
            {
                "round": 2,
                "home_team": "A",
                "away_team": "B",
                "home_score": 0,
                "away_score": 0,
                "winner": None,
            },
            {
                "round": 3,
                "home_team": "A",
                "away_team": "B",
                "home_score": 1,
                "away_score": 0,
                "winner": 1,
            },
        ])

        X, y = extract_features(df)

        self.assertEqual(len(X), 2)
        self.assertEqual(len(y), 2)
        self.assertEqual(y.iloc[0], 1)
        self.assertEqual(X.iloc[0]["home_last5_wins"], 0)
        self.assertEqual(X.iloc[1]["home_last5_wins"], 1)


if __name__ == "__main__":
    unittest.main()
    #print(feature_engineering.team_history.get("New Zealand Warriors", []))

