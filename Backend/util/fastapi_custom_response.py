from fastapi import Response
from fastapi.responses import JSONResponse


def create_json_response(tuple_message_status):
    message, status_code = tuple_message_status
    result = {"result": message}
    es_response = JSONResponse(content=result, status_code=status_code)
    return es_response


def create_ordinary_response(tuple_message_status):
    message, status_code = tuple_message_status
    response = Response(content=str(message), status_code=status_code)
    return response
