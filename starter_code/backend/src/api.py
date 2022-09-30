from crypt import methods
import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
!! Running this funciton will add one
'''
db_drop_and_create_all()

# ROUTES
'''
@TODO implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks', methods=['GET'])
def get_drinks():
    try:
        drinks=Drink.query.all()
    except Exception:
        abort(422)

    drinks = [drinks.short() for drinks in drinks]
    return jsonify({
            'success':True,
            'drinks':drinks

        }),200

'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drink_details', methods=['GET'])
@requires_auth('get:drinks-detail')
def get_drinks_details(payload):
    try:
        drink_details=Drink.querry.all()
    except:
        abort(422)

    drinks= [drinks.long() for drinks in drink_details]
    return jsonify({
        "success":True,
        "drinks":drinks
    }),200



    



'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''

@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def post_drinks(payload):

    data = request.get_json()
    all_drinks = Drink.query.all()
    drink_titles = [drink.title for drink in all_drinks]
    if data['title'] in drink_titles:
        abort(403)
    try:
        data_recipe = data['recipe']
        if type(data_recipe) is dict:
            data_recipe = [data_recipe]
        drink = Drink(title=data['title'],
                recipe=json.dumps(data_recipe))
        drink.insert()
    
    except Exception:
        abort(400)
    
    return jsonify({
        "success":True,
        "drinks":[drink.long()]

    }), 200


'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks/<int:id>', methods=["PATCH"])
@requires_auth('patch:drinks')
def patch_drinks():

    data = request.get_json()
    drink = Drink.query.all(Drink.id == id).one_or_none()
    
    if not drink:
        abort (404)

    all_drinks=Drink.query.all()
    drink_titles=[drink.title for drink in all_drinks]

    if 'title' in data:
        if data['title'] not in drink_titles:
            drink.title = data['title']
    try:
        if 'recipe' in data:
            drink.recipe = json.dumps(data['recipe'])

        drink.update()

    except Exception as e:
        print(e)
        abort(400)

    return jsonify({
        "success":True,
        "drinks":[drink.long()]

    }), 200








'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''

@app.route('/drinks/<int:id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drinks(payload, id):
    deleted_drink= Drink.query.filter(Drink.id == id).all()
    if not deleted_drink:
        abort(404)
    try:
        deleted_drink.delete()

    except Exception:
        abort(422)

    return jsonify({
        "success":True,
        "deleted_drink":id
    }), 200



# Error Handling
'''
Example error handling for unprocessable entity
'''


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422
@app.errorhandler(404)
def unprocessable(error):
    return jsonify({
        "success":False,
        "error":404,
        "message":"resource not found"}),404
    

'''
@TODO implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False,
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''

'''
@TODO implement error handler for 404
    error handler should conform to general task above
'''


'''
@TODO implement error handler for AuthError
    error handler should conform to general task above
'''
