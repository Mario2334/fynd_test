import pymongo
from sanic import Sanic
from sanic_jwt import exceptions, initialize
from sanic_motor import BaseModel
from models import User, Movie
from settings import mongoSettings
from views.MovieView import movies
from views.UserView import users
import json

app = Sanic(__name__)

app.config.update(mongoSettings)
BaseModel.init_app(app)


async def authenticate(request, *args, **kwargs):
    username = request.json.get("username", None)
    password = request.json.get("password", None)

    if not username or not password:
        raise exceptions.AuthenticationFailed("Missing username or password.")

    user = await User.find_one({"username": username})
    if user is None:
        raise exceptions.AuthenticationFailed("User not found.")

    if password != user.password:
        raise exceptions.AuthenticationFailed("Password is incorrect.")

    return user


async def setup_movie_index(app, loop):
    data = json.load(open("scripts/imdb.json", "r"))
    await Movie.insert_many(data)
    await Movie.create_index([('name', pymongo.TEXT)], name='search_index')
    print(data)
    pass


async def scope_extender(user, *args, **kwargs):
    print(user)
    return [user.role,]


if __name__ == "__main__":
    # app.register_listener(setup_movie_index,
    #                       'before_server_start')
    initialize(app, authenticate=authenticate,add_scopes_to_payload=scope_extender)
    app.blueprint(users)
    app.blueprint(movies)
    app.run(host="0.0.0.0", port=8000, debug=True)
