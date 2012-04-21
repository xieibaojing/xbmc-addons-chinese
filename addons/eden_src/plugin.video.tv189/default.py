# -*- coding: utf-8 -*-
import xbmc, xbmcgui, xbmcplugin, xbmcaddon, urllib2, urllib, re, string, sys, os, gzip, StringIO
       
############################################################
# 天翼视讯(TV189) by taxigps, 2012
############################################################

# Plugin constants 
__addonname__ = "天翼视讯(TV189)"
__addonid__   = "plugin.video.tv189"
__addon__     = xbmcaddon.Addon(id=__addonid__)
__cwd__       = xbmc.translatePath(__addon__.getAddonInfo('path'))
__icon__      = os.path.join( __cwd__, 'icon.png' )

CHANNEL_LIST = [['电影','movie'], ['电视剧','tv'], ['综艺','zy'], ['娱乐','ent'], ['纪实','real'], ['原创','show']]
ORDER_LIST = [['0','最新'], ['1','热播'], ['2','热评'], ['3','得分'],['4','收录']]
RES_LIST = [['0','全部'], ['1080P','超清'], ['720P','高清'], ['450P','标清']]

def GetHttpData(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    httpdata = response.read()
    if response.headers.get('content-encoding', None) == 'gzip':
        httpdata = gzip.GzipFile(fileobj=StringIO.StringIO(httpdata)).read()
    charset = response.headers.getparam('charset')
    response.close()
    match = re.compile('<meta http-equiv=["]?[Cc]ontent-[Tt]ype["]? content="text/html;[\s]?charset=(.+?)"').findall(httpdata)
    if len(match)>0:
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

def getcatList(listpage, listtype):
    match = re.compile('<h4>'+listtype+'</h4>(.+?)</ul>', re.DOTALL).findall(listpage)
    catlist = re.compile('tkey="[^"]+" tvalue="([^"]+)"><a href=[^>]+><span>(.+?)</span>', re.DOTALL).findall(match[0])
    if not catlist:
        catlist = re.compile('tvalue="([^"]+)" tkey="[^"]+"><a href=[^>]+><span>(.+?)</span>', re.DOTALL).findall(match[0])
    return catlist

def rootList():
    name = '电视直播'
    li = xbmcgui.ListItem(name)
    u = sys.argv[0]+"?mode=10&name="+urllib.quote_plus(name)
    xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
    for name, id in CHANNEL_LIST:
        li = xbmcgui.ListItem(name)
        u = sys.argv[0]+"?mode=1&name="+urllib.quote_plus(name)+"&id="+urllib.quote_plus(id)+"&cat="+urllib.quote_plus("0")+"&area="+urllib.quote_plus("0")+"&year="+urllib.quote_plus("0")+"&order="+urllib.quote_plus("0")+"&page="+urllib.quote_plus("1")+"&res="+urllib.quote_plus("0")+"&group="+urllib.quote_plus("0")
        xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

def progList(name,id,page,cat,area,year,order,res,group):
    if group == '0':
        url = 'http://'+id+'.tv189.com/l/'+cat+'_'+year+'_0_0_'+area+'_'+res+'_'+order+'_0/'+page+'.htm'
    else:
        if id == 'zy': url = 'http://zy.tv189.com/g/'+group+'_0_0/'+page+'.htm'
        elif id == 'real': url = 'http://'+id+'.tv189.com/l/'+cat+'_'+group+'_0_0_0_'+res+'_'+order+'_0/'+page+'.htm'
    currpage = int(page)
    link = GetHttpData(url)
    match = re.compile('<a href="/l/[^/]+/([0-9]+).htm">尾页</a>', re.DOTALL).findall(link)
    if len(match):
        totalpages = int(match[0])
    else:
        totalpages = 1
    match = re.compile('检索</h2>(.+?)<div class="foot">', re.DOTALL).findall(link)
    if match:
        listpage = match[0]
    else:
        listpage = ''
    match = re.compile('<dl><dt><span class="img">(.+?)</dl>', re.DOTALL).findall(link)
    totalItems = len(match) + 1
    if currpage > 1: totalItems = totalItems + 1
    if currpage < totalpages: totalItems = totalItems + 1

    if cat == '0':
        catstr = '全部类型'
    else:
        catlist = getcatList(link, '按类型')
        catstr = searchDict(catlist,cat)
    selstr = '[COLOR FFFF0000]' + catstr + '[/COLOR]'
    if id in ('movie', 'tv', 'zy'):
        if area == '0':
            areastr = '全部地区'
        else:
            areastr = area
        selstr += '/[COLOR FF00FF00]' + areastr + '[/COLOR]'
    if id in ('zy', 'real'):
        if group == '0':
            groupstr = '全部节目'
        else:
            groupstr = group
        selstr += '/[COLOR FFFFFF00]' + groupstr + '[/COLOR]'
    if id in ('movie', 'tv'):
        if year == '0':
            yearstr = '全部年份'
        else:
            yearstr = year
        selstr += '/[COLOR FFFFFF00]' + yearstr + '[/COLOR]'
    if id in ('movie', 'tv', 'real'):
        if res == '0':
            resstr = '全部清晰度'
        else:
            resstr = searchDict(RES_LIST,res)
        selstr += '/[COLOR FFFF00FF]' + resstr + '[/COLOR]'
    selstr += '/[COLOR FF00FFFF]' + searchDict(ORDER_LIST,order) + '[/COLOR]'
    li = xbmcgui.ListItem(name+'（第'+str(currpage)+'/'+str(totalpages)+'页）【'+selstr+'】（按此选择）')
    u = sys.argv[0]+"?mode=4&name="+urllib.quote_plus(name)+"&id="+urllib.quote_plus(id)+"&cat="+urllib.quote_plus(cat)+"&area="+urllib.quote_plus(area)+"&year="+urllib.quote_plus(year)+"&order="+order+"&res="+urllib.quote_plus(res)+"&page="+urllib.quote_plus(listpage)
    xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, True, totalItems)
    for i in range(0,len(match)):
        match1 = re.compile('tpic="(.+?)"').search(match[i])
        p_thumb = match1.group(1)
        match1 = re.compile('<a href="/v/([0-9]+).htm"  target="video">([^<]+)</a>').search(match[i])
        p_id = match1.group(1)
        p_name = match1.group(2)
        match1 = re.compile('<a href="javascript:cellection\([^\)]+\)">([^<]+)</a>').search(match[i])
        p_info = match1.group(1).replace("&nbsp;", "")
        if p_info:
            p_name1 = p_name + '（' + p_info + '）'
        else:
            p_name1 = p_name
        if id in ('tv'):
            mode = 2
            match1 = re.compile('[^\d]*(\d+)').search(p_info)
            p_num = match1.group(1)
            isdir = True
        else:
            mode = 3
            p_num = '1'
            isdir = False
        match1 = re.compile('<s>([^<]+)</s>').search(match[i])
        if match1:
            p_rating = float(match1.group(1))
        else:
            p_rating = 0
        match1 = re.compile('<p>导演：(.+?)</p>').search(match[i])
        if match1:
            p_director = ' / '.join(re.compile('<a href="[^"]+">([^<]*)</a>').findall(match1.group(1)))
        else:
            p_director = ''
        match1 = re.compile('<p>主演：(.+?)</p>').search(match[i])
        if match1:
            p_cast = re.compile('<a href="[^"]+">([^<]*)</a>').findall(match1.group(1))
        else:
            p_cast = ''
        match1 = re.compile('<p>标签：(.+?)</p>').search(match[i])
        if match1:
            p_genre = ' / '.join(re.compile('<a href="[^"]+">([^<]*)</a>').findall(match1.group(1)))
        else:
            p_genre = ''
        match1 = re.compile('<p>年份：(.+?)</p>').search(match[i])
        if match1:
            p_year = int(re.compile('<a href="[^"]+">([^<]*)</a>').findall(match1.group(1))[0])
        else:
            p_year = 0
        match1 = re.compile('>详细>></a></p><p id=[^>]*>(.+?)<a href=').search(match[i])
        if match1:
            p_plot = match1.group(1).replace("&nbsp;", " ").replace("</br>", "\n")
        else:
            p_plot = ''
        li = xbmcgui.ListItem(str(i + 1) + '.' + p_name1, iconImage = '', thumbnailImage = p_thumb)
        u = sys.argv[0]+"?mode="+str(mode)+"&name="+urllib.quote_plus(p_name)+"&id="+urllib.quote_plus(p_id)+"&thumb="+urllib.quote_plus(p_thumb)+"&num="+urllib.quote_plus(p_num)
        li.setInfo(type = "Video", infoLabels = {"Title":p_name, "Director":p_director, "Genre":p_genre, "Plot":p_plot, "Year":p_year, "Cast":p_cast, "Rating":p_rating})
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, isdir, totalItems)

    if currpage > 1:
        li = xbmcgui.ListItem('上一页')
        u = sys.argv[0]+"?mode=1&name="+urllib.quote_plus(name)+"&id="+urllib.quote_plus(id)+"&cat="+urllib.quote_plus(cat)+"&area="+urllib.quote_plus(area)+"&year="+urllib.quote_plus(year)+"&order="+order+"&page="+urllib.quote_plus(str(currpage-1))+"&res="+res+"&group="+group
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, True, totalItems)
    if currpage < totalpages:
        li = xbmcgui.ListItem('下一页')
        u = sys.argv[0]+"?mode=1&name="+urllib.quote_plus(name)+"&id="+urllib.quote_plus(id)+"&cat="+urllib.quote_plus(cat)+"&area="+urllib.quote_plus(area)+"&year="+urllib.quote_plus(year)+"&order="+order+"&page="+urllib.quote_plus(str(currpage+1))+"&res="+res+"&group="+group
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, True, totalItems)
    xbmcplugin.setContent(int(sys.argv[1]), 'movies')
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

