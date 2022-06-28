from flask import Blueprint, request, jsonify, make_response, abort
from app import db
from app.models.card import Card
from app.models.board import Board

cards_bp = Blueprint('cards_bp', __name__, url_prefix="/cards")
# cards_bp = Blueprint('cards_bp', __name__, url_prefix="/boards/<board_id>/cards")
boards_bp = Blueprint('boards_bp', __name__, url_prefix="/boards")

# helper functions
def get_card_or_abort(card_id):
    try:
        card_id = int(card_id)
    except ValueError:
        rsp = {"msg":f"Invalid id {card_id}"}
        abort(make_response(jsonify(rsp), 400))
    
    card = Card.query.get(card_id)
    if card is None:
        rsp = {"msg":f"Could not find card with id {card_id}"}
        abort(make_response(jsonify(rsp), 404))
    return card

def get_board_or_abort(board_id):
    try:
        board_id = int(board_id)
    except ValueError:
        rsp = {"msg":f"Invalid id {board_id}"}
        abort(make_response(jsonify(rsp), 400))
    
    board = Board.query.get(board_id)
    if board is None:
        rsp = {"msg":f"Could not find board with id {board_id}"}
        abort(make_response(jsonify(rsp), 404))
    return board

# routes

@boards_bp.route("", methods=['POST'])
def create_one_board():
    request_body = request.get_json()

    try:
        new_board = Board(title = request_body["title"],owner = request_body["owner"])
    except KeyError:
        return { "details": "Invalid data"}, 400
    db.session.add(new_board)
    db.session.commit()
    return jsonify(
        {
            "board": new_board.to_dict()
        }
    ),201

@boards_bp.route("", methods=['GET'])
def get_all_boards():
    boards = Board.query.all()
    boards_response = []
    for board in boards:
        boards_response.append(board.to_dict())

    return jsonify(boards_response), 200

# GET /boards
@boards_bp.route('/<board_id>', methods=['GET'])
def get_one_board(board_id):
    board = get_board_or_abort(board_id)
    return jsonify(
        {
            "board": board.to_dict()
        }
    ), 200

# POST /boards/<board_id>/cards
@boards_bp.route('/<board_id>/cards', methods=['POST'])
def add_cards_to_boards(board_id):

    board = get_board_or_abort(board_id)
    request_body = request.get_json()

    try:
        card_ids = request_body["card_ids"]
    except KeyError:
        return { "details": "Invalid data, missing card_ids"}, 400
    if not isinstance(card_ids,list):
        return { "details": "Expected list of card ids"}, 400
    
    cards = []
    for id in card_ids:
        card = get_card_or_abort(id)
        cards.append(card)

    for card in cards:
        card.board_id=board_id

    db.session.commit()

    return jsonify(
        {
            "id": board.board_id,
            "card_ids": card_ids
        }
    ),200

# GET /boards/<board_id>/cards
@boards_bp.route('/<board_id>/cards', methods=['GET'])
def get_cards_at_one_board(board_id):
    board = get_board_or_abort(board_id)
    cards = []
    for card in board.cards:
        cards.append(card.to_dict())
    return ({
                "id": board.board_id,
                "title": board.title,
                "cards": cards
            }), 200


# DELETE /cards/<card_id>
@cards_bp.route('/<card_id>', methods=['DELETE'])
def delete_one_card(card_id):
    card = get_card_or_abort(card_id)
    db.session.delete(card)
    db.session.commit()

    return {
        "details" : f'Card {card.id} "{card.title}" successfully deleted'
    }, 200

# PUT /cards/<card_id>/like ???
@cards_bp.route('/<card_id>/like', methods=['PUT'])
def update_card(card_id):
    card = get_card_or_abort(card_id)
    request_body = request.get_json()

    try:
        card.message = request_body["message"]
        card.likes_count = request_body["likes_count"]
        # card.likes_count = request_body.get("likes_count")
    
    except KeyError:
        return {
            "msg" : "Message and likes are required" 
        }, 400
    
    db.session.commit()
    return jsonify(
        {
            "card": card.to_dict()
        }
    ), 200