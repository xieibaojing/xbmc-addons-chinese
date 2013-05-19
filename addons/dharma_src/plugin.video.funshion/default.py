# -*- coding: utf-8 -*-
import xbmc, xbmcgui, xbmcplugin, xbmcaddon, urllib2, urllib, re, string, sys, os, gzip, StringIO
if sys.version_info < (2, 7):
    import simplejson
else:
    import json as simplejson

# Plugin constants 
__addon__     = xbmcaddon.Addon()
__addonname__ = __addon__.getAddonInfo('name')

CHANNEL_LIST = [['电影','movie'],['电视剧','tv'],['动漫','cartoon'],['综艺','variety'],['娱乐','ent'],['体育','sports'],['视频','video']]
ORDER_LIST = [['mo','最近更新'], ['z4','最受欢迎'], ['ka','评分最高'], ['re','最新上映']]
RES_LIST = [['tv','标清'], ['dvd','高清'], ['high-dvd','超清']]
LANG_LIST = [['chi','国语'], ['arm','粤语'], ['und','原声']]
TYPES1 = ('movie', 'tv', 'cartoon', 'variety') # 电影, 电视剧, 动漫, 综艺
TYPES2 = ('ent', 'video') # 娱乐, 视频
TYPES3 = ('ent', 'sports') # 娱乐, 体育
UserAgent = 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)'

def log(txt):
    message = '%s: %s' % (__addonname__, txt)
    xbmc.log(msg=message, level=xbmc.LOGDEBUG)

def GetHttpData(url):
    log("%s::url - %s" % (sys._getframe().f_code.co_name, url))
    req = urllib2.Request(url)
    req.add_header('User-Agent', UserAgent)
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

def getList(listpage,type,area,genre,stat,year):
    arealist = []
    genrelist = []
    statlist = []
    yearlist = []
    if type in TYPES1: # 电影, 电视剧, 动漫, 综艺
        match = re.compile('<li><label>按地区：</label>(.+?)</li>', re.DOTALL).search(listpage)
        arealist = re.compile("<a\s+href='/list/%s/.*?\.r-([^'\.]+)[^>]*><span>(.+?)</span></a>" % (type), re.DOTALL).findall(match.group(1))
        arealist.insert(0,['','全部地区'])
        match = re.compile('<li><label>按类型：</label>(.+?)</li>', re.DOTALL).search(listpage)
        genrelist = re.compile("<a\s+href='/list/%s/c-(.+?)\.o-[^>]*><span>(.+?)</span></a>" % (type), re.DOTALL).findall(match.group(1))
        genrelist.insert(0,['','全部类型'])
        match = re.compile('<li><label>按区间：</label>(.+?)</li>', re.DOTALL).search(listpage)
        yearlist = re.compile("<a\s+href='/list/%s/.*?\.p-([^\.]+)\.[^>]*>(.+?)</a>" % (type), re.DOTALL).findall(match.group(1))
        yearlist.insert(0,['','全部年份'])
        statlist = re.compile("<a\s+href='/list/%s/.*?\.u-(\d+)[^>]*>(.+?)</a>" % (type), re.DOTALL).findall(match.group(1))
        statlist.insert(0,['','全部更新'])
    else:
        if type in TYPES2: # 娱乐, 视频
            match = re.compile('<li><label>按类型：</label>(.+?)</li>', re.DOTALL).search(listpage)
            genrelist = re.compile("<a\s+href='/list/%s/c-([^'\.]+)[^>]*><span>(.+?)</span></a>" % (type), re.DOTALL).findall(match.group(1))
            genrelist.insert(0,['','全部类型'])
        else:
            match = re.compile('<li><label>按项目：</label>(.+?)</li>', re.DOTALL).search(listpage)
            genrelist = re.compile("<a\s+href='/list/%s/.*?s-([^'\.]+)[^>]*><span>(.+?)</span></a>" % (type), re.DOTALL).findall(match.group(1))
            genrelist.insert(0,['','全部项目'])
        if type in TYPES3: # 娱乐, 体育
            match = re.compile('<li><label>按更新：</label>(.+?)</li>', re.DOTALL).search(listpage)
            statlist = re.compile("<a\s+href='/list/%s/.*?m-(\d+)[^>]*><span>(.+?)</span></a>" % (type), re.DOTALL).findall(match.group(1))
        
    return arealist,genrelist,statlist,yearlist

