# Inspiration Board: Back-end Layer

This scaffold includes the following:

## `app/__init__.py`

This file configures the app. It's where:

We expect developers to modify this file by:

- Replacing the database connection string
- Importing all models
- Registering all blueprints

Note that `create_app` also uses CORS. There is no extra action needed to be done with CORS.

## `app/routes.py`

We expect endpoints to be defined here.

The file already imports:

- `Blueprint`
- `request`
- `jsonify`
- `make_response`
- `db`

Feel free to alter these import statements.

This file also has a comment to define a Blueprint. Feel free to delete it.

## `app/models` Directory

This project already includes `app/models/board.py` and `app/models/card.py`, to anticipate the models `Board` and `Card`.

Both files already import `db`, for convenience!

## `requirements.txt`

This file lists the dependencies we anticipate are needed for the project.

## `Procfile`

This file already has the contents needed for a Heroku deployment.

If the `create_app` function in `app/__init__.py` is renamed or moved, the contents of this file need to change. Otherwise, we don't anticipate this file to change.

## `Endpoints`
| Verb  | Path  | Body of Request | What it does  |
|---|---|---|---|
| `GET`  | `/boards`  | None | Retrieves a list of boards  |
| `POST`  | `/boards`  | `{ title: 'titleText', owner: 'ownerText' }`  | Creates a board with title and owner informtion   |
| `GET`  | `/boards/<board_id>/cards`  | None  | Retrieves a list of cards under one specific board   |
| `POST`  | `/boards/<board_id>/cards`  | `{ message: 'messageText', likes_count: likesCount, board_id: boardID }` | Creates a new card   |
| `DELETE`  | `/boards/<board_id>/cards/<card_id>`  | None  | Deletes a card |
| `PATCH`  | `/boards/<board_id>/cards/<card_id>/like`  | `{likes_count: likesCount }`  | Updates the like counts of a card |