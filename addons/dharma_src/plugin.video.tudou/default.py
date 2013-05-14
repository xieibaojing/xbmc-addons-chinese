# -*- coding: utf-8 -*-
import xbmc, xbmcgui, xbmcplugin, xbmcaddon, urllib2, urllib, re, string, sys, os, gzip, StringIO

# Plugin constants 
__addon__     = xbmcaddon.Addon()
__addonname__ = __addon__.getAddonInfo('name')

CHANNEL_LIST = [['电影','ach22'],['电视剧','ach30'],['综艺','ach31'],['动漫','ach9'],['财富','ich24'],['科技','ich21'],['游戏','ich10'],['搞笑','ich5'],['美容','ich34'],['女性','ich27'],['乐活','ich3'],['健康','ich33'],['教育','ich25']]
ORDER_LIST = [['1','人气最旺'], ['2','最新发布'], ['3','评论最多'], ['5','挖得最多']]
ORDER_LIST2 = [['1','人气最旺'], ['2','最新发布'], ['3','评论最多'], ['4','分享最多'], ['5','挖得最多'], ['6','评分最高']]
RES_LIST = ['high', 'super']
TYPES1 = ('ach22', 'ach30', 'ach31') # 电影, 电视剧, 综艺
TYPES2 = ('ich24', 'ich21', 'ich10', 'ich5', 'ich34', 'ich27', 'ich3', 'ich33', 'ich25') # 财富, 科技, 游戏, 搞笑, 美容, 女性, 乐活, 健康, 教育
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

def getCurrent(text,list,id):
    match = re.compile('<li\s*class="current"\s*>\s*<a href="[^"]*">(.+?)</a>\s*</li>', re.DOTALL).search(text)
    if match:
        list.append([id, match.group(1)])

def getList(listpage,type,area,genre,stat,year):
    arealist = []
    genrelist = []
    statlist = []
    yearlist = []
    if type in TYPES1: # 电影, 电视剧, 综艺
        match = re.compile('<h3>地区：</h3>(.+?)</div>', re.DOTALL).search(listpage)
        arealist = re.compile('<li\s*>\s*<a href="ach\d+a([\-\d]+)[^"]*">(.+?)</a>\s*</li>', re.DOTALL).findall(match.group(1))
        getCurrent(match.group(1), arealist, area)
        match = re.compile('<h3>类型：</h3>(.+?)</div>', re.DOTALL).search(listpage)
        genrelist = re.compile('<li\s*>\s*<a href="ach\d+a[\-\d]+b([\-\d]+)[^"]*">(.+?)</a>\s*</li>', re.DOTALL).findall(match.group(1))
        getCurrent(match.group(1), genrelist, genre)
        match = re.compile('<h3>状态：</h3>(.+?)</div>', re.DOTALL).search(listpage)
        statlist = re.compile('<li\s*>\s*<a href="ach\d+a[\-\d]+b[\-\d]+c([\-\d]+)[^"]*">(.+?)</a>\s*</li>', re.DOTALL).findall(match.group(1))
        getCurrent(match.group(1), statlist, stat)
        match = re.compile('<h3>(年代|上映)：</h3>(.+?)</div>', re.DOTALL).search(listpage)
        yearlist = re.compile('<li\s*>\s*<a href="ach\d+a[\-\d]+b[\-\d]+c[\-\d]+d([\-\d]+)[^"]*">(.+?)</a>\s*</li>', re.DOTALL).findall(match.group(2))
        getCurrent(match.group(2), yearlist, year)
    elif type == 'ach9': # 动漫
        match = re.compile('<h3>版本：</h3>(.+?)</div>', re.DOTALL).search(listpage)
        yearlist = re.compile('<li\s*>\s*<a href="ach\d+a([\-\d]+)[^"]*">(.+?)</a>\s*</li>', re.DOTALL).findall(match.group(1))
        getCurrent(match.group(1), yearlist, year)
        match = re.compile('<h3>地区：</h3>(.+?)</div>', re.DOTALL).search(listpage)
        arealist = re.compile('<li\s*>\s*<a href="ach\d+a[\-\d]+b([\-\d]+)[^"]*">(.+?)</a>\s*</li>', re.DOTALL).findall(match.group(1))
        getCurrent(match.group(1), arealist, area)
        match = re.compile('<h3>类型：</h3>(.+?)</div>', re.DOTALL).search(listpage)
        genrelist = re.compile('<li\s*>\s*<a href="ach\d+a[\-\d]+b[\-\d]+c([\-\d]+)[^"]*">(.+?)</a>\s*</li>', re.DOTALL).findall(match.group(1))
        getCurrent(match.group(1), genrelist, genre)
        match = re.compile('<h3>状态：</h3>(.+?)</div>', re.DOTALL).search(listpage)
        statlist = re.compile('<li\s*>\s*<a href="ach\d+a[\-\d]+b[\-\d]+c[\-\d]+d([\-\d]+)[^"]*">(.+?)</a>\s*</li>', re.DOTALL).findall(match.group(1))
        getCurrent(match.group(1), statlist, stat)
    elif type in TYPES2: # 财富, 科技, 游戏, 搞笑, 美容, 女性, 乐活, 健康, 教育
        match = re.compile('<h3>类型：</h3>(.+?)</div>', re.DOTALL).search(listpage)
        genrelist = re.compile('<li\s*>\s*<a href="ich\d+a([\-\d]+)[^"]*">(.+?)</a>\s*</li>', re.DOTALL).findall(match.group(1))
        getCurrent(match.group(1), genrelist, genre)
        match = re.compile('<h3>发布时间：</h3>(.+?)</div>', re.DOTALL).search(listpage)
        yearlist = re.compile('<li\s*>\s*<a href="ich.+?so\d+pe([\-\d]+)[^"]*">(.+?)</a>\s*</li>', re.DOTALL).findall(match.group(1))
        getCurrent(match.group(1), yearlist, year)
    return arealist,genrelist,statlist,yearlist

