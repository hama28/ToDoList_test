from http import client
from google.cloud import datastore

def get_all():
    client = datastore.Client()
    query = client.query(kind='Account')
    data = list(query.fetch())
    for entity in data:
        entity['id'] = entity.key.id
    return data

def get_by_id():
    client = datastore.Client()
    key = client.key('Account', 5072058866204672)
    entity = client.get(key=key)
    if entity:
        entity['id'] = entity.key.id
    return entity