def seriesList(name,id,thumb,num):
    totalItems = int(num)
    for i in range(1,totalItems+1):
        p_name = name+' 第'+str(i)+'集'
        li = xbmcgui.ListItem(p_name, iconImage = '', thumbnailImage = thumb)
        u = sys.argv[0]+"?mode=3&name="+urllib.quote_plus(p_name)+"&id="+urllib.quote_plus(id)+"&thumb="+urllib.quote_plus(thumb)+"&num="+urllib.quote_plus(str(i))
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, False, totalItems)
    xbmcplugin.setContent(int(sys.argv[1]), 'episodes')
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

def PlayVideo(name,id,thumb,num):
    url = 'http://pgmsvr.tv189.cn/program/getVideoPlayInfo?pid='+id+'&indexid='+num
    resolution = int(__addon__.getSetting('resolution'))
    link = GetHttpData(url)
    match = re.compile('<url cr="([^"]+)" tm="[^"]+" vid="[^"]+"  sz="[^"]+"><!\[CDATA\[(.+?)\]\]></url>', re.DOTALL).findall(link)
    if not match:
       dialog = xbmcgui.Dialog()
       ok = dialog.ok(__addonname__,'您当前选择的节目暂不能播放，请选择其它节目')   
       return
    print match
    ratelist = []
    for i in range(0,len(match)):
        if match[i][0] == '450P': ratelist.append([3, '标清', i])    # 清晰度设置值, 清晰度, match索引
        if match[i][0] == '720P': ratelist.append([2, '高清', i])
        if match[i][0] == '1080P': ratelist.append([1, '超清', i])
    ratelist.sort()
    if len(ratelist)>1:
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
    playlist = xbmc.PlayList(1)
    playlist.clear()
    listitem=xbmcgui.ListItem(name,thumbnailImage=thumb)
    playlist.add(match[ratelist[sel][2]][1], listitem)
    xbmc.Player().play(playlist)

