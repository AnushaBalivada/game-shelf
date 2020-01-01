import markdown
import os
import shelve

# Import framework
from flask import Flask, g, request
from flask_restful import Resource, Api, reqparse

# Create an instance of Flask
app = Flask(__name__)

# Create the API
api = Api(app)


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = shelve.open("games.db")
    return db


@app.teardown_appcontext
def teardown_db(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route("/")
def index():
    ''' Documentation'''
    with open(os.path.dirname(app.root_path) + '/README.md', 'r') as markdown_file:

        # Reading the contents of README.md
        content = markdown_file.read()

        return markdown.markdown(content)


class GameList(Resource):
    def get(self):
        shelf = get_db()
        keys = list(shelf.keys())
        loaned = request.args.get('loaned')

        games = []
        loaned_games = []

        for key in keys:
            games.append(shelf[key])

        for game in games:
            if game.loaned_to != "":
                loaned_games.append(game)

        if loaned == "true":
            output = loaned_games
        else:
            output = games

        return {'message': 'Success', 'data': output}, 200

    def post(self):
        parser = reqparse.RequestParser()

        parser.add_argument('title', required=True)
        parser.add_argument('completed', required=False)
        parser.add_argument('loaned_to', required=False)

        # Parse the arguments into an object
        args = parser.parse_args()

        shelf = get_db()
        shelf[args['title']] = args

        return {'message': 'New game added to the library', 'data': args}, 201


class Game(Resource):
    def get(self, title):
        shelf = get_db()

        if title not in shelf:
            return {'message': 'Game not found', 'data': {}}, 404

        return {'message': "Game Found", 'data': shelf[title]}, 200

    def delete(self, title):
        shelf = get_db()

        if title not in shelf:
            return {'message': 'Game not found', 'data': {}}, 404

        del shelf[title]
        return '', 204


api.add_resource(GameList, '/games')
api.add_resource(Game, '/game/<string:title>')
