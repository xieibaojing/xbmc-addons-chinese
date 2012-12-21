# -*- coding: utf-8 -*-
import xbmc, xbmcgui, xbmcplugin, xbmcaddon, urllib2, urllib, re, string, sys, os, gzip, StringIO
if sys.version_info < (2, 7):
    import simplejson
else:
    import json as simplejson

############################################################
# 奇艺视频(QIYI) by taxigps, 2012
############################################################

# Plugin constants 
__addonname__ = "奇艺视频(QIYI)"
__addonid__   = "plugin.video.qiyi"
__addon__     = xbmcaddon.Addon(id=__addonid__)
__cwd__       = xbmc.translatePath(__addon__.getAddonInfo('path'))
__icon__      = os.path.join( __cwd__, 'icon.png' )

CHANNEL_LIST = [['电影','1'], ['电视剧','2'], ['纪录片','3'], ['动漫','4'], ['音乐','5'], ['综艺','6'], ['娱乐','7'], ['旅游','9'], ['片花','10'], ['时尚','13']]
ORDER_LIST = [['2','最新更新'], ['3','最近热播'], ['6 ','最新上映'], ['4','最受好评']]
PAYTYPE_LIST = [['','全部影片'], ['0','免费影片'], ['1','会员免费'], ['2','付费点播']]

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
   
def urlExists(url):
    try:
        resp = urllib2.urlopen(url)
        result = True
        resp.close()
    except:
        result = False
    return result

def searchDict(dlist,idx):
    for i in range(0,len(dlist)):
        if dlist[i][0] == idx:
            return dlist[i][1]
    return ''

def getcatList(listpage, id):
    if id == '5':   # 音乐
        match = re.compile('<label>\s*按流派：\s*</label>(.*?)</ul>', re.DOTALL).findall(listpage)
    elif id == '13':   # 时尚
        match = re.compile('<label>\s*按行业：\s*</label>(.*?)</ul>', re.DOTALL).findall(listpage)
    else:
        match = re.compile('<label>\s*按类型：\s*</label>(.*?)</ul>', re.DOTALL).findall(listpage)
    if id in ('3','9'):   # 纪录片&旅游
        catlist = re.compile('href="http://list.iqiyi.com/www/' + id + '/(\d*)-[^>]+>(.*?)</a>').findall(match[0])
    elif id in ('5','10'):   # 音乐&片花
        catlist = re.compile('href="http://list.iqiyi.com/www/' + id + '/\d*-\d*-\d*-(\d*)-[^>]+>(.*?)</a>').findall(match[0])
    elif id == '13':  # 时尚
        catlist = re.compile('href="http://list.iqiyi.com/www/' + id + '/\d*-\d*-\d*-\d*-(\d*)-[^>]+>(.*?)</a>').findall(match[0])
    else:
        catlist = re.compile('href="http://list.iqiyi.com/www/' + id + '/\d*-(\d*)-[^>]+>(.*?)</a>').findall(match[0])
    return catlist

def getareaList(listpage, id):
    match = re.compile('<label>\s*按地区：\s*</label>(.*?)</ul>', re.DOTALL).findall(listpage)
    if id == '7':   # 娱乐
        arealist = re.compile('href="http://list.iqiyi.com/www/' + id + '/\d*-\d*-(\d*)-[^>]+>(.*?)</a>').findall(match[0])
    elif id in ('9','10'):   # 旅游&片花
        arealist = re.compile('href="http://list.iqiyi.com/www/' + id + '/\d*-(\d*)-[^>]+>(.*?)</a>').findall(match[0])
    else:
        arealist = re.compile('href="http://list.iqiyi.com/www/' + id + '/(\d*)-[^>]+>(.*?)</a>').findall(match[0])
    return arealist

