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