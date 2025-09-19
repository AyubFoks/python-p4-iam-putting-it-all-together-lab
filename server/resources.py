from flask_restful import Resource
from flask import request, jsonify

from flask import request
from server.models import User
from server.app import db

class Signup(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        bio = data.get('bio', '')
        image_url = data.get('image_url', '')

        if not username or not password:
            return {"error": "Username and password are required."}, 422

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return {"error": "Username already exists."}, 422

        new_user = User(
            username=username,
            bio=bio,
            image_url=image_url
        )
        new_user.password_hash = password

        db.session.add(new_user)
        db.session.commit()

        return {"message": "User created successfully."}, 201


from flask import session

class Login(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return {"error": "Username and password are required."}, 422

        user = User.query.filter_by(username=username).first()
        if not user or not user.authenticate(password):
            return {"error": "Invalid username or password."}, 401

        session['user_id'] = user.id

        return {
            "id": user.id,
            "username": user.username,
            "bio": user.bio,
            "image_url": user.image_url
        }, 200

from flask import session

class Logout(Resource):
    def delete(self):
        user_id = session.get('user_id')
        if not user_id:
            return {"error": "Unauthorized"}, 401
        session.pop('user_id', None)
        return {"message": "Logged out successfully."}, 200

from flask import session
from server.models import User

class CheckSession(Resource):
    def get(self):
        user_id = session.get('user_id')
        if not user_id:
            return {"error": "Unauthorized"}, 401

        user = db.session.get(User, user_id)
        if not user:
            return {"error": "Unauthorized"}, 401

        return {
            "id": user.id,
            "username": user.username,
            "bio": user.bio,
            "image_url": user.image_url
        }, 200

from server.models import Recipe

from flask import session

class RecipeIndex(Resource):
    def get(self):
        user_id = session.get('user_id')
        if not user_id:
            return {"error": "Unauthorized"}, 401

        recipes = Recipe.query.all()
        return [
            {
                "id": recipe.id,
                "title": recipe.title,
                "instructions": recipe.instructions,
                "minutes_to_complete": recipe.minutes_to_complete,
                "user_id": recipe.user_id
            }
            for recipe in recipes
        ], 200

    def post(self):
        user_id = session.get('user_id')
        if not user_id:
            return {"error": "Unauthorized"}, 401

        data = request.get_json()
        title = data.get('title')
        instructions = data.get('instructions')
        minutes_to_complete = data.get('minutes_to_complete')

        if not title or not instructions:
            return {"error": "Title and instructions are required."}, 422

        try:
            new_recipe = Recipe(
                title=title,
                instructions=instructions,
                minutes_to_complete=minutes_to_complete,
                user_id=user_id
            )
            db.session.add(new_recipe)
            db.session.commit()
        except ValueError as e:
            return {"error": str(e)}, 422

        return {
            "id": new_recipe.id,
            "title": new_recipe.title,
            "instructions": new_recipe.instructions,
            "minutes_to_complete": new_recipe.minutes_to_complete,
            "user_id": new_recipe.user_id
        }, 201