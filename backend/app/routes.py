import hashlib
import json
import time

from flask import render_template, jsonify, request

from app import app, lock
from .settings import *


@app.route('/')
@app.route('/index')
def index():
    return 'hello'


@app.route('/label')
def label():
    return render_template('label.html')


@app.route('/ping')
def ping():
    return 'ping'


@app.route('/context')
def context():
    lock.acquire()
    get_condition = {"is_labeled": False, "is_used": False}
    data = table.find_one(get_condition)
    if data is None:
        condition = {"is_labeled": False}
        new_condition = {"is_labeled": False, "is_used": False}
        # results = table.find(condition)
        table.update_many(condition, {"$set": new_condition})
        data = table.find_one(get_condition)
        if data is None:
            return {
                "title": '',
                "title_md5": '',
                "index": '',
                "context": '数据已经处理完'
            }
    print(data)
    data["is_used"] = True
    condition = {"title_md5": data['title_md5'], "index": data['index']}
    table.update_one(condition, {"$set": data})
    lock.release()
    print(data)
    out = {
        "title": data['title'],
        "title_md5": data['title_md5'],
        "index": data['index'],
        "context": data['context']
    }
    # response = make_response(jsonify(out))
    # response.headers['Access-Control-Allow-Origin'] = '*'
    # response.headers['Access-Control-Allow-Methods'] = 'PUT,GET,POST,DELETE,OPTIONS'
    # response.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'

    return jsonify(out)


@app.route('/context_v2')
def context_v2():
    lock.acquire()
    get_condition = {"is_labeled": False, "is_used": False}
    data = table_v2.find_one(get_condition)
    if data is None:
        condition = {"is_labeled": False}
        new_condition = {"is_labeled": False, "is_used": False}
        # results = table.find(condition)
        table_v2.update_many(condition, {"$set": new_condition})
        data = table_v2.find_one(get_condition)
        if data is None:
            return jsonify({
                "title": '',
                "title_md5": '',
                "index": '',
                "context": '数据已经处理完'
            })
    print(data)
    data["is_used"] = True
    condition = {"title_md5": data['title_md5'], "index": data['index']}
    table_v2.update_one(condition, {"$set": data})
    lock.release()
    print(data)
    out = {
        "title": data['title'],
        "title_md5": data['title_md5'],
        "index": data['index'],
        "context": data['context']
    }
    # response = make_response(jsonify(out))
    # response.headers['Access-Control-Allow-Origin'] = '*'
    # response.headers['Access-Control-Allow-Methods'] = 'PUT,GET,POST,DELETE,OPTIONS'
    # response.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'

    return jsonify(out)


@app.route('/put_question_ans', methods=['POST'])
def put_question_ans():
    data = json.loads(request.data)
    condition = {"title_md5": data['mongo_data']['title_md5'], "index": data['mongo_data']['index']}
    mongo_data = table.find_one(condition)
    if mongo_data is None:
        return 'error'
    mongo_data['question_answer'] = data['labels']
    mongo_data['user_name'] = data['user']['name']
    mongo_data['user_email'] = data['user']['name']
    mongo_data['version'] = int(time.time())
    mongo_data['is_labeled'] = True
    mongo_data['is_used'] = False
    table.update_one(condition, {'$set': mongo_data})
    # print("success")
    return "success"


@app.route('/get_context_to_check')
def get_context_to_check():
    lock.acquire()
    condition = {'is_all_checked': False, 'is_used': False, 'is_labeled': True}
    mongo_data = table_v2.find_one(condition)
    t = int(time.time())
    if mongo_data is None:
        return jsonify({
            "title": '',
            "title_md5": '',
            "index": 0,
            "is_labeled": False,
            "is_used": False,
            "is_all_checked": False,
            "user_name": "",
            "user_email": "",
            "context": '数据已经处理完',
            "question_answer": [],
            "version": t
        })
    print(mongo_data)
    mongo_data['is_used'] = True
    new_condition = {'title_md5': mongo_data['title_md5'], 'index': mongo_data['index']}
    # table_v2.update_one(new_condition, {'$set': mongo_data})
    lock.release()
    del mongo_data['_id']
    return jsonify(mongo_data)


@app.route('/put_question_ans_v2', methods=['POST'])
def put_question_ans_v2():
    data = json.loads(request.data)
    condition = {"title_md5": data['mongo_data']['title_md5'], "index": data['mongo_data']['index']}
    mongo_data = table_v2.find_one(condition)
    if mongo_data is None:
        return 'error'
    mongo_data['question_answer'] = data['labels']
    mongo_data['user_name'] = data['user']['name']
    mongo_data['user_email'] = data['user']['name']
    mongo_data['version'] = int(time.time())
    mongo_data['is_labeled'] = True
    mongo_data['is_used'] = False
    mongo_data['is_all_checked'] = False
    table_v2.update_one(condition, {'$set': mongo_data})
    # print("success")
    return "success"


@app.route('/checkEmail', methods=['POST'])
def check_email():
    data = json.loads(request.data)
    print(data)
    condition = {"user_email": data['email']}
    mongo_data = table_user.find_one(condition)
    print(mongo_data)
    if mongo_data is not None:
        return 'success'
    return 'error'


@app.route('/register', methods=['POST'])
# @CORS.cross_origin()
def register():
    form = json.loads(request.data)['form']
    password_md5 = hashlib.md5(form['password'].encode(encoding='UTF-8')).hexdigest()
    mongo_data = {'user_email': form['email'], 'user_name': form['name'], 'password_md5': password_md5}
    print(mongo_data)
    try:
        table_user.insert_one(mongo_data)
    except:
        return 'error'
    return 'success'


@app.route('/login', methods=['POST'])
def login():
    form = json.loads(request.data)['form']
    condition = {'user_email': form['email']}
    ans = table_user.find_one(condition)
    if ans is None:
        return 'wa'
    password_md5 = hashlib.md5(form['password'].encode(encoding='UTF-8')).hexdigest()
    if ans['password_md5'] == password_md5:
        return ans['user_name']
    return 'wa'
