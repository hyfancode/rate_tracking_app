from flask import Blueprint, render_template
from datetime import datetime
from models.log import Log
from models.user.decorator import requires_admin


log_blueprint = Blueprint("logs", __name__)  # file name


@log_blueprint.route('/')
@requires_admin
def index():
    """
    Sort logs and integrate the Jinja2 template engine with the app.
    """
    NUM_OF_LOGS = 100  # View latest 100 logs.

    logs = Log.find_all()
    logs_sorted = sorted(
        logs, key=lambda log: datetime.strptime(log.date_time, "%m/%d/%Y %H:%M:%S"), reverse=True)
    return render_template("logs/index.html", logs=logs_sorted[:NUM_OF_LOGS])