def rootList():
    totalItems = len(CHANNEL_LIST)
    for name, type in CHANNEL_LIST:
        li = xbmcgui.ListItem(name)
        u = sys.argv[0]+"?mode=1&name="+urllib.quote_plus(name)+"&type="+urllib.quote_plus(type)+"&area=-2&genre=-2&stat=-2&year=-2&order=1&page=1"
        xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True,totalItems)
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

#          id     a       b     c      d     so    pa    pe
# 电影   ach22  area   genre  stat   year  order  page
# 电视剧 ach30  area   genre  stat   year  order  page
# 综艺   ach31  area   genre  stat   year  order  page
# 动漫   ach9   ver    area   genre  stat  order  page
# 财富   ich24  genre                                   time
# 科技   ich21  genre                                   time
# 游戏   ich10  genre                                   time
# 搞笑   ich5   genre                                   time
# 教育   ich25  genre                                   time
#
# 注：area/地区；type/类型；stat/状态；year/年代；ver/版本；time/发布时间
#　　 ver值用year参数保存和传递
#     time值用year参数保存和传递
def progList(name,type,area,genre,stat,year,order,page):
    para = ''
    if type in TYPES1: # 电影, 电视剧, 综艺
        para = 'a%sb%sc%sd%se-2f-2g-2h-2i-2j-2k-2l-2m-2n-2o-2so%spe-2pa%s.html' % (area, genre, stat, year, order, page)
    elif type == 'ach9': # 动漫
        para = 'a%sb%sc%sd%se-2f-2g-2h-2i-2j-2k-2l-2m-2n-2o-2so%spe-2pa%s.html' % (year, area, genre, stat, order, page)
    elif type in TYPES2: # 财富, 科技, 游戏, 搞笑, 美容, 女性, 乐活, 健康, 教育
        para = 'a%sb-2c-2d-2e-2f-2g-2h-2i-2j-2k-2l-2m-2n-2o-2so%spe%spa%s.html' % (genre, order, year, page)
    url = 'http://www.tudou.com/cate/%s%s' % (type, para)
    link = GetHttpData(url)
    match = re.compile('<div class="page-nav">(.+?)</div>', re.DOTALL).search(link)
    plist = []
    if match:
        match1 = re.compile('<li.+?>([0-9]+)(</a>)?</li>', re.DOTALL).findall(match.group(1))
        for num, temp in match1:
            if (num not in plist) and (num != page):
                plist.append(num)
        totalpages = int(match1[len(match1)-1][0])
    else:
        totalpages = 1
    match = re.compile('<div class="category-filter">(.+?)<div class="content">', re.DOTALL).search(link)
    if match:
        listpage = match.group(1)
    else:
        listpage = ''
    match = re.compile('<div class="pack pack_[^"]+">(.+?)<span class="ext_arrow"></span>', re.DOTALL).findall(link)
    if not match:
        match = re.compile('<div class="pack pack_[^"]+">(.+?)<li class="d_nums">', re.DOTALL).findall(link)
    totalItems = len(match) + 1 + len(plist)
    currpage = int(page)

    arealist,genrelist,statlist,yearlist = getList(listpage,type,area,genre,stat,year)
    if area == '-2':
        areastr = '全部地区'
    else:
        areastr = searchDict(arealist,area)
    if genre == '-2':
        genrestr = '全部类型'
    else:
        genrestr = searchDict(genrelist,genre)
    if stat == '-2':
        statstr = '全部状态'
    else:
        statstr = searchDict(statlist,stat)
    if year == '-2':
        if type == 'ach9': # 动漫
            yearstr = '全部版本'
        elif type in TYPES2: # 财富, 科技, 游戏, 搞笑, 美容, 女性, 乐活, 健康, 教育
            yearstr = '全部时间'
        else:
            yearstr = '全部年份'
    else:
        yearstr = searchDict(yearlist,year)
    li = xbmcgui.ListItem(name+'（第'+str(currpage)+'/'+str(totalpages)+'页）【[COLOR FFFF0000]' + areastr + '[/COLOR]/[COLOR FF00FF00]' + genrestr + '[/COLOR]/[COLOR FFFFFF00]' + statstr + '[/COLOR]/[COLOR FF00FFFF]' + yearstr + '[/COLOR]/[COLOR FF0000FF]' + searchDict(ORDER_LIST,order) + '[/COLOR]】（按此选择）')
    u = sys.argv[0]+"?mode=4&name="+urllib.quote_plus(name)+"&type="+urllib.quote_plus(type)+"&area="+urllib.quote_plus(area)+"&genre="+urllib.quote_plus(genre)+"&stat="+urllib.quote_plus(stat)+"&year="+urllib.quote_plus(year)+"&order="+order+"&page="+urllib.quote_plus(listpage)
    xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, True, totalItems)
    for i in range(0,len(match)):
        match1 = re.compile('<div class="txt">\s*<h6 class="caption">\s*<a [^>]+>(.+?)</a>\s*</h6>').search(match[i])
        p_name = match1.group(1)
        match1 = re.compile('<img class="quic" src="(.+?)"').search(match[i])
        if not match1:
            match1 = re.compile('class="pack_listImg" src="(.+?)"').search(match[i])
            p_thumb = match1.group(1)
            mode = 3
            isdir = False
        else:
            p_thumb = match1.group(1)
            mode = 2
            isdir = True
        match1 = re.compile('<div class="pic">\s*<a href="(.+?)"').search(match[i])
        p_url = match1.group(1)
        match1 = re.compile('<a .*?class="vinf".*?>(.*?)</a>').search(match[i])
        if match1 and match1.group(1):
            p_name1 = p_name + '（' + match1.group(1) + '）'
        else:
            p_name1 = p_name
        if match[i].find('<span class="hd720"></span>')>0:
            p_name1 += '[超清]'
            p_res = 1
        else:
            p_res = 0

        match1 = re.compile('<li class="desc">(.+?)</li>').search(match[i])
        if match1:
            p_tagline = match1.group(1)
        else:
            p_tagline = ''
        match1 = re.compile('<li class="cast">(.+?)</li>').search(match[i])
        if match1:
            p_cast = re.compile('<a [^>]+>(.+?)</a>').findall(match1.group(1))
        else:
            p_cast = []
        match1 = re.compile('<span class="ext_cast">导演: <a [^>]+>(.+?)</a>').search(match[i])
        if match1:
            p_director = match1.group(1)
        else:
            p_director = ''
        match1 = re.compile('<span class="ext_type">类型: (.+?)</span>').search(match[i])
        if match1:
            p_genre = match1.group(1)
        else:
            p_genre = ''
        match1 = re.compile('<p class="ext_intro">(.+?)</p>', re.DOTALL).search(match[i])
        if match1:
            p_plot = match1.group(1)
        else:
            p_plot = ''
        match1 = re.compile('<span class="ext_date">年代: ([0-9]+)</span>').search(match[i])
        if match1:
            p_year = int(match1.group(1))
        else:
            p_year = 0
        li = xbmcgui.ListItem(str(i + 1) + '. ' + p_name1, iconImage = '', thumbnailImage = p_thumb)
        u = sys.argv[0]+"?mode="+str(mode)+"&name="+urllib.quote_plus(p_name)+"&url="+urllib.quote_plus(p_url)+"&thumb="+urllib.quote_plus(p_thumb)+"&res="+str(p_res)
        li.setInfo(type = "Video", infoLabels = {"Title":p_name, "Director":p_director, "Genre":p_genre, "Plot":p_plot, "Year":p_year, "Cast":p_cast, "Tagline":p_tagline})
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, isdir, totalItems)

    # Fetch and build user selectable page number 
    for num in plist:
        li = xbmcgui.ListItem("... 第" + num + "页")
        u = sys.argv[0]+"?mode=1&name="+urllib.quote_plus(name)+"&type="+urllib.quote_plus(type)+"&area="+urllib.quote_plus(area)+"&genre="+urllib.quote_plus(genre)+"&stat="+urllib.quote_plus(stat)+"&year="+year+"&order="+order+"&page="+num
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, True, totalItems) 
    xbmcplugin.setContent(int(sys.argv[1]), 'movies')
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

