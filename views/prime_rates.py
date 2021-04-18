from flask import Blueprint, render_template
from datetime import datetime
from models.prime_rate import PrimeRate
from models.user.decorator import requires_login


prime_rate_blueprint = Blueprint("prime_rates", __name__)  # file name


@prime_rate_blueprint.route('/')
def index():
    """
    Sort prime rates and integrate the Jinja2 template engine with the app.
    """
    prime_rate_plot = PrimeRate.create_plot('prime_rate')  # Default plot

    prime_rates = PrimeRate.find_all()
    prime_rates_sorted = sorted(
        prime_rates, key=lambda prime_rate: datetime.strptime(prime_rate.date, '%m/%d/%Y'), reverse=True)

    return render_template("prime_rates/index.html", prime_rates=prime_rates_sorted, plot=prime_rate_plot)
