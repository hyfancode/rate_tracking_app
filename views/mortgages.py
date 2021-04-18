from flask import Blueprint, render_template
from datetime import datetime
from models.mortgage import Mortgage
from models.user.decorator import requires_login


mortgage_blueprint = Blueprint("mortgages", __name__)  # file name


@mortgage_blueprint.route('/')
@requires_login
def index():
    """
    Sort mortgages and integrate the Jinja2 template engine with the app.
    """
    NUM = 6  # Only present latest 2 weeks (6 rows)

    mortgages = Mortgage.find_all()
    # Sorted by date first, then by name
    mortgages_sorted = sorted(
        mortgages, key=lambda mortgage: (datetime.strptime(mortgage.date, '%m/%d/%Y'), 0 - ord(mortgage.name[0])), reverse=True)
    return render_template("mortgages/index.html", mortgages=mortgages_sorted[:NUM])
