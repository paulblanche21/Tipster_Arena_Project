from flask import Blueprint, render_template

sports_bp = Blueprint('sports', __name__)


@sports_bp.route('/football')
def football():
    """
    Renders the football.html template with the 'football' sport parameter.

    Returns:
    The rendered HTML template.
    """
    return render_template('football.html', sport='football')


@sports_bp.route('/golf')
def golf():
    """
    Renders the golf.html template with the 'golf' sport parameter.

    Returns:
    The rendered HTML template.
    """
    return render_template('golf.html', sport='golf')


@sports_bp.route('/horse_racing')
def horse_racing():
    """
    Renders the horse racing template with the sport parameter set to 'horseracing'.
    
    Returns:
    The rendered horse racing template.
    """
    return render_template('horse_racing.html', sport='horseracing')


@sports_bp.route('/tennis')
def tennis():
    """
    Renders the tennis.html template with the sport parameter set to 'tennis'.
    """
    return render_template('tennis.html', sport='tennis')


@sports_bp.route('/latest-tips')
def latest_tips():
    """
    Returns the latest tips as an HTML page using the 'latest-tips.html' template.
    """
    return render_template('latest-tips.html')


@sports_bp.route('/tipster-league-table')
def tipster_league_table():
    """
    Renders the tipster league table HTML template.

    Returns:
        The rendered HTML template for the tipster league table.
    """
    return render_template('tipster-league-table.html')


@sports_bp.route('/fixtures-results')
def fixtures_results():
    """Display the fixtures and results page."""
    return render_template('fixtures_results.html')


@sports_bp.route('/in-play')
def in_play():
    """Display the in-play events page."""
    return render_template('inplay.html')
