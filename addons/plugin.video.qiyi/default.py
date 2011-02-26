# -*- coding: utf-8 -*-
import xbmc, xbmcgui, xbmcplugin, xbmcaddon, urllib2, urllib, re, string, sys, os

# QIYI.COM(奇艺视频) by taxigps, 2011

# Plugin constants 
__addonname__ = "奇艺视频"
__addonid__ = "plugin.video.qiyi"
__addon__ = xbmcaddon.Addon(id=__addonid__)

CHANNEL_LIST = [['电影','1'], ['电视剧','2'], ['动漫','4'], ['综艺','6']]
CHANNEL_DICT = dict(CHANNEL_LIST)
ORDER_LIST = [['关注','5'], ['最新','2'], ['热播','3'], ['好评','4']]
ORDER_DICT = dict(ORDER_LIST)

MOVIE_TYPE_LIST = {}
MOVIE_TYPE_DICT = {}
MOVIE_AREA_LIST = {}
MOVIE_AREA_DICT = {}
MOVIE_TYPE_LIST['1'] = [['全部',''],['爱情','6'],['战争','7'],['喜剧','8'],['动作','11'],['动画','12'],['悲剧','13'],['灾难','14'],['剧情','127'],['惊悚','128'],['青春','130'],['传记','132'],['恐怖','10'],['魔幻','129'],['科幻','9'],['枪战','131'],['艺术片','133'],]
MOVIE_AREA_LIST['1'] = [['全部',''],['华语','1'],['美国','2'],['欧洲','3'],['韩国','4'],['日本','308'],]
MOVIE_TYPE_LIST['2'] = [['全部',''],['言情','20'],['历史','21'],['战争','22'],['谍战','290'],['武侠','23'],['古装','24'],['传记','25'],['现代','26'],['年代','27'],['都市','28'],['农村','29'],['偶像','30'],['刑侦','31'],['悬疑','32'],['情景','33'],['伦理','35'],['生活','136'],['宫廷','139'],['励志','147'],['革命','142'],['主旋律','137'],['名著','143'],['儿童','36'],['喜剧','135'],['商战','140'],['神话','145'],['罪案','149'],['科幻','34'],['穿越','148'],['青少','144'],['反腐','146'],['戏说','141'],]
MOVIE_AREA_LIST['2'] = [['全部',''],['内地','15'],['港台','16'],['韩国','17'],['美剧','18'],['其他','19'],]
MOVIE_TYPE_LIST['4'] = [['全部',''],['动作','41'],['亲子','316'],['热血','42'],['冒险','48'],['古代','45'],['未来','46'],['竞技','49'],['体育','50'],['搞笑','51'],['言情','52'],['校园','53'],['都市','54'],['魔幻','55'],['科幻','56'],['励志','297'],['剧情','59'],['悬疑','60'],['宠物','61'],['LOLI','62'],['益智','298'],['童话','299'],['真人','300'],['神话','301'],]
MOVIE_AREA_LIST['4'] = [['全部',''],['大陆','37'],['日本','38'],['美国','39'],['其他','40'],]
MOVIE_TYPE_LIST['6'] = [['全部',''],['播报','155'],['访谈','156'],['搞笑','157'],['游戏','158'],['选秀','159'],['时尚','160'],['杂谈','161'],['情感','163'],['盛会','292'],['曲艺','293'],]
MOVIE_AREA_LIST['6'] = [['全部',''],['内地','151'],['港台','152'],]
for channel, id in CHANNEL_LIST:
    MOVIE_TYPE_DICT[id] = dict(MOVIE_TYPE_LIST[id])
    MOVIE_AREA_DICT[id] = dict(MOVIE_AREA_LIST[id])

