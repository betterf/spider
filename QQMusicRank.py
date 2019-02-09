'''
Created on 2019年1月23日

@author: LF
# '''
import requests
import re
import json
import random
import sys
import time
# {'Franking_value': '937592', 'cur_count': '937592', 'data': {'albumdesc': '', 'albumid': 5880120, 'albummid': '001vMyUg24lPJE', 'albumname': '歌手第三季 第2期', 'alertid': 42, 'belongCD': 1, 'cdIdx': 0, 'interval': 282, 'isonly': 1, 'label': '0', 'msgid': 13, 'pay': {'payalbum': 0, 'payalbumprice': 0, 'paydownload': 1, 'payinfo': 1, 'payplay': 1, 'paytrackmouth': 1, 'paytrackprice': 200, 'timefree': 0}, 'preview': {'trybegin': 0, 'tryend': 0, 'trysize': 960887}, 'rate': 23, 'singer': [{'id': 14013, 'mid': '004COQ9L4X13uj', 'name': '吴青峰'}], 'size128': 4523358, 'size320': 11308089, 'size5_1': 0, 'sizeape': 0, 'sizeflac': 49185728, 'sizeogg': 5608272, 'songid': 227979846, 'songmid': '000V5DnN0ZkPhg', 'songname': '我们 (Live)', 'songorig': '我们', 'songtype': 0, 'strMediaMid': '000V5DnN0ZkPhg', 'stream': 1, 'switch': 17405697, 'type': 0, 'vid': ''}, 'in_count': '3.75', 'old_count': '0'}
#请看每个排行榜的地址栏    https://y.qq.com/n/yqq/toplist/(这个括号里面的数字为topid).html    比如
#巅峰榜·流行指数    topid=4
#topid可能会发生变化
#song_begin是从第几首个开始下载    注意song_begin=0是第一首
#song_num是从第song_begin开始下多少首歌    song_num=30下载30首歌
#date是当天2019-01-23也可能是下个月2019_02
topid,song_begin,song_num,date='58','0','60','2019_02'
# url="https://c.y.qq.com/v8/fcg-bin/fcg_v8_toplist_cp.fcg?tpl=3&page=detail&date=2019-01-23&topid=%s&type=top&song_begin=%s&song_num=%s&g_tk=1040850964&jsonpCallback=MusicJsonCallbacktoplist&hostUin=0&format=jsonp&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0"%(topid,song_begin,song_num)
url="https://c.y.qq.com/v8/fcg-bin/fcg_v8_toplist_cp.fcg?tpl=3&page=detail&date=%s&topid=%s&type=top&song_begin=%s&song_num=%s&g_tk=1040850964&jsonpCallback=MusicJsonCallbacktoplist&hostUin=0&format=jsonp&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0"%(date,topid,song_begin,song_num)
headers={
         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"
     }
response=requests.get(url,headers=headers)
songinfo=json.loads(response.text[26:-1])
print(songinfo['songlist'])
# {'Franking_value': '937592', 'cur_count': '937592', 'data': {'albumdesc': '', 'albumid': 5880120, 'albummid': '001vMyUg24lPJE', 'albumname': '歌手第三季 第2期', 'alertid': 42, 'belongCD': 1, 'cdIdx': 0, 'interval': 282, 'isonly': 1, 'label': '0', 'msgid': 13, 'pay': {'payalbum': 0, 'payalbumprice': 0, 'paydownload': 1, 'payinfo': 1, 'payplay': 1, 'paytrackmouth': 1, 'paytrackprice': 200, 'timefree': 0}, 'preview': {'trybegin': 0, 'tryend': 0, 'trysize': 960887}, 'rate': 23, 'singer': [{'id': 14013, 'mid': '004COQ9L4X13uj', 'name': '吴青峰'}], 'size128': 4523358, 'size320': 11308089, 'size5_1': 0, 'sizeape': 0, 'sizeflac': 49185728, 'sizeogg': 5608272, 'songid': 227979846, 'songmid': '000V5DnN0ZkPhg', 'songname': '我们 (Live)', 'songorig': '我们', 'songtype': 0, 'strMediaMid': '000V5DnN0ZkPhg', 'stream': 1, 'switch': 17405697, 'type': 0, 'vid': ''}, 'in_count': '3.75', 'old_count': '0'}
# sys.exit(0)
print('开始下载歌曲')
start=time.time()
for i in songinfo['songlist']:
    songname=i["data"]['songname']
    songname=re.sub("[/\|\*\?\">:<\\\\]",'',songname)
    songid=i["data"]['songmid']
    getvkeyurl="https://c.y.qq.com/base/fcgi-bin/fcg_music_express_mobile3.fcg"
    callback="MusicJsonCallback"+str(random.random())[2:10]
    filename="C400"+songid+".m4a"
    getvkeyparams={
        "g_tk": "5381",
        "jsonpCallback": callback,
        "loginUin": "0",
        "hostUin": "0",
        "format": "json",
        "inCharset": "utf8",
        "outCharset": "utf - 8",
        "notice": "0",
        "platform": "yqq",
        "needNewCode": "0",
        "cid": "205361747",
        "callback": callback,
        "uin": "0",
        "songmid": songid,
        "filename": filename,
        "guid": "674695650"
    }
    vkey_response=requests.get(url=getvkeyurl,params=getvkeyparams,headers=headers)
    vkey_response_dict=json.loads(vkey_response.text[26:-1])
    vkey=vkey_response_dict['data']['items'][0]['vkey']

    song_url="http://isure.stream.qqmusic.qq.com/%s?vkey=%s&guid=674695650&uin=0&fromtag=66"%(filename,vkey)
    
    r=requests.get(song_url,headers=headers,stream=True)
    with open('./qq_music/说唱榜/'+songname+".mp3",'wb') as file:
        for j in r.iter_content(1024):
            file.write(j)
    print(songname+'  下载完成')
end=time.time()
print('下载完成，总用时%.2fs'%(end-start))    
# print(response.status_code)  # 打印状态码
# print(response.url)          # 打印请求url
# print(response.headers)      # 打印头信息
# print(response.cookies)      # 打印cookie信息
# print(response.text)  #以文本形式打印网页源码
# print(response.content) #以字节流形式打印
# songname='Wolves'
# with open(save_path+'/'+songname+".mp3",'wb') as file:
#         for j in r.iter_content(1024):
#             file.write(j)
# print("%s下载完成"%songname)









