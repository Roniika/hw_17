from flask import current_app as app, request
from flask_restx import Api, Resource
from application.models import db
from application import models, schema

api = app.config['api']
movies_ns = api.namespace('movies')
directors_ns = api.namespace('directors')
genres_ns = api.namespace("genres")


movies_schema = schema.Movie(many=True)
movie_schema = schema.Movie()

directors_schema = schema.Director(many=True)
director_schema = schema.Director()

genres_schema = schema.Genre(many=True)
genre_schema = schema.Genre()


@movies_ns.route('/')
class MoviesView(Resource):
    def get(self):
        movies_query = db.session.query(models.Movie)

        args = request.args

        director_id = args.get('director_id')
        if director_id is not None:
            movies_query = movies_query.filter(models.Movie.director_id == director_id)

        genre_id = args.get('genre_id')
        if genre_id is not None:
            movies_query = movies_query.filter(models.Movie.genre_id == genre_id)

        movies = movies_query.all()

        return movies_schema.dump(movies), 200

    def post(self):
        movie = movie_schema.load(request.json)
        db.session.add(models.Movie(**movie))
        db.session.commit()

        return "", 201


@movies_ns.route('/<int:mid>')
class MovieView(Resource):
    def get(self, mid: int):
        movie = db.session.query(models.Movie).filter(models.Movie.id == mid).one()

        if movie is None:
            return "", 404

        return movie_schema.dump(movie), 200

    def put(self, mid):
        db.session.query(models.Movie).filter(models.Movie.id == mid).update(request.json)
        db.session.commit()

        return "", 204

    def delete(self, mid):
        db.session.query(models.Movie).filter(models.Movie.id == mid).delete()
        db.session.commit()

        return "", 204


@directors_ns.route('/')
class DirectorsView(Resource):
    def get(self):
        directors = db.session.query(models.Director).all()

        return directors_schema.dump(directors), 200

    def post(self):
        director = director_schema.load(request.json)
        db.session.add(models.Director(**director))
        db.session.commit()

        return "", 201


@directors_ns.route('/<int:did>')
class DirectorView(Resource):
    def get(self, did: int):
        director = db.session.query(models.Director).filter(models.Director.id == did).one()

        if director is None:
            return "", 404

        return director_schema.dump(director), 200

    def put(self, did):
        db.session.query(models.Director).filter(models.Director.id == did).update(request.json)
        db.session.commit()

        return "", 204

    def delete(self, did):
        db.session.query(models.Director).filter(models.Director.id == did).delete()
        db.session.commit()

        return "", 204


@genres_ns.route('/')
class GenresView(Resource):
    def get(self):
        genres = db.session.query(models.Genre).all()

        return genres_schema.dump(genres), 200

    def post(self):
        genre = genre_schema.load(request.json)
        db.session.add(models.Genre(**genre))
        db.session.commit()

        return "", 201


@genres_ns.route('/<int:gid>')
class GenreView(Resource):
    def get(self, gid: int):
        genre = db.session.query(models.Genre).filter(models.Genre.id == gid).one()

        if genre is None:
            return "", 404

        return genre_schema.dump(genre), 200

    def put(self, gid):
        db.session.query(models.Genre).filter(models.Genre.id == gid).update(request.json)
        db.session.commit()

        return "", 204

    def delete(self, gid):
        db.session.query(models.Genre).filter(models.Genre.id == gid).delete()
        db.session.commit()

        return "", 204