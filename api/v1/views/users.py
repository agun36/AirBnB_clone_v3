#!/usr/bin/python3
""" Flask routes for `User` object related URI using the
`app_views` Blueprint.
"""
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request, make_response
from models import storage
from models.user import User


@app_views.route("/users", methods=['GET'],
                 strict_slashes=False)
def GET_all_User():
    """ Returns te JSON list of all `User` instances in storage
    """
    user_list = []
    for user in storage.all(User).values():
        user_list.append(user.to_dict())
    response = make_response(jsonify(user_list), 200)

    return response


@app_views.route("/users/<user_id>", methods=['GET'],
                 strict_slashes=False)
def GET_User(user_id):
    """ Returns `User` instance in storage by id in URI subpath    """
    user = storage.get(User, user_id)

    if user:
        return jsonify(user.to_dict(), 200)
    else:
        abort(404)


@app_views.route("/users/<user_id>", methods=['DELETE'],
                 strict_slashes=False)
def DELETE_User(user_id):
    """ Deletes `User` instance in storage by id in URI subpath

    """
    user = storage.get(User, user_id)

    if user:
        storage.delete(user)
        storage.save()
        return ({})
    else:
        abort(404)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def POST_User():
    """ Creates new `User` instance in storage

    Return:
        Empty dictionary and response status 200, or 404 response
    on error
    """
    req_dict = request.get_json()
    if not req_dict:
        return (jsonify({'error': 'Not a JSON'}), 400)
    elif 'email' not in req_dict:
        return (jsonify({'error': 'Missing email'}), 400)
    elif 'password' not in req_dict:
        return (jsonify({'error': 'Missing password'}), 400)
    new_User = User(**req_dict)
    new_User.save()

    return (jsonify(new_User.to_dict()), 201)


@app_views.route("/users/<user_id>", methods=['PUT'],
                 strict_slashes=False)
def PUT_User(user_id):
    """ Updates `User` instance in storage by id in URI subpath, with
    kwargs from HTTP body request JSON dict

    Args:
        user_id: uuid of `User` instance in storage

    Return:
        Empty dictionary and response status 200, or 404 response
    on error
    """
    user = storage.get(User, user_id)
    req_dict = request.get_json()

    if user:
        if not req_dict:
            return (jsonify({'error': 'Not a JSON'}), 400)
        for key, value in req_dict.items():
            if key not in ['id', 'created_at', 'updated_at', 'email']:
                setattr(user, key, value)
        storage.save()
        return (jsonify(user.to_dict()), 200)
    else:
        abort(404)
