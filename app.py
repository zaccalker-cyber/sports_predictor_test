from database import create_database, fetch_data_from_database
from scraper import pull_data_from_api
from feature_engineering import extract_features, train_model
from predict import predict_future_games
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

    # 6. Predict future games and create csv
    predict_future_games()

except Exception as e:
    print(f"✗ Pipeline failed: {e}", file=sys.stderr)
    sys.exit(1)

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request

import pandas as pd

app = FastAPI()

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
def home(request: Request):

    df = pd.read_csv("data/predictions.csv")

    predictions = df.to_dict(orient="records")

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "predictions": predictions
        }
    )
