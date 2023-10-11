from flask import Blueprint, render_template
import logging
from flask_wtf.csrf import CSRFError


# Define the Blueprint
handler = Blueprint('handler', __name__)


# Specific Error Handlers


@handler.app_errorhandler(404)
def page_not_found(e):
    logging.error("Page not found: %s", e)
    return render_template('404.html'), 404


@handler.app_errorhandler(500)
def internal_server_error(e):
    logging.error("Internal server error: %s", e)
    return render_template('500.html'), 500


@handler.app_errorhandler(Exception)
def handle_exception(e):
    logging.exception("An error occurred: %s", e)
    return render_template("error.html", error=str(e)), 500


@handler.app_errorhandler(CSRFError)
def handle_csrf_error(e):
    return render_template('csrf_error.html', reason=e.description), 400

<<<<<<< HEAD

@handler.app_errorhandler(ValueError)
def handle_value_error(e):
    error_message = "Invalid value: " + str(e)
    return render_template("error.html", error=error_message), 400
=======
@app.errorhandler(ValueError)
def handle_value_error(e):
    error_message = "Invalid value: " + str(e)
    return render_template("error.html", error=error_message), 400
>>>>>>> 84f6b4b (Give me back my life)
