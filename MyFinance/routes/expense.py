"""
==========================================================
MyFinance
Expense Routes
Expense Blueprint

Responsibilities
----------------
- HTTP routing
- Call ExpenseService
- Render templates
- Redirect
- Flash messages

No SQL.
No business logic.
==========================================================
"""

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    jsonify
)

from services.expense_service import (ExpenseService)
from services.category_service import (CategoryService)
from services.store_service import (StoreService)

from datetime import datetime

expense_bp = Blueprint(

    "expense",

    __name__,

    url_prefix="/expense",

)


# ==========================================================
# Add Expense
# ==========================================================

@expense_bp.route("/add",methods=["GET", "POST"],)
def add_expense():

    if request.method == "POST":
        # print("========== FORM ==========")
        # print(request.form)
        # print(request.form.to_dict())
        # print("==========================")
        try:
            
            result = ExpenseService.save_expense(
                request.form
            )

            if result.success:

                flash(
                    result.message,
                    "success",
                )

                return redirect(

                    url_for(
                        "expense.add_expense"
                    )

                )

            flash(
                result.message,
                "warning",
            )

        except Exception as ex:

            flash(
                str(ex),
                "danger",
            )

    dropdown = ExpenseService.load_expense_form()

    return render_template(

        "expense/expense_add.html",

        active_page="expense",

        page_title="Add Expense",

        stores=dropdown["stores"],

        expense_categories=dropdown["categories"],

        payment_methods=dropdown["payment_methods"],

    )


# ==========================================================
# Edit Expense
# ==========================================================

@expense_bp.route("/edit/<int:transaction_id>",methods=["GET", "POST"],)
def edit_expense(
    transaction_id: int,
):

    if request.method == "POST":

        try:

            result = ExpenseService.update_expense(

                transaction_id,

                request.form,

            )

            flash(
                result.message,
                "success",
            )

            return redirect(

                url_for(
                    "expense.edit_expense",
                    transaction_id=transaction_id,
                )

            )

        except Exception as ex:

            flash(
                str(ex),
                "danger",
            )

    expense = ExpenseService.get_expense(
        transaction_id
    )

    if expense is None:

        flash(
            "Expense transaction not found.",
            "warning",
        )

        return redirect(

            url_for(
                "expense.add_expense"
            )

        )

    dropdown = ExpenseService.load_expense_form()

    return render_template(

        "expense/expense_add.html",

        active_page="expense",

        page_title="Edit Expense",

        expense=expense,

        stores=dropdown["stores"],

        categories=dropdown["categories"],

        payment_methods=dropdown["payment_methods"],

    )


# ==========================================================
# Delete Expense
# ==========================================================

@expense_bp.route(
    "/delete/<int:transaction_id>",
    methods=["POST"],
)
def delete_expense(
    transaction_id: int,
):

    try:

        result = ExpenseService.delete_expense(
            transaction_id
        )

        if result.success:

            flash(
                result.message,
                "success",
            )

        else:

            flash(
                result.message,
                "warning",
            )

    except Exception as ex:

        flash(
            str(ex),
            "danger",
        )

    return redirect(

        url_for(
            "expense.add_expense"
        )

    )


# ==========================================================
# View Expense
# ==========================================================

@expense_bp.route("/view/<int:transaction_id>")
def view_expense(transaction_id: int,):

    expense = ExpenseService.get_expense(
        transaction_id
    )

    if expense is None:

        flash(
            "Expense transaction not found.",
            "warning",
        )

        return redirect(

            url_for(
                "expense.add_expense"
            )

        )

    return render_template(

        "expense/expense_view.html",

        active_page="expense",

        page_title="Expense Detail",

        expense=expense,

    )

# ==========================================================
# Report: Expense Monthly
# ==========================================================
@expense_bp.route("/expense_monthly_report")
def view_monthly_report():
    
    report_filter = ExpenseService.get_report_filter()

    return render_template(
        "expense/report_expense_monthly.html",
        **report_filter
        
    )

# ==========================================================
# API : Available Months by Year
# ==========================================================
@expense_bp.route("/api/expense/months/<int:year>")
def get_available_months(year):

    months = ExpenseService.get_available_months(year)

    return jsonify(months)


# ========================================================
# API : Generate Report Based on Selected Year and Month
# ========================================================
@expense_bp.route("/report/expense/monthly")
def expense_monthly():

    year = request.args.get(
        "year",
        type=int,
        default=datetime.now().year
    )

    month = request.args.get(
        "month",
        type=int,
        default=datetime.now().month
    )

    report = ExpenseService.get_monthly_report(
        year,
        month
    )

    # print("DEBUG: year = ", year)
    # print("DEBUG: month = ", month)

    return render_template(
        "expense/report_expense_monthly.html",

        years=report["years"],
        months=report["months"],

        selected_year=year,
        selected_month=month,

        total_expense=report["total_expense"],
        highest_category=report["highest_category"],
        highest_category_total=report["highest_category_total"],
        highest_transaction_store=report["highest_transaction_store"],
        highest_transaction_amount=report["highest_transaction_amount"],

        category_summary=report["category_summary"],
        daily_trend=report["daily_trend"],
        transactions=report["transactions"]
    )

# ========================================================
# API : Get item_name base on selected category id
# ========================================================
@expense_bp.route("/api/items/<int:category_id>", methods=["GET"])
def get_items_by_category(category_id):
    """
    Return previous expense items for the specified category.
    """

    try:
        items = ExpenseService.get_items_by_category(category_id)

        return jsonify({
            "success": True,
            "data": items
        }), 200

    except Exception as ex:
        return jsonify({
            "success": False,
            "message": str(ex)
        }), 500

# ==========================================================
# Expense Plan
# ==========================================================
@expense_bp.route("/plan",methods=["GET", "POST"],)
def expense_plan():

    # KPI Card debug
    monthly_budget = 3000000
    current_expense = 1363000
    remaining_budget = monthly_budget - current_expense
    previous_month = 3234500
    comparison = previous_month - current_expense

    categories = CategoryService.get_all()
    stores = StoreService.get_all()

    return render_template(
        "expense/expense_plan.html",
        monthly_budget=monthly_budget,
        remaining_budget=remaining_budget,
        previous_month=previous_month,
        comparison=comparison,

        page_title="Expense Planning",
        page_subtitle="Plan your monthly expenses and compare them with previous purchases.",
        categories=categories,
        stores=stores,

    )

# ======================================================
# Get Available Items
# ======================================================

@expense_bp.route("/expense-plan/available-items",methods=["GET"])
def get_available_items():

    category_id = request.args.get(
        "category_id",
        type=int
    )

    store_id = request.args.get(
        "store_id",
        type=int
    )

    keyword = request.args.get(
        "keyword",
        default="",
        type=str
    ).strip()

    items = ExpenseService.get_available_items(
        category_id=category_id,
        store_id=store_id,
        keyword=keyword
    )

    return jsonify(items)

# debug
# print("expense.py loaded")