#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : main.py
# @Author: zixiao
# @Date  : 2019-04-25
# @Desc  :
import hashlib
import os
import time

import bs4
from bs4 import BeautifulSoup

from app.utils.export2mongo.settings import *


def solve_wiki(file_name):
    soup = BeautifulSoup(open(file_name), features="lxml")
    main_content = soup.select('#content #bodyContent #mw-content-text .mw-parser-output')[0]
    items = main_content.contents
    start = 0
    filter_items = []
    for item in items:
        if type(item) != bs4.element.Tag:
            continue
        if 'h' in item.name or item.name == 'p':
            filter_items.append(item)
    while start < len(filter_items):
        if filter_items[start].name == 'h2':
            break
        start += 1
    res = [filter_items[0:start]]
    end = start + 1
    flag_p = False
    while end < len(filter_items):
        if filter_items[end].name == 'h2':
            if not end - start == 1 and flag_p:
                res.append(filter_items[start:end])
            start = end
            flag_p = False
        elif filter_items[end].name == 'p':
            flag_p = True
        end += 1
    if end - 1 < len(filter_items) and not filter_items[end - 1].name == 'h2' and flag_p:
        res.append(filter_items[start:end])
    string_list = []
    for tag_list in res:
        tmp = ''
        for tag in tag_list:
            if 'h' in tag.name:
                tmp += tag.get_text()[:-4] + '\n'
            else:
                tmp += tag.get_text()
        string_list.append(tmp)
    title = soup.select('body h1')[0].get_text()
    title_md5 = hashlib.md5(title.encode(encoding='UTF-8')).hexdigest()
    store_mongo(string_list, title, title_md5)


def store_mongo(string_list: list, title, title_md5):
    t = int(time.time())
    for index, item in enumerate(string_list):
        mongo_item = table.find_one({"title_md5": title_md5, "index": index})
        if mongo_item is None:
            table.insert_one({
                "title": title,
                "title_md5": title_md5,
                "index": index,
                "is_labeled": False,
                "is_used": False,
                "user_name": "",
                "user_email": "",
                "context": item,
                "question_answer": [],
                "version": t
            })
        else:
            print(title + " " + str(index) + " already exits")


def solve_baidu(file_path):
    soup = BeautifulSoup(open(file_path), features="lxml")
    doc_type = soup.contents[0]
    if 'mobile' in doc_type:
        return

    try:
        title = soup.select('.main-content h1')[0].get_text()
        title_md5 = hashlib.md5(title.encode(encoding='UTF-8')).hexdigest()
        main_content = soup.select('.main-content')[0]
        summary = main_content.select('.lemma-summary')[0]
    except:
        return
    contents = main_content.contents
    filter_contents = []
    for item in contents:
        if type(item) != bs4.element.Tag:
            continue
        else:
            if 'class' in item.attrs and 'para' in item['class'][0]:
                filter_contents.append(item)
    string_list = [summary.get_text()[1:]]
    start = 0
    while start < len(filter_contents):
        if filter_contents[start]['class'][-1] == 'level-2':
            break
        start += 1
    end = start + 1
    flag_para = False
    res = []
    while end < len(filter_contents):
        if len(filter_contents[end]['class']) > 1 and filter_contents[end]['class'][-1] == 'level-2':
            if end - start != 1 and flag_para:
                res.append(filter_contents[start:end])
            flag_para = False
            start = end
        elif len(filter_contents[end]['class']) == 1:
            flag_para = True
        end += 1
    if end - 1 < len(filter_contents) and filter_contents[end - 1]['class'][-1] != 'level-2' and flag_para:
        res.append(filter_contents[start:end])

    for tag_list in res:
        tmp = ''
        for tag in tag_list:
            if len(tag['class']) > 1:
                tmp += tag.get_text()[:-2]
            else:
                tmp += tag.get_text()[:]
        string_list.append(tmp)
    store_mongo(string_list, title, title_md5)


if __name__ == '__main__':
    path = dir_path
    print(path)
    baike_files = []
    for root, dirs, files in os.walk(path):
        print(files)
        print(len(files))
        for file in files:
            file_path = path + '/' + file
            print(file)
            if 'baike' in file:
                solve_baidu(file_path)
            elif 'wiki' in file:
                solve_wiki(file_path)