def seriesList(name,url,thumb,res):
    link = GetHttpData(url)
    match = re.compile('<div class="pack pack_video_card">\s*<div class="pic">\s*<a target="new" title="(.+?)"\s*href="\s*(http://www.tudou.com/.*?.html)\s*"></a>\s*<div class="inner">\s*<img\s*src="(.+?)"', re.DOTALL).findall(link)
    if match:
        totalItems = len(match)
        for p_name, p_url, p_thumb in match:
            li = xbmcgui.ListItem(p_name, iconImage = '', thumbnailImage = p_thumb)
            u = sys.argv[0] + "?mode=3&name=" + urllib.quote_plus(p_name) + "&url=" + urllib.quote_plus(p_url)+ "&thumb=" + urllib.quote_plus(p_thumb)+"&res="+str(res)
            #li.setInfo(type = "Video", infoLabels = {"Title":p_name, "Director":p_director, "Cast":p_cast, "Plot":p_plot, "Year":p_year, "Rating":p_rating, "Votes":p_votes})
            xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, False, totalItems)
        xbmcplugin.setContent(int(sys.argv[1]), 'episodes')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
    else:
        match = re.compile('<div class="album-btn">\s*<a href="(http://www.tudou.com/.*?.html)"', re.DOTALL).findall(link)
        if match:
            PlayVideo(name,match[0],thumb,res)
        else:
            dialog = xbmcgui.Dialog()
            ok = dialog.ok(__addonname__, '没有可播放的视频')

