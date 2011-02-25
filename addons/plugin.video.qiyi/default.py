# -*- coding: utf-8 -*-
import xbmc, xbmcgui, xbmcplugin, xbmcaddon, urllib2, urllib, re, string, sys, os

# QIYI.COM(奇艺视频) by taxigps, 2011

# Plugin constants 
__addonname__ = "奇艺视频"
__addonid__ = "plugin.video.qiyi"
__addon__ = xbmcaddon.Addon(id=__addonid__)

CHANNEL_LIST = [['电影','1'], ['电视剧','2']]
CHANNEL_DICT = dict(CHANNEL_LIST)
ORDER_LIST = [['关注','5'], ['最新','2'], ['热播','3'], ['好评','4']]
ORDER_DICT = dict(ORDER_LIST)

def GetHttpData(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    httpdata = response.read()
    response.close()
    return httpdata

link = GetHttpData('http://list.qiyi.com/www/1/------------2-1-1----.html')
link = re.sub("\s", "", link)
match1 = re.compile('<dtdata-value="2">按类型</dt>(.*?)</dd>').findall(link)
match = re.compile('href="http://list.qiyi.com/www/1/-([0-9]*)-----------2-1-1----.html">(.*?)</a>').findall(match1[0])
MOVIE_TYPE_LIST = [[x[1],x[0]] for x in match]
MOVIE_TYPE_DICT = dict(MOVIE_TYPE_LIST)
match1 = re.compile('<dtdata-value="1">按地区</dt>(.*?)</dd>').findall(link)
match = re.compile('href="http://list.qiyi.com/www/1/([0-9]*)------------2-1-1----.html">(.*?)</a>').findall(match1[0])
MOVIE_AREA_LIST = [[x[1],x[0]] for x in match]
MOVIE_AREA_DICT = dict(MOVIE_AREA_LIST)

def updateList():
    page = __addon__.getSetting('page')
    currpage = int(page)
    channel = __addon__.getSetting('channel')
    c0 = CHANNEL_DICT[channel]
    movie_area = __addon__.getSetting('movie_area')
    c1 = MOVIE_AREA_DICT[movie_area]
    movie_type = __addon__.getSetting('movie_type')
    c2 = MOVIE_TYPE_DICT[movie_type]
    order = __addon__.getSetting('order')
    c13 = ORDER_DICT[order]
    url = 'http://list.qiyi.com/www/' + c0 + '/' + c1 + '-' + c2 + '-----------' + c13 + '-1-' + page + '----.html'
    link = GetHttpData(url)
    link = re.sub("\s", "", link)
    match1 = re.compile('data-key="([0-9]+)"').findall(link)
    totalpages = int(match1[len(match1) - 1])
    match1 = re.compile('<ulid="rs"(.+?)</ul>').findall(link)
    match = re.compile('<li><ahref="(.+?)"class="imgBg1(.*?)"><.+?src="(.+?)"title="(.+?)"alt=".+?<spanid="fenshu"class="fRed"><strong>(.+?)</strong>(.*?)</span><spanclass="fBlack"></span>(.*?)</p></li>').findall(match1[0])
    totalItems = len(match) + 1
    if currpage > 1: totalItems = totalItems + 1
    if currpage < totalpages: totalItems = totalItems + 1

    li = xbmcgui.ListItem('类型[COLOR FFFF0000]【' + movie_type + '】[/COLOR] 地区[COLOR FFFF0000]【' + movie_area + '】[/COLOR] 排序[COLOR FFFF0000]【' + order + '】[/COLOR]（按此选择）')
    u = sys.argv[0] + "?mode=4"
    xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, True, totalItems)

    for i in range(0,len(match)):
        p_url = match[i][0]
        p_name = match[i][3]
        if match[i][1]=='chaoqing_pic':
            p_name = p_name + '(超清)'
        p_thumb = match[i][2]
        p_rating = match[i][4] + match[i][5] + match[i][6]

        link = GetHttpData(p_url)
        link = re.sub(' ', '', link)
        match1 = re.compile('pid:"(.+?)",//').findall(link)
        pid = match1[0]
        match1 = re.compile('ptype:"(.+?)",//').findall(link)
        ptype = match1[0]
        match1 = re.compile('videoId:"(.+?)",//').findall(link)
        videoId = match1[0]
        p_url='http://cache.video.qiyi.com/v/' + videoId + '/' + pid + '/' + ptype + '/'

        li = xbmcgui.ListItem(str(i + 1) + '.' + p_name + "【" + p_rating + "】", p_thumb, p_thumb)
        u = sys.argv[0] + "?mode=2&name=" + urllib.quote_plus(p_name) + "&url=" + urllib.quote_plus(p_url)+ "&thumb=" + urllib.quote_plus(p_thumb)
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, False, totalItems)

    if currpage > 1:
        li = xbmcgui.ListItem('上一页（第'+page+'页/共'+str(totalpages)+'页）')
        u = sys.argv[0] + "?mode=1&page=" + urllib.quote_plus(str(currpage - 1))
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, True, totalItems)
    if currpage < totalpages:
        li = xbmcgui.ListItem('下一页（第'+page+'页/共'+str(totalpages)+'页）')
        u = sys.argv[0] + "?mode=1&page=" + urllib.quote_plus(str(currpage + 1))
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, True, totalItems)
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