def rootList():
    totalItems = len(CHANNEL_LIST)
    for name, type in CHANNEL_LIST:
        li = xbmcgui.ListItem(name)
        u = sys.argv[0]+"?mode=1&name="+urllib.quote_plus(name)+"&type="+urllib.quote_plus(type)+"&area=&genre=&stat=&year=&order=z4&page=1"
        xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True,totalItems)
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

def progList(name,type,area,genre,stat,year,order,page):
    para = []
    if type in TYPES1: # 电影, 电视剧, 动漫, 综艺
        # http://www.funshion.com/list/tv/c-e788b1e68385.o-z4.p-2013.pg-2.pt-vp.r-e58685e59cb0.u-4
        if genre:
            para.append('c-%s' % (genre))
        para.append('o-%s' % (order))
        if year:
            para.append('p-%s' % (year))
        para.append('pg-%s' % (page))
        para.append('pt-vp')
        if area:
            para.append('r-%s' % (area))
        if stat:
            para.append('u-%s' % (stat))
    else:
        if type in TYPES2: # 娱乐, 视频
            if genre:
                para.append('c-%s' % (genre))
        if type in TYPES3: # 娱乐, 体育
            if not stat:
                stat = '0'
            para.append('m-%s' % (stat))
        para.append('o-%s' % (order))
        para.append('pg-%s' % (page))
        if type == 'sports':
            if genre:
                para.append('s-%s' % (genre))
    url = 'http://www.funshion.com/list/%s/%s' % (type, '.'.join(para))
    link = GetHttpData(url)
    match = re.compile('<p class="page-index">(.+?)</p>', re.DOTALL).search(link)
    plist = []
    if match:
        match1 = re.compile('pg-(\d+)', re.DOTALL).findall(match.group(1))
        for num in match1:
            if (num not in plist) and (num != page):
                plist.append(num)
    match = re.compile('<div class="sort"(.+?)</ul>', re.DOTALL).search(link)
    if match:
        listpage = match.group(1)
    else:
        listpage = ''
    match = re.compile('(<div class="video-block[^"]*">.+?)</div>\s*</div>', re.DOTALL).findall(link)
    totalItems = len(match) + 1 + len(plist)
    currpage = int(page)

    arealist,genrelist,statlist,yearlist = getList(listpage,type,area,genre,stat,year)
    areastr = searchDict(arealist,area)
    genrestr = searchDict(genrelist,genre)
    statstr = searchDict(statlist,stat)
    yearstr = searchDict(yearlist,year)
    li = xbmcgui.ListItem(name+'（第'+str(currpage)+'页）【[COLOR FFFF0000]' + areastr + '[/COLOR]/[COLOR FF00FF00]' + genrestr + '[/COLOR]/[COLOR FFFFFF00]' + statstr + '[/COLOR]/[COLOR FF00FFFF]' + yearstr + '[/COLOR]/[COLOR FF0000FF]' + searchDict(ORDER_LIST,order) + '[/COLOR]】（按此选择）')
    u = sys.argv[0]+"?mode=10&name="+urllib.quote_plus(name)+"&type="+urllib.quote_plus(type)+"&area="+urllib.quote_plus(area)+"&genre="+urllib.quote_plus(genre)+"&stat="+urllib.quote_plus(stat)+"&year="+urllib.quote_plus(year)+"&order="+order+"&page="+urllib.quote_plus(listpage)
    xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, True, totalItems)
    for i in range(0,len(match)):
        if type in ('tv', 'cartoon', 'variety'): # 电视剧, 动漫, 综艺
            isdir = True
            mode = 2
        elif type == 'movie': # 电影
            isdir = False
            mode = 3
        else:                 # 娱乐, 体育, 视频
            isdir = False
            mode = 4
        if type in TYPES1: # 电影, 电视剧, 动漫, 综艺
            match1 = re.compile('<div class="trumb" rel="(\d+)">').search(match[i])
            p_id = match1.group(1)
        else:
            match1 = re.compile('/play/(\d+)"').search(match[i])
            p_id = match1.group(1)
        match1 = re.compile('class="(title theight|title|tit)"[^>]*>(.+?)</a>').search(match[i])
        p_name = match1.group(2)
        match1 = re.compile('_lazysrc="(.*?)"').search(match[i])
        if not match1:
            match1 = re.compile('<img src="(.*?)"').search(match[i])
        p_thumb = match1.group(1)
        match1 = re.compile("<span class='sright'>(.+?)</span>").search(match[i])
        if match1 and match1.group(1):
            p_name1 = p_name + '（' + match1.group(1) + '）'
        else:
            p_name1 = p_name
        if match[i].find('class="video-block mvsp"')>0:
            p_name1 += ' [超清]'
        elif match[i].find('class="video-block mvhd"')>0:
            p_name1 += ' [高清]'
        li = xbmcgui.ListItem(str(i + 1) + '. ' + p_name1, iconImage = '', thumbnailImage = p_thumb)
        u = sys.argv[0]+"?mode="+str(mode)+"&name="+urllib.quote_plus(p_name)+"&id="+urllib.quote_plus(p_id)+"&thumb="+urllib.quote_plus(p_thumb)+"&type="+urllib.quote_plus(type)
        li.setInfo(type = "Video", infoLabels = {"Title":p_name})
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, isdir, totalItems)

    for num in plist:
        li = xbmcgui.ListItem("... 第" + num + "页")
        u = sys.argv[0]+"?mode=1&name="+urllib.quote_plus(name)+"&type="+urllib.quote_plus(type)+"&area="+urllib.quote_plus(area)+"&genre="+urllib.quote_plus(genre)+"&stat="+urllib.quote_plus(stat)+"&year="+year+"&order="+order+"&page="+num
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, True, totalItems) 
    xbmcplugin.setContent(int(sys.argv[1]), 'movies')
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

