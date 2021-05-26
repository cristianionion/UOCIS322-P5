import acp_times
import random
from pymongo import MongoClient

client = MongoClient('mongodb://' + os.environ['MONGODB_HOSTNAME'], 27017)
db = client.tododb
db2 = client.difdb


def dbinsert():
    list = [3,1,4,1,5,9]
    for i in range(len(list)):
        db.tododb.insert_one(i)
    return db


def dbdrop():
    db.tododb.drop()
    return db


