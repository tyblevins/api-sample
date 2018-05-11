import json
import os
import uuid

import redis
from flask import Flask, request, jsonify, abort
from schematics.exceptions import DataError
from schematics.models import Model
from schematics.types import IntType, StringType, FloatType
from schematics.types.compound import ModelType, ListType

app = Flask(__name__)

REDIS_HOST = os.environ.get('DB_PORT_6379_TCP_ADDR')


class User(Model):
    age = IntType(required=True)
    gender = StringType(required=True, choices=['male', 'female'])


class Household(Model):
    members = ListType(ModelType(User), required=True, min_size=1)
    income = FloatType(required=True)


def get_fpl_pct(income, members):
    n = members - 1
    fpl_guideline = 12140.0 + (n * 4320.0)
    return income / fpl_guideline


def get_redis_connection():
    return redis.StrictRedis(host=REDIS_HOST)


@app.route('/sample-household/', methods=['GET'])
def get_sample_household():
    """ Retrieves a static, sample household object

    This route exists to demonstrate the schema for a Household object.
    It does not touch Redis.
    """
    sample_household = Household({
        'income': 50000,
        'members': [
            {'age': 45, 'gender': 'female'},
            {'age': 40, 'gender': 'male'},
        ],
    })

    return jsonify(sample_household.to_primitive()), 200


@app.route('/')
def index():
    return "Household API"


@app.route('/household/<hh_id>', methods=['GET'])
def get_household(hh_id):
    """ Retrieves a created household object

    The Household ID is specified in the URL. Invalid IDs will return a 400 response.
    e.g. http://0.0.0.0:5000/household/194411f0-2afa-11e8-9e68-0242ac110003
    """
    r = get_redis_connection()
    try:
        hh = json.loads(r.get(hh_id))
    except TypeError:
        abort(400)
    return jsonify(hh), 200


@app.route('/household/', methods=['POST'])
def create_household():
    """ Creates a Household object

    Invalid payloads will return a 400 response.

    :return: unique Household ID for later references to object.
    {"household_id": "194411f0-2afa-11e8-9e68-0242ac110003"}
    """
    if not request.json or 'income' not in request.json or 'members' not in request.json:
        abort(400)
    hh = {
        'income': request.json['income'],
        'members': request.json['members']
    }
    try:
        Household(hh).validate()
    except DataError:
        abort(400)
    uid = uuid.uuid1()  # generate unique ID
    r = get_redis_connection()
    r.set(uid, json.dumps(Household(hh).to_primitive()))
    return jsonify({'household_id': uid}), 200


@app.route('/fpl/<hh_id>', methods=['GET'])
def household_fpl(hh_id):
    """ Calculates fpl percentage of specified Household

    The Household ID is specified in the URL. Invalid IDs will return a 400 response.
     eg.   http://0.0.0.0:5000/fpl/194411f0-2afa-11e8-9e68-0242ac110003

    :return: fpl percentage (float)
    0.5 -> 50%
    """
    r = get_redis_connection()
    try:
        hh = Household(json.loads(r.get(hh_id)))
    except TypeError:
        abort(400)
    return jsonify(get_fpl_pct(hh.income, len(hh.members))), 200


@app.route('/household/<hh_id>', methods=['PUT'])
def update_household(hh_id):
    if not request.json or 'income' not in request.json or 'members' not in request.json:
        abort(400)
    hh = {
        'income': request.json['income'],
        'members': request.json['members']
    }
    try:
        Household(hh).validate()
    except DataError:
        abort(400)
    r = get_redis_connection()
    r.set(hh_id, json.dumps(Household(hh).to_primitive()))
    return jsonify(Household(hh).to_primitive()), 200


@app.route('/household/<hh_id>', methods=['DELETE'])
def delete_household(hh_id):
    r = get_redis_connection()
    r.delete(hh_id)
    return "{} deleted".format(hh_id), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