def seriesList(name,id,thumb):
    url = 'http://api.funshion.com/ajax/get_web_fsp/%s/mp4' % (id)
    link = GetHttpData(url)
    json_response = simplejson.loads(link)
    items = json_response['data']['fsps']['mult']
    totalItems = len(items)
    for item in items:
        p_name = item['full'].encode('utf-8')
        p_name1 = '%s(%s)' % (p_name, searchDict(RES_LIST,item['clarity_value'].encode('utf-8')))
        p_id2 = item['number'].encode('utf-8')
        p_thumb = item['imagepath'].encode('utf-8')
        if not p_thumb:
            p_thumb = thumb
        li = xbmcgui.ListItem(p_name1, iconImage = '', thumbnailImage = p_thumb)
        u = sys.argv[0] + "?mode=3&name=" + urllib.quote_plus(p_name) + "&id=" + urllib.quote_plus(id)+ "&thumb=" + urllib.quote_plus(p_thumb) + "&id2=" + urllib.quote_plus(p_id2)
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, False, totalItems)
    xbmcplugin.setContent(int(sys.argv[1]), 'episodes')
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

def selResolution(items):
    ratelist = []
    for i in range(0,len(items)):
        if items[i][0] == RES_LIST[0][0]: ratelist.append([3, RES_LIST[0][1], i]) # [清晰度设置值, 清晰度, items索引]
        if items[i][0] == RES_LIST[1][0]: ratelist.append([2, RES_LIST[1][1], i])
        if items[i][0] == RES_LIST[2][0]: ratelist.append([1, RES_LIST[2][1], i])
    ratelist.sort()
    if len(ratelist) > 1:
        resolution = int(__addon__.getSetting('resolution'))
        if resolution == 0:    # 每次询问视频清晰度
            list = [x[1] for x in ratelist]
            sel = xbmcgui.Dialog().select('清晰度（低网速请选择低清晰度）', list)
            if sel == -1:
                return None, None
        else:
            sel = 0
            while sel < len(ratelist)-1 and resolution > ratelist[sel][0]: sel += 1
    else:
        sel = 0
    return items[ratelist[sel][2]][1], ratelist[sel][1]

