# portfolio\app.py

from flask import Flask, render_template

app = Flask(__name__)

from routes.portfolio import portfolio
from routes.ocr import ocr

app.register_blueprint(portfolio)
app.register_blueprint(ocr)


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)