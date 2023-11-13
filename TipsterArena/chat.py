from flask import Blueprint, render_template

chat_bp = Blueprint('chat', __name__)


@chat_bp.route('/football-chat')
def football_chat():
    """
    Renders the football chat template with the logo hidden and sets
    the is_chatroom flag to True.

    Returns:
        The rendered football chat template.
    """
    return render_template('football_chat.html',
                           hide_logo=True,
                           is_chatroom=True)


@chat_bp.route('/horse-racing-chat')
def horse_racing_chat():
    """
    Renders the horse racing chat template with the logo hidden
    and the chatroom active.

    Returns:
        The rendered horse racing chat template.
    """
    return render_template('horse_racing_chat.html',
                           hide_logo=True,
                           is_chatroom=True)


@chat_bp.route('/tennis-chat')
def tennis_chat():
    """
    Renders the tennis chat template with the hide_logo
    and is_chatroom parameters set to True.

    Returns:
        The rendered tennis chat template.
    """
    return render_template('tennis_chat.html',
                           hide_logo=True,
                           is_chatroom=True)


@chat_bp.route('/golf-chat')
def golf_chat():
    """
    Renders the golf chat template with the hide_logos
    and is_chatroom parameters set to True.

    Returns:
        The rendered golf chat template.
    """
    return render_template('golf_chat.html',
                           hide_logo=True,
                           is_chatroom=True)
