"""
@Project ：AutoTest_MeiDuo 
@File ：sync_to_mongo.py
@Author ：张建
@Date ：2022/3/11 10:23 上午 
"""
from bson import ObjectId
from pymongo import MongoClient

from utils.tools import load_yaml, dump_yaml

conn = MongoClient('101.43.61.175', 39006, username="xz_test", password="xz_test_pwd")

info = load_yaml("./info.yaml")
data = load_yaml("./data.yaml")


db = conn.autotest
my_set = db.tp

dump_yaml("./info.yaml", info)


for i in my_set.find():
    print(i)

# my_set.delete_one({'_id': ObjectId("622ac3bdb366cd0794590c8f")})

# my_set.insert_one(info)
