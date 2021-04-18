from flask import Blueprint, render_template, request
from datetime import datetime
from models.treasury import Treasury
from models.user.decorator import requires_login


treasury_blueprint = Blueprint("treasuries", __name__)


@treasury_blueprint.route('/')
@requires_login
def index():
    """
    Sort treasuries and integrate the Jinja2 template engine with the app.
    """
    NUM_OF_DAY = 15  # Only present latest 15  rates

    treasury_plot = Treasury.create_plot('1_year')  # Default plot

    treasuries = Treasury.find_all()
    treasuries_sorted = sorted(
        treasuries, key=lambda treasury: datetime.strptime(treasury.date, '%m/%d/%Y'), reverse=True)

    treasury_1_year, treasury_2_year, treasury_3_year, treasury_5_year, treasury_7_year, treasury_10_year = [], [], [], [], [], []

    for treasury in treasuries_sorted:
        if treasury.name == '1_year':
            treasury_1_year.append(treasury)

        elif treasury.name == '2_year':
            treasury_2_year.append(treasury)

        elif treasury.name == '3_year':
            treasury_3_year.append(treasury)

        elif treasury.name == '5_year':
            treasury_5_year.append(treasury)

        elif treasury.name == '7_year':
            treasury_7_year.append(treasury)

        elif treasury.name == '10_year':
            treasury_10_year.append(treasury)

        else:
            raise NameError('The treasury name is invalid.')

    return render_template("treasuries/index.html",
                           treasury_1_year=treasury_1_year[:NUM_OF_DAY],
                           treasury_2_year=treasury_2_year[:NUM_OF_DAY],
                           treasury_3_year=treasury_3_year[:NUM_OF_DAY],
                           treasury_5_year=treasury_5_year[:NUM_OF_DAY],
                           treasury_7_year=treasury_7_year[:NUM_OF_DAY], treasury_10_year=treasury_10_year[:NUM_OF_DAY], plot=treasury_plot)


@treasury_blueprint.route('/types', methods=['GET', 'POST'])
@requires_login
def change_features():
    """
    Change the treasury plot.
    """
    feature = request.args['selected']
    graphJSON = Treasury.create_plot(feature)
    return graphJSON
