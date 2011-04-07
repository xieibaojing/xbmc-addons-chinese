# -*- coding: utf-8 -*-
import xbmc, xbmcgui, xbmcplugin, xbmcaddon, urllib2, urllib, re, string, sys, os, gzip, StringIO

# 搜狐视频(SoHu) by taxigps, 2011

# Plugin constants 
__addonname__ = "搜狐视频(SoHu)"
__addonid__ = "plugin.video.sohuvideo"
__addon__ = xbmcaddon.Addon(id=__addonid__)

CHANNEL_LIST = [['电影','1'], ['电视剧','2'], ['综艺','7'], ['纪录片','8'], ['新闻','13'], ['动漫','16'], ['公开课','21'], ['其它','0']]
ORDER_LIST = [['相关程度',''], ['最多播放','1'], ['最新发布','3'], ['最高评分','4']]

def GetHttpData(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    httpdata = response.read()
    if response.headers.get('content-encoding', None) == 'gzip':
        httpdata = gzip.GzipFile(fileobj=StringIO.StringIO(httpdata)).read()
    response.close()
    match = re.compile('<meta http-equiv="[Cc]ontent-[Tt]ype" content="text/html; charset=(.+?)"').findall(httpdata)
    if len(match)>0:
        charset = match[0].lower()
        if (charset != 'utf-8') and (charset != 'utf8'):
            httpdata = unicode(httpdata, charset).encode('utf8')
    return httpdata

def searchDict(dlist,idx):
    for i in range(0,len(dlist)):
        if dlist[i][1] == idx:
            return dlist[i][0]
    return ''

def rootList():
    for name, id in CHANNEL_LIST:
        li=xbmcgui.ListItem(name)
        u=sys.argv[0]+"?mode=1&name="+urllib.quote_plus(name)+"&id="+urllib.quote_plus(id)
        xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

def getList(listpage):
    catlist = re.compile("javascript:setValue\('cat','(.+?)',true\)").findall(listpage)
    if len(catlist)>0: catlist.insert(0,'全部')
    arealist = re.compile("javascript:setValue\('area','(.+?)',true\)").findall(listpage)
    if len(arealist)>0: arealist.insert(0,'全部')
    yearlist = re.compile("javascript:setValue\('year','(.+?)',true\)").findall(listpage)
    if len(yearlist)>0: yearlist.insert(0,'全部')
    return catlist,arealist,yearlist

def progList(name,id,page,cat,area,year,order):
    url = 'http://so.tv.sohu.com/mts?c='+id+'&cat='+unicode(cat, 'utf8').encode('gbk')+'&area='+unicode(area, 'utf8').encode('gbk')+'&year='+year
    if len(order)>0:
        url = url + '&o=' + order
    if len(page)>0:
        url = url + '&p=' + page
        currpage = int(page)
    else:
        currpage = 1
    link = GetHttpData(url)
    match = re.compile('<li class="page">(.+?)</li>').findall(link)
    if len(match):
        totalpages = int(match[0].split('/')[1])
    else:
        totalpages = 1
    match = re.compile('<div class="type_list">(.+?)</div>', re.DOTALL).findall(link)
    if len(match):
        listpage = match[0]
    else:
        listpage = ''
    match = re.compile('<div class="list_pack">(.+?)target="_blank"> 播 放 </a>', re.DOTALL).findall(link)
    totalItems = len(match) + 1
    if currpage > 1: totalItems = totalItems + 1
    if currpage < totalpages: totalItems = totalItems + 1

    if cat:
        catstr = cat
    else:
        catstr = '全部类型'
    if area:
        areastr = area
    else:
        areastr = '全部地区'
    if not year:
        yearstr = '全部年份'
    elif year in ('80','90'):
        yearstr = year+'年代'
    elif year == '100':
        yearstr = '更早年代'
    else:
        yearstr = year+'年'
    li = xbmcgui.ListItem(name+'（第'+str(currpage)+'/'+str(totalpages)+'页）【[COLOR FFFF0000]' + catstr + '[/COLOR]/[COLOR FF00FF00]' + areastr + '[/COLOR]/[COLOR FFFFFF00]' + yearstr + '[/COLOR]/[COLOR FF00FFFF]' + searchDict(ORDER_LIST,order) + '[/COLOR]】（按此选择）')
    u = sys.argv[0]+"?mode=4&name="+urllib.quote_plus(name)+"&id="+id+"&cat="+urllib.quote_plus(cat)+"&area="+urllib.quote_plus(area)+"&year="+urllib.quote_plus(year)+"&order="+order+"&url="+urllib.quote_plus(listpage)
    xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, True, totalItems)
    for i in range(0,len(match)):
        match1 = re.compile('class="img" href="(.+?)".+?<img src="(.+?)" alt="(.+?)"', re.DOTALL).search(match[i])
        p_url = match1.group(1)
        p_thumb = match1.group(2)
        p_name = match1.group(3)
        match1 = re.compile('<span class="commet">\(([0-9]+)人评价\)</span><span class="grade"><font>([0-9]*)</font>([\.0-9]*).*?</span>').search(match[i])
        if match1:
            p_rating = float(match1.group(2) + match1.group(3))
            p_votes = match1.group(1)
        else:
            p_rating = 0
            p_votes = ''
        match1 = re.compile('<span>导演：<a href="[^"]*"><font class="highlight"></font>(.*?)</a>').search(match[i])
        if match1:
            p_director = match1.group(1)
        else:
            p_director = ''
        match1 = re.compile('<span class="show">类型：(.+?</span>)').search(match[i])
        if match1:
            match0 = re.compile('<font class="highlight"></font>([^<]+)').findall(match1.group(1))
            p_genre = ' / '.join(match0)
        else:
            p_genre = ''
        match1 = re.compile('<p class="detail">(.+?)(</p>|</b>)').search(match[i])
        if match1:
            p_plot = re.sub('<b id=.*?>','',match1.group(1))
        else:
            p_plot = ''
        match1 = re.compile('<font>年份：<a href="\?c=1&year=([0-9]+)">').search(match[i])
        if match1:
            p_year = int(match1.group(1))
        else:
            p_year = 0
        if match[i].find('class="episodes"')>0:
            p_url = url
            p_dir = True
            mode = 2
        else:
            p_dir = False
            mode = 3
        if match[i].find('class="pay"')>0:
            p_name =  p_name + '(付费)'
            mode = 100
        li = xbmcgui.ListItem(str(i + 1) + '.' + p_name, iconImage = '', thumbnailImage = p_thumb)
        u = sys.argv[0]+"?mode="+str(mode)+"&name="+urllib.quote_plus(p_name)+"&url="+urllib.quote_plus(p_url)+"&thumb="+urllib.quote_plus(p_thumb)+"&id="+urllib.quote_plus(str(i))
        li.setInfo(type = "Video", infoLabels = {"Title":p_name, "Director":p_director, "Genre":p_genre, "Plot":p_plot, "Year":p_year, "Rating":p_rating, "Votes":p_votes})
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, p_dir, totalItems)

    if currpage > 1:
        li = xbmcgui.ListItem('上一页')
        u = sys.argv[0]+"?mode=1&name="+urllib.quote_plus(name)+"&id="+id+"&cat="+urllib.quote_plus(cat)+"&area="+urllib.quote_plus(area)+"&year="+urllib.quote_plus(year)+"&order="+order+"&page="+urllib.quote_plus(str(currpage-1))
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, True, totalItems)
    if currpage < totalpages:
        li = xbmcgui.ListItem('下一页')
        u = sys.argv[0]+"?mode=1&name="+urllib.quote_plus(name)+"&id="+id+"&cat="+urllib.quote_plus(cat)+"&area="+urllib.quote_plus(area)+"&year="+urllib.quote_plus(year)+"&order="+order+"&page="+urllib.quote_plus(str(currpage+1))
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, True, totalItems)
    xbmcplugin.setContent(int(sys.argv[1]), 'movies')
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

