from model.user_model import T


def login_query(email: str, password: str):
    query = {
        'query': {
            'bool': {
                'must': [
                    {'match': {'email': email}},
                    {'match': {'password': password}}
                ]
            }
        }
    }
    return query


def user_exclude_friend(user_id: T):
    query = {
        '_source': {
            'excludes': ['friends']
        },
        'query': {
            'bool': {
                'must': [{'match': {'_id': user_id}}],
            }
        }
    }

    return query


def delete_all_query() -> dict:
    delete_query = {
        "query": {
            "match_all": {}
        }
    }

    return delete_query


def user_friends_query(user_id: T):
    query = {
        "_source": "friends",
        "query": {
            "bool": {
                "must": [
                    {"term": {"_id": user_id}}
                ]
            }
        }
    }
    return query
