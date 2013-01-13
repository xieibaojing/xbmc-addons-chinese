# -*- coding: utf-8 -*-
import xbmc, xbmcgui, xbmcplugin, xbmcaddon, urllib2, urllib, re, string, sys, os, gzip, StringIO

# Plugin constants 
__addon__     = xbmcaddon.Addon()
__addonname__ = __addon__.getAddonInfo('name')

CHANNEL_LIST = [['电影','movie'],['电视剧','teleplay'],['综艺','tv'],['动漫','anime'],['微电影','vmovie'],['纪录片','documentary'],['公开课','lesson']]
ORDER_LIST = [['hits','热门'], ['update','更新'], ['rat','评分'], ['release','新上映'], ['guess','猜你喜欢']]
RES_LIST = ['normal', 'high']

def log(txt):
    message = '%s: %s' % (__addonname__, txt)
    xbmc.log(msg=message, level=xbmc.LOGDEBUG)

def GetHttpData(url):
    log("%s::url - %s" % (sys._getframe().f_code.co_name, url))
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
        log( "%s (%d) [%s]" % (
               sys.exc_info()[2].tb_frame.f_code.co_name,
               sys.exc_info()[2].tb_lineno,
               sys.exc_info()[1]
               ))
        return ''
    match = re.compile('<meta http-equiv=["]?[Cc]ontent-[Tt]ype["]? content="text/html;[\s]?charset=(.+?)"').findall(httpdata)
    if match:
        charset = match[0]
    else:
        match = re.compile('<meta charset="(.+?)"').findall(httpdata)
        if match:
            charset = match[0]
    if charset:
        charset = charset.lower()
        if (charset != 'utf-8') and (charset != 'utf8'):
            httpdata = httpdata.decode(charset, 'ignore').encode('utf8', 'ignore')
    return httpdata

def searchDict(dlist,idx):
    for i in range(0,len(dlist)):
        if dlist[i][0] == idx:
            return dlist[i][1]
    return ''

def getList(listpage,type,genre,area,year):
    match = re.compile('<dt>按分类:</dt>\s*<dd id="div_genre"><a[^>]*>全部</a>(.+?)</dd>', re.DOTALL).search(listpage)
    match1 = re.compile('<a\s*href="http://movie.kankan.com/(.+?)/(.+?)/"[^>]*>(.+?)</a>').findall(match.group(1))
    items = match1[0][0].split(',')
    for i in range(0,len(items)):
        if items[i] == 'genre':
            genrelist = [[x[1].split(',')[i] ,x[2]] for x in match1]
            break
    match1 = re.compile('<a class="on">(.+?)</a>').findall(match.group(1))
    if match1:
        genrelist.append([genre, match1[0]])

    if type in ('movie', 'teleplay', 'tv', 'anime'):
        match = re.compile('<dt>按地区:</dt>\s*<dd id="div_area"><a[^>]*>全部</a>(.+?)</dd>', re.DOTALL).search(listpage)
        match1 = re.compile('<a\s*href="http://movie.kankan.com/(.+?)/(.+?)/"[^>]*>(.+?)</a>').findall(match.group(1))
        items = match1[0][0].split(',')
        for i in range(0,len(items)):
            if items[i] == 'area':
                arealist = [[x[1].split(',')[i] ,x[2]] for x in match1]
                break
        match1 = re.compile('<a class="on">(.+?)</a>').findall(match.group(1))
        if match1:
            arealist.append([area, match1[0]])
    elif type == 'lesson':
        match = re.compile('<dt>按学校:</dt>\s*<dd id="div_school"><a[^>]*>全部</a>(.+?)</dd>', re.DOTALL).search(listpage)
        match1 = re.compile('<a\s*href="http://movie.kankan.com/(.+?)/(.+?)/"[^>]*>(.+?)</a>').findall(match.group(1))
        items = match1[0][0].split(',')
        for i in range(0,len(items)):
            if items[i] == 'school':
                arealist = [[x[1].split(',')[i] ,x[2]] for x in match1]
                break
        match1 = re.compile('<a class="on">(.+?)</a>').findall(match.group(1))
        if match1:
            arealist.append([area, match1[0]])
    else:
        arealist = []

    match = re.compile('<dt>按年份:</dt>\s*<dd id="div_year"><a[^>]*>全部</a>(.+?)</dd>', re.DOTALL).search(listpage)
    match1 = re.compile('<a\s*href="http://movie.kankan.com/(.+?)/(.+?)/"[^>]*>(.+?)</a>').findall(match.group(1))
    items = match1[0][0].split(',')
    for i in range(0,len(items)):
        if items[i] == 'year':
            yearlist = [[x[1].split(',')[i] ,x[2]] for x in match1]
            break
    match1 = re.compile('<a class="on">(.+?)</a>').findall(match.group(1))
    if match1:
        yearlist.append([year, match1[0]])
    return genrelist,arealist,yearlist

