#!/usr/bin/env python3

from flask import request, session
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError

from config import app, db, api
from models import User, Recipe

class Signup(Resource):
    def post(self):
        json = request.get_json()
        if 'username' not in json:
            return {'error': 'nonono'}, 422
        user = User(
            username = json['username'],
            image_url = json['image_url'],
            bio = json['bio'],
        )
        user.password_hash = json['password']
        db.session.add(user)
        db.session.commit()
        session['user_id'] = user.id
        return user.to_dict(), 201

class CheckSession(Resource):
    def get(self):
        if session['user_id']:
            user = User.query.filter_by(id = session['user_id']).first()
            return user.to_dict(), 200
        else:
            return {'error': 'no'}, 401

class Login(Resource):
    def post(self):
        user = User.query.filter_by(username=request.get_json()['username']).first()
        if user:
            session['user_id'] = user.id
            return user.to_dict(), 201
        else:
            return {'error': 'no'}, 401

class Logout(Resource):
    def delete(self):
        if session['user_id']:
            session['user_id'] = None
            return '', 204
        else:
            return {'error': 'no'}, 401 


class RecipeIndex(Resource):
    def get(self):
        if session['user_id']:
            print('hello')
            print(Recipe.query.all())
            recipes = [recipe.to_dict() for recipe in Recipe.query.all()]
            user = User.query.filter_by(id=session['user_id']).first().to_dict()
            recipes.append(user)
            return recipes, 200
        else:
            return {'error':'no'}, 401
    def post(self):
        if session['user_id']:
            json = request.get_json()
            try:
                recipe = Recipe(
                title = json['title'],
                instructions = json['instructions'],
                minutes_to_complete = json['minutes_to_complete'],
                user_id = session['user_id'],
            )
            except:
                return {'error': 'no'}, 422
            db.session.add(recipe)
            db.session.commit()
            return recipe.to_dict(),201
        else:
            return {'error': 'no'}, 401

api.add_resource(Signup, '/signup', endpoint='signup')
api.add_resource(CheckSession, '/check_session', endpoint='check_session')
api.add_resource(Login, '/login', endpoint='login')
api.add_resource(Logout, '/logout', endpoint='logout')
api.add_resource(RecipeIndex, '/recipes', endpoint='recipes')


if __name__ == '__main__':
    app.run(port=5555, debug=True)