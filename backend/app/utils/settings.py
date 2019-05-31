from pymongo import MongoClient

dir_path = '/Users/zixiao/PycharmProjects/untitled1/app/static/Museum_130'
conn = MongoClient('10.102.3.18', port=30017)
db = conn['reading']
table = db['test']
