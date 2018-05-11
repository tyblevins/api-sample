import json

import requests

headers = {'Content-Type': 'application/json'}

sample = {u'members': [{u'gender': u'female', u'age': 45}, {u'gender': u'male', u'age': 40}], u'income': 50000.0}
good_data = '{"members": [{"gender": "female", "age": 22}, {"gender": "male", "age": 25}], "income": 16460.0}'
bad_data = '{"members": [{"gender": "female", "age": "twenty-two"}], "income": 16460.0}'
update_data = '{"members": [{"gender": "male", "age": 25}], "income": 20000.0}'


def create_household(data):
    r = requests.post('http://0.0.0.0:5000/household/', data=data, headers=headers)
    return r


def test_api_connection():
    r = requests.get('http://0.0.0.0:5000/')
    assert r.status_code == 200


def test_sample_household():
    r = requests.get('http://0.0.0.0:5000/sample-household/')
    assert r.json() == sample


def test_create_household():
    r = create_household(good_data)
    assert r.status_code == 200


def test_get_household():
    r = create_household(good_data)
    hh_id = r.json()['household_id']
    r2 = requests.get('http://0.0.0.0:5000/household/' + hh_id)
    assert r2.status_code == 200
    assert r2.json() == json.loads(good_data)


def test_fpl_calc():
    r = create_household(good_data)
    hh_id = r.json()['household_id']
    r2 = requests.get('http://0.0.0.0:5000/fpl/' + hh_id)
    assert r2.status_code == 200
    assert r2.json() == 1.0


def test_bad_data():
    r = create_household(bad_data)
    assert r.status_code == 400


def test_invalid_get_household():
    r = requests.get('http://0.0.0.0:5000/household/bad-id')
    assert r.status_code == 400


def test_invalid_fpl_household():
    r = requests.get('http://0.0.0.0:5000/fpl/bad-id')
    assert r.status_code == 400


def test_update_household():
    r = create_household(good_data)
    hh_id = r.json()['household_id']
    r2 = requests.put('http://0.0.0.0:5000/household/' + hh_id, data=update_data, headers=headers)
    assert r2.status_code == 200
    r3 = requests.get('http://0.0.0.0:5000/household/' + hh_id)
    assert r3.json() == json.loads(update_data)


def test_delete_household():
    r = create_household(good_data)
    hh_id = r.json()['household_id']
    r2 = requests.get('http://0.0.0.0:5000/household/' + hh_id)
    assert r2.status_code == 200
    requests.delete('http://0.0.0.0:5000/household/' + hh_id)
    r3 = requests.get('http://0.0.0.0:5000/household/' + hh_id)
    assert r3.status_code == 400
