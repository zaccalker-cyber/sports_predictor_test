from database import create_database
from scraper import pull_data_from_api
from feature_engineering import extract_features, train_model

# 1. Create database
create_database()

# 2. Pull data from API and insert into database
pull_data_from_api()

# 3. Run feature extraction and model training

# Assuming you have a DataFrame `df` with the event data
features = extract_features()
train_model(features)