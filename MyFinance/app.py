"""
==========================================================
MyFinance

Application Entry Point
==========================================================
"""

from datetime import datetime
from pathlib import Path

from flask import (
    Flask,
    render_template,
)

from config import Config

from routes.expense import expense_bp


# ==========================================================
# Helper Functions
# ==========================================================

def create_required_directories() -> None:
    """
    Create application directories if they do not exist.
    """

    directories = [

        Config.INSTANCE_DIR,

        Config.BASE_DIR / "logs",

    ]

    for directory in directories:

        Path(directory).mkdir(

            parents=True,

            exist_ok=True,

        )


# ==========================================================
# Application Factory
# ==========================================================

def create_app() -> Flask:
    """
    Create and configure Flask application.
    """

    create_required_directories()

    app = Flask(

        __name__,

        template_folder=Config.TEMPLATE_DIR,

        static_folder=Config.STATIC_DIR,

        instance_path=Config.INSTANCE_DIR,

    )

    # ======================================================
    # Configuration
    # ======================================================

    app.config.from_object(Config)

    # ======================================================
    # Register Blueprints
    # ======================================================

    app.register_blueprint(
        expense_bp
    )

    # ======================================================
    # Template Context
    # ======================================================

    @app.context_processor
    def inject_global_variables():

        return {

            "app_name": Config.APP_NAME,

            "app_version": Config.APP_VERSION,

            "current_year": datetime.now().year,

        }

    # ======================================================
    # Home Page
    # ======================================================

    @app.route("/")
    def index():

        return render_template(

            "index.html",
            # "expense/expense_add.html",

            # active_page="dashboard",

            # page_title="Dashboard",

        )

    # ======================================================
    # Error Pages
    # ======================================================

    @app.errorhandler(404)
    def page_not_found(e):

        return "404 Not Found",404

    @app.errorhandler(500)
    def internal_server_error(error):

        return "500 Not Found",500

    return app


# ==========================================================
# Application Instance
# ==========================================================

app = create_app()


# ==========================================================
# Run Application
# ==========================================================

if __name__ == "__main__":

    # print("\n========== REGISTERED ROUTES ==========")

    # for rule in app.url_map.iter_rules():
    #     print(f"{rule.endpoint:35} {rule}")

    # print("=======================================\n")

    app.run(

        host="127.0.0.1",

        port=5000,

        debug=Config.DEBUG,

    )