def seriesList(name,id,url,thumb):
    link = GetHttpData(url)
    link = re.compile('<div class="list_pack">(.+?)target="_blank"> 播 放 </a>', re.DOTALL).findall(link)[int(id)]
    match0 = re.compile('class="episodes">(.+?)<p class="detail">', re.DOTALL).search(link)
    match = re.compile('<a href="(.+?)" title="(.+?)"').findall(match0.group(1))
    totalItems = len(match)
    for p_url, p_name in match:
        li = xbmcgui.ListItem(p_name, iconImage = '', thumbnailImage = thumb)
        u = sys.argv[0] + "?mode=3&name=" + urllib.quote_plus(p_name) + "&url=" + urllib.quote_plus(p_url)+ "&thumb=" + urllib.quote_plus(thumb)
        #li.setInfo(type = "Video", infoLabels = {"Title":p_name, "Director":p_director, "Cast":p_cast, "Plot":p_plot, "Year":p_year, "Rating":p_rating, "Votes":p_votes})
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, False, totalItems)
    xbmcplugin.setContent(int(sys.argv[1]), 'episodes')
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

def PlayVideo(name,url,thumb):
    print url
    if url[0:5]!='http:':
        url='http://so.tv.sohu.com'+url
    link = GetHttpData(url)
    match1 = re.compile('var vid="(.+?)";').search(link)
    if not match1:
        match1 = re.compile('<a href="(http://[^/]+/[0-9]+/[^\.]+.shtml)" target="?_blank"?><img').search(link)
        if match1:
            PlayVideo(name,match1.group(1),thumb)
        return
    link = GetHttpData('http://hot.vrs.sohu.com/vrs_flash.action?vid='+match1.group(1))
    match = re.compile('"tvName":"(.+?)"').findall(link)
    name = match[0]
    match = re.compile('"clipsURL"\:\["(.+?)"\]').findall(link)
    paths = match[0].split('","')
    playlist = xbmc.PlayList(1)
    playlist.clear()
    for i in range(0,len(paths)):
        listitem=xbmcgui.ListItem(name,thumbnailImage=thumb)
        listitem.setInfo(type="Video",infoLabels={"Title":name+" 第"+str(i+1)+"/"+str(len(paths))+" 节"})
        playlist.add(paths[i], listitem)
    xbmc.Player().play(playlist)

