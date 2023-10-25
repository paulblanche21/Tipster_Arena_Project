from flask import Blueprint, current_app, render_template
import logging


# Create a Blueprint instance
handler = Blueprint('handler', __name__)

# Now you can use the handler Blueprint to define error handlers


@handler.app_errorhandler(404)
def page_not_found(e):
    current_app.logger.warning(f"Page not found: {e}")
    return render_template('404.html'), 404


@handler.app_errorhandler(500)
def internal_server_error(e):
    current_app.logging.error("Internal server error: %s", e)
    return render_template('500.html'), 500


@handler.app_errorhandler(Exception)
def handle_exception(e):
    current_app.logging.exception("An error occurred: %s", e)
    return render_template("error.html", error=str(e)), 500
