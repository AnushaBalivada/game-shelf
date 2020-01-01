import markdown
import os
import shelve

# Import framework
from flask import Flask, g
from flask_restful import Resource, Api

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

        games = []

        for key in keys:
            games.append(shelf[key])

        return {'message': 'Success', 'data': games}, 200


api.add_resource(GameList, '/games')