def PlayTudou(name,iid,thumb):
    url = 'http://v2.tudou.com/v2/cdn?id=%s' % (iid)
    link = GetHttpData(url)
    match = re.compile('<f.+?brt="(\d+)"[^>]*>(.+?)</f>', re.DOTALL).findall(link)
    match.sort(reverse=True)
    listitem = xbmcgui.ListItem(name,thumbnailImage=thumb)
    listitem.setInfo(type="Video",infoLabels={"Title":name})
    xbmc.Player().play('%s|User-Agent=%s' % (match[0][1], UserAgent), listitem)

def PlayYouku(name,url,thumb,res):
    link = GetHttpData("http://www.flvcd.com/parse.php?kw=%s&format=%s" % (url, RES_LIST[res]))
    match = re.compile('<br>下载地址：(.*?)<br>花费时间：', re.DOTALL).findall(link)
    if match:
        match = re.compile('<a href="(http://.+?)" target="_blank"').findall(match[0])
        urls = ['%s|User-Agent=%s' % (x, UserAgent) for x in match]
        stackurl = 'stack://' + ' , '.join(urls)
        listitem = xbmcgui.ListItem(name,thumbnailImage=thumb)
        listitem.setInfo(type="Video",infoLabels={"Title":name})
        xbmc.Player().play(stackurl, listitem)
    else:
        match = re.compile('<br/>提示：\s*(.*?)</td>', re.DOTALL).findall(link)
        dialog = xbmcgui.Dialog()
        if match:
            ok = dialog.ok(__addonname__, match[0])
        else:
            ok = dialog.ok(__addonname__, '没有可播放的视频')

