from flask import Blueprint, jsonify
from App.models import CommandHistory
from App.database import db

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

def get_command_history_byID(id):
    """
    Retrieve a CommandHistory entry by its ID.
    :param id: The ID of the command history entry
    :return: CommandHistory object or None if not found
    """
    # Use .first() to retrieve a single result (or None if not found)
    history = CommandHistory.query.filter_by(id=id).first()
    
    # If no history is found, return None
    if history is None:
        return None
    
    # Return the CommandHistory instance or its dictionary representation
    return history  # Return the CommandHistory object itself
    # Or if you need to return it as a dictionary:
    # return history.to_dict()



def get_all_command_history():
    """
    Retrieve all CommandHistory entries.
    :return: List of CommandHistory objects or an empty list if none exist
    """
    # Query the database to get all command histories
    histories = CommandHistory.query.all()
    
    # If no histories exist, return an empty list
    if not histories:
        return []
    
    # Return the list of CommandHistory instances (not dictionaries)
    return histories




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