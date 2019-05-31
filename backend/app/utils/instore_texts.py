from pymongo import MongoClient
import hashlib
import time
import os

dir_path = '/Users/zixiao/PycharmProjects/untitled1/app/static/Museum_130'
conn = MongoClient('10.102.3.18', port=30017)
db = conn['reading']
table = db['test_v2']


def instore(line, title, t_md5, index):
    t = int(time.time())
    item = table.find_one({"title_md5": t_md5, "index": index})
    if item is None:
        table.insert_one({
            "title": title,
            "title_md5": t_md5,
            "index": index,
            "is_labeled": False,
            "is_used": False,
            "user_name": "",
            "user_email": "",
            "context": line,
            "question_answer": [],
            "version": t
        })
    else:
        print(title + " " + str(index) + " already exits")


def sovle_one(path, title):
    f = open(path)
    title_md5 = hashlib.md5(title.encode(encoding='UTF-8')).hexdigest()
    index = 0
    for line in f.readlines():
        if line != '\n':
            instore(line[:-1], title, title_md5, index)
            index += 1


if __name__ == "__main__":
    # file_name = '上海博物馆.txt'
    # sovle_one(dir_path + '/' + file_name, title=file_name.split('.')[-2])
    for root, dirs, files in os.walk(dir_path):
        print(files)
        for file in files:
            try:
                sovle_one(dir_path + '/' + file, title=file.split('.')[-2])
            except:
                pass
