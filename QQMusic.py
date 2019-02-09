#歌曲id，在列表页里有

#1.查找多首歌之间的连接有什么不同？
#http://isure.stream.qqmusic.qq.com/C400003ZYkMo3g8c2U.m4a?vkey=B2972B6FFC4C72CD982A2B0F42E1ADD205BC6BE2FAC6776263A1A7FF98774BD8838DE7850A91D3AB59CDD709DFC8296C1D6B6B3DB006C209&guid=674695650&uin=0&fromtag=66
#http://isure.stream.qqmusic.qq.com/C4000006FOpH2XBod0.m4a?vkey=41895D671207873E9979D6B3D4BCE3301C07FEF448E851E5C6CB0A8AE1A1090D34FFCF6035E156EDDE3B8A3AF4266EEBFEBAD26BA456FC9B&guid=674695650&uin=0&fromtag=66
#http://isure.stream.qqmusic.qq.com/C400001BqoH92Me5XP.m4a?vkey=B4BC955B4553D525269996866811545E3CD69D05663D499ECA982472CDFD98D10B4103AD29D5A21835F1EBDE15B2C2F63F24C8462E70F8CF&guid=674695650&uin=0&fromtag=66
#http://isure.stream.qqmusic.qq.com/C4000032ZOkm0LBgHW.m4a?vkey=19522967936D070DF01A42193FC14E633B3564B9CE3D2CCC524CC47F763A8B5A7FE94214AF030F0ED9318FD1B79DFDDA4A70CF85762AB453&guid=674695650&uin=0&fromtag=66
# url="http://isure.stream.qqmusic.qq.com/C400003lWqnk4QckKI.m4a?vkey=2EDAD31EFE978395021A6C1ACB78F31A9823C8DA338A5A82070427C53C97D39A252EBD5F0F8EE31EBD8A592FA157BD45D68A824427ADF523&guid=3231507578&uin=0&fromtag=66"
#不同点，歌曲名字不同，vkey不同，
#对比列表页发现，列表页的歌曲连接里有 https://y.qq.com/n/yqq/song/001BqoH92Me5XP.html
#001BqoH92Me5XP  跟 真正的下载歌曲连接 filename部分 相同，只是拼接了  C400++.m4a
#vkey 在哪？
#在控制台network里找到了一个url连接返回值带有 filename和vkey的
#链接
#https://c.y.qq.com/base/fcgi-bin/fcg_music_express_mobile3.fcg  -----https://c.y.qq.com/base/fcgi-bin/fcg_music_express_mobile3.fcg
#
# jsonpCallback: MusicJsonCallback9211762249380087----------jsonpCallback: MusicJsonCallback31831938060021003
#
#                MusicJsonCallback4381652361789885

# callback: MusicJsonCallback9211762249380087----------callback: MusicJsonCallback31831938060021003
# guid  请求时的guid要和歌曲的下载链接处的guid相同
# songmid: 0032ZOkm0LBgHW----------songmid: 004JCcIC4OCi1Q
# filename: C4000032ZOkm0LBgHW.m4a----------filename: C400004JCcIC4OCi1Q.m4a

import random
import requests
import json
import re
import os

headers={
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"
}

#有歌曲名，歌曲id获取歌曲的下载链接
def song_id_get_download_url(songname,songid="004JCcIC4OCi1Q"):

    # songid="004JCcIC4OCi1Q" #歌曲id
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
    return {"songname":songname,'songurl':song_url}

def download_music(songinfo,dissname=""):
    base_path="./qq_music"
    if dissname=="":
        save_path=base_path
    else:
        save_path=base_path+'/'+dissname
        if os.path.exists(save_path)==False:
            os.mkdir(save_path)
    r=requests.get(songinfo['songurl'],headers=headers,stream=True)
    with open(save_path+'/'+songinfo['songname']+".mp3",'wb') as file:
        for j in r.iter_content(1024):
            file.write(j)
    print("%s下载完成"%songinfo['songname'])

#获取一个歌单里所有的音乐名称和id
def songlist(disstid="3851947927"):
    # 每日新歌：牛奶咖啡呈上恋爱加油歌
    list_url="https://c.y.qq.com/qzone/fcg-bin/fcg_ucc_getcdinfo_byids_cp.fcg?type=1&json=1&utf8=1&onlysong=0&disstid=%s&format=jsonp&g_tk=5381&jsonpCallback=playlistinfoCallback&loginUin=0&hostUin=0&format=jsonp&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0"%disstid
    headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
        "referer":"https://y.qq.com/n/yqq/playlist/4472732881.html",
    }
    r=requests.get(list_url,headers=headers)
    dissname=json.loads(r.text[21:-1])['cdlist'][0]['dissname'] #歌单名
    songs_list=json.loads(r.text[21:-1])['cdlist'][0]['songlist']
    song_list_list=[]
    for one_song in songs_list:
        songname=one_song['songname']
        songname=re.sub("[/\|\*\?\">:<\\\\]",'',songname)
        songid=one_song['songmid']
        song_list_list.append({'songname':songname,"songid":songid}) #所有的歌曲
    return {"song_list":song_list_list,"dissname":dissname}


def search_list(w='邓紫棋',page=1):
    callback=str(random.random())[2:10]

    url="https://c.y.qq.com/soso/fcgi-bin/client_search_cp?ct=24&qqmusic_ver=1298&new_json=1&remoteplace=txt.yqq.center&searchid=%s&t=0&aggr=1&cr=1&catZhida=1&lossless=0&flag_qc=0&p=%d&n=20&w=%s&g_tk=5381&jsonpCallback=MusicJsonCallback%s&loginUin=0&hostUin=0&format=jsonp&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0"%(callback,page,w,callback)
    r=requests.get(url,headers=headers)
    song_dict=json.loads(r.text[26:-1])
    song_list=song_dict['data']['song']['list']
    keyword=song_dict['data']['keyword']
    song_list_list=[]
    for one_song in song_list:
        songname=one_song['name']
        songid=one_song['mid']
        song_list_list.append({"songname":songname,"songid":songid})
    return {'songlist':song_list_list,'keyword':keyword}

# 搜索下载
for page in range(1,2):
    search_song=search_list("邓紫棋",page)
    for one_search in search_song['songlist']:
        one_song=song_id_get_download_url(one_search['songname'],one_search['songid'])
        download_music(one_song,search_song['keyword'])

# https://c.y.qq.com/soso/fcgi-bin/client_search_cp
# searchid: 46220329270224133------searchid: 42252389373975887
# w: 周杰伦------w: 鹿先森乐队
# jsonpCallback: MusicJsonCallback10217751331856206------jsonpCallback: MusicJsonCallback42396228148671344




# song_list=songlist("6042461646")
# for one_song in song_list['song_list']:
#     songinfo=song_id_get_download_url(one_song['songname'],one_song['songid'])
#     download_music(songinfo,song_list['dissname'])


# songinfo=song_id_get_download_url("演员","001Qu4I30eVFYb")
# download_music(songinfo)
