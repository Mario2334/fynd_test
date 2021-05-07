
user_schema = {
    'role': {'type': 'string', 'required': True},
    'username': {'type': 'string', 'required': True},
    'password': {'type': 'string', 'required': True}
}

movie_schema = {
    'name': {'type': 'string', 'required': True},
    'director': {'type': 'string', 'required': True},
    'imdb_score': {'type': 'string', 'required': True},
    '99popularity': {'type': 'integer', 'required': True},
    'genre':{'type':'list','required':True}
}
