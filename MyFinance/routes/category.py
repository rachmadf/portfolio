from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
)

from services.category_service import (
    CategoryService,
)

from datetime import datetime

category_bp = Blueprint(
    "category",
    __name__,
    url_prefix="master/category"
)