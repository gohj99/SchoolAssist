#!/usr/bin/python
# -*- coding:utf-8 -*-
#SchoolAssist  Copyright (C) 2024  gohj99
# 主程序
import requests
import sfrw
import uvicorn as uvicorn
from fastapi import FastAPI, Request
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import json

# 函数
def get_requests(url):
    headers = {
        'Content-Type': 'application/json',
        'Cookie':str(cookies),
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
        }
    response = requests.get(url, headers=headers, proxies=proxies)
    return eval(response.text.replace('null', 'None').replace('false', 'False').replace('true', 'True'))

def post_requests(url, data):
    headers = {
        'Content-Type': 'application/json',
        'Cookie': str(cookies),
        'X-XSRF-TOKEN': X_XSRF_TOKEN,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
        }
    response = requests.post(url, headers=headers, json=data, proxies=proxies)
    return eval(response.text.replace('null', 'None').replace('false', 'False').replace('true', 'True'))

#等级比较
#需要提供s1和s2
#s1等级高或等于于s2，返回True
#s1等级低于s2，返回False
def djbj(s1_ys, s2_ys):
    s1 = s1_ys
    s2 = s2_ys
    #检测总分
    s1_zf = s1[:s1.find('（')]
    s1 = s1[s1.find('（') + 1 :]
    s2_zf = s2[:s2.find('（')]
    s2 = s2[s2.find('（') + 1 :]
    if dj_list.index(s1_zf) != dj_list.index(s2_zf):
        if dj_list.index(s1_zf) < dj_list.index(s2_zf):return True
        return False
    #总分相等，便利检测等级
    for dj in dj_list:
        #检测s1等级
        temp1 = s1.find(dj)
        if temp1 != -1:
            s1_qtdj = s1[temp1 - 1:temp1]
            s1 = s1[temp1 + 1 :]
            try:s1_qtdj = int(s1_qtdj)
            except Exception as e:s1_qtdj = 1
        else:s1_qtdj = 0
        #检测s2等级
        temp2 = s2.find(dj)
        if temp2 != -1:
            s2_qtdj = s2[temp2 - 1:temp2]
            s2 = s2[temp2 + 1 :]
            try:s2_qtdj = int(s2_qtdj)
            except Exception as e:s2_qtdj = 1
        else:s2_qtdj = 0
        #对比s1、s2等级
        if s1_qtdj != s2_qtdj:
            if s1_qtdj > s2_qtdj:return True
            return False
    return True

# 初始化软件

# 加载 .env 文件
load_dotenv()

# 读取环境变量
cookies = os.getenv('COOKIES')
X_XSRF_TOKEN = os.getenv('X_XSRF_TOKEN')
best_school_id = int(os.getenv('BEST_SCHOOL_ID'))
proxies = json.loads(os.getenv('PROXIES'))

school_list = get_requests('https://www.nnzkzs.com/api/services/app/student/GetEnableSchool')['result']
dj_list = ['A+', 'A', 'B+', 'B', 'C+', 'C', 'D', 'E']
req_json = get_requests('https://www.nnzkzs.com/api/services/app/student/GetScore')
all_dj = req_json['result']['sumScore'] + '（' + req_json['result']['combinedScore'] + '）'
print('你的等级为' + all_dj)
sfrw.set_best_school_id(best_school_id)
sfrw.set_proxies(proxies)
sfrw.set_cookies(cookies)

#教程：https://www.pythonheidong.com/blog/article/493123/e5a7af67c2f3c5c76aee/
app = FastAPI(
    docs_url=None,
    redoc_url=None
)  # 必须实例化该类，启动的时候调用，并删除自带文档

class People(BaseModel):  # 必须继承
    name: str
    age: int
    address: str
    salary: float

@app.get('/get_rwqk')
def items(request: Request):
    dq_requests = sfrw.get_situation()
    if dq_requests['situation'] == '你已入围':
        return {
            "code": 200,
            "school": dq_requests['school'],
            "is_finalist": dq_requests['situation'],
            "order": dq_requests['order'],
            "counter_order": dq_requests['counter_order'],
            'runTime': dq_requests['runTime'],
            'best_school_score': dq_requests['best_school_score']
        }
    elif dq_requests['situation'] == '数据加载中':
        return {
            "code": 200,
            "school": dq_requests['school'],
            "is_finalist": dq_requests['situation'],
            "order": dq_requests['order'],
            "counter_order": dq_requests['counter_order'],
            'runTime': dq_requests['runTime'],
            'best_school_score': dq_requests['best_school_score']
        }
    else:
        return {
            "code": 200,
            "school": dq_requests['school'],
            "is_finalist": dq_requests['situation'],
            "order": None,
            "counter_order": None,
            'runTime': dq_requests['runTime'],
            'best_school_score': dq_requests['best_school_score']
        }

@app.get('/check_school_finalist/{school_id}')
def items(school_id: int, request: Request):
    if school_id == 2063:
        school_type = 'guide'
        status = '3'
    else:
        school_type = 'directional'
    for school in school_list:
        if school['schoolCode'] == str(school_id):
            if 'status' not in vars():
                status = school['status']
            req_json = post_requests('https://www.nnzkzs.com/api/services/app/publicityDetail/GetGeneralDetail?schoolCode=' + str(school_id) + '&type=' + school_type + '&status=' + status, {})
            req_json = eval(req_json['result'])
            main_school_score = req_json['lists'][-1]['SumScore'] + '（' + req_json['lists'][-1]['CombinedScore'] + '）'
            for x in range(1, len(req_json['lists'])):
                bj_all_dj = req_json['lists'][-x]['SumScore'] + '（' + req_json['lists'][-x]['CombinedScore'] + '）'
                #print(bj_all_dj)
                if djbj(all_dj, bj_all_dj):
                    continue
                else:
                    break
            return {
                'code': 200,
                'counter_order': x,
                'main_school_score': main_school_score
            }
    return {
                "counter_order": '不存在该学校'
            }

@app.get('/set_school/{school_id}')
def items(school_id: int, request: Request):
    for school in school_list:
        if school['schoolCode'] == str(school_id):
            if school['enInstruction']:
                req_json = post_requests('https://www.nnzkzs.com/api/services/app/student/SaveWish?type=%E6%8C%87%E4%BB%A4%E5%85%BC%E6%8C%87%E5%AF%BC', school)
            else:
                req_json = post_requests('https://www.nnzkzs.com/api/services/app/student/SaveWish?type=%E6%8C%87%E5%AF%BC', school)
            return req_json['result']
    return {
                "result": '不存在该学校'
            }

if __name__ == '__main__':
    uvicorn.run(app=app, host="127.0.0.1", port=38534)