def GetHttpData(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    httpdata = response.read()
    response.close()
    httpdata = re.sub("\s", "", httpdata)
    return httpdata

def getPlayURL(html):
    match1 = re.compile('pid:"(.+?)",//').findall(html)
    if len(match1) > 0:
        pid = match1[0]
        match1 = re.compile('ptype:"(.+?)",//').findall(html)
        ptype = match1[0]
        match1 = re.compile('videoId:"(.+?)",//').findall(html)
        videoId = match1[0]
        url = 'http://cache.video.qiyi.com/v/' + videoId + '/' + pid + '/' + ptype + '/'
    else:
        url = ''
    return url

def rootList():
    page = __addon__.getSetting('page')
    currpage = int(page)
    channel = __addon__.getSetting('channel')
    id = CHANNEL_DICT[channel]
    movie_area = __addon__.getSetting('movie_area')
    c1 = MOVIE_AREA_DICT[id][movie_area]
    movie_type = __addon__.getSetting('movie_type')
    c2 = MOVIE_TYPE_DICT[id][movie_type]
    order = __addon__.getSetting('order')
    c13 = ORDER_DICT[order]
    url = 'http://list.qiyi.com/www/' + id + '/' + c1 + '-' + c2 + '-----------' + c13 + '-1-' + page + '----.html'
    link = GetHttpData(url)
    match1 = re.compile('data-key="([0-9]+)"').findall(link)
    totalpages = int(match1[len(match1) - 1])
    match1 = re.compile('<ulid="rs"(.+?)</ul>').findall(link)
    match = re.compile('<li><ahref="(.+?)"class="imgBg1(.*?)"><.+?src="(.+?)"title="(.+?)"alt=".+?<spanid="fenshu"class="fRed"><strong>(.+?)</strong>(.*?)</span><spanclass="fBlack"></span>（(.*?)评）</p></li>').findall(match1[0])
    totalItems = len(match) + 2
    if currpage > 1: totalItems = totalItems + 1
    if currpage < totalpages: totalItems = totalItems + 1

    li = xbmcgui.ListItem('节目分类[COLOR FF00FF00]【' + channel + '】[/COLOR]（按此选择）')
    u = sys.argv[0] + "?mode=4"
    xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, True, totalItems)
    li = xbmcgui.ListItem('类型[COLOR FFFF0000]【' + movie_type + '】[/COLOR] 地区[COLOR FFFF0000]【' + movie_area + '】[/COLOR] 排序[COLOR FFFF0000]【' + order + '】[/COLOR]（按此选择）')
    u = sys.argv[0] + "?mode=5"
    xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, True, totalItems)

    for i in range(0,len(match)):
        p_url = match[i][0]
        p_name = match[i][3]
        if match[i][1]=='chaoqing_pic':
            p_name = p_name + '(超清)'
        p_thumb = match[i][2]
        p_rating = float(match[i][4] + match[i][5])
        p_votes = match[i][6]
        li = xbmcgui.ListItem(str(i + 1) + '.' + p_name, p_thumb, p_thumb)
        link = GetHttpData(p_url)
        v_url = getPlayURL(link)
        if v_url != '':
            # 能够获取播放页面，为单个视频
            match1 = re.compile('上映年份：<ahref=".*?">([0-9]*)').findall(link)
            if len(match1) == 0:
                match1 = re.compile('出品年份：<!--.*?-->([0-9]*)').findall(link)
            if len(match1) == 0:
                p_year = 0
            else:
                p_year = int(match1[0])
            match1 = re.compile('导演：<ahref=".*?">(.*?)</a>').findall(link)
            if len(match1) == 0:
                p_director = ''
            else:
                p_director = match1[0]
            p_cast = re.compile('class="f14">(.*?)</a>饰演<spanclass="f14">(.*?)</span>').findall(link)
            match1 = re.compile('<pid="desc1".*?>(.*?)</p>').findall(link)
            p_plot = match1[0]
            u = sys.argv[0] + "?mode=2&name=" + urllib.quote_plus(p_name) + "&url=" + urllib.quote_plus(v_url)+ "&thumb=" + urllib.quote_plus(p_thumb)
            li.setInfo(type = "Video", infoLabels = {"Title":p_name, "Director":p_director, "Cast":p_cast, "Plot":p_plot, "Year":p_year, "Rating":p_rating, "Votes":p_votes})
            xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, False, totalItems)
        else:
            # 无法获取播放页面，为剧集
            match1 = re.compile('年份：<ahref=".*?">([0-9]*)').findall(link)
            if len(match1) == 0:
                match1 = re.compile('出品年份：([0-9]*)').findall(link)
            p_year = int(match1[0])
            match1 = re.compile('导演：<ahref=".*?">(.*?)</a>').findall(link)
            if len(match1) == 0:
                p_director = ''
            else:
                p_director = match1[0]
            p_cast = re.compile('class="f14">(.*?)</a>饰演<spanclass="f14">(.*?)</span>').findall(link)
            match1 = re.compile('<pclass="zhuanjiP2">(.*?)</p>').findall(link)
            p_plot = match1[0]
            u = sys.argv[0] + "?mode=3&name=" + urllib.quote_plus(p_name) + "&url=" + urllib.quote_plus(p_url)+ "&thumb=" + urllib.quote_plus(p_thumb)
            li.setInfo(type = "Video", infoLabels = {"Title":p_name, "Director":p_director, "Cast":p_cast, "Plot":p_plot, "Year":p_year, "Rating":p_rating, "Votes":p_votes})
            xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, True, totalItems)

    if currpage > 1:
        li = xbmcgui.ListItem('上一页（第'+page+'页/共'+str(totalpages)+'页）')
        u = sys.argv[0] + "?mode=1&page=" + urllib.quote_plus(str(currpage - 1))
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, True, totalItems)
    if currpage < totalpages:
        li = xbmcgui.ListItem('下一页（第'+page+'页/共'+str(totalpages)+'页）')
        u = sys.argv[0] + "?mode=1&page=" + urllib.quote_plus(str(currpage + 1))
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, True, totalItems)
    xbmcplugin.setContent(int(sys.argv[1]), 'movies')
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