def PlayVideo(name,url,thumb,res):
    link = GetHttpData(url)
    match = re.compile('itemData=\{(.+?)\};', re.DOTALL).search(link)
    if match:
        iid = ''
        vcode = ''
        #llist = ''
        # 解析土豆视频id (iid)
        match1 = re.compile('iid: (\d+)').search(match.group(1))
        if match1:
            iid = match1.group(1)
        # 解析优酷视频id (vcode)
        match1 = re.compile("vcode: '([^']+)'").search(match.group(1))
        if match1:
            vcode = match1.group(1)
        lang_select = int(__addon__.getSetting('lang_select')) # 默认|每次选择|自动首选
        if lang_select != 0:
            # 解析优酷多语种id
            match1 = re.compile("\{id: \d+, vcode: '([^']+)', lan: '([^']+)'\}").findall(link)
            if match1:
                #llist =  '; '.join(['%s=%s' % (x[1],x[0]) for x in match1])
                if lang_select == 1:
                    list = [x[1] for x in match1]
                    sel = xbmcgui.Dialog().select('选择语言', list)
                    if sel ==-1:
                        return
                    vcode = match1[sel][0]
                    name = '%s（%s）' % (name, match1[sel][1])
                else:
                    lang_prefer = __addon__.getSetting('lang_prefer') # 国语|粤语
                    for i in range(0,len(match1)):
                        if match1[i][1] == lang_prefer:
                            vcode = match1[i][0]
                            name = '%s（%s）' % (name, match1[i][1])
                            break
        #ok = xbmcgui.Dialog().ok(__addonname__, 'iid=%s, vcode=%s' % (iid,vcode), llist)
        if (not vcode) and iid:
            PlayTudou(name,iid,thumb)
            return
        if vcode:
            url = 'http://v.youku.com/v_show/id_%s.html' % (vcode)
    PlayYouku(name,url,thumb,res)

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
        sel = dialog.select('类型', list)
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
area = '-2'
genre = '-2'
stat = '-2'
year = '-2'
order = '1'
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
    seriesList(name,url,thumb,res)
elif mode == 3:
    PlayVideo(name,url,thumb,res)
elif mode == 4:
    performChanges(name,page,type,area,genre,stat,year,order)
