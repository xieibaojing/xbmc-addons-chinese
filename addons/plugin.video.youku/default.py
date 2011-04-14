# -*- coding: utf-8 -*-
import xbmc, xbmcgui, xbmcplugin, xbmcaddon, urllib2, urllib, re, string, sys, os, gzip, StringIO

# 优酷视频(YouKu) by taxigps, 2011

# Plugin constants 
__addonname__ = "优酷视频(YouKu)"
__addonid__ = "plugin.video.youku"
__addon__ = xbmcaddon.Addon(id=__addonid__)
__addonicon__ = os.path.join( __addon__.getAddonInfo('path'), 'icon.png' )

UserAgent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'
ORDER_LIST = [['1','历史最多播放'], ['6','本周最多播放'], ['7','今日最多播放'], ['3','最新上映'], ['9','最近上映'], ['5','最多评论'], ['11','用户好评']]
ORDER_LIST2 = [['1','最新发布'], ['2','最多播放'], ['3','最热话题'], ['8','最具争议'], ['4','最多收藏'], ['5','最广传播'], ['6','用户推荐']]
YEAR_LIST2 = [['1','今日'], ['2','本周'], ['3','本月'], ['4','历史']]
RES_LIST = ['normal', 'high', 'super']

def GetHttpData(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', UserAgent)
    response = urllib2.urlopen(req)
    httpdata = response.read()
    if response.headers.get('content-encoding', None) == 'gzip':
        httpdata = gzip.GzipFile(fileobj=StringIO.StringIO(httpdata)).read()
    response.close()
    match = re.compile('<meta http-equiv="[Cc]ontent-[Tt]ype" content="text/html; charset=(.+?)"').findall(httpdata)
    if len(match)<=0:
        match = re.compile('meta charset="(.+?)"').findall(httpdata)
    if len(match)>0:
        charset = match[0].lower()
        if (charset != 'utf-8') and (charset != 'utf8'):
            httpdata = unicode(httpdata, charset).encode('utf8')
    return httpdata

def searchDict(dlist,idx):
    for i in range(0,len(dlist)):
        if dlist[i][0] == idx:
            return dlist[i][1]
    return ''

def getList(listpage):
    match0 = re.compile('<label>类型:</label>(.+?)</ul>', re.DOTALL).search(listpage)
    catlist = re.compile('<li.+?>([^<]+)(?:</a>|</span>)</li>').findall(match0.group(1))
    match0 = re.compile('<label>地区:</label>(.+?)</ul>', re.DOTALL).search(listpage)
    arealist = re.compile('<li.+?>([^<]+)(?:</a>|</span>)</li>').findall(match0.group(1))
    match0 = re.compile('<label>上映:</label>(.+?)</ul>', re.DOTALL).search(listpage)
    yearlist = re.compile('<li.+?>([^<]+)(?:</a>|</span>)</li>').findall(match0.group(1))
    return catlist,arealist,yearlist

def getList2(listpage, cat):
    match0 = re.compile('<label>类型:</label>(.+?)</ul>', re.DOTALL).search(listpage)
    if match0:
        catlist = re.compile('<li><a href="/v_showlist/[^g]*g([0-9]+)[^\.]*.html"[^>]*>(.+?)</a></li>').findall(match0.group(1))
        match1 = re.compile('<li class="current"><span>(.+?)</span>').search(match0.group(1))
        if match1:
            catlist.append([cat,match1.group(1)])
    else:
        catlist = []
    return catlist

def rootList():
    link = GetHttpData('http://www.youku.com/v/')
    match0 = re.compile('<div class="left">(.+?)<!--left end-->', re.DOTALL).search(link)
    match = re.compile('<li><a href="/([^/]+)/([^\.]+)\.html"[^>]+>(.+?)</a></li>').findall(match0.group(1))
    totalItems = len(match)
    for path, id, name in match:
        if path == 'v_olist':
            u = sys.argv[0]+"?mode=1&name="+urllib.quote_plus(name)+"&id="+urllib.quote_plus(id)+"&cat="+urllib.quote_plus('不限')+"&area="+urllib.quote_plus('不限')+"&year="+urllib.quote_plus('不限')+"&order="+urllib.quote_plus('7')
        else:
            u = sys.argv[0]+"?mode=11&name="+urllib.quote_plus(name)+"&id="+urllib.quote_plus(id)+"&cat="+'0'+"&year="+'1'+"&order="+'2'
        li = xbmcgui.ListItem(name)
        xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True,totalItems)
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

