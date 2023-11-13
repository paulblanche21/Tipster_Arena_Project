from flask import Blueprint, current_app, render_template
from flask_wtf.csrf import CSRFError


# Create a Blueprint instance
handler = Blueprint('handler', __name__)

# Now you can use the handler Blueprint to define error handlers


@handler.app_errorhandler(404)
def page_not_found(e):
    """
    Handle 404 errors (page not found).

    Args:
        e: The error that occurred.

    Returns:
        A tuple containing the rendered template and the HTTP status code 404.
    """
    current_app.logger.warning(f"Page not found: {e}")
    return render_template('404.html'), 404


@handler.app_errorhandler(500)
def internal_server_error(e):
    """
    Handle internal server errors and log the exception.

    Args:
        e: The exception that occurred.

    Returns:
        A rendered template for the 500 error page with a 500 status code.
    """
    current_app.logger.exception("An error occurred: %s", e)
    return render_template('500.html'), 500


@handler.app_errorhandler(Exception)
def handle_exception(e):
    """
    Handle an exception by logging it and rendering an error template.

    Args:
        e (Exception): The exception to handle.

    Returns:
        tuple: A tuple containing the rendered error template and the HTTP
        status code 500.
    """
    current_app.logger.exception("An error occurred: %s", e)
    return render_template("error.html", error=str(e)), 500


@handler.app_errorhandler(CSRFError)
def handle_csrf_error(e):
    """
    Handle CSRF errors by logging the error and rendering a template with
    the error description.

    Args:
        e: The CSRF error.

    Returns:
        A rendered template with the error description and a 400 status code.
    """
    current_app.logger.error('CSRF error occurred: %s', e.description)
    return render_template('csrf_error.html', reason=e.description), 400


@handler.app_errorhandler(401)
def unauthorized_error(e):
    """
    Handle 401 unauthorized errors.

    Args:
        e: The error that occurred.

    Returns:
        A tuple containing the rendered template and the HTTP status code 401.
    """
    current_app.logger.warning('Unauthorized access attempt: %s', e)
    return render_template('401.html'), 401
