from pymongo import MongoClient
import pandas as pd

client = MongoClient(
    "mongodb://4handywork:Utf-8.com@db-hostingviet.4-handy.com:27017,db-vt.4-handy.com:27017,db-kdata.4-handy.com:27017/4handy-work?replicaSet=4handyrs"
)
db = client["4handy-work"]


def find_to_df(collection, query, fields=None):
    if fields:
        results = db[collection].find(query, {field: 1 for field in fields})
    else:
        results = db[collection].find(query)
    return pd.DataFrame(list(results))


def aggregate_to_df(collection, pipeline, columns=None):
    df = db[collection].aggregate(pipeline=pipeline)
    results = pd.DataFrame(list(df), columns=columns)
    return results
