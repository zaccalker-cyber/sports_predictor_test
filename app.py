from database import create_database, fetch_data_from_database
from scraper import pull_data_from_api
from feature_engineering import extract_features, train_model
import sys

try:
    # 1. Create database
    create_database()

    # 2. Pull data from API and insert into database
    pull_data_from_api()

    # 3. fetch data from database
    df = fetch_data_from_database()
    print(df.head())

    # 4. Run feature extraction and model training
    X, y = extract_features(df)

    # 5. Train the model
    train_model(X, y)
    print("✓ Pipeline completed successfully")

except Exception as e:
    print(f"✗ Pipeline failed: {e}", file=sys.stderr)
    sys.exit(1)
