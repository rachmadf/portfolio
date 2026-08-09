from flask import Blueprint
from flask import render_template

portfolio = Blueprint(
    "portfolio",
    __name__,
    url_prefix="/portfolio"
)


@portfolio.route("/", methods=["GET"])
def index():

    return render_template(
        "/portfolio/index.html"
    )