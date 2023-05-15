# from elasticsearch import Elasticsearch
# from config.es import (
#     POSTS_INDEX_NAME,
#     POSTS_INDEX_SETTINGS,
#     POSTS_INDEX_MAPPINGS
# )
#
#
# def get_es_client():
#     es = Elasticsearch([{"host": "localhost", "port": 9200, "scheme": "http"}])
#     es.indices.create(
#         index=POSTS_INDEX_NAME,
#         settings=POSTS_INDEX_SETTINGS,
#         mappings=POSTS_INDEX_MAPPINGS
#     )
#
#     try:
#         yield es
#     finally:
#         es.close()
#
# @router.get("/")
# async def get_posts(
#         query: str = Query(alias="q"),
#
# ):

from fastapi import FastAPI
from elasticsearch import Elasticsearch

app = FastAPI()

es = Elasticsearch([{"host": "localhost", "port": 9200, "scheme": "http"}])

index_name = "index"


@app.post("/document")
async def create_document(document: dict):
    response = es.index(index=index_name, body=document)
    return {"message": "Doc Created", "document_id": response["_id"]}


@app.get("/document/{document_id}")
async def get_document(document_id: str):
    response = es.get(index=index_name, id=document_id)
    return {"document": response["_source"]}


@app.get("/")
async def hello_world():
    return {"message": "hello world"}

