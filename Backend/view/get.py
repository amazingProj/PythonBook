from fastapi import APIRouter, Query, HTTPException, Depends
from controller.search import \
    user as search_user, friends, gender, matches, locations, hobbies, users, multiple_users
from model.user_model import T
from util.fastapi_custom_response import create_json_response
from util.algorithm import friends_of_friends_algorithm
from util.validation import check_valid_user_id, check_hobbies_locations


router = APIRouter()


@router.get("/")
async def im_alive():
    return "the service is alive!"


@router.get("/user/{user_id}")
async def user_by_id(user_id: T):
    check_valid_user_id(user_id)
    return create_json_response(search_user(user_id))


@router.get("/matches/{user_id}")
async def user_matches(user_id: T):
    check_valid_user_id(user_id)
    gender_of_user = gender(user_id)
    return create_json_response(matches(gender_of_user))


@router.get("/suggestions/{user_id}")
async def user_suggestions(user_id: T):
    check_valid_user_id(user_id)
    return friends_of_friends_algorithm(user_id)


@router.get("/friends/{user_id}")
async def user_friends(user_id: T):
    check_valid_user_id(user_id)
    friends_of_user, status_code = friends(user_id)
    return create_json_response(multiple_users(friends_of_user))


def validate_locations(location_x: float = Query(None, alias="locationX"), location_y: float = Query(None, alias="locationY")):
    if location_x is None and location_y is None:
        return

    if location_x is not None and location_y is not None:
        return

    raise HTTPException(status_code=400, detail="Both locationX and locationY are required.")


@router.get("/users")
def filter_users(
        hobbies_list: list = Query(None, alias="hobbies"),
        location_x: float = Query(None, alias="locationX"),
        location_y: float = Query(None, alias="locationY"),
        validate = Depends(validate_locations)
):
    check_hobbies_locations(hobbies_list, location_x)
    if hobbies_list is not None:
        return create_json_response(hobbies(hobbies_list))

    if location_x is not None and location_y is not None:
        return create_json_response(locations(location_x, location_y))

    return create_json_response(users())

