from flask import Blueprint, render_template, request
from datetime import datetime
from models.libor import Libor


libor_blueprint = Blueprint("libors", __name__)


@libor_blueprint.route('/')
def index():
    """
    Sort libors and integrate the Jinja2 template engine with the app.
    """
    DAYS = 15  # Only present latest 15 rates.

    libor_plot = Libor.create_plot('overnight')  # Default plot

    libors = Libor.find_all()
    libors_sorted = sorted(
        libors, key=lambda libor: datetime.strptime(libor.date, '%m/%d/%Y'), reverse=True)

    libor_overnight, libor_1_week, libor_1_month, libor_3_months, libor_6_months, libor_12_months = [], [], [], [], [], []

    for libor in libors_sorted:
        if libor.name == 'overnight':
            libor_overnight.append(libor)

        elif libor.name == '1-week':
            libor_1_week.append(libor)

        elif libor.name == '1-month':
            libor_1_month.append(libor)

        elif libor.name == '3-months':
            libor_3_months.append(libor)

        elif libor.name == '6-months':
            libor_6_months.append(libor)

        elif libor.name == '12-months':
            libor_12_months.append(libor)

        else:
            raise NameError('The libor name is invalid.')

    return render_template("libors/index.html",
                           libor_overnight=libor_overnight[:DAYS],
                           libor_1_week=libor_1_week[:DAYS],
                           libor_1_month=libor_1_month[:DAYS],
                           libor_3_months=libor_3_months[:DAYS],
                           libor_6_months=libor_6_months[:DAYS],
                           libor_12_months=libor_12_months[:DAYS],
                           plot=libor_plot)


@libor_blueprint.route('/types', methods=['GET', 'POST'])
def change_features():
    """
    Change the libor plot.
    """
    feature = request.args['selected']
    graphJSON = Libor.create_plot(feature)
    return graphJSON