def progList(name,id,page,cat,area,year,order):
    if cat == '不限':
        catstr = ''
    else:
        catstr = cat
    if area == '不限':
        areastr = ''
    else:
        areastr = area
    if year == '不限':
        yearstr = ''
    elif year.find('年代')>0:
        yearstr = '19' + year[0:2]
    else:
        yearstr = year
    url = 'http://www.youku.com/v_olist/'+id+'_a_'+areastr+'_s__g_'+catstr+'_r_'+yearstr+'_o_'+order
    if page:
        url = url + '_p_' + page
        currpage = int(page)
    else:
        currpage = 1
    url += '.html'
    link = GetHttpData(url)
    match = re.compile('<ul class="pages">(.+?)</ul>', re.DOTALL).findall(link)
    if len(match):
        match1 = re.compile('<li.+?>([0-9]+)(</a>|</span>)</li>', re.DOTALL).findall(match[0])
        totalpages = int(match1[len(match1)-1][0])
    else:
        totalpages = 1
    match = re.compile('<div class="filter" id="filter">(.+?)<!--filter end-->', re.DOTALL).findall(link)
    if len(match):
        listpage = match[0]
    else:
        listpage = ''
    match = re.compile('<ul class="p">(.+?)</ul>', re.DOTALL).findall(link)
    totalItems = len(match) + 1
    if currpage > 1: totalItems = totalItems + 1
    if currpage < totalpages: totalItems = totalItems + 1
    if cat == '不限':
        catstr = '全部类型'
    else:
        catstr = cat
    if area == '不限':
        areastr = '全部地区'
    else:
        areastr = area
    if year == '不限':
        yearstr = '全部年份'
    else:
        yearstr = year
    li = xbmcgui.ListItem(name+'（第'+str(currpage)+'/'+str(totalpages)+'页）【[COLOR FFFF0000]' + catstr + '[/COLOR]/[COLOR FF00FF00]' + areastr + '[/COLOR]/[COLOR FFFFFF00]' + yearstr + '[/COLOR]/[COLOR FF00FFFF]' + searchDict(ORDER_LIST,order) + '[/COLOR]】（按此选择）')
    u = sys.argv[0]+"?mode=4&name="+urllib.quote_plus(name)+"&id="+urllib.quote_plus(id)+"&cat="+urllib.quote_plus(cat)+"&area="+urllib.quote_plus(area)+"&year="+urllib.quote_plus(year)+"&order="+order+"&page="+urllib.quote_plus(listpage)
    xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, True, totalItems)
    for i in range(0,len(match)):
        match1 = re.compile('<li class="p_link"><a href="http://www.youku.com/show_page/id_(.+?).html"').search(match[i])
        p_id = match1.group(1)
        match1 = re.compile('<li class="p_thumb"><img src="(.+?)"').search(match[i])
        p_thumb = match1.group(1)
        match1 = re.compile('<li class="p_title"><a [^>]+>(.+?)</a>').search(match[i])
        p_name = match1.group(1)
        match1 = re.compile('<li class="p_status"><span class="status">(.+?)</span>').search(match[i])
        if match1:
            p_name1 = p_name + '（' + match1.group(1) + '）'
        else:
            p_name1 = p_name
        if match[i].find('<span class="ico__SD"')>0:
            p_name1 += '[超清]'
            p_res = 2
        elif match[i].find('<span class="ico__HD"')>0:
            p_name1 += '[高清]'
            p_res = 1
        else:
            p_res = 0
        if match[i].find('<li class="p_ischarge">')>0:
            p_name1 += '[付费节目]'
        if id == 'c_96':
            mode = 2
            isdir = False
        else:
            mode = 3
            isdir = True
        li = xbmcgui.ListItem(str(i + 1) + '.' + p_name1, iconImage = '', thumbnailImage = p_thumb)
        u = sys.argv[0]+"?mode="+str(mode)+"&name="+urllib.quote_plus(p_name)+"&id="+urllib.quote_plus(p_id)+"&thumb="+urllib.quote_plus(p_thumb)+"&res="+str(p_res)
        #li.setInfo(type = "Video", infoLabels = {"Title":p_name, "Director":p_director, "Genre":p_genre, "Plot":p_plot, "Year":p_year, "Cast":p_cast, "Tagline":p_tagline})
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, isdir, totalItems)

    if currpage > 1:
        li = xbmcgui.ListItem('上一页')
        u = sys.argv[0]+"?mode=1&name="+urllib.quote_plus(name)+"&id="+urllib.quote_plus(id)+"&cat="+urllib.quote_plus(cat)+"&area="+urllib.quote_plus(area)+"&year="+urllib.quote_plus(year)+"&order="+order+"&page="+urllib.quote_plus(str(currpage-1))
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, True, totalItems)
    if currpage < totalpages:
        li = xbmcgui.ListItem('下一页')
        u = sys.argv[0]+"?mode=1&name="+urllib.quote_plus(name)+"&id="+urllib.quote_plus(id)+"&cat="+urllib.quote_plus(cat)+"&area="+urllib.quote_plus(area)+"&year="+urllib.quote_plus(year)+"&order="+order+"&page="+urllib.quote_plus(str(currpage+1))
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, True, totalItems)
    xbmcplugin.setContent(int(sys.argv[1]), 'movies')
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

def getMoive(name,id,thumb,res):
    link = GetHttpData('http://www.youku.com/show_page/id_' + id + '.html')
    match = re.compile('<div id="showBanner".+?href="(http://v.youku.com/v_show/id_.+?.html)"', re.DOTALL).search(link)
    if match:
        PlayVideo(name, match.group(1), thumb, res)

def seriesList(name,id,thumb,page):
    url = "http://www.youku.com/show_eplist/showid_"+id+"_type_pic_from_ajax_page_"+page+".html"
    currpage = int(page)
    link = GetHttpData(url)
    match = re.compile('<ul class="pages">(.+?)</ul>', re.DOTALL).findall(link)
    if len(match):
        match1 = re.compile('<li.+?>([0-9]+)(</a>|</span>)</li>', re.DOTALL).findall(match[0])
        totalpages = int(match1[len(match1)-1][0])
    else:
        totalpages = 1
    match = re.compile('<ul class="v">(.+?)</ul>', re.DOTALL).findall(link)
    totalItems = len(match) + 1
    if currpage > 1: totalItems = totalItems + 1
    if currpage < totalpages: totalItems = totalItems + 1


    li = xbmcgui.ListItem("当前节目："+name+'（第'+str(currpage)+'/'+str(totalpages)+'页）')
    u=sys.argv[0]+"?mode=40&name="+urllib.quote_plus(name)
    xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, True, totalItems)
    for i in range(0,len(match)):
        match1 = re.compile('<li class="v_link"><a .*?href="(http://v.youku.com/v_show/id_.+?.html)"').search(match[i])
        p_url = match1.group(1)
        match1 = re.compile('<li class="v_thumb"><img src="(.+?)"').search(match[i])
        p_thumb = match1.group(1)
        match1 = re.compile('<li class="v_title">[\s]*<a [^>]+>(.+?)</a>').search(match[i])
        p_name = match1.group(1)
        if match[i].find('<span class="ico__SD"')>0:
            p_name += '[超清]'
            p_res = 2
        elif match[i].find('<span class="ico__HD"')>0:
            p_name += '[高清]'
            p_res = 1
        else:
            p_res = 0
        li = xbmcgui.ListItem(str(i + 1) + '.' + p_name, iconImage = '', thumbnailImage = p_thumb)
        u = sys.argv[0]+"?mode=10&name="+urllib.quote_plus(p_name)+"&url="+urllib.quote_plus(p_url)+"&thumb="+urllib.quote_plus(p_thumb)+"&res="+str(p_res)
        #li.setInfo(type = "Video", infoLabels = {"Title":p_name, "Director":p_director, "Genre":p_genre, "Plot":p_plot, "Year":p_year, "Cast":p_cast, "Tagline":p_tagline})
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, False, totalItems)

    if currpage > 1:
        li = xbmcgui.ListItem('上一页')
        u = sys.argv[0]+"?mode=3&name="+urllib.quote_plus(name)+"&id="+urllib.quote_plus(id)+"&thumb="+urllib.quote_plus(thumb)+"&page="+urllib.quote_plus(str(currpage-1))
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, True, totalItems)
    if currpage < totalpages:
        li = xbmcgui.ListItem('下一页')
        u = sys.argv[0]+"?mode=3&name="+urllib.quote_plus(name)+"&id="+urllib.quote_plus(id)+"&thumb="+urllib.quote_plus(thumb)+"&page="+urllib.quote_plus(str(currpage+1))
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, True, totalItems)
    xbmcplugin.setContent(int(sys.argv[1]), 'movies')
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

def progList2(name,id,page,cat,year,order):
    url = 'http://www.youku.com/v_showlist/t'+order+'d'+year+id+'g'+cat
    if page:
        url += 'p' + page
        currpage = int(page)
    else:
        currpage = 1
    url += '.html'
    link = GetHttpData(url)
    match = re.compile('<ul class="pages">(.+?)</ul>', re.DOTALL).findall(link)
    if len(match):
        match1 = re.compile('<li.+?>([0-9]+)(</a>|</span>)</li>', re.DOTALL).findall(match[0])
        totalpages = int(match1[len(match1)-1][0])
    else:
        totalpages = 1
    match = re.compile('<div class="filter" id="filter">(.+?)<!--filter end-->', re.DOTALL).findall(link)
    if len(match):
        listpage = match[0]
    else:
        listpage = ''
    catlist = getList2(listpage, cat)
    match = re.compile('<ul class="v">(.+?)</ul>', re.DOTALL).findall(link)
    totalItems = len(match) + 1
    if currpage > 1: totalItems = totalItems + 1
    if currpage < totalpages: totalItems = totalItems + 1
    if cat == '0':
        catstr = '全部类型'
    else:
        catstr = searchDict(catlist,cat)
    li = xbmcgui.ListItem(name+'（第'+str(currpage)+'/'+str(totalpages)+'页）【[COLOR FFFF0000]' + catstr + '[/COLOR]/[COLOR FF00FF00]' + searchDict(YEAR_LIST2,year) + '[/COLOR]/[COLOR FF00FFFF]' + searchDict(ORDER_LIST2,order) + '[/COLOR]】（按此选择）')
    u = sys.argv[0]+"?mode=12&name="+urllib.quote_plus(name)+"&id="+urllib.quote_plus(id)+"&cat="+urllib.quote_plus(cat)+"&year="+urllib.quote_plus(year)+"&order="+order+"&page="+urllib.quote_plus(listpage)
    xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, True, totalItems)
    for i in range(0,len(match)):
        match1 = re.compile('<li class="v_link"><a href="(http://v.youku.com/v_show/id_.+?.html)"').search(match[i])
        p_url = match1.group(1)
        match1 = re.compile('<li class="v_thumb"><img src="(.+?)"').search(match[i])
        p_thumb = match1.group(1)
        match1 = re.compile('<li class="v_title"><a [^>]+>(.+?)</a>').search(match[i])
        p_name = match1.group(1).replace('&quot;','"')
        if match[i].find('<span class="ico__SD"')>0:
            p_name += '[超清]'
            p_res = 2
        elif match[i].find('<span class="ico__HD"')>0:
            p_name += '[高清]'
            p_res = 1
        else:
            p_res = 0
        li = xbmcgui.ListItem(str(i + 1) + '.' + p_name, iconImage = '', thumbnailImage = p_thumb)
        u = sys.argv[0]+"?mode=10&name="+urllib.quote_plus(p_name)+"&url="+urllib.quote_plus(p_url)+"&thumb="+urllib.quote_plus(p_thumb)+"&res="+str(p_res)
        #li.setInfo(type = "Video", infoLabels = {"Title":p_name, "Director":p_director, "Genre":p_genre, "Plot":p_plot, "Year":p_year, "Cast":p_cast, "Tagline":p_tagline})
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, False, totalItems)

    if currpage > 1:
        li = xbmcgui.ListItem('上一页')
        u = sys.argv[0]+"?mode=11&name="+urllib.quote_plus(name)+"&id="+urllib.quote_plus(id)+"&cat="+urllib.quote_plus(cat)+"&year="+urllib.quote_plus(year)+"&order="+order+"&page="+urllib.quote_plus(str(currpage-1))
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, True, totalItems)
    if currpage < totalpages:
        li = xbmcgui.ListItem('下一页')
        u = sys.argv[0]+"?mode=11&name="+urllib.quote_plus(name)+"&id="+urllib.quote_plus(id)+"&cat="+urllib.quote_plus(cat)+"&year="+urllib.quote_plus(year)+"&order="+order+"&page="+urllib.quote_plus(str(currpage+1))
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, True, totalItems)
    xbmcplugin.setContent(int(sys.argv[1]), 'movies')
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

