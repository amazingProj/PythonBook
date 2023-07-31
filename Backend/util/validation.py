from fastapi import HTTPException, status
from constant import MAXIMUM_LENGTH_ELASTIC_SEARCH_ID, ERROR_MAXIMUM_LENGTH_MESSAGE


def check_valid_user_id(user_id: str):
    if user_id is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Please use alias of user")
    if len(user_id) >= MAXIMUM_LENGTH_ELASTIC_SEARCH_ID:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{ERROR_MAXIMUM_LENGTH_MESSAGE} {MAXIMUM_LENGTH_ELASTIC_SEARCH_ID}")
    if user_id == "":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Not a valid empty user id")
    if user_id == "null":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Not a valid user id {user_id}")
    return


def check_hobbies_locations(hobbies, location_x):
    if hobbies is None and location_x is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="must alias hobbies or locations")
    return
