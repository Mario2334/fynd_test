from sanic import json, Blueprint
from sanic.views import HTTPMethodView
from sanic_jwt import scoped, protected
from sanic_validation import validate_json
from Constants import ROLE
from models import Movie
from utils import parse_json
from validators import movie_schema

movies = Blueprint("movies", url_prefix="/movies")


class MovieView(HTTPMethodView):

    @protected()
    async def get(self, request):
        try:
            search = request.args["search"][0]
            pipeline = {"$text": {"$search": search}}
        except KeyError:
            pipeline = {}
        users = Movie.get_collection().find(pipeline, )
        users = await users.to_list(10)
        data = parse_json(users)
        # data = [parse_json(users) for user in users]
        return json(data)

    @scoped(ROLE["Admin"])
    @validate_json(movie_schema)
    async def post(self, request):
        data = request.json
        await Movie.insert_one(data)
        return json({"message": "Movie Added Successfully"}, 201)


class SaveMovieView(HTTPMethodView):
    @scoped(ROLE["Admin"])
    @validate_json(movie_schema)
    async def put(self, request, _id):
        movie = await Movie.find_one(_id)
        doc = request.json
        movie.clean_for_dirty(doc)
        new_movie = await Movie.update_one({"_id": movie.id}, {"$set": doc})
        return json({"message":"Movie updated"})

    @scoped(ROLE["Admin"])
    async def delete(self, request, _id):
        movie = await Movie.find_one(_id)
        await movie.destroy()
        return json({"message": "User was deleted successfully"})


movies.add_route(MovieView.as_view(),"/")
movies.add_route(SaveMovieView.as_view(), "/update/<_id>")
