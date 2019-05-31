from settings import *
from pymongo import MongoClient
import json

import time

from datetime import datetime, timedelta

now = datetime.now()

yestoday = now - timedelta(days=1.5)
yestodayLast = now - timedelta(days=1.5)
tommorow = now + timedelta(days=1)


otherStyleTime = yestoday.strftime("%Y-%m-%d %H:%M:%S")

un_time = int(time.mktime(yestoday.timetuple()))
last_un_time = int(time.mktime(yestodayLast.timetuple()))

print(now)
print(yestoday)
print(yestodayLast)
print(un_time)
print(tommorow)
print(otherStyleTime)




conn = MongoClient('10.102.3.18', port=30017)
db = conn['reading']
table = db['test']
table_v2 = db['test_v2']


def solve(user_name):
    user_name = user_name
    # condition = {"user_name": user_name,"version":{"$lt":un_time,"$gt":last_un_time}}
    condition = {"user_name": user_name, "version": {"$gt": un_time}}
    results = table_v2.find(condition).sort([("version" , 1)])
    data = []
    out = {}
    res_num = 0
    qa_id = 0
    for reslut in results:
        title = reslut['title']
        title_md5 = reslut['title_md5']
        index = reslut['index']
        context = reslut['context']
        question_answers = reslut['question_answer']
        qas = []
        res_num += len(question_answers)
        for question_answer in question_answers:
            if not question_answer['is_impossible']:
                qas.append({
                    "answers": [{
                        "answer_start": question_answer["start"],
                        "text": question_answer['answer'],
                    }],
                    "question": question_answer['question'],
                    "question_id": qa_id,
                    "is_impossible": question_answer['is_impossible']
                })
            else:
                qas.append({
                    "plausible_answers": [{
                        "answer_start": question_answer["start"],
                        "text": question_answer['answer'],
                    }],
                    "answers": [],
                    "question": question_answer['question'],
                    "question_id": qa_id,
                    "is_impossible": question_answer['is_impossible']
                })
            qa_id += 1
        if not title_md5 in out:
            out.update({
                title_md5: {
                    "title": title,
                    'paragraphs': [{
                        "index": index,
                        "context": context,
                        "qas": qas
                    }]
                }
            })
        else:
            out[title_md5]['paragraphs'].append({
                "index": index,
                "context": context,
                "qas": qas
            })
    for item in out:
        data.append(out[item])

    ans = {"data": data}
    f = open('../json2/' + user_name + '.json', 'w+')
    json.dump(ans, f, ensure_ascii=False, indent=2)
    f.close()


if __name__ == "__main__":
    uses = ['hanbingqing', 'renzeyu', 'zhaozihan', 'liuyaping', 'nanqiong']
    for name in uses:
        print(name)
        solve(name)