from settings import *
import os
import hashlib
import time

condition = {"is_labeled": False, "is_used": True}
new_condition = {"is_labeled": False, "is_used": False}
# results = table.find(condition)
table.update_many(condition, {"$set": new_condition})

# path = '/Users/zixiao/work/annotation/backend/app/static/Museum_130'
# out = []
# for (root, dirs, files) in os.walk(path):
#     print(files)
# t = int(time.time())
# for file in files:
#     f = open(path + '/' + file)
#     index = 0
#     title = file.split('.')[0]
#     for line in f.readlines():
#         if len(line) > 1:
#             out.append({
#                 "title": title,
#                 "title_md5": hashlib.md5(title.encode(encoding='UTF-8')).hexdigest(),
#                 "context": line[:-1],
#                 "is_labeled": False,
#                 "is_used": False,
#                 "user_name": "",
#                 "user_email": "",
#                 "question_answer": [],
#                 "version": t
#             })
# table.insert_many(out)
# print(out)