def PlayVideo(name,url,thumb,res):
    res_limit = int(__addon__.getSetting('movie_res'))
    if res > res_limit:
        res = res_limit
    link = GetHttpData("http://www.flvcd.com/parse.php?kw="+url+"&format="+RES_LIST[res])
    match = re.compile('"(http://f.youku.com/player/getFlvPath/.+?)" target="_blank"').findall(link)
    if len(match)>0:
        playlist=xbmc.PlayList(1)
        playlist.clear()
        for i in range(0,len(match)):
            listitem = xbmcgui.ListItem(name, thumbnailImage = __addonicon__)
            listitem.setInfo(type="Video",infoLabels={"Title":name+" 第"+str(i+1)+"/"+str(len(match))+" 节"})
            playlist.add(match[i], listitem)
        xbmc.Player().play(playlist)
    else:
        if link.find('该视频为加密视频')>0:
            dialog = xbmcgui.Dialog()
            ok = dialog.ok(__addonname__, '无法播放：该视频为加密视频')
        elif link.find('解析失败，请确认视频是否被删除')>0:
            dialog = xbmcgui.Dialog()
            ok = dialog.ok(__addonname__, '无法播放：该视频或为收费节目')

def performChanges(name,id,listpage,cat,area,year,order):
    catlist,arealist,yearlist = getList(listpage)
    change = False
    dialog = xbmcgui.Dialog()
    if len(catlist)>0:
        sel = dialog.select('类型', catlist)
        if sel != -1:
            cat = catlist[sel]
            change = True
    if len(arealist)>0:
        sel = dialog.select('地区', arealist)
        if sel != -1:
            area = arealist[sel]
            change = True
    if len(yearlist)>0:
        sel = dialog.select('年份', yearlist)
        if sel != -1:
            year = yearlist[sel]
            change = True

    list = [x[1] for x in ORDER_LIST]
    sel = dialog.select('排序方式', list)
    if sel != -1:
        order = ORDER_LIST[sel][0]
        change = True

    if change:
        progList(name,id,'1',cat,area,year,order)

def performChanges2(name,id,listpage,cat,year,order):
    catlist = getList2(listpage, cat)
    change = False
    dialog = xbmcgui.Dialog()
    if len(catlist)>0:
        list = [x[1] for x in catlist]
        sel = dialog.select('类型', list)
        if sel != -1:
            cat = catlist[sel][0]
            change = True
    list = [x[1] for x in ORDER_LIST2]
    sel = dialog.select('排序方式', list)
    if sel != -1:
        order = ORDER_LIST2[sel][0]
        change = True
    list = [x[1] for x in YEAR_LIST2]
    sel = dialog.select('统计周期', list)
    if sel != -1:
        year = YEAR_LIST2[sel][0]
        change = True

    if change:
        progList2(name,id,'1',cat,year,order)

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
cat = None
area = None
year = None
order = None
page = '1'
url = None
thumb = None
res = 0

try:
    res = int(params["res"])
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
    getMoive(name,id,thumb,res)
elif mode == 3:
    seriesList(name,id,thumb,page)
elif mode == 4:
    performChanges(name,id,page,cat,area,year,order)
elif mode == 10:
    PlayVideo(name,url,thumb,res)
elif mode == 11:
    progList2(name,id,page,cat,year,order)
elif mode == 12:
    performChanges2(name,id,page,cat,year,order)

