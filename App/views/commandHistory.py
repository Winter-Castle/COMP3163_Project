from flask import Blueprint, jsonify, request
from App.controllers.commandHistory import (
    create_command_history,
    get_command_history_byID,
    get_all_command_history,
)

# Define the Blueprint for command history
command_history_views = Blueprint('command_history_views', __name__)


# Route to create a command history with reviewID through URL
@command_history_views.route('/command-history/<int:reviewID>', methods=['POST'])
def create_command_history_endpoint(reviewID):
    """
    Endpoint to create a new command history record using reviewID from URL.
    """
    # Call the function to create a new command history, passing the reviewID from the URL
    result = create_command_history(reviewID)
    
    if result:
        return jsonify({'message': f"Command history for review ID {reviewID} created successfully."}), 201
    else:
        return jsonify({'message': 'Failed to create command history'}), 400


# Route to get a command history by ID
@command_history_views.route('/command-history/<int:id>', methods=['GET'])
def get_history_by_id(id):
    return get_command_history_byID(id)

# Route to get all command histories
@command_history_views.route('/command-history', methods=['GET'])
def get_all_histories():
    return get_all_command_history()

# Route to update a command history
@command_history_views.route('/command-history/<int:id>', methods=['PUT'])
def update_history(id):
    return update_command_history(id)

# Route to delete a command history
@command_history_views.route('/command-history/<int:id>', methods=['DELETE'])
def delete_history(id):
    return delete_command_history(id)
