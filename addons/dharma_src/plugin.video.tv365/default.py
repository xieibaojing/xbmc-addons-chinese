# -*- coding: utf-8 -*-
import xbmc, xbmcgui, xbmcplugin, urllib2, urllib, re, sys

######################################################
# TV365网络电视直播插件 - http://www.tv365w.com/ 
######################################################
# Version 1.1.0 2012-03-05 (cmeng)
# a. Convert code to utf-8 for not Chinese OS  
# b. Make plugin compatible for Eden & Dharma

# Version 1.0.0  2010 (originator: Robinttt)
######################################################

UserAgent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'
TVLIST=[["tjtv","推荐电视台"],["gatv","港澳电视台"],["rhtv","日韩电视台"],["CCTV","中央电视台"],["twtv","台湾电视台"],["hwtv","欧美电视台"],["gntv","全国地方台"],["shtv","海电视台"],["gdtv","广东电视台"],["zjtv","浙江电视台"],["hntv","湖南电视台"],["lntv","辽宁电视台"],["jstv","江苏电视台"],["tytv","体育直播频道"],["wxtv","全国卫星频道"],["dwtv","网上动物园"],["dytv","电影频道专区"],["wlgb","网络广播电台"],["MTV","音乐电视台"],["wt","网通用户电视"],["cjgs","财经股市频道"]]

##################################################################################
# Routine to fetech url site data using Mozilla browser
# - deletc '\r|\n|\t' for easy re.compile
# - do not delete ' ' i.e. <space> as some url include spaces
# - unicode with 'replace' option to avoid exception on some url
# - translate to utf8
##################################################################################
def getHttpData(url):
    print url
    req = urllib2.Request(url)
    req.add_header('User-Agent', UserAgent)
    response = urllib2.urlopen(req)
    httpdata = response.read()
    response.close()
    httpdata = re.sub('\r|\n|\t', '', httpdata)
    match = re.compile('<meta.+?charset=["]*(.+?)"').findall(httpdata)
    if not len(match): match = ["gbk"]
    charset = match[0].lower()
    if (charset != 'utf-8') and (charset != 'utf8'):
        httpdata = unicode(httpdata, charset,'replace').encode('utf8')
    return httpdata


##################################################################################
def fetchID(dlist, idx):
    for i in range(0, len(dlist)):
        if dlist[i][0] == idx:
            return dlist[i][1]
    return ''
##################################################################################
def Roots():
    url='http://www.tv365w.com/1.js'
    link = re.sub('\\\\', '', getHttpData(url))
    match=re.compile('<a target="etshowlist" href="list/(.+?).htm" tppabs=".+?">').findall(link)
    num=0
    for p_url in match:
        num=num+1
        url="list/"+p_url+".htm"
        name = fetchID(TVLIST,p_url)
        if name.find('网络广播电台')==-1:
            li=xbmcgui.ListItem(str(num)+'. '+name)
            u=sys.argv[0]+"?mode=1&name="+urllib.quote_plus(name)+"&url="+urllib.quote_plus('http://www.tv365w.com/'+url)
            xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
            print url
        else:
            li=xbmcgui.ListItem(str(num)+'. '+name)
            u=sys.argv[0]+"?mode=3&name="+urllib.quote_plus(name)+"&url="+urllib.quote_plus('http://www.tv365w.com/'+url)
            xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)


##################################################################################
def Channel_TV(url,name):
    li=xbmcgui.ListItem('当前位置：'+name)
    u=sys.argv[0]
    xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li)
    link = getHttpData(url)
    num=0
    match=re.compile('<TD(.+?)/TD>').findall(link)
    for td in match:
        match1=re.compile('href="(.+?)">(.+?)<').findall(td)
        if len(match1)>=1:
            channel=match1[0][1]
            for i in range(0,len(match1)):
                if match1[i][0].find('/itv/')!=-1:
                    num=num+1
                    url='http://www.tv365w.com'+match1[i][0].replace('..','')
                    if i>0:
                        li=xbmcgui.ListItem(str(num)+'. '+channel+match1[i][1])
                    else:
                        li=xbmcgui.ListItem(str(num)+'. '+channel)
                    u=sys.argv[0]+"?mode=2&name="+urllib.quote_plus(channel)+"&url="+urllib.quote_plus(url)
                    xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)


