# portfolio\app.py

from flask import Flask, render_template

app = Flask(__name__)

from routes.portfolio import portfolio
from routes.research_notes import research_notes

app.register_blueprint(portfolio)
app.register_blueprint(research_notes)


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)