def rootList():
    totalItems = len(CHANNEL_LIST)
    for name, type in CHANNEL_LIST:
        li = xbmcgui.ListItem(name)
        u = sys.argv[0]+"?mode=1&name="+urllib.quote_plus(name)+"&type="+urllib.quote_plus(type)+"&genre=&area=&year=&order=hits&page=1"
        xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True,totalItems)
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

def progList(name,type,genre,area,year,order,page):
    str1 = 'type'
    str2 = type
    if genre:
        str1 = str1 + ',genre'
        str2 = str2 + ',' + genre
    if area:
        if type == 'lesson':
            str1 = str1 + ',school'
            str2 = str2 + ',' + area
        else:
            str1 = str1 + ',area'
            str2 = str2 + ',' + area
    if year:
        str1 = str1 + ',year'
        str2 = str2 + ',' + year
    url = 'http://movie.kankan.com/' + str1 +'/' + str2 + '/'
    if page:
        url = url + 'page' + page + '/'
        currpage = int(page)
    else:
        currpage = 1
    link = GetHttpData(url)
    match = re.compile('class="de_btn_l[^"]*"></a><span>[0-9]+/([0-9]+)</span>', re.DOTALL).findall(link)
    if len(match):
        totalpages = int(match[0])
    else:
        totalpages = 1
    match = re.compile('<div class="taglist_box">(.+?)<div id="taglist_more_div"', re.DOTALL).findall(link)
    if len(match):
        listpage = match[0]
    else:
        listpage = ''
    match = re.compile('<li id="movie_list_li_(.+?)</li>', re.DOTALL).findall(link)
    totalItems = len(match) + 1
    if currpage > 1: totalItems = totalItems + 1
    if currpage < totalpages: totalItems = totalItems + 1
    genrelist,arealist,yearlist = getList(listpage,type,genre,area,year)
    if genre:
        genrestr = searchDict(genrelist, genre)
    else:
        genrestr = '全部'
    if area:
        areastr = searchDict(arealist, area)
    else:
        areastr = '全部'
    if year:
        yearstr = searchDict(yearlist, year)
    else:
        yearstr = '全部'
    li = xbmcgui.ListItem(name+'（第'+str(currpage)+'/'+str(totalpages)+'页）【[COLOR FFFF0000]' + genrestr + '[/COLOR]/[COLOR FF00FF00]' + areastr + '[/COLOR]/[COLOR FFFFFF00]' + yearstr + '[/COLOR]/[COLOR FF00FFFF]' + searchDict(ORDER_LIST,order) + '[/COLOR]】（按此选择）')
    u = sys.argv[0]+"?mode=4&name="+urllib.quote_plus(name)+"&type="+urllib.quote_plus(type)+"&genre="+urllib.quote_plus(genre)+"&area="+urllib.quote_plus(area)+"&year="+urllib.quote_plus(year)+"&order="+urllib.quote_plus(order)+"&page="+urllib.quote_plus(listpage)
    xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, True, totalItems)
    for i in range(0,len(match)):
        match1 = re.compile('<a ref="post" href="(http://[^"]+)" title="([^"]+)"').search(match[i])   
        p_url = match1.group(1)
        p_name = match1.group(2)
        match1 = re.compile('<img src="[^"]+" _src="([^"]+)"').search(match[i])
        p_thumb = match1.group(1)
        match1 = re.compile('<span class="movtxt">(.+?)</span>').search(match[i])
        if match1:
            p_name1 = p_name + '（' + match1.group(1) + '）'
        else:
            p_name1 = p_name
        if match[i].find('<span class="movnum movnum_720">')>0:
            p_name1 += '[720P]'
            p_res = 1
        else:
            p_res = 0
        li = xbmcgui.ListItem(str(i + 1) + '. ' + p_name1, iconImage = '', thumbnailImage = p_thumb)
        u = sys.argv[0]+"?mode=2&name="+urllib.quote_plus(p_name)+"&url="+urllib.quote_plus(p_url)+"&thumb="+urllib.quote_plus(p_thumb)+"&res="+str(p_res)
        #li.setInfo(type = "Video", infoLabels = {"Title":p_name, "Director":p_director, "Genre":p_genre, "Plot":p_plot, "Year":p_year, "Cast":p_cast, "Tagline":p_tagline})
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, True, totalItems)
        
    if currpage > 1:
        li = xbmcgui.ListItem('上一页')
        u = sys.argv[0]+"?mode=1&name="+urllib.quote_plus(name)+"&type="+urllib.quote_plus(type)+"&genre="+urllib.quote_plus(genre)+"&area="+urllib.quote_plus(area)+"&year="+urllib.quote_plus(year)+"&order="+urllib.quote_plus(order)+"&page="+urllib.quote_plus(str(currpage-1))
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, True, totalItems)
    if currpage < totalpages:
        li = xbmcgui.ListItem('下一页')
        u = sys.argv[0]+"?mode=1&name="+urllib.quote_plus(name)+"&type="+urllib.quote_plus(type)+"&genre="+urllib.quote_plus(genre)+"&area="+urllib.quote_plus(area)+"&year="+urllib.quote_plus(year)+"&order="+urllib.quote_plus(order)+"&page="+urllib.quote_plus(str(currpage+1))
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, True, totalItems)
    xbmcplugin.setContent(int(sys.argv[1]), 'movies')
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

