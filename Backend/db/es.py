from elasticsearch import Elasticsearch
from db.es_conf import (
    POSTS_INDEX_NAME,
    POSTS_INDEX_SETTINGS,
    POSTS_INDEX_MAPPINGS
)

es = Elasticsearch([{"host": "localhost", "port": 9200, "scheme": "http"}])


def create_index():
    if not es.indices.exists(index=POSTS_INDEX_NAME):
        es.indices.create(
            index=POSTS_INDEX_NAME,
            settings=POSTS_INDEX_SETTINGS,
            mappings=POSTS_INDEX_MAPPINGS)