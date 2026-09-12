from flask import Blueprint
from flask import render_template

about = Blueprint(
    "about",
    __name__,
    url_prefix="/about"
)


@about.route("/", methods=["GET"])
def index():

    return render_template(
        "about/about_me.html"
    )