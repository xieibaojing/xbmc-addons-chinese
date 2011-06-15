# -*- coding: utf-8 -*-
import xbmc, xbmcgui, xbmcplugin, xbmcaddon, urllib2, urllib, re, string, sys, os, gzip, StringIO

# 热点影院(www.wzipad.com) by wow1122(wht9000@gmail.com), 2011

# Plugin constants 
__addonname__ = "热点影院(www.wzipad.com)"
__addonid__ = "plugin.video.wzipad"
__addon__ = xbmcaddon.Addon(id=__addonid__)
__addonicon__ = os.path.join( __addon__.getAddonInfo('path'), 'icon.png' )

UserAgent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'

ORDER_LIST = [['按最近更新','new'], ['按热门点播','hot'], ['按最新上映','release'],['今日','today'],['本周','week'],['本月','month'],]
ORDER_DICT = dict(ORDER_LIST)

MOVIE_TYPE_LIST = {}
MOVIE_TYPE_LIST['1'] = [['全部','0'],['动画片','1404'],['科教片','1401'],['动作片','1'],['爱情片','19'],['科幻片','4'],['恐怖片','5'],['喜剧片','7'],['灾难片','1401'],['伦理片','1379'],['战争片','1387'],['悬疑片','1403'],['纪录片','1405'],]
MOVIE_TYPE_LIST['2'] = [['全部','0'],['大陆古装','1382'],['连载区','1450'],['欧美经典','1400'],['日　韩','1385'],['卡通剧','1383'],['港台现代','1378'],['大陆现代','1386'],['港台古装','1381'],]
MOVIE_TYPE_LIST['3'] = [['全部','0'],['娱乐','1384'],['MTV','1402'],['体育','1441'],]

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
            httpdata=httpdata.decode('gbk', 'ignore').encode('utf8')
            #httpdata = unicode(httpdata, charset).encode('utf8')
    return httpdata
  
def rootList():
    li=xbmcgui.ListItem('电影')
    u=sys.argv[0]+"?mode=1&name="+urllib.quote_plus('电影')+"&baseurl="+urllib.quote_plus('http://www.wzipad.com/category.aspx')+"&type="+urllib.quote_plus('1')+"&order="+urllib.quote_plus('new')+"&page="+urllib.quote_plus('1')
    xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
    li=xbmcgui.ListItem('电视剧')
    u=sys.argv[0]+"?mode=1&name="+urllib.quote_plus('电视剧')+"&baseurl="+urllib.quote_plus('http://www.wzipad.com/category.aspx')+"&type="+urllib.quote_plus('3')+"&order="+urllib.quote_plus('new')+"&page="+urllib.quote_plus('1')
    xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
    li=xbmcgui.ListItem('综艺')
    u=sys.argv[0]+"?mode=1&name="+urllib.quote_plus('综艺')+"&baseurl="+urllib.quote_plus('http://www.wzipad.com/category.aspx')+"&type="+urllib.quote_plus('1020')+"&order="+urllib.quote_plus('new')+"&page="+urllib.quote_plus('1')
    xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
    xbmcplugin.endOfDirectory(int(sys.argv[1]))
    
def searchDict(dlist,idx):
    for i in range(0,len(dlist)):
        if dlist[i][1] == idx:
            return dlist[i][0]
    return ''

def progList(name,baseurl,type,order,page):
    #http://www.wzipad.com/category.aspx?typeid=1
    #baseurl='http://www.wzipad.com/category.aspx?typeid='+type
    if page:
        currpage = int(page)
    else:
        currpage = 1
    url = baseurl +'?typeid='+type+ '&order='+ order + '&page=' +str(currpage)
    link = GetHttpData(url)
    match1 = re.compile('<div class="list_right">(.+?)</ul>', re.DOTALL).findall(link)
    match = re.compile('<li>.+?<a href="(.+?)" target="movieurl">.+?<img src="(.+?)" alt="(.+?)".+?</li>', re.DOTALL).findall(match1[0])
    totalItems = len(match)
    
    if type in ('1','3','1020'): catstr='全部'
    elif name=='电影': catstr=searchDict(MOVIE_TYPE_LIST['1'],type)
    elif name=='电视剧': catstr=searchDict(MOVIE_TYPE_LIST['2'],type)
    elif name=='综艺': catstr=searchDict(MOVIE_TYPE_LIST['3'],type)
   
    orderstr=searchDict(ORDER_LIST,order)
    
    li = xbmcgui.ListItem('类型[COLOR FFFF0000]【' + name+'-'+catstr + '】[/COLOR] 排序[COLOR FFFF0000]【' + orderstr + '】[/COLOR]（按此选择）')
    u = sys.argv[0] + "?mode=5&name="+urllib.quote_plus(name)
    xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, True, totalItems)
    
    for p_id,p_thumb,p_name in match:
        li = xbmcgui.ListItem(p_name, iconImage = '', thumbnailImage = p_thumb)
        isDir=True
        u = sys.argv[0]+"?mode=2&name="+urllib.quote_plus(p_name)+"&url="+'http://www.wzipad.com/'+urllib.quote_plus(p_id)+"&thumb="+urllib.quote_plus(p_thumb)
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, isDir, totalItems)
    if currpage > 1:
        li = xbmcgui.ListItem('上一页')
        u = sys.argv[0]+"?mode=1&name="+urllib.quote_plus(name)+"&baseurl="+urllib.quote_plus(baseurl)+"&type="+urllib.quote_plus(type)+"&order="+order+"&page="+urllib.quote_plus(str(currpage-1))
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, True, totalItems)
    if len(match) > 11:
        li = xbmcgui.ListItem('下一页')
        u = sys.argv[0]+"?mode=1&name="+urllib.quote_plus(name)+"&baseurl="+urllib.quote_plus(baseurl)+"&type="+urllib.quote_plus(type)+"&order="+order+"&page="+urllib.quote_plus(str(currpage+1))
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, True, totalItems)
    xbmcplugin.setContent(int(sys.argv[1]), 'movies')
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