def getyearList(listpage, id):
    match = re.compile('<label>按时间：</label>(.*?)</ul>', re.DOTALL).findall(listpage)
    yearlist = re.compile('href="http://list.iqiyi.com/www/' + id + '/\d*-\d*---------\d*-(\d*)-[^>]+>(.*?)</a>').findall(match[0])
    return yearlist

def rootList():
    for name, id in CHANNEL_LIST:
        li = xbmcgui.ListItem(name)
        u = sys.argv[0]+"?mode=1&name="+urllib.quote_plus(name)+"&id="+urllib.quote_plus(id)+"&cat="+urllib.quote_plus("")+"&area="+urllib.quote_plus("")+"&year="+urllib.quote_plus("")+"&order="+urllib.quote_plus("3")+"&page="+urllib.quote_plus("1")+"&paytype="+urllib.quote_plus("0")
        xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

#         id   c1   c2   c3   c4   c5     c11  c12   c13
# 电影     1 area  cat                paytype year order
# 电视剧   2 area  cat                paytype year order
# 纪录片   3  cat                     paytype      order
# 动漫     4 area  cat  ver  age      paytype      order
# 音乐     5 area lang       cat  grp paytype      order
# 综艺     6 area  cat                paytype      order
# 娱乐     7       cat area           paytype      order
# 旅游     9  cat area                paytype      order
# 片花    10      area       cat      paytype      order
# 时尚    13                      cat paytype      order
def progList(name,id,page,cat,area,year,order,paytype):
    c1 = ''
    c2 = ''
    c3 = ''
    c4 = ''
    if id == '7':          # 娱乐
        c3 = area
    elif id in ('9','10'): # 旅游&片花
        c2 = area
    elif id != '3':        # 非纪录片
        c1 = area
    if id in ('3','9'):    # 纪录片&旅游
        c1 = cat
    elif id in ('5','10'): # 音乐&片花
        c4 = cat
    elif id == '13':       # 时尚
        c5 = cat
    else:
        c2 = cat
    url = 'http://list.iqiyi.com/www/' + id + '/' + c1 + '-' + c2 + '-' + c3 + '-' + c4 + '-------' + paytype + '-' + year + '-' + order + '-1-' + page + '----.html'
    currpage = int(page)
    link = GetHttpData(url)
    match1 = re.compile('data-key="([0-9]+)"').findall(link)
    if len(match1) == 0:
        totalpages = 1
    else:
        totalpages = int(match1[len(match1) - 1])
    match = re.compile('<div class="panel"(.+?)<div class="list_content"', re.DOTALL).findall(link)
    if match:
        listpage = match[0]
    else:
        listpage = ''
    match = re.compile('<!--列表部分_START-->(.+?)<!--列表部分_END-->', re.DOTALL).findall(link)
    if match:
        match = re.compile('<li[^>]+>(.+?)</li>', re.DOTALL).findall(match[0])
    totalItems = len(match) + 1
    if currpage > 1: totalItems = totalItems + 1
    if currpage < totalpages: totalItems = totalItems + 1

    
    if cat == '':
        catstr = '全部类型'
    else:
        catlist = getcatList(listpage, id)
        catstr = searchDict(catlist, cat)
    selstr = '[COLOR FFFF0000]' + catstr + '[/COLOR]'
    if not (id in ('3','13')):
        if area == '':
            areastr = '全部地区'
        else:
            arealist = getareaList(listpage, id)
            areastr = searchDict(arealist, area)
        selstr += '/[COLOR FF00FF00]' + areastr + '[/COLOR]'
    if id in ('1', '2'):
        if year == '':
            yearstr = '全部年份'
        else:
            yearlist = getyearList(listpage, id)
            yearstr = searchDict(yearlist, year)
        selstr += '/[COLOR FFFFFF00]' + yearstr + '[/COLOR]'
    selstr += '/[COLOR FF00FFFF]' + searchDict(ORDER_LIST, order) + '[/COLOR]'
    selstr += '/[COLOR FFFF00FF]' + searchDict(PAYTYPE_LIST, paytype) + '[/COLOR]'
    li = xbmcgui.ListItem(name+'（第'+str(currpage)+'/'+str(totalpages)+'页）【'+selstr+'】（按此选择）')
    u = sys.argv[0]+"?mode=4&name="+urllib.quote_plus(name)+"&id="+urllib.quote_plus(id)+"&cat="+urllib.quote_plus(cat)+"&area="+urllib.quote_plus(area)+"&year="+urllib.quote_plus(year)+"&order="+order+"&paytype="+urllib.quote_plus(paytype)+"&page="+urllib.quote_plus(listpage)
    xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, True, totalItems)
    for i in range(0,len(match)):
        p_url  = re.compile('class="imgBg1" href="(.+?)"').findall(match[i])[0]
        p_name = re.compile('alt="(.+?)"').findall(match[i])[0]
        p_thumb = re.compile('src="(.+?)"').findall(match[i])[0]
        
        match1 = re.compile('<span class="imgBg1C">(共\d+集全)</span>').search(match[i])
        if not match1:
            match1 = re.compile('<span class="imgBg1C">(更新至第\d+集)</span>').search(match[i])
        if match1:
            mode = 2
            p_name1 = p_name + '（' + match1.group(1) + '）'
            isdir = True
        else:
            mode = 3
            p_name1 =  p_name
            isdir = False
        match1 = re.compile('<p class="dafen2">\s*<strong class="fRed"><span>(\d*)</span>([\.\d]*)</strong><span>分</span>\s*</p>').search(match[i])
        if match1:
            p_rating = float(match1.group(1)+match1.group(2))
        else:
            p_rating = 0
        match1 = re.compile('<span>导演：</span>(.+?)</p>', re.DOTALL).search(match[i])
        if match1:
            p_director = ' / '.join(re.compile('<a [^>]+>([^<]*)</a>').findall(match1.group(1)))
        else:
            p_director = ''
        match1 = re.compile('<span>主演：</span>(.+?)</p>', re.DOTALL).search(match[i])
        if match1:
            p_cast = re.compile('<a [^>]+>([^<]*)</a>').findall(match1.group(1))
        else:
            p_cast = ''
        match1 = re.compile('<span>类型：</span>(.+?)</p>', re.DOTALL).search(match[i])
        if match1:
            p_genre = ' / '.join(re.compile('<a [^>]+>([^<]*)</a>').findall(match1.group(1)))
        else:
            p_genre = ''
        match1 = re.compile('<p class="s1">\s*<span>([^<]*)</span>\s*</p>').search(match[i])
        if match1:
            p_plot = match1.group(1)
        else:
            p_plot = ''
        li = xbmcgui.ListItem(str(i + 1) + '.' + p_name1, iconImage = '', thumbnailImage = p_thumb)
        u = sys.argv[0]+"?mode="+str(mode)+"&name="+urllib.quote_plus(p_name)+"&url="+urllib.quote_plus(p_url)+"&thumb="+urllib.quote_plus(p_thumb)
        li.setInfo(type = "Video", infoLabels = {"Title":p_name, "Director":p_director, "Genre":p_genre, "Plot":p_plot, "Cast":p_cast, "Rating":p_rating})
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, isdir, totalItems)

    if currpage > 1:
        li = xbmcgui.ListItem('上一页')
        u = sys.argv[0]+"?mode=1&name="+urllib.quote_plus(name)+"&id="+urllib.quote_plus(id)+"&cat="+urllib.quote_plus(cat)+"&area="+urllib.quote_plus(area)+"&year="+urllib.quote_plus(year)+"&order="+order+"&page="+urllib.quote_plus(str(currpage-1))+"&paytype="+paytype
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, True, totalItems)
    if currpage < totalpages:
        li = xbmcgui.ListItem('下一页')
        u = sys.argv[0]+"?mode=1&name="+urllib.quote_plus(name)+"&id="+urllib.quote_plus(id)+"&cat="+urllib.quote_plus(cat)+"&area="+urllib.quote_plus(area)+"&year="+urllib.quote_plus(year)+"&order="+order+"&page="+urllib.quote_plus(str(currpage+1))+"&paytype="+paytype
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, True, totalItems)
    xbmcplugin.setContent(int(sys.argv[1]), 'movies')
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

