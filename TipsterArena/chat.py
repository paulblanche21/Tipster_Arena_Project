from flask import Blueprint, render_template, session

chat_bp = Blueprint('chat', __name__)


@chat_bp.route('/general-chat')
def general_chat():
    """
    Renders the general chat template with the logo hidden and sets
    the is_chatroom flag to True.

    Returns:
        The rendered general chat template.
    """
    username = session.get('username', '')
    return render_template('general_chat.html',
                           hide_logo=True,
                           is_chatroom=True,
                           username=username)
    