def performChanges(name,id,listpage,cat,area,year,order,res,group):
    change = False
    catlist= getcatList(listpage, '按类型')
    dialog = xbmcgui.Dialog()
    if len(catlist)>0:
        list = [x[1] for x in catlist]
        sel = dialog.select('类型', list)
        if sel != -1:
            cat = catlist[sel][0]
            change = True
    if id in ('movie','tv','zy'):
        arealist = getcatList(listpage, '按地区')
        if len(arealist)>0:
            list = [x[1] for x in arealist]
            sel = dialog.select('地区', list)
            if sel != -1:
                area = arealist[sel][0]
                change = True       
    if id in ('zy','real'):
        grouplist = getcatList(listpage, '按节目')
        print grouplist
        if len(grouplist)>0:
            list = [x[1] for x in grouplist]
            sel = dialog.select('节目', list)
            if sel != -1:
                group = grouplist[sel][0]
                change = True
    if id in ('movie','tv'):
        yearlist = getcatList(listpage, '按年代')
        if len(yearlist)>0:
            list = [x[1] for x in yearlist]
            sel = dialog.select('年份', list)
            if sel != -1:
                year = yearlist[sel][0]
                change = True
    if id in ('movie','tv','real'):
        list = [x[1] for x in RES_LIST]
        sel = dialog.select('清晰度', list)
        if sel != -1:
            res = RES_LIST[sel][0]
            change = True
    list = [x[1] for x in ORDER_LIST]
    sel = dialog.select('排序方式', list)
    if sel != -1:
        order = ORDER_LIST[sel][0]
        change = True
    if change:
        progList(name,id,'1',cat,area,year,order,res,group)