def seriesList(url, name, thumb):
    link = GetHttpData(url)
    match1 = re.compile('年份：<ahref=".*?">([0-9]*)').findall(link)
    if len(match1) == 0:
        match1 = re.compile('出品年份：([0-9]*)').findall(link)
    p_year = int(match1[0])
    match1 = re.compile('导演：<ahref=".*?">(.*?)</a>').findall(link)
    if len(match1) == 0:
        p_director = ''
    else:
        p_director = match1[0]
    p_cast = re.compile('class="f14">(.*?)</a>饰演<spanclass="f14">(.*?)</span>').findall(link)
    match1 = re.compile('<divid="j-album-[^>]*>(.*?)</div>').findall(link)
    album = ''
    for url1 in match1:
        album = album + GetHttpData('http://www.qiyi.com' + url1)
    match2 = re.compile('<divid="j-desc-[^>]*>(.*?)</div>').findall(link)
    desc = ''
    for url1 in match2:
        desc = desc + GetHttpData('http://www.qiyi.com' + url1)
    match = re.compile('<li><ahref="(.+?)"class="imgBg1"><.+?src="(.+?)"title="(.+?)".*?">第([0-9]+)集</a></li>').findall(album)
    totalItems = len(match)
    for p_url, p_thumb, p_name, p_episode in match:
        match1 = re.compile('<ahref="' + p_url + '">' + p_name + '</a></span><pstyle=.*?>(.*?)</p>').findall(desc)
        if len(match1) > 0:
            p_plot = match1[0]
        else:
            p_plot = ''
        li = xbmcgui.ListItem(p_name, p_thumb, p_thumb)
        li.setInfo(type = "Video", infoLabels = {"Title":p_name, "Director":p_director, "Cast":p_cast, "Plot":p_plot, "Year":p_year})
        u = sys.argv[0] + "?mode=2&name=" + urllib.quote_plus(p_name) + "&url=" + urllib.quote_plus(p_url)+ "&thumb=" + urllib.quote_plus(p_thumb)
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, False, totalItems)
    xbmcplugin.setContent(int(sys.argv[1]), 'episodes')
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

def PlayVideo(url,name,thumb):
    if url.find('http://cache.video.qiyi.com/v/') == -1:
        link = GetHttpData(url)
        url = getPlayURL(link)
    link = GetHttpData(url)
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

def performChannel():
    dialog = xbmcgui.Dialog()
    list = [x[0] for x in CHANNEL_LIST]
    sel = dialog.select('节目分类', list)
    if sel != -1:
        __addon__.setSetting(id="channel", value=list[sel])
        __addon__.setSetting(id="movie_type", value='全部')
        __addon__.setSetting(id="movie_area", value='全部')
        __addon__.setSetting(id="order", value='最新')
        __addon__.setSetting(id="page", value="1")
        xbmc.executebuiltin('Container.Refresh')

def performChanges():
    change = False
    channel = __addon__.getSetting('channel')
    id = CHANNEL_DICT[channel]
    dialog = xbmcgui.Dialog()
    list = [x[0] for x in MOVIE_TYPE_LIST[id]]
    sel = dialog.select('类型', list)
    if sel != -1:
        __addon__.setSetting(id="movie_type", value=list[sel])
        __addon__.setSetting(id="page", value="1")
        change = True

    list = [x[0] for x in MOVIE_AREA_LIST[id]]
    sel = dialog.select('地区', list)
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
    rootList()
elif mode == 1:
    __addon__.setSetting(id="page", value=page)
    xbmc.executebuiltin('Container.Refresh')
elif mode == 2:
    PlayVideo(url, name, thumb)
elif mode == 3:
    seriesList(url, name, thumb)
elif mode == 4:
    performChannel()
elif mode == 5:
    performChanges()

