import pandas as pd
from flask import Flask

app = Flask(__name__)


@app.route("/")
def home():
    return "Hello from Flask!"


@app.route("/data")
def data():
    pf = pd.read_csv("data/Telco-Customer-Churn.csv")
    return pf.to_html()


if __name__ == "__main__":
    app.run(debug=True)
