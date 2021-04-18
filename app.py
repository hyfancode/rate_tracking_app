import os
from flask import Flask, render_template
from views.libors import libor_blueprint
from views.prime_rates import prime_rate_blueprint
from views.treasuries import treasury_blueprint
from views.mortgages import mortgage_blueprint
from views.cofis import cofi_blueprint
from views.mirses import mirs_blueprint
from views.users import user_blueprint
from views.logs import log_blueprint


app = Flask(__name__)
app.secret_key = os.urandom(64)
app.config.update(ADMIN=os.environ.get('ADMIN'))


@app.route('/')
def home():
    '''
    Go to the home page.
    '''
    return render_template("home.html")


app.register_blueprint(libor_blueprint, url_prefix='/libors')
app.register_blueprint(prime_rate_blueprint, url_prefix='/prime_rates')
app.register_blueprint(treasury_blueprint, url_prefix='/treasuries')
app.register_blueprint(mortgage_blueprint, url_prefix='/mortgages')
app.register_blueprint(cofi_blueprint, url_prefix='/cofis')
app.register_blueprint(mirs_blueprint, url_prefix='/mirses')
app.register_blueprint(user_blueprint, url_prefix='/users')
app.register_blueprint(log_blueprint, url_prefix='/logs')


if __name__ == "__main__":
    # No debug mode in production
    app.run(debug=True)
