from fastapi import APIRouter
from controller.search import \
    (user as search_user, friends, gender, matches)
from view.response import *
from util.es_object import extract_first_hit, extract_hits

router = APIRouter()


@router.get("/matches/{user_id}")
async def user_matches(user_id: T):
    return matches(gender(user_id))


@router.get("/suggestions/{user_id}")
async def user_suggestions(user_id: T):
    print()
# friends_dict = set()
#
# friends_user = friends(user_id)[0]["friends"]
#
# friends_of  _friends = []
# for friend_id in friends_user:
#     friends_of_friends.extend(friends(friend_id))
#
# for friend in friends_of_friends:
#     friends_dict.add(friend)
#
# return list(friends_dict)


#
# @router.get("/suggestions/{user_id}")
# async def user_suggestions(user_id: T):
#     friends_dict = {}
#     friends_user = friends(user_id)
#     friends_user = friends_user[0]["friends"]
#
#     for friend_id in friends_user:
#         friends_to_add = first_hit(friends(friend_id))
#
#         if not friends_to_add:
#             continue
#
#         friends_to_add = friends_to_add["friends"]
#         for key in friends_to_add:
#             friends_dict[key] = None
#
#     return [*friends_dict.keys()]


@router.get("/friends/{user_id}")
async def user_friends(user_id: T):
    return friends(user_id)


@router.get("/{user_id}")
async def user_by_id(user_id):
    return search_user(user_id)