def listA(name,url,thumb):
    link = GetHttpData(url)
    match1 = re.compile('<div class="data_bofang2">(.+?)</div>', re.DOTALL).findall(link)   
    match = re.compile('clipID=(.+?)&SortID=(.+?)">\r\n(.+?)</a></td>', re.DOTALL).findall(match1[0])   
    totalItems=len(match)
    for p_cid,p_sid,p_name in match:
        li = xbmcgui.ListItem(name+'-'+p_name.lstrip(), iconImage = '', thumbnailImage = thumb)
        u = sys.argv[0] + "?mode=10&name="+urllib.quote_plus(name+'-'+p_name.lstrip())+"&cid="+urllib.quote_plus(p_cid)+"&sid="+urllib.quote_plus(p_sid)+"&thumb="+urllib.quote_plus(thumb)
        #li.setInfo(type = "Video", infoLabels = {"Title":p_name.lstrip(), "Director":p_director, "Genre":p_genre, "Plot":p_plot, "Year":p_year, "Cast":p_cast, "Tagline":p_tagline})
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, False, totalItems)
    xbmcplugin.setContent(int(sys.argv[1]), 'movies')
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

       
def PlayVideo(name,cid,sid,thumb):
    req = urllib2.Request('http://www.wzipad.com/getUrl.aspx','cid='+cid+'&sid='+sid)
    response = urllib2.urlopen(req)
    url=response.read()
    url=url.replace('streams=','')
    url=url.replace('&file=','')
    playlist=xbmc.PlayList(1)
    playlist.clear()
    listitem = xbmcgui.ListItem(name, thumbnailImage = __addonicon__)
    listitem.setInfo(type="Video",infoLabels={"Title":name})
    playlist.add(url, listitem)
    xbmc.Player().play(playlist)

def performChanges(name):
    change = False
    dialog = xbmcgui.Dialog()
    if name=='电影':
           list = [x[0] for x in MOVIE_TYPE_LIST['1']]
    elif name=='电视剧':
           list = [x[0] for x in MOVIE_TYPE_LIST['2']]   
    elif name=='综艺':
           list = [x[0] for x in MOVIE_TYPE_LIST['3']] 
    sel = dialog.select('类型', list)
    if sel != -1:
        if name=='电影':
            type=MOVIE_TYPE_LIST['1'][sel][1]
            if MOVIE_TYPE_LIST['1'][sel][1]=='0':baseurl='http://www.wzipad.com/category.aspx'
            else:baseurl='http://www.wzipad.com/list.aspx'
        elif name=='电视剧':
            type=MOVIE_TYPE_LIST['2'][sel][1]
            if MOVIE_TYPE_LIST['2'][sel][1]=='0':baseurl='http://www.wzipad.com/category.aspx'
            else:baseurl='http://www.wzipad.com/list.aspx'
        elif name=='综艺':
            type=MOVIE_TYPE_LIST['3'][sel][1]
            if MOVIE_TYPE_LIST['3'][sel][1]=='0':baseurl='http://www.wzipad.com/category.aspx'
            else:baseurl='http://www.wzipad.com/list.aspx'
        change = True
 
    list = [x[0] for x in ORDER_LIST]
    sel = dialog.select('排序方式', list)
    if sel != -1:
        order = ORDER_LIST[sel][1]
        change = True    
    if change:
        progList(name,baseurl,type,order,'1')
        
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
order = None
page = '1'
url = ''
baseurl = ''
cid = ''
sid = ''
thumb = None
res = 0

try:
    type = urllib.unquote_plus(params["type"])
except:
    pass
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
    baseurl = urllib.unquote_plus(params["baseurl"])
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
    cid = urllib.unquote_plus(params["cid"])
except:
    pass  
try:
    sid = urllib.unquote_plus(params["sid"])
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
    progList(name,baseurl,type,order,page)
elif mode == 2:
    listA(name,url,thumb)
elif mode == 5:
    performChanges(name)
elif mode == 10:
    PlayVideo(name,cid,sid,thumb)

