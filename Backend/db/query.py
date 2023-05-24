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


def user_minimal_details(user_id: T):
    query = {
        "query": {
            "match": {
                "_id": user_id
            }
        },
        "_source": ["gender", "relationship_status", "interested_in", "hobbies", "email", "first_name", "last_name",
                    "phone_number", "location"]
    }
    return query


def user_full_details(user_id: T):
    query = {
        "query": {
            "match": {
                "_id": user_id
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


def user_gender_query(user_id: T):
    query = {
        "_source": "gender",
        "query": {
            "bool": {
                "must": [
                    {"term": {"_id": user_id}}
                ]
            }
        }
    }

    return query


def user_matches_query(gender: str):
    query = {
        "query": {
            "bool": {
                "must": [
                    {"term": {"interested_in": gender}},
                    {'match': {"relationship_status": "single"}}
                ]
            }
        },
        "_source": ["gender", "relationship_status", "interested_in", "hobbies", "email", "first_name", "last_name",
                    "phone_number", "location"]
    }

    return query


def user_phone_query(phone: str):
    query = {
        "query": {
            "match": {
                "phone_number": str(phone)
            }
        },
        "_source": "_id"
    }

    return query


def users_hobbies_query(hobbies):
    query = {
        "query": {
            "bool": {
                "filter": {
                    "terms": {
                        "hobbies": hobbies
                    }
                }
            }
        },
        "_source": ["gender", "relationship_status", "interested_in", "hobbies", "email", "first_name", "last_name",
                    "phone_number", "location"]
    }

    return query


def users_location_query(location_x, location_y):
    query = {
        "query": {
            "bool": {
                "filter": [
                    {
                        "term": {
                            "location.x": location_x
                        }
                    },
                    {
                        "term": {
                            "location.y": location_y
                        }
                    }
                ]
            }
        },
        "_source": ["gender", "relationship_status", "interested_in", "hobbies", "email", "first_name", "last_name",
                    "phone_number", "location"]
    }

    return query


def all_users_query():
    query = {
        "query": {
            "match_all": {}
        },
        "_source": ["gender", "relationship_status", "interested_in", "hobbies", "email", "first_name", "last_name",
                    "phone_number", "location"]
    }

    return query
