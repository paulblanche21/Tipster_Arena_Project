from flask import Blueprint, render_template

chat_bp = Blueprint('chat', __name__)


@chat_bp.route('/football-chat')
def football_chat():
    return render_template('football_chat.html', hide_logo=True, is_chatroom=True)


@chat_bp.route('/horse-racing-chat')
def horse_racing_chat():
    return render_template('horse_racing_chat.html', hide_logo=True, is_chatroom=True)


@chat_bp.route('/tennis-chat')
def tennis_chat():
    return render_template('tennis_chat.html', hide_logo=True, is_chatroom=True)


@chat_bp.route('/golf-chat')
def golf_chat():
    return render_template('golf_chat.html', hide_logo=True, is_chatroom=True)
