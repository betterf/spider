import requests
from lxml import etree
import re
import pymysql
import json

def kw_get_job_list(kw="人工智能",page=1):
    url="https://fe-api.zhaopin.com/c/i/sou"
    # pageSize: 60  #每次返回的条数
    # cityId: 538   #城市id
    # workExperience: -1  #工作经验 -1 不限 0000 无经验 0001 一年以下 0103 一到三年  0305 0510 1099
    # education: -1       #学历 7 高中 5 大专  4 本科  3 硕士  1  博士  8 其他
    # companyType: -1     #公司类型   1 国企 5 民营  。。。。
    # employmentType: -1  #职位类型  2 全职 1 兼职  4  实习  5 校园
    # jobWelfareTag: -1   #公司福利  10000  五险一金
    # kw: 人工智能   #搜索关键字
    # kt: 3         #不确定  猜想是关键字类型
    # lastUrlQuery: {"pageSize":"60","jl":"538","kw":"人工智能","kt":"3"}   #上次的请求
    headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"
    }
    params={
        "start":(page-1)*60,
        "pageSize": "100",
        "cityId": "538",
        "workExperience": "-1",
        "education":"-1",
        "companyType": "-1",
        "employmentType": "-1",
        "jobWelfareTag": "-1",
        "kw": kw,
        "kt": "3",
        "lastUrlQuery": '{"pageSize":"60","jl":"538","we":"0103","kw":"人工智能","kt":"3"}'
    }

    r=requests.get(url,params=params,headers=headers)
    all_data=r.json()
    all_jobs=all_data['data']['results']
    all_job_list=[]
    for once_job in all_jobs:
        jobname=once_job['jobName']
        companyname=once_job['company']['name']
        salary=once_job['salary']
        workplace=once_job['city']['display']
        workexp=once_job['workingExp']['name']
        edulevel=once_job['eduLevel']['name']
        companytype=once_job['company']['type']['name']
        companysize=once_job['company']['size']['name']
        lat=once_job['geo']['lat']
        lon=once_job['geo']['lon']

        #公司详细地址没有在返回值里，
        positionurl=once_job['positionURL']
        headers={
            "referer":"https://sou.zhaopin.com/?pageSize=60&jl=538&we=0103&kw=%E4%BA%BA%E5%B7%A5%E6%99%BA%E8%83%BD&kt=3",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"
        }
        position_response=requests.get(positionurl,headers=headers)
        position_regx=re.compile("<b>工作地址：</b>\s<h2>\s(.*?)(\s.*?)?\s</h2>")
        address=position_regx.search(position_response.text)
        if address:
            address=address.group(1)
        else:
            continue

        if lat=='0': #如果从列表里取到的经纬度为0，那么根据实际位置获取经纬度
            result=address_get_location(address)
            print(result)
            lat=result['lat']
            lon=result['lon']

        all_job_list.append({"jobname":jobname,"companyname":companyname,'salary':salary,'workplace':workplace,'workexp':workexp,'edulevel':edulevel,'companytype':companytype,'companysize':companysize,"lat":lat,"lon":lon,"address":address})
        print(jobname)
    return all_job_list

def saveToFile(jobs):
    with open("./ZhiLianData/人工智能.csv",'w',encoding="utf-8") as file:

        for once_job in jobs:
            once_str=list(once_job.values())
            once_str1="::".join(once_str)
            file.write(once_str1+"\n")

def saveToMysql(jobs,searchkeyword=''):
    db=pymysql.connect("localhost","root",'',"zhilian")
    cursor=db.cursor()
    for o in jobs:
        sql="insert into zhilian_data(jobname,companyname,salary,workplace,workexp,edulevel,companytype,companysize,lat,lon,address,searchkeyword) values('%s','%s','%s','%s','%s','%s','%s','%s',%f,%f,'%s','%s')"%(o['jobname'],o['companyname'],o['salary'],o['workplace'],o['workexp'],o['edulevel'],o['companytype'],o['companysize'],float(o['lat']),float(o['lon']),o['address'],searchkeyword)
        cursor.execute(sql)
        db.commit()
    db.close()

#根据地址获取经纬度
def address_get_location(address):
    url="http://api.map.baidu.com/geocoder/v2/?address=%s&output=json&ak=jPRAv0mZ52gDMHCUGrixx2DGnSv87u1Q"%address
    r=requests.get(url)
    result=r.json()
    lon=result['result']['location']['lng']
    lat=result['result']['location']['lat']
    return {"lon":lon,"lat":lat}

# print(address_get_location("上海市普陀区李子园"))



# kw="人工智能"
# for page in range(1,3):
#     jobs_list=kw_get_job_list(kw,page)
#     saveToMysql(jobs_list,kw)

# 把得到的数据保存到json文件里，前台js页面调用
#json.loads() 把json字符串转换为Python 字典或者列表
#json.dumps() 把列表或者字典转换为json字符串

jobs_list=kw_get_job_list()
json_str=json.dumps(jobs_list)
print(json_str)

with open("zhilian_data.json",'w',encoding='utf-8') as file:
    file.write(json_str)