from flask import Blueprint, request, jsonify, make_response, abort
from app import db
from app.models.board import Board
from app.models.card import Card

boards_bp = Blueprint("boards_bp", __name__, url_prefix="/boards")

# helper function
# validate if has non-empty title and owner. if not, return error msg
def validate_board(request_body):
    new_title = request_body["title"]
    new_owner = request_body["owner"]
    # if empty string, return error msg
    if not new_title or not new_owner:
        rsp = {"msg": f"Please enter valid title and owner to create a board."}
        abort(make_response(jsonify(rsp), 400))
    new_board = Board(title=new_title, owner=new_owner)
    return new_board
    # try:
    #     if new_title and new_owner:
    #         new_board = Board(title=new_title, owner=new_owner)
    #         return new_board
    # except:
    #     rsp = {"msg": f"Please enter valid title and owner to create a board."}
    #     abort(make_response(jsonify(rsp), 400))
    

def validate_id(board_id):
    try:
        id = int(board_id)
    except ValueError:
        rsp = {"msg": f"Invalid id: {id}"}
        abort(make_response(jsonify(rsp), 400))
    chosen_board = Board.query.get(id)
    if chosen_board is None:
        rsp = {"msg": f"Could not find id {id}"}
        abort(make_response(jsonify(rsp), 404))
    return chosen_board


# CREATE one board using title and owner
@boards_bp.route("", methods=["POST"])
def create_board():
    request_body = request.get_json()
    # validate if has title and owner, if not, return error msg
    new_board = validate_board(request_body)
    
    # add record to the table
    db.session.add(new_board)
    db.session.commit
    return {
        "msg": f"Successfully created {new_board.title} by {new_board.owner}"
    }, 201



# READ all boards
@boards_bp.route('', methods=['GET'])
def get_all_boards():
    boards = Board.query.all()
    rsp = f"show all boards: {boards}"
    return jsonify(rsp), 200



# READ one board
@boards_bp.route('/<board_id>', methods=['GET'])
def get_one_board(board_id):
    chosen_board = validate_id(board_id)

    rsp = {"Board": chosen_board}
    return jsonify(rsp), 200


# (optional) DELETE one board
@boards_bp.route("/<board_id>", methods=['DELETE'])
def delete_one_task(board_id):
    chosen_board = validate_id(board_id)

    db.session.delete(chosen_board)
    db.session.commit()
    rsp = {
        "details": f'Board {board_id} "{chosen_board.title}" successfully deleted'
    }
    return jsonify(rsp), 200
