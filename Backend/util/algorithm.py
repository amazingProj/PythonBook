from fastapi import Response, status
from fastapi.responses import JSONResponse

from controller.migration import add_friend
from controller.search import friends, multiple_users, users_friends


def friends_of_friends_algorithm(user_id):
    user_friends, status_code = friends(user_id)

    if status_code == status.HTTP_404_NOT_FOUND:
        return Response(content=f"user id not found {user_id}", status_code=status_code)

    if not user_friends:
        message = "There are no suggestions due to no friends existing for the user."
        return Response(content=message, status_code=status.HTTP_200_OK)

    users_f, response = users_friends(user_friends)
    friends_ids = [friend['friends'] for friend in users_f]
    friends_of_friends = set(
        friend_id for friends_list in friends_ids for friend_id in friends_list if friend_id != user_id)

    result, status_code = multiple_users(list(friends_of_friends))

    result = {"result": result}

    return JSONResponse(content=result, status_code=status_code)


def add_friends_algorithm(new_friends, user_id):
    friends_user, status_code_friends_request = friends(user_id)
    friends_to_add = [friend_id for friend_id in new_friends if not friends_user.__contains__(friend_id)]
    for friend_id in friends_to_add:
        # here is the opposite (friend_id, user_id) because I want the friend to add him the current user as a friend
        add_friend(friend_id, user_id)

    result, status_code = add_friend(user_id, friends_to_add)
    return Response(content=result, status_code=status_code)
