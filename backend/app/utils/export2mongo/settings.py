#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : settings.py
# @Author: zixiao
# @Date  : 2019-04-25
# @Desc  :
from pymongo import MongoClient

dir_path = '/Users/zixiao/work/annotation/backend/app/static/export'
conn = MongoClient('10.102.3.18', port=30017)
db = conn['reading']
table = db['test_v2']
