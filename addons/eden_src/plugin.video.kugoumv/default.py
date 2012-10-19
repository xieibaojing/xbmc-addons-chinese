# -*- coding: utf-8 -*-
############################################################
# 酷狗MV
# v1.0.0 2012/10/16 by runner@gmail.com
############################################################

import xbmc, xbmcgui, xbmcplugin, xbmcaddon, urllib2, urllib, re, string, sys, os, gzip, StringIO,time

#
# Kugou tag
#
UrlBase="http://www.kugou.com/mvweb/html/"

CHANNEL_LIST =[['新歌推荐','http://www.kugou.com/mvweb/html/index_9_1.html'],['LIVE现场', 'http://www.kugou.com/mvweb/html/index_10_1.html'],['经典流行', 'http://www.kugou.com/mvweb/html/index_11_1.html'],['网络热播', 'http://www.kugou.com/mvweb/html/index_12_1.html'],['华语精选', 'http://www.kugou.com/mvweb/html/index_13_1.html'],['欧美日韩', 'http://www.kugou.com/mvweb/html/index_14_1.html'],['星乐坊', 'http://www.kugou.com/mvweb/html/index_15_1.html']]

def GetHttpData(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)')
    try:
        response = urllib2.urlopen(req)
        httpdata = response.read()
        if response.headers.get('content-encoding', None) == 'gzip':
            httpdata = gzip.GzipFile(fileobj=StringIO.StringIO(httpdata)).read()
        charset = response.headers.getparam('charset')
        response.close()
    except:
        print 'GetHttpData Error: %s' % url
        return ''
    match = re.compile('<meta http-equiv=["]?[Cc]ontent-[Tt]ype["]? content="text/html;[\s]?charset=(.+?)"').findall(httpdata)
    if len(match)>0:
        charset = match[0]
    if charset:
        charset = charset.lower()
        if (charset != 'utf-8') and (charset != 'utf8'):
            httpdata = httpdata.decode(charset, 'ignore').encode('utf8', 'ignore')
    return httpdata

def rootList():
    for name, url in CHANNEL_LIST:
        li = xbmcgui.ListItem(name)
        u = sys.argv[0]+"?level=1&url="+url+"&name="+name
        xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

def catList(name,url):
    link = GetHttpData(url)
    match = re.compile('class="mvlist"(.+?)<style>', re.DOTALL).findall(link)
    if match:
        match = re.compile('<li>(.+?)</li>', re.DOTALL).findall(match[0])
        totalItems=len(match)+1
        #提取当页全部歌曲名称图标
        for i in range(0,len(match)):
            p_name = re.compile('title="(.+?)"').findall(match[i])[0]
            p_thumb = re.compile('src="(.+?)"').findall(match[i])[0]
            li = xbmcgui.ListItem(p_name, iconImage = '', thumbnailImage = p_thumb)
            u = sys.argv[0]+"?level=2&songsn="+str(i)+"&url="+urllib.quote_plus(url)
            xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, False, totalItems)
        #添加上、下页链接
        match = re.compile('<div class="page">(.+?)</div>', re.DOTALL).findall(link)
        if match:
            match1 = re.compile('href="(.+?)"><em>上一页', re.DOTALL).findall(match[0])
            if match1:
                totalItems = totalItems+1
                p_url  = UrlBase+match1[0]
                p_name = '上一页'
                li = xbmcgui.ListItem(p_name)
                u = sys.argv[0]+"?level=1&name="+urllib.quote_plus(p_name)+"&url="+urllib.quote_plus(p_url)
                xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, True, totalItems)
            match1 = re.compile('<a(.+?)</a>', re.DOTALL).findall(match[0])
            if match1:
                for i in range(0,len(match1)):
                    match2 = re.compile('href="(.+?)"><em>下一页', re.DOTALL).findall(match1[i]) 
                    if match2:
                        totalItems = totalItems+1
                        p_url  = UrlBase+match2[0]
                        p_name = '下一页'
                        li = xbmcgui.ListItem(p_name)
                        u = sys.argv[0]+"?level=1&name="+urllib.quote_plus(p_name)+"&url="+urllib.quote_plus(p_url)
                        xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, True)
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

def PlayVideo(songsn,url):
    playlist=xbmc.PlayList(1)
    playlist.clear()
    #添加全部歌曲链接地址形成播放列表
    link = GetHttpData(url)
    match = re.compile('class="mvlist"(.+?)<style>', re.DOTALL).findall(link)
    if match:
        match = re.compile('<li>(.+?)</li>', re.DOTALL).findall(match[0])
        #提取该页全部歌曲的页面链接地址
        for i in range(0,len(match)):
            k=(i+int(songsn))%len(match)
            urlk  = UrlBase+re.compile('href="(.+?).html"').findall(match[k])[0]+'.html'
            namek = re.compile('title="(.+?)"').findall(match[k])[0]
            thumbk = re.compile('src="(.+?)"').findall(match[k])[0]
            #提取第k首歌曲页的实际下载地址
            linkk = GetHttpData(urlk)
            matchk = re.compile('webmvplayer(.+?)</script>', re.DOTALL).findall(linkk)
            if matchk:
                matchk = re.compile('&url=(.+?)&autoplay', re.DOTALL).findall(matchk[0])
                if matchk:
                    listitem = xbmcgui.ListItem(namek, thumbnailImage = thumbk)
                    listitem.setInfo(type="Video",infoLabels={"Title":namek})
                    playlist.add(matchk[0], listitem = listitem)
        xbmc.Player().play(xbmc.PlayList(1))
def get_params():
    param = []
    paramstring = sys.argv[2]
    if len(paramstring) >= 2:
        params = sys.argv[2]
        cleanedparams = params.replace('?', '')
        if (params[len(params) - 1] == '/'):
            params = params[0:len(params) - 2]
        pairsofparams = cleanedparams.split('&')
        param = {}
        for i in range(len(pairsofparams)):
            splitparams = {}
            splitparams = pairsofparams[i].split('=')
            if (len(splitparams)) == 2:
                param[splitparams[0]] = splitparams[1]
    return param

params = get_params()
level=None

try:
    level = int(params["level"])
except:
    pass
try:
    url = urllib.unquote_plus(params["url"])
except:
    pass
try:
    name = urllib.unquote_plus(params["name"])
except:
    pass
try:
    songsn = urllib.unquote_plus(params["songsn"])
except:
    pass
    
if level == None:
    rootList()
elif level == 1:
    catList(name,url)
elif level == 2:
    PlayVideo(songsn,url)
