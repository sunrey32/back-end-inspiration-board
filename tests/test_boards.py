from urllib import response
from app.models.board import Board
import pytest

def test_get_boards_no_saved_boards(client):
    # Act
    response = client.get("/boards")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == []


# def test_create_board(client):
#     #Act
#     response client.post("/boards", json={
#         "title": "A Brand New Board",
#         "owner": "Test Owner"
#     })
#     response_body = response.get_json()