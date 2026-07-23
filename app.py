from database import create_database, fetch_data_from_database
from scraper import pull_data_from_api
from feature_engineering import extract_features, train_model
import sys

try:
    # 1. Create database
    # create_database()

    # 2. Pull data from API and insert into database
    # pull_data_from_api()

    # fetch data from database and perform feature extraction
    df = fetch_data_from_database()
    print(df.head())

    # 3. Run feature extraction and model training
    X, y = extract_features(df)

    # X = features[
    #     [
    #         "home_last5_wins",
    #         "away_last5_wins",
    #         "home_avg_points",
    #         "away_avg_points",
    #         "home_avg_against",
    #         "away_avg_against",
    #         "round"
    #     ]
    # ]
    # y = features["winner"]

    train_model(X, y)
    print("✓ Pipeline completed successfully")
    
except Exception as e:
    print(f"✗ Pipeline failed: {e}", file=sys.stderr)
    sys.exit(1)
