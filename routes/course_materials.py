from flask import Blueprint
from flask import render_template

course_materials = Blueprint(
    "course_materials",
    __name__,
    url_prefix="/course_materials"
)


@course_materials.route("/", methods=["GET"])
def index():

    return render_template(
        "/course_materials/course_materials_home.html"
    )