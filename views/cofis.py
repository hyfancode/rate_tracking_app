from flask import Blueprint, render_template
from datetime import datetime
from models.cofi import Cofi
from models.user.decorator import requires_login


cofi_blueprint = Blueprint("cofis", __name__)  # file name


@cofi_blueprint.route('/')
@requires_login
def index():
    """
    Sort COFIs and integrate the Jinja2 template engine with the app.
    """
    cofis = Cofi.find_all()
    cofis_sorted = sorted(
        cofis, key=lambda cofi: (datetime.strptime(cofi.date, '%m/%d/%Y'), cofi.name), reverse=True)
    return render_template("cofis/index.html", cofis=cofis_sorted)
