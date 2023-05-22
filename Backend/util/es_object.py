def extract_hits(es_object):
    return [hit['_source'] for hit in es_object.body['hits']['hits']]


def extract_first_hit(es_object):
    return extract_hits(es_object)[0]


def extract_data_from_es_response(es_response):
    status_code = es_response.meta.status
    new_user_id = es_response.body['_id']
    return new_user_id, status_code
