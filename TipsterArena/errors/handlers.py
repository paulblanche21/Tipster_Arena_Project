from flask import Blueprint, render_template
import logging


# Create a Blueprint instance
handler = Blueprint('handler', __name__)

# Now you can use the handler Blueprint to define error handlers


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
