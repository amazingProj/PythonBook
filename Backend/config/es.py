POSTS_INDEX_NAME = "users_index"

POSTS_INDEX_SETTINGS = {
    "number_of_shards": 3,
    "number_of_replicas": 2
}

POSTS_INDEX_MAPPINGS = {
    "properties": {
        "id": {"type": "keyword"},
        "email": {"type": "keyword"},
        "password": {"type": "keyword"},
        "first_name": {"type": "text"},
        "last_name": {"type": "text"},
        "phone_number": {"type": "keyword"},
        "location": {"type": "object"},
        "gender": {"type": "keyword"},
        "relationship_status": {"type": "keyword"},
        "interested_in": {"type": "keyword"},
        "hobbies": {"type": "text"},
        "friends": {"type": "keyword"},
        "published_at": {"type": "date"}
    }
}