def seriesList(name,url,thumb):
    link = GetHttpData(url)
    match1 = re.compile('<em>\(<a href="[^"]+">(\d+)</a>\)</em>').findall(link)
    if len(match1) == 0:
        p_year = 0
    else:
        p_year = int(match1[0])
    match1 = re.compile('导演：(.+?)</p>', re.DOTALL).search(link)
    if match1:
        p_director = ' / '.join(re.compile('<a [^>]+>([^<]*)</a>').findall(match1.group(1)))
    else:
        p_director = ''
    match1 = re.compile('主演：(.+?)</p>', re.DOTALL).search(link)
    if match1:
        p_cast = re.compile('<a [^>]+>([^<]*)</a>').findall(match1.group(1))
    else:
        p_cast = ''

    match1 = re.compile('<div id="j-album-[0-9]+[^>]*>(.*?)</div>').findall(link)
    album = ''
    for url1 in match1:
        album = album + GetHttpData('http://www.iqiyi.com' + url1)
    match2 = re.compile('<div id="j-desc-[0-9]+[^>]*>(.*?)</div>').findall(link)
    desc = ''
    for url1 in match2:
        desc = desc + GetHttpData('http://www.iqiyi.com' + url1)
    match = re.compile('<li><a href="([^"]+)" class="[^"]+">.+?data-lazy="([^"]+)" title="([^"]+)"', re.DOTALL).findall(album)
    if not match:
        match = re.compile('<li><a href="([^"]+)" class="[^"]+">.+?src="([^"]+)" title="([^"]+)"', re.DOTALL).findall(album)
    totalItems = len(match)
    for i in range(0,len(match)):
        p_url = match[i][0]
        p_thumb = match[i][1]
        p_name = match[i][2]
        match1 = re.compile('<a href="' + p_url + '">' + p_name + '</a></dt>\s*<dd>(.*?)</dd>').findall(desc)
        if len(match1) > 0:
            p_plot = match1[0].replace('&nbsp;','')
        else:
            p_plot = ''
        li = xbmcgui.ListItem(p_name, iconImage = '', thumbnailImage = p_thumb)
        li.setInfo(type = "Video", infoLabels = {"Title":p_name, "Director":p_director, "Cast":p_cast, "Plot":p_plot, "Year":p_year})
        u = sys.argv[0] + "?mode=3&name=" + urllib.quote_plus(p_name) + "&url=" + urllib.quote_plus(p_url)+ "&thumb=" + urllib.quote_plus(p_thumb)
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, False, totalItems)
    xbmcplugin.setContent(int(sys.argv[1]), 'episodes')
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

