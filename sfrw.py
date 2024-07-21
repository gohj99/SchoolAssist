#!/usr/bin/python
# -*- coding:utf-8 -*-
#SchoolAssist  Copyright (C) 2024  gohj99
# 持续入围异步检测工具
import requests
import threading
import time
import signal

cookies = ''
calculateResult = {}
dqxx_sj = {}
situation = ''
school = ''
order = 0
counter_order = 0
runTime = ''
yqxy_id = 2014
best_school_score = ''

# 创建一个事件对象，用于通知线程停止运行
stop_event = threading.Event()

def signal_handler(sig, frame):
    #print("Caught signal:", sig)
    stop_event.set()  # 设置事件，通知线程停止
    #sys.exit(0)  # 退出主程序

def set_cookies(new_cookies):
    global cookies
    cookies = new_cookies

def set_best_school_id(id: int):
    global yqxy_id
    yqxy_id = id

def set_proxies(list):
    global proxies
    proxies = list

def get_situation():
    return {
        'situation': situation,
        'school': school,
        'order': order,
        'counter_order': counter_order,
        'runTime': runTime,
        'best_school_score': best_school_score
        }

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
        'Cookie':str(cookies),
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
        }
    response = requests.post(url, headers=headers, json=data, proxies=proxies)
    return eval(response.text.replace('null', 'None').replace('false', 'False').replace('true', 'True'))

def main():
    global calculateResult, dqxx_sj, situation, order, counter_order, school, runTime, best_school_score
    print('后台成绩持续查询已开始')
    while not stop_event.is_set():
        time.sleep(0.3)
        if cookies == '':continue
        try:
            #req_json = get_requests('https://www.nnzkzs.com/api/services/app/student/GetScore')
            #all_dj = req_json['result']['sumScore'] + '（' + req_json['result']['combinedScore'] + '）'
            #print('你的等级为' + all_dj)
            situation = '数据加载中'
            req_json = get_requests('https://www.nnzkzs.com/api/services/app/student/GetMatriculateInfo')
            dq_school_id = req_json['result']['signupSchoolCode']
            school = req_json['result']['signupSchoolName']
            #print('你当前选择的学校：' + req_json['result']['signupSchoolName'])
            #print('你当前选择的学校的ID：' + dq_school_id)
            calculateResult = req_json['result']['calculateResult']
            runTime = calculateResult['runTime']
            best_school_score = get_requests('https://www.nnzkzs.com/api/services/app/student/GetStat?highSchoolCodes=' + str(yqxy_id))['result']['guideLevel']
            #print(best_school_score)
            if calculateResult == None:
                #print('数据刷新中')
                situation = '数据刷新中'
                continue
            if calculateResult['calculateType'] == '':
                #print('你未入围')
                situation = '你未入围'
                continue
            else:
                situation = '你已入围'
                if calculateResult['calculateType'] == '非定向':
                    #print('你已入围')
                    order = calculateResult['order']
                    #print('排名为：' + str(calculateResult['order']))
                    req_json = get_requests('https://www.nnzkzs.com/api/services/app/student/GetStat?highSchoolCodes=' + dq_school_id)
                    dqxx_sj = req_json['result']
                    counter_order = dqxx_sj['dirPlan'] - order
                    #print('倒数排名为：' + str(dqxx_sj['dirPlan'] - calculateResult['order']))
                    continue
                elif calculateResult['calculateType'] == '定向':
                    #print('你已入围')
                    order = calculateResult['order']
                    #print('排名为：' + str(calculateResult['order']))
                    req_json = get_requests('https://www.nnzkzs.com/api/services/app/student/GetStat?highSchoolCodes=' + dq_school_id)
                    dqxx_sj = req_json['result']
                    counter_order = dqxx_sj['instPlan'] - order
                    #print('倒数排名为：' + str(dqxx_sj['instPlan'] - calculateResult['order']))
                    continue
                elif calculateResult['calculateType'] == '指导':
                    order = calculateResult['order']
                    req_json = get_requests('https://www.nnzkzs.com/api/services/app/student/GetStat?highSchoolCodes=' + dq_school_id)
                    dqxx_sj = req_json['result']
                    counter_order = dqxx_sj['guidePlan'] - order
                    continue
        except Exception as e:
            situation = '数据刷新中'
            print(e)
            continue
    print('后台成绩持续查询已停止\n最后一次查询数据为')
    print(situation)
    if calculateResult != None:
        print('排名为：' + str(order))
        print('倒数排名为：' + str(counter_order))

if __name__ == '__main__':
    main()
else:
    # 注册信号处理函数
    signal.signal(signal.SIGINT, signal_handler)
    # 创建线程
    thread = threading.Thread(target=main)
    thread.start()