def LiveChannel(name):
    url = 'http://live.tv189.com/index.php?r=index/indexL'
    link = GetHttpData(url)
    match = re.compile("<a href=\"javascript:void\(0\);\" onclick=\"Live.playChannel\(\d+,'','','','([^']*)','([^']*)'\);\">([^<]+)</a>").findall(link)
    totalItems = len(match)
    if match:
        for item in match:
            url = ';'.join([item[0].replace('\t', ''), item[1].replace('\t', '')])
            li = xbmcgui.ListItem(item[2], iconImage = '', thumbnailImage = __icon__)
            u = sys.argv[0] + "?mode=11&name=" + urllib.quote_plus(item[2]) + "&url=" + urllib.quote_plus(url)
            xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, False, totalItems)
    xbmcplugin.setContent(int(sys.argv[1]), 'movies')
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

def LivePlay(name,url):
    urls = url.split(';')
    bitsrate = int(__addon__.getSetting('bitsrate'))
    ratelist = []
    if urls[0]: ratelist.append(['高清',0])
    if urls[1]: ratelist.append(['流畅',1])
    if len(ratelist)>1:
        if bitsrate == 0:    # 每次询问直播视频码率
            dialog = xbmcgui.Dialog()
            list = [x[0] for x in ratelist]
            sel = dialog.select('网速（低网速请选择流畅）', list)
            if sel == -1:
                return
        else:
            sel = bitsrate - 1
    else:
        sel = 0
    link = GetHttpData(urls[ratelist[sel][1]])
    match = re.compile('<Ref href="(rtmp://[^"]+)" />').findall(link)
    if match:
        li = xbmcgui.ListItem(name,iconImage='',thumbnailImage=__icon__)
        xbmc.Player().play(match[0], li)

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
cat = '0'
area = '0'
year = '0'
order = '0'
res = '0'
group = '0'
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
    group = urllib.unquote_plus(params["group"])
except:
    pass
try:
    res = urllib.unquote_plus(params["res"])
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
    progList(name,id,page,cat,area,year,order,res,group)
elif mode == 2:
    seriesList(name,id,thumb,num)
elif mode == 3:
    PlayVideo(name,id,thumb,num)
elif mode == 4:
    performChanges(name,id,page,cat,area,year,order,res,group)
elif mode == 10:
    LiveChannel(name)
elif mode == 11:
    LivePlay(name,url)