def performChanges(name,id,listpage,cat,area,year,order):
    catlist,arealist,yearlist = getList(listpage)
    change = False
    dialog = xbmcgui.Dialog()
    if len(catlist)>0:
        sel = dialog.select('类型', catlist)
        if sel != -1:
            if sel == 0:
                cat = ''
            else:
                cat = catlist[sel]
            change = True
    if len(arealist)>0:
        sel = dialog.select('地区', arealist)
        if sel != -1:
            if sel == 0:
                area = ''
            else:
                area = arealist[sel]
            change = True
    if len(yearlist)>0:
        tmplist = []
        for item in yearlist:
            if item in ('80','90'):
                tmplist.append(item+'年代')
            elif item == '100':
                tmplist.append('更早')
            else:
                tmplist.append(item)
        sel = dialog.select('年份', tmplist)
        if sel != -1:
            if sel == 0:
                year = ''
            else:
                year = yearlist[sel]
            change = True

    list = [x[0] for x in ORDER_LIST]
    sel = dialog.select('排序方式', list)
    if sel != -1:
        order = ORDER_LIST[sel][1]
        change = True

    if change:
        progList(name,id,'',cat,area,year,order)

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
id = None
cat = ''
area = ''
year = ''
order = ''
page = ''
url = None
thumb = None

try:
    thumb = urllib.unquote_plus(params["thumb"])
except:
    pass
try:
    url = urllib.unquote_plus(params["url"])
except:
    pass
try:
    page = urllib.unquote_plus(params["page"])
except:
    pass
try:
    order = urllib.unquote_plus(params["order"])
except:
    pass
try:
    year = urllib.unquote_plus(params["year"])
except:
    pass
try:
    area = urllib.unquote_plus(params["area"])
except:
    pass
try:
    cat = urllib.unquote_plus(params["cat"])
except:
    pass
try:
    id = urllib.unquote_plus(params["id"])
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
    rootList()
elif mode == 1:
    progList(name,id,page,cat,area,year,order)
elif mode == 2:
    seriesList(name,id,url,thumb)
elif mode == 3:
    PlayVideo(name,url,thumb)
elif mode == 4:
    performChanges(name,id,url,cat,area,year,order)

