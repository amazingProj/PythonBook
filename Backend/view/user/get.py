from fastapi import APIRouter, Response, status
from fastapi.responses import JSONResponse
from controller.search import \
    (user as search_user, friends, gender, matches)
from model.user_model import T
from util.fastapi_custom_response import create_json_response

router = APIRouter()


@router.get("/{user_id}")
async def user_by_id(user_id):
    return create_json_response(search_user(user_id))


@router.get("/matches/{user_id}")
async def user_matches(user_id: T):
    gender_of_user = gender(user_id)
    return create_json_response(matches(gender_of_user))


@router.get("/suggestions/{user_id}")
async def user_suggestions(user_id: T):
    friends_dict = set()

    friends_user, status_code = friends(user_id)

    if status_code == status.HTTP_404_NOT_FOUND:
        return Response(content=friends_user, status_code=status_code)

    friends_of_friends = []

    if not friends_user:
        response = Response(content="There are no suggestions due to no friends existing for the user.",
                            status_code=status.HTTP_200_OK)
        return response

    for friend_id in friends_user:
        response, status_code = friends(friend_id)
        if isinstance(response, str):
            friends_of_friends.extend(response)
        elif isinstance(response, list):
            for friend_of_friend_id in response:
                if friend_of_friend_id == user_id:
                    continue
                friends_of_friends.append(friend_of_friend_id)

    for friend in friends_of_friends:
        if isinstance(friend, list):
            friend_id = ''.join(friend)  # Join the characters into a single string
            friends_dict.add(friend_id)
        elif isinstance(friend, str):
            friends_dict.add(friend)

    result = {"result": []}
    for friend_id in list(friends_dict):
        response, status_code = search_user(friend_id)
        result["result"].append(response)

    response = JSONResponse(content=result, status_code=status_code)
    return response


@router.get("/friends/{user_id}")
async def user_friends(user_id: T):
    response, status_code = friends(user_id)
    array_result = []
    for friend_id in response:
        new_response, new_status_code = search_user(friend_id)
        array_result.append(new_response)

    result = {"result": array_result}
    es_response = JSONResponse(content=result, status_code=status_code)
    return es_response