def seriesList(name,url,thumb,res):
    data = GetHttpData(url)
    match = re.compile("subids:\[(.+?)\],subnames:\['(.+?)'\]", re.DOTALL).search(data)
    subids = match.group(1).split(",")
    subnames = match.group(2).split("','")
    totalItems = len(subids)
    if totalItems == 1:
        PlayVideo(name,url,thumb,res)
        return
    for i in range(0, totalItems):
        p_url = "%s/%s.shtml" % (url[:-6], subids[i])
        p_name = "%s %s" % (name, subnames[i])
        if res == 1:
            p_name += '[720P]'
        li = xbmcgui.ListItem(p_name, iconImage = '', thumbnailImage = thumb)
        u = sys.argv[0]+"?mode=10&name="+urllib.quote_plus(p_name)+"&url="+urllib.quote_plus(p_url)+"&thumb="+urllib.quote_plus(thumb)+"&res="+str(res)
        #li.setInfo(type = "Video", infoLabels = {"Title":p_name, "Director":p_director, "Genre":p_genre, "Plot":p_plot, "Year":p_year, "Cast":p_cast, "Tagline":p_tagline})
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, False, totalItems)
    xbmcplugin.setContent(int(sys.argv[1]), 'movies')
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

def PlayVideo(name,url,thumb,res):
    res_limit = int(__addon__.getSetting('movie_res'))
    if res > res_limit:
        res = res_limit
    link = GetHttpData("http://www.flvcd.com/parse.php?kw="+url+"&format="+RES_LIST[res])
    match = re.compile('<a href="(http://[^/]+/data\d/cdn_transfer/[^"]+)" target="_blank"').findall(link)
    if not match:
        link = GetHttpData("http://www.flvcd.com/parse.php?kw="+url)
        match = re.compile('<a href="(http://[^/]+/data\d/cdn_transfer/[^"]+)" target="_blank"').findall(link)
    if match:
        playlist = xbmc.PlayList(1)
        playlist.clear()
        for i in range(0,len(match)):
            title = name+" 第"+str(i+1)+"/"+str(len(match))+"节"
            listitem = xbmcgui.ListItem(title, thumbnailImage=thumb)
            listitem.setInfo(type="Video",infoLabels={"Title":title})
            playlist.add(match[i], listitem)
        xbmc.Player().play(playlist)
    else:
        dialog = xbmcgui.Dialog()
        ok = dialog.ok(__addonname__, '无法解析视频')

def performChanges(name,type,genre,area,year,order,listpage):
    genrelist,arealist,yearlist = getList(listpage,type,genre,area,year)
    change = False
    dialog = xbmcgui.Dialog()
    if len(genrelist)>0:
        list = [x[1] for x in genrelist]
        sel = dialog.select('类型', list)
        if sel != -1:
            genre = genrelist[sel][0]
            change = True
    if len(arealist)>0:
        list = [x[1] for x in arealist]
        if type == 'lesson':
            title = '学校'
        else:
            title = '地区'
        sel = dialog.select(title, list)
        if sel != -1:
            area = arealist[sel][0]
            change = True       
    if len(yearlist)>0:
        list = [x[1] for x in yearlist]
        sel = dialog.select('年份', list)
        if sel != -1:
            year = yearlist[sel][0]
            change = True

    list = [x[1] for x in ORDER_LIST]
    sel = dialog.select('排序方式', list)
    if sel != -1:
        order = ORDER_LIST[sel][0]
        change = True

    if change:
        progList(name,type,genre,area,year,order,'1')

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
type = ''
genre = ''
area = ''
year = ''
order = ''
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
    genre = urllib.unquote_plus(params["genre"])
except:
    pass
try:
    type = urllib.unquote_plus(params["type"])
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
    progList(name,type,genre,area,year,order,page)
elif mode == 2:
    seriesList(name,url,thumb,res)
elif mode == 4:
    performChanges(name,type,genre,area,year,order,page)
elif mode == 10:
    PlayVideo(name,url,thumb,res)
