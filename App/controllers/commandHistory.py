from flask import Blueprint, jsonify, request
from App.models import commandHistory
from App.database import db


command_history_views = Blueprint('command_history_views', __name__)


def create_command_history():
    data = request.json
    if not data or 'review_id' not in data:
        return jsonify({'error': 'Invalid data'}), 400

    try:
        command_history = CommandHistory(review_id=data['review_id'])
        db.session.add(command_history)
        db.session.commit()
        return jsonify({'message': 'Command history created', 'data': command_history.get_json()}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

def get_command_history_byID(id):
    command_history = CommandHistory.query.get(id)
    if not command_history:
        return jsonify({'error': 'Command history not found'}), 404

    return jsonify({'data': command_history.get_json()}), 200




def get_all_command_history():
    try:
        command_histories = CommandHistory.query.all()
        return jsonify({'data': [ch.get_json() for ch in command_histories]}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