##################################################################################
def Channel_Radio(url,name):
    li=xbmcgui.ListItem('当前位置：'+name)
    u=sys.argv[0]
    xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li)

    num=1
    li=xbmcgui.ListItem(str(num)+'.推荐')
    u=sys.argv[0]+"?mode=4&name="+urllib.quote_plus(name+'>推荐')+"&url="+urllib.quote_plus('http://www.tv365w.com/list/radio.htm')
    xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)

    link = getHttpData(url)
    match=re.compile('href="(.+?)">(.+?)</a>').findall(link)
    for url1,name1 in match:
        if url1.find('/radio/radio')!=-1:
            num=num+1
            li=xbmcgui.ListItem(str(num)+'. '+name1)
            u=sys.argv[0]+"?mode=4&name="+urllib.quote_plus(name+'>'+name1)+"&url="+urllib.quote_plus('http://www.tv365w.com'+url1)
            xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)


##################################################################################
def List_Radio(url,name):
    li=xbmcgui.ListItem('当前位置：'+name)
    u=sys.argv[0]
    xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li)

    link = getHttpData(url)
    match=re.compile('href="(.+?)">(.+?)</a>').findall(link)
    num=0
    for url1,name1 in match:
        if url1.find('new/')!=-1:
            if url1.find('/radio/new/')==-1:
                 url1='http://www.tv365w.com/radio/'+url1
            else:
                 url1='http://www.tv365w.com'+url1
            num=num+1
            li=xbmcgui.ListItem(str(num)+'. '+name1)
            u=sys.argv[0]+"?mode=5&name="+urllib.quote_plus(name1)+"&url="+urllib.quote_plus(url1)
            xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)


##################################################################################
def Path_TV(url,name):
    #获取流媒体地址，mms地址基本都可以，其他地址可能不能用  
    link = getHttpData(url)
    match=re.compile('<param name="URL" value="(.+?)"').findall(link)
    if len(match)>0:
       li=xbmcgui.ListItem('播放：'+name+'  【'+match[0]+'】')
       li.setInfo(type="Video",infoLabels={"Title":name})
       xbmcplugin.addDirectoryItem(int(sys.argv[1]),match[0],li)


##################################################################################
def Path_Radio(url,name):
    #获取流媒体地址，mms地址基本都可以，其他地址可能不能用  
    link = getHttpData(url)
    match=re.compile('"mms://(.+?)"').findall(link)
    if len(match)>0:
       li=xbmcgui.ListItem('播放：'+name+'  【mms://'+match[0]+'】')
       li.setInfo(type="Video",infoLabels={"Title":name})
       xbmcplugin.addDirectoryItem(int(sys.argv[1]),'mms://'+match[0],li)


##################################################################################
def get_params():
    param=[]
    paramstring=sys.argv[2]
    if len(paramstring)>=2:
        params=sys.argv[2]
        cleanedparams=params.replace('?','')
        if (params[len(params)-1]=='/'):
            params=params[0:len(params)-2]
        pairsofparams=cleanedparams.split('&')
        param={}
        for i in range(len(pairsofparams)):
            splitparams={}
            splitparams=pairsofparams[i].split('=')
            if (len(splitparams))==2:
                  param[splitparams[0]]=splitparams[1]
    return param

params=get_params()
mode=None
name=None
url=None
thumb=None


try:
    url=urllib.unquote_plus(params["url"])
except:
    pass
try:
    name=urllib.unquote_plus(params["name"])
except:
    pass
try:
    mode=int(params["mode"])
except:
    pass


if mode==None:
    name=''
    Roots()

elif mode==1:
    Channel_TV(url,name)

elif mode==2:
    Path_TV(url,name)

elif mode==3:
    Channel_Radio(url,name)

elif mode==4:
    List_Radio(url,name)

elif mode==5:
    Path_Radio(url,name)

xbmcplugin.setPluginCategory(int(sys.argv[1]), name )
xbmcplugin.endOfDirectory(int(sys.argv[1]))
