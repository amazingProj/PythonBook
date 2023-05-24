from fastapi import APIRouter, HTTPException, Depends, Query
from controller.search import locations, hobbies, users
from util.fastapi_custom_response import create_json_response

router = APIRouter()


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
    if hobbies_list is not None:
        return create_json_response(hobbies(hobbies_list))

    if location_x is not None and location_y is not None:
        return create_json_response(locations(location_x, location_y))

    return create_json_response(users())

