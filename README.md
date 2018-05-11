# Household Resource REST API
by Tyler Blevins

To start the API, run up.sh (`bash up.sh`) from the terminal. Once the docker containers are up and running, you may make requests.
Additionally, unit tests can be evaluated by running test.sh (`bash test.sh`)from the terminal if the docker containers are up.  Stop the application
by hitting `ctrl+C` in the terminal where `up.sh` was run.

## The Rationale
To demonstrate my API knowledge, I wanted to develop a sample REST API that allows an API consumer to create a household and read it back later.
The API required the following elements.

1. Ability to create a new Household resource.
2. Ability to retrieve Household resources by unique ID.
3. Return an HTTP 400 Bad Request response if API users try to create a household with an invalid format.
4. Ability to retrieve a Household's percentage of Federal Poverty Level

#### Additional functionality

1. Ability to update an existing Household.
2. Ability to delete an existing Household.


## Routing
### `/household/`
Endpoint for household creation. 

**METHOD** - `PUT`

**EXAMPLE PAYLOAD** - `'{"members": [{"gender": "female", "age": 22}, {"gender": "male", "age": 25}], "income": 16460.0}'`

**EXAMPLE REQUEST** - `curl -i -H "Content-Type: application/json" -X POST -d '{"income": 80000, "members": [{"age": 27, "gender": "female"}, {"age": 29, "gender": "male"}]}' http://0.0.0.0:5000/household/`

**EXAMPLE RESPONSE** - 
```HTTP/1.0 200 OK 
Content-Type: application/json 
Content-Length: 61 
Server: Werkzeug/0.14.1 Python/2.7.14 
Date: Sun, 18 Mar 2018 23:27:18 GMT

{ 
  "household_id": "e654dd7e-2b03-11e8-9e68-0242ac110003" 
}
```
### `/household/<household_id>`
Endpoint for retrieving, updating, or deleting a household resource

**METHOD** - `GET`

**EXAMPLE REQUEST** `curl http://0.0.0.0:5000/household/e654dd7e-2b03-11e8-9e68-0242ac110003`

**EXAMPLE RESPONSE** - \
```{ 
  "income": 80000, 
  "members": [ 
    { 
      "age": 27, 
      "gender": "female" 
    }, 
    { 
      "age": 29, 
      "gender": "male" 
    } 
  ] 
} 
```

**METHOD** - `PUT`

**EXAMPLE PAYLOAD** - `'{"members": [{"gender": "female", "age": 22}, {"gender": "male", "age": 25}], "income": 16460.0}'`

**EXAMPLE REQUEST** - `curl -i -H "Content-Type: application/json" -X PUT -d '{"income": 140000, "members": [{"age": 25, "gender": "female"}, {"age": 25, "gender": "male"}]}' http://0.0.0.0:5000/household/`

```{ 
  "income": 140000, 
  "members": [ 
    { 
      "age": 25, 
      "gender": "female" 
    }, 
    { 
      "age": 25, 
      "gender": "male" 
    } 
  ] 
} 
```

**METHOD** - `DELETE`

**EXAMPLE REQUEST** - `curl -i -X DELETE http://0.0.0.0:5000/household/e654dd7e-2b03-11e8-9e68-0242ac110003`

**EXAMPLE RESPONSE** - 
```HTTP/1.0 200 OK
Content-Type: text/html; charset=utf-8
Content-Length: 44
Server: Werkzeug/0.14.1 Python/2.7.14
Date: Mon, 19 Mar 2018 01:26:48 GMT

8200d0ce-2b14-11e8-8363-0242ac110003 deleted
```

### `/fpl/<household_id>`
Endpoint for retrieving the percentage of Federal Poverty Level for a household

**METHOD** - `GET`

**EXAMPLE REQUEST** - `http://0.0.0.0:5000/fpl/e654dd7e-2b03-11e8-9e68-0242ac110003`

**EXAMPLE RESPONSE** - 
```8.50546780072904```

## Unit Tests
Unit tests can be found in `/test_api.py`.
* test_api_connection()
* test_sample_household()
* test_create_household()
* test_bad_data()
* test_get_household()
* test_fpl_calc()
* test_invalid_get_household()
* test_invalid_fpl_household()
* test_update_household()
* test_delete_household()

Unit tests are evaluated upon running `bash test.sh` from the terminal after `bash up.sh`. This script docker exec's into
the `api-sample_web_1` container and runs `pytest -v` from the root directory.

### test_api_connection()
Checks for 200 OK response from host.

### test_sample_household()
Checks that `/sample-household/` returns the sample household data.

### test_create_household()
Checks that household creation returns 200 OK response.

### test_bad_data()
Checks that an HTTP 400 Bad Request response is returned if API users try to create a household with an invalid format.

### test_get_household()
Checks that a household object can be retrieved after household creation.

### test_fpl_calc()
Checks that a percentage of Federal Poverty Level can be retrieved after household creation.

### test_invalid_household()
Checks that an HTTP 400 Bad Request response is returned if an unknown household id is supplied when requesting household resource.

### test_invalid_fpl_household()
Checks that an HTTP 400 Bad Request response is returned if an unknown household id is supplied when requesting percentage of Federal Poverty Limit.

### test_update_household()
Checks that an existing household can be successfully updated.

### test_delete_household()
Checks that an existing household can be successfully deleted.