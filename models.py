from sanic_motor import BaseModel


class User(BaseModel):
    __coll__ = "users"
    __unique_fields__ = ['username']

    def __repr__(self):
        return "User(id='{}')".format(self._id)

    def to_dict(self):
        return {
            "user_name": self.username,
            "password": self.password,
            "role": self.role
        }



class Movie(BaseModel):
    __coll__ = "movies"
    __unique_fields__ = "name"

    def to_dict(self):
        return {
            "popularity": self["99popularity"],
            "director":self.director,
            "genre": self.genre,
            "imdb_score": self.imdb_score,
            "name": self.name
        }
