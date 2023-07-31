import time

from fastapi import status
from fastapi.testclient import TestClient
import main
from util.test import *
from util.very_long_id import LONG_ID

from constant import MAXIMUM_LENGTH_ELASTIC_SEARCH_ID, ERROR_MAXIMUM_LENGTH_MESSAGE

client = TestClient(main.app)


def test_get_route():
    # case ordinary existing user id
    response = client.get("/api/user/user/kaj6ZogBES4kQr_fdGqF")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["result"] == data

    # case missing id
    response = client.get("/api/user/user/9")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "User does not exist in database"

    # case null id
    response = client.get("/api/user/user/null")
    assert response.status_code == status.HTTP_400_BAD_REQUEST

    # case too long id
    response = client.get(f"/api/user/user/{LONG_ID}")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == f"{ERROR_MAXIMUM_LENGTH_MESSAGE} {MAXIMUM_LENGTH_ELASTIC_SEARCH_ID}"


def test_register():
    # case already exists user - check conflict
    add_user = {
      "email": "asa@gmail.com",
      "password": "random-password",
      "first_name": "Eyal",
      "last_name": "Tz",
      "phone_number": "0551112231",
      "location": {"x": 9, "y": 10},
      "gender": "male",
      "relationship_status": "single",
      "interested_in": "female",
      "hobbies": ["filming", "programming"]
    }
    response = client.post("/api/user/register", json=add_user)
    assert response.json()["result"] == {}
    assert response.status_code == status.HTTP_409_CONFLICT

    # case missing password in user
    response = client.post("/api/user/register", json=data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    # case entity with additional wrong field "frist_name" instead of "first_name"
    add_user = {
        "email": "asa@gmail.com",
        "password": "random-password",
        "frist_name": "Eyal",
        "last_name": "Tz",
        "phone_number": "0551112231",
        "location": {"x": 9, "y": 10},
        "gender": "male",
        "relationship_status": "single",
        "interested_in": "female",
        "hobbies": ["filming", "programming"]
    }
    response = client.post("/api/user/register", json=add_user)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    # case give in the field interested_in or gender something it is not 'male' or 'female'
    add_user = {
            "email": "asa@gmail.com",
            "password": "random-password",
            "first_name": "Foud",
            "last_name": "Hillel",
            "phone_number": "0519471472",
            "location": {
                "x": 9,
                "y": 10
            },
            "gender": "other",
            "relationship_status": "single",
            "interested_in": "no idea",
            "hobbies": [
                "filming",
                "programming"
            ]
        }

    response = client.post("/api/user/register", json=add_user)
    assert response.status_code == status.HTTP_400_BAD_REQUEST

    # case relationship_status is not valid
    add_user = {
            "email": "asa@gmail.com",
            "password": "random-password",
            "first_name": "Foud",
            "last_name": "Hillel",
            "phone_number": "0519471472",
            "location": {
                "x": 9,
                "y": 10
            },
            "gender": "male",
            "relationship_status": "non of the option",
            "interested_in": "female",
            "hobbies": [
                "filming",
                "programming"
            ]
        }
    response = client.post("/api/user/register", json=add_user)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_get_hobbies():
    # case hobbies array contained in like hobbies=k&p contained in hobbies array [k, p, l]

    response = client.get("/api/user/users?hobbies=programming&filming")
    obj = {'email': 'asa@gmail.com', 'first_name': 'Noa', 'last_name': 'Finkell', 'phone_number': '0515871913', 'location': {'x': 9, 'y': 10},
           'gender': 'female', 'relationship_status': 'single', 'interested_in': 'male', 'hobbies': ['filming', 'programming']}
    print(response.json()["result"])
    assert obj in response.json()["result"]

    # case wrong alias 'hobbbies' instead of 'hobbies'
    response = client.get("/api/user/users?hobbbies=programming&filming")
    assert response.status_code == status.HTTP_400_BAD_REQUEST

    # case no params
    response = client.get("/api/user/users?hobbbies=programming&filming")
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_delete_user():
    # case
    add_user = {
        "email": "orenS@gmail.com",
        "password": "random-password",
        "first_name": "Oren",
        "last_name": "S",
        "phone_number": "03894765",
        "location": {
            "x": 3,
            "y": 9
        },
        "gender": "male",
        "relationship_status": "in_a_relationship",
        "interested_in": "female",
        "hobbies": [
            "programming",
            "empty void **"
        ]
    }
    response = client.post("/api/user/register", json=add_user)
    new_user_id = response.json()["result"]
    time.sleep(2)
    url = f"/api/user/user/{new_user_id}"
    print(url)
    response = client.delete(url)
    assert response.status_code == status.HTTP_200_OK


def test_patch():
    change = {
        "first_name": "Paul"
    }
    client.patch("/api/user/update/gqhcZogBES4kQr_fNmrg", json=change)
    response = client.get("/api/user/user/gqhcZogBES4kQr_fNmrg")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["result"]["first_name"] == change.get("first_name")


def test_get_locations():
    response = client.get("/api/user/users?locationX=9.0&locationY=10")
    obj = {
            "email": "asa@gmail.com",
            "first_name": "Paul",
            "last_name": "Finkell",
            "phone_number": "0529938918",
            "location": {
                "x": 9,
                "y": 10
            },
            "gender": "male",
            "relationship_status": "single",
            "interested_in": "female",
            "hobbies": [
                "filming",
                "programming"
            ]
        }
    assert obj in response.json()["result"]


def test_add_friends():
    # case add multiple friends
    response = client.post("/api/user/friends/OLXWTYgBGjE9aYZBJsUo",
                           json=["iKi_ZogBES4kQr_ftGrm", "eKgwYYgBES4kQr_fbmq9", "k6iEZ4gBES4kQr_f7Gqy"])
    assert response.status_code == status.HTTP_200_OK

    # case no list given
    response = client.post("/api/user/friends/OLXWTYgBGjE9aYZBJsUo-moH", json="h6i_ZogBES4kQr_ftGq3")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_get_friends():
    response = client.get("/api/user/friends/NLXKTYgBGjE9aYZBe8U8")
    assert response.status_code == status.HTTP_200_OK
    for index, res in enumerate(response.json()["result"]):
        print(f"index:{index}")
        print(res) # there is no id field
        assert res in [
        {
            "email": "asa@gmail.com",
            "first_name": "Paul",
            "last_name": "Finkell",
            "phone_number": "0529938918",
            "location": {
                "x": 9,
                "y": 10
            },
            "gender": "male",
            "relationship_status": "single",
            "interested_in": "female",
            "hobbies": [
                "filming",
                "programming"
            ]
        },
        {
            "email": "asa@gmail.com",
            "first_name": "Noa",
            "last_name": "Finkell",
            "phone_number": "0515121913",
            "location": {
                "x": 9,
                "y": 10
            },
            "gender": "female",
            "relationship_status": "single",
            "interested_in": "male",
            "hobbies": [
                "filming",
                "programming"
            ]
        },
        {
            "email": "asa@gmail.com",
            "first_name": "Asaf",
            "last_name": "Finkell",
            "phone_number": "0522929911",
            "location": {
                "x": 9,
                "y": 10
            },
            "gender": "male",
            "relationship_status": "single",
            "interested_in": "female",
            "hobbies": [
                "filming",
                "programming"
            ]
        },
        {
            "email": "asa@gmail.com",
            "first_name": "Paul",
            "last_name": "Finkell",
            "phone_number": "0512931893",
            "location": {
                "x": 9,
                "y": 10
            },
            "gender": "male",
            "relationship_status": "single",
            "interested_in": "female",
            "hobbies": [
                "filming",
                "programming"
            ]
        },
        {
            "email": "asa@gmail.com",
            "first_name": "Noa",
            "last_name": "Finkell",
            "phone_number": "0515871913",
            "location": {
                "x": 9,
                "y": 10
            },
            "gender": "female",
            "relationship_status": "single",
            "interested_in": "male",
            "hobbies": [
                "filming",
                "programming"
            ]
        }
    ]


def test_matches():
    response = client.get("/api/user/matches/d6gZYYgBES4kQr_fU2ot")
    assert response.status_code == status.HTTP_200_OK


def test_suggestions():
    response = client.get("/api/user/suggestions/PLXaTYgBGjE9aYZBacXH")
    assert response.status_code == status.HTTP_200_OK