def PlayVideo(url,name,thumb):
    print url
    print thumb
    link = GetHttpData(url)
    link=re.sub("\s", "", link)
    match=re.compile('<file>http://data.video.qiyi.com/videos/([^/]+?)/(.+?)</file>').findall(link)
    playlist=xbmc.PlayList(1)
    playlist.clear()
    listitem = xbmcgui.ListItem(name, thumbnailImage = thumb)
    listitem.setInfo(type="Video",infoLabels={"Title":name+" 第"+str(1)+"/"+str(len(match))+" 节"})
    playlist.add('http://qiyi.soooner.com/videos2/'+match[0][0]+'/'+match[0][1], listitem = listitem)
    for i in range(1,len(match)):
        listitem=xbmcgui.ListItem(name, thumbnailImage = thumb)
        listitem.setInfo(type="Video",infoLabels={"Title":name+" 第"+str(i+1)+"/"+str(len(match))+" 节"})
        playlist.add('http://qiyi.soooner.com/videos2/'+match[i][0]+'/'+match[i][1], listitem = listitem)
    xbmc.Player().play(playlist)

def performChanges():
    change = False
    dialog = xbmcgui.Dialog()
    list = [x[0] for x in MOVIE_TYPE_LIST]
    sel = dialog.select('电影类型', list)
    if sel != -1:
        __addon__.setSetting(id="movie_type", value=list[sel])
        __addon__.setSetting(id="page", value="1")
        change = True

    list = [x[0] for x in MOVIE_AREA_LIST]
    sel = dialog.select('电影地区', list)
    if sel != -1:
        __addon__.setSetting(id="movie_area", value=list[sel])
        __addon__.setSetting(id="page", value="1")
        change = True

    list = [x[0] for x in ORDER_LIST]
    sel = dialog.select('排序方式', list)
    if sel != -1:
        __addon__.setSetting(id="order", value=list[sel])
        __addon__.setSetting(id="page", value="1")
        change = True

    if change:
        xbmc.executebuiltin('Container.Refresh')

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
mode = None
name = None
url = None
thumb = None
page = None

try:
    page = urllib.unquote_plus(params["page"])
except:
    pass
try:
    thumb = urllib.unquote_plus(params["thumb"])
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
    mode = int(params["mode"])
except:
    pass

if mode == None:
    updateList()
elif mode == 1:
    __addon__.setSetting(id="page", value=page)
    xbmc.executebuiltin('Container.Refresh')
elif mode == 2:
    PlayVideo(url, name, thumb)
elif mode == 4:
    performChanges()

