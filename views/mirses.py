from flask import Blueprint, render_template
from datetime import datetime
from models.mirs import Mirs
from models.user.decorator import requires_login


mirs_blueprint = Blueprint("mirses", __name__)  # file name


@mirs_blueprint.route('/')
@requires_login
def index():
    """
    Sort MIRSes and integrate the Jinja2 template engine with the app.
    """
    NUM_OF_MONTH = 12  # Only present latest 12 months

    mirs_plot = Mirs.create_plot('MIRS Transition Index')  # Default plot

    mirses = Mirs.find_all()
    mirses_sorted = sorted(
        mirses, key=lambda mirs: datetime.strptime(mirs.date, '%m/%Y'), reverse=True)
    return render_template("mirses/index.html", mirses=mirses_sorted[:NUM_OF_MONTH], plot=mirs_plot)
