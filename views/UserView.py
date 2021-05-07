from sanic import Blueprint, json
from sanic.views import HTTPMethodView
from sanic_jwt import protected, scoped
from sanic_validation import validate_json
from Constants import ROLE
from models import User
from validators import user_schema

users = Blueprint("users", url_prefix="/users")


class UserView(HTTPMethodView):
    @scoped(ROLE["User"])
    async def get(self, request):
        users = await User.find()
        data = [user.to_dict() for user in users.objects]
        return json({"data":data})

    @scoped(ROLE["Admin"])
    @validate_json(user_schema)
    async def post(self, request):
        # username = request.json.get("username", "")
        # password = request.json.get("password", "")
        # role = request.json.get("role", "")
        data = request.json
        is_uniq = await User.is_unique(data["username"])
        if is_uniq in (True, None):
            await User.insert_one(data)
            return json({"message": "User Added Successfully"}, 201)
        else:
            return json({"message": "User name is already taken"}, 400)


users.add_route(UserView.as_view(), "/")
