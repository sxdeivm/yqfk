import requests #爬取网页
import json #json文件可以通过角标索引读取内容 爬取json文件
import datetime
import random
import pymysql
import urllib.request, urllib.parse, urllib.error
import json
import hashlib
import time
import requests
import matplotlib.pyplot as plt
from pylab import mpl
# 设置显示中文字体
mpl.rcParams["font.sans-serif"] = ["SimHei"]
# 设置正常显示符号
mpl.rcParams["axes.unicode_minus"] = False
url = 'https://c.m.163.com/ug/api/wuhan/app/data/list-total?t=329822670771' #请求URL
headers = {'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36 Edg/97.0.1072.55'} #浏览器访问
response = requests.get(url , headers = headers)
print(response)
db = pymysql.connect(host='localhost', port=3306, user='root', passwd='123456', db='db_yiqing_manage_system', charset='utf8')
cursor = db.cursor()
 
# print(response.status_code) #200表示访问成功
# print(response.json()) # 打印内容
def get_url(name):    
    queryStr = '/geocoding/v3/?address={}&output=json&ak={}'.format(name,'m0L5UKvh1AbiUwuLVFZSLkxeGmSEWTe6')
    # 对queryStr进行转码，safe内的保留字符不转换
    encodedStr = urllib.parse.quote(queryStr, safe="/:=&?#+!$,;'@()*[]")
    #由于URL里面含有中文，所以需要用parse.quote进行处理，然后返回最终可调用的url
    url = urllib.parse.quote("http://api.map.baidu.com" + queryStr, safe="/:=&?#+!$,;'@()*[]")
    #print('URL:', url)
    return url

def insertDB(add, confirm, dead, heal,lng,lat):
    try:
        date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        id = ''.join(random.sample(
        ['z', 'y', 'x', 'w', 'v', 'u', 't', 's', 'r', 'q', 'p', 'o', 'n', 'm', 'l', 'k', 'j', 'i', 'h', 'g', 'f', 'e',
         'd', 'c', 'b', 'a'], 5))
        sql = "insert into maps (id,location,create_time,count,lng,lat) values('%s','%s','%s',%d,%d,%d)" % (
        id,add, date,confirm,lng,lat)
        cursor.execute(sql)
        db.commit()
    except Exception as e:
        db.rollback()
        print(e)
 
def toTotal():
    json_data = response.json()['data']['areaTree'][2]['children']  # 中国省份数据
    print(json_data)
    for i in range(34):  # 网页数据显示共有0-33个省份
        proData = json_data[i]  # 每个省份的数据
        add = eval(json.dumps(proData['name']).encode('utf-8').decode('unicode_escape'))  # 省份名，unicode转化为utf-8，去掉两端引号，真累 l_l
        today_confirm = json.dumps(proData['today']['confirm'])  # 确诊数目
        today_dead = json.dumps(proData['total']['dead'])  # 死亡数
        today_heal = json.dumps(proData['total']['heal'])  # 治疗数
        print(add)
        url1 = get_url(add)
        res = requests.get(url1)
        print(res.text)
        jd = json.loads(res.text)   
        coords = jd['result']['location']            # 将json格式转化为Python字典
        print(coords['lng'])
        insertDB(add, int(today_confirm), today_dead, today_heal,float(coords['lng']),float(coords['lat']))

toTotal()