def PlayVideo(name,url,thumb):
    link = GetHttpData(url)
    match1 = re.compile('<script\s*type="text/javascript">\s*var info\s*=(.*?)</script>', re.DOTALL).findall(link)
    if match1:
        try:
            data = unicode(match1[0], 'utf-8', errors='ignore')
            json_response = simplejson.loads(data)
            pid = json_response['pid'].encode('utf-8')
            ptype = json_response['ptype'].encode('utf-8')
            videoId = json_response['videoId'].encode('utf-8')
        except:
            dialog = xbmcgui.Dialog()
            ok = dialog.ok(__addonname__, '未能解析视频地址')
            return
    else:
        dialog = xbmcgui.Dialog()
        ok = dialog.ok(__addonname__, '未能解析视频地址')
        return
    url = 'http://cache.video.qiyi.com/v/' + videoId + '/' + pid + '/' + ptype + '/'
    link = GetHttpData(url)
    match1 = re.compile('<data version="(\d+)">([^<]+)</data>').findall(link)
    ratelist = []
    for i in range(0,len(match1)):
        if match1[i][0] == '96': ratelist.append([4, '极速', i])    # 清晰度设置值, 清晰度, match索引
        if match1[i][0] == '1': ratelist.append([3, '流畅', i])
        if match1[i][0] == '2': ratelist.append([2, '高清', i])
        if match1[i][0] == '3': ratelist.append([1, '超清', i])
    ratelist.sort()
    if len(ratelist)>1:
        resolution = int(__addon__.getSetting('resolution'))
        if resolution == 0:    # 每次询问点播视频清晰度
            dialog = xbmcgui.Dialog()
            list = [x[1] for x in ratelist]
            sel = dialog.select('清晰度（低网速请选择低清晰度）', list)
            if sel == -1:
                return
        else:
            sel = 0
            while sel < len(ratelist)-1 and resolution > ratelist[sel][0]: sel =  sel + 1
    else:
        sel = 0
    if match1[ratelist[sel][2]][1] != videoId:
        url = 'http://cache.video.qiyi.com/v/' + match1[ratelist[sel][2]][1] + '/' + pid + '/' + ptype + '/'
        link = GetHttpData(url)

    match=re.compile('<file>(.+?)</file>').findall(link)
    playlist=xbmc.PlayList(1)
    playlist.clear()
    listitem = xbmcgui.ListItem(name, thumbnailImage = thumb)
    listitem.setInfo(type="Video",infoLabels={"Title":name+" 第"+str(1)+"/"+str(len(match))+" 节"})
    filepart = '/'.join(match[0].split('/')[-3:])
    if urlExists('http://qiyi.soooner.com/videos2/'+filepart):
        baseurl = 'http://qiyi.soooner.com/videos2/'
    elif urlExists('http://qiyi.soooner.com/videos/'+filepart):
        baseurl = 'http://qiyi.soooner.com/videos/'
    else:
        dialog = xbmcgui.Dialog()
        ok = dialog.ok(__addonname__, '未能获取视频地址')
        return
    playlist.add(baseurl+filepart, listitem = listitem)
    for i in range(1,len(match)):
        listitem=xbmcgui.ListItem(name, thumbnailImage = thumb)
        listitem.setInfo(type="Video",infoLabels={"Title":name+" 第"+str(i+1)+"/"+str(len(match))+" 节"})
        filepart = '/'.join(match[i].split('/')[-3:])
        playlist.add(baseurl+filepart, listitem = listitem)
    xbmc.Player().play(playlist)

def performChanges(name,id,listpage,cat,area,year,order,paytype):
    change = False
    catlist= getcatList(listpage, id)
    dialog = xbmcgui.Dialog()
    if len(catlist)>0:
        list = [x[1] for x in catlist]
        sel = dialog.select('类型', list)
        if sel != -1:
            cat = catlist[sel][0]
            change = True
    if not (id in ('3','13')):
        arealist = getareaList(listpage, id)
        if len(arealist)>0:
            list = [x[1] for x in arealist]
            sel = dialog.select('地区', list)
            if sel != -1:
                area = arealist[sel][0]
                change = True       
    if id in ('1','2'):
        yearlist = getyearList(listpage, id)
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
        progList(name,id,'1',cat,area,year,order,paytype)

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
order = '3'
paytype = '0'
num = '1'
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
    num = urllib.unquote_plus(params["num"])
except:
    pass
try:
    res = urllib.unquote_plus(params["paytype"])
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
    progList(name,id,page,cat,area,year,order,paytype)
elif mode == 2:
    seriesList(name,url,thumb)
elif mode == 3:
    PlayVideo(name,url,thumb)
elif mode == 4:
    performChanges(name,id,page,cat,area,year,order,paytype)