def PlayVideo(name,id,thumb,id2):
    url = 'http://api.funshion.com/ajax/get_webplayinfo/%s/%s/mp4' % (id, id2)
    link = GetHttpData(url)
    json_response = simplejson.loads(link)
    if not json_response['playinfos']:
        ok = xbmcgui.Dialog().ok(__addonname__, '没有可播放的视频')
        return

    langlist = set([x['dub_one'].encode('utf-8') for x in json_response['playinfos']])
    langlist = [x for x in langlist]
    langid = json_response['playinfos'][0]['dub_one'].encode('utf-8')
    lang_select = int(__addon__.getSetting('lang_select')) # 默认|每次选择|自动首选
    if lang_select != 0 and len(langlist) > 1:
        if lang_select == 1:
            list = [searchDict(LANG_LIST,x) for x in langlist]
            sel = xbmcgui.Dialog().select('选择语言', list)
            if sel ==-1:
                return
            langid = langlist[sel]
        else:
            lang_prefer = __addon__.getSetting('lang_prefer') # 国语|粤语
            for i in range(0,len(LANG_LIST)):
                if LANG_LIST[i][1] == lang_prefer:
                    if LANG_LIST[i][0] in langlist:
                        langid = LANG_LIST[i][0]
                    break

    items = [[x['clarity'].encode('utf-8'), x['hashid'].encode('utf-8')]for x in json_response['playinfos'] if x['dub_one'].encode('utf-8') == langid]
    hashid, res = selResolution(items)
    lang = searchDict(LANG_LIST,langid)
    name = '%s(%s %s)' % (name, lang, res)
    url = 'http://jobsfe.funshion.com/query/v1/mp4/%s.json' % (hashid)
    link = GetHttpData(url)
    json_response = simplejson.loads(link)
    if json_response['return'].encode('utf-8') == 'succ':
        listitem = xbmcgui.ListItem(name,thumbnailImage=thumb)
        xbmc.Player().play(json_response['playlist'][0]['urls'][0], listitem)
    else:
        ok = xbmcgui.Dialog().ok(__addonname__, '没有可播放的视频')

def PlayVideo2(name,id,thumb,type):
    if type == 'video':
        url = 'http://api.funshion.com/ajax/get_media_data/ugc/%s' % (id)
    else:
        url = 'http://api.funshion.com/ajax/get_media_data/video/%s' % (id)
    link = GetHttpData(url)
    json_response = simplejson.loads(link)
    hashid = json_response['data']['hashid'].encode('utf-8')
    filename = json_response['data']['filename'].encode('utf-8')
    url = 'http://jobsfe.funshion.com//query/v1/mp4/%s.json?file=%s' % (hashid, filename)
    link = GetHttpData(url)
    json_response = simplejson.loads(link)
    if json_response['return'].encode('utf-8') == 'succ':
        listitem = xbmcgui.ListItem(name,thumbnailImage=thumb)
        xbmc.Player().play(json_response['playlist'][0]['urls'][0], listitem)
    else:
        ok = xbmcgui.Dialog().ok(__addonname__, '没有可播放的视频')

def performChanges(name,listpage,type,area,genre,stat,year,order):
    arealist,genrelist,statlist,yearlist = getList(listpage,type,area,genre,stat,year)
    change = False
    dialog = xbmcgui.Dialog()
    if len(arealist)>0:
        list = [x[1] for x in arealist]
        sel = dialog.select('地区', list)
        if sel != -1:
            area = arealist[sel][0]
            change = True
    if len(genrelist)>0:
        list = [x[1] for x in genrelist]
        sel = dialog.select('类型', list)
        if sel != -1:
            genre = genrelist[sel][0]
            change = True
    if len(statlist)>0:
        list = [x[1] for x in statlist]
        sel = dialog.select('更新', list)
        if sel != -1:
            stat = statlist[sel][0]
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
        progList(name,type,area,genre,stat,year,order,'1')

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
area = ''
genre = ''
stat = ''
year = ''
order = ''
page = '1'
id = None
thumb = None
id2 = '1'

try:
    id2 = int(params["id2"])
except:
    pass
try:
    thumb = urllib.unquote_plus(params["thumb"])
except:
    pass
try:
    id = urllib.unquote_plus(params["id"])
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
    stat = urllib.unquote_plus(params["stat"])
except:
    pass
try:
    genre = urllib.unquote_plus(params["genre"])
except:
    pass
try:
    area = urllib.unquote_plus(params["area"])
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
    progList(name,type,area,genre,stat,year,order,page)
elif mode == 2:
    seriesList(name,id,thumb)
elif mode == 3:
    PlayVideo(name,id,thumb,id2)
elif mode == 4:
    PlayVideo2(name,id,thumb,type)
elif mode == 10:
    performChanges(name,page,type,area,genre,stat,year,order)
