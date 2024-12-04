from flask import Blueprint, jsonify
<<<<<<< Updated upstream
from App.models import commandHistory
=======
from App.models import CommandHistory
>>>>>>> Stashed changes
from App.database import db

command_history_views = Blueprint('command_history_views', __name__)


<<<<<<< Updated upstream
def create_command_history(reviewID):
    try:
        command_history = commandHistory(reviewID)
        db.session.add(command_history)
        db.session.commit()
        return command_history  # Returning the object directly
    except Exception as e:
        db.session.rollback()
        return None
=======
def create_command_history(review_id):
    """
    Create a new CommandHistory entry in the database.
    :param review_id: The ID of the associated review
    :return: The created CommandHistory object
    """
    command_history = CommandHistory(review_id=review_id)  # Automatically uses datetime.utcnow for time
    db.session.add(command_history)
    db.session.commit()
    return command_history

>>>>>>> Stashed changes

def get_command_history_byID(id):
<<<<<<< Updated upstream
    command_history = commandHistory.query.get(id)
    return command_history  # Returns None if not found


def get_all_command_history():
    try:
        command_histories = commandHistory.query.all()
        return command_histories  # Returns a list of objects or an empty list
    except Exception:
        return None
=======
    """
    Retrieve a CommandHistory entry by its ID.
    :param id: The ID of the command history entry
    :return: CommandHistory object or None if not found
    """
    return CommandHistory.query.get(id)


def get_all_command_history():
    """
    Retrieve all CommandHistory entries.
    :return: List of CommandHistory objects or an empty list if none exist
    """
    return CommandHistory.query.all()




# Commented out as requested
# def update_command_history(id):
#     if not request.is_json:
#         return jsonify({'error': 'Request must be JSON'}), 400

#     data = request.json
#     if not data:
#         return jsonify({'error': 'No data provided for update'}), 400

#     try:
#         command_history = commandHistory.query.get(id)
#         if not command_history:
#             return jsonify({'error': 'Command history not found'}), 404

#         # Update fields (example: updating review_id; add more as needed)
#         if 'review_id' in data:
#             command_history.review_id = data['review_id']

#         db.session.commit()
#         return jsonify({'message': 'Command history updated', 'data': command_history.get_json()}), 200
#     except Exception as e:
#         db.session.rollback()
#         return jsonify({'error': 'An error occurred while updating command history'}), 500


# def delete_command_history(id):
#     try:
#         command_history = commandHistory.query.get(id)
#         if not command_history:
#             return jsonify({'error': 'Command history not found'}), 404

#         db.session.delete(command_history)
#         db.session.commit()
#         return jsonify({'message': 'Command history deleted'}), 200
#     except Exception as e:
#         db.session.rollback()
#         return jsonify({'error': 'An error occurred while deleting command history'}), 500
