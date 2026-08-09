from flask import Blueprint
from flask import render_template

research_notes = Blueprint(
    "research_notes",
    __name__,
    url_prefix="/research_notes"
)


@research_notes.route("/", methods=["GET"])
def index():

    return render_template(
        "/research_notes/research_notes_home.html"
    )