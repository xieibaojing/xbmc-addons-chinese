# -*- coding: utf-8 -*-
import xbmc, xbmcgui, xbmcplugin, xbmcaddon, urllib2, urllib, re, string, sys, os, gzip, StringIO

# 新浪视频(video.sina.com.cn) by wow1122(wht9000@gmail.com), 2011

# Plugin constants 
__addonname__ = "新浪视频(video.sina.com.cn)"
__addonid__ = "plugin.video.sina"
__addon__ = xbmcaddon.Addon(id=__addonid__)
__addonicon__ = os.path.join( __addon__.getAddonInfo('path'), 'icon.png' )

UserAgent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'

ORDER_LIST = [['最新发布','1'], ['最多播放','2'], ['最高评分','3'], ['最热评论','4'], ['字母排序','5']]
ORDER_DICT = dict(ORDER_LIST)
MOVIE_MAIN_LIST = [['movie','电影'],['teleplay','电视剧'],['cartoon','动画片'],['original','原创'],['arts','综艺'],['documentary','纪录片'],['zt','专题'],]
MOVIE_AREA_LIST = [['全部','index'],['大陆','1'],['香港','2'],['台湾','3'],['美国','4'],['欧洲','6'],['日本','7'],['韩国','5'],['其他','8'],]
MOVIE_YEAR_LIST = [['全部','index'],['2011年','2011'],['2010年','2010'],['2009年','2009'],['2008年','2008'],['更早','earlier'],]
MOVIE_TYPE_LIST = {}
MOVIE_TYPE_LIST['1'] = [['全部','index'],['剧情','1'],['喜剧','2'],['爱情','3'],['动作','4'],['惊悚','5'],['犯罪','6'],['恐怖','7'],['冒险','8'],['家庭','9'],['伦理','10'],['动画','11'],['悬疑','12'],['短片','13'],['战争','14'],['歌舞','15'],['传记','16'],['历史','17'],['古装','18'],['运动','19'],['武侠','20'],['儿童','21'],['青春','22'],['纪实','23'],['科幻魔幻','24'],['黑色幽默','25'],]
MOVIE_TYPE_LIST['2'] = [['全部','index'],['剧情','1'],['喜剧','2'],['爱情','3'],['动作','4'],['惊悚','5'],['犯罪','6'],['恐怖','7'],['冒险','8'],['家庭','9'],['伦理','10'],['动画','11'],['悬疑','12'],['短片','13'],['战争','14'],['歌舞','15'],['传记','16'],['历史','17'],['古装','18'],['运动','19'],['武侠','20'],['儿童','21'],['青春','22'],['纪实','23'],['科幻魔幻','24'],['黑色幽默','25'],]
MOVIE_TYPE_LIST['3'] = [['全部','index'],['搞笑','1'],['剧情','2'],['冒险','3'],['魔幻','4'],['励志','5'],['体育','6'],['益智','7'],['神话','8'],['童话','9'],['真人','10'],]
MOVIE_TYPE_LIST['4'] = [['全部','index'],['剧情','1'],['喜剧','2'],['爱情','3'],['动画','4'],['惊悚','5'],['家庭','6'],['科幻奇幻','7'],['黑色幽默','8'],]
MOVIE_TYPE_LIST['5'] = [['全部','index'],['真人秀','1'],['访谈','2'],['搞笑','3'],['游戏','4'],['选秀','5'],['时尚','6'],['杂谈','7'],['情感','8'],['盛会','9'],]
MOVIE_TYPE_LIST['6'] = [['全部','index'],['人文纪实','1'],['探索发现','2'],]

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
  
def rootList():
    li=xbmcgui.ListItem('电影')
    u=sys.argv[0]+"?mode=1&name="+urllib.quote_plus('电影')+"&type="+urllib.quote_plus('movie')+"&leftid="+urllib.quote_plus('movie-index')+"&order="+urllib.quote_plus('1')+"&page="+urllib.quote_plus('1')
    xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
    li=xbmcgui.ListItem('电视剧')
    u=sys.argv[0]+"?mode=1&name="+urllib.quote_plus('电视剧')+"&type="+urllib.quote_plus('teleplay')+"&leftid="+urllib.quote_plus('teleplay-index')+"&order="+urllib.quote_plus('1')+"&page="+urllib.quote_plus('1')
    xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
    li=xbmcgui.ListItem('动画片')
    u=sys.argv[0]+"?mode=1&name="+urllib.quote_plus('动画片')+"&type="+urllib.quote_plus('cartoon')+"&leftid="+urllib.quote_plus('cartoon-index')+"&order="+urllib.quote_plus('1')+"&page="+urllib.quote_plus('1')
    xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
    li=xbmcgui.ListItem('原创')
    u=sys.argv[0]+"?mode=1&name="+urllib.quote_plus('原创')+"&type="+urllib.quote_plus('original')+"&leftid="+urllib.quote_plus('original-index')+"&order="+urllib.quote_plus('1')+"&page="+urllib.quote_plus('1')
    xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
    li=xbmcgui.ListItem('综艺')
    u=sys.argv[0]+"?mode=1&name="+urllib.quote_plus('综艺')+"&type="+urllib.quote_plus('arts')+"&leftid="+urllib.quote_plus('arts-index')+"&order="+urllib.quote_plus('1')+"&page="+urllib.quote_plus('1')
    xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
    li=xbmcgui.ListItem('纪录片')
    u=sys.argv[0]+"?mode=1&name="+urllib.quote_plus('纪录片')+"&type="+urllib.quote_plus('documentary')+"&leftid="+urllib.quote_plus('documentary-index')+"&order="+urllib.quote_plus('1')+"&page="+urllib.quote_plus('1')
    xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
    li=xbmcgui.ListItem('专题')
    u=sys.argv[0]+"?mode=1&name="+urllib.quote_plus('专题')+"&type="+urllib.quote_plus('zt')+"&leftid="+urllib.quote_plus('zt-index')+"&order="+urllib.quote_plus('1')+"&page="+urllib.quote_plus('1')
    xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
    xbmcplugin.endOfDirectory(int(sys.argv[1]))
    
def searchDict(dlist,idx):
    for i in range(0,len(dlist)):
        if dlist[i][1] == idx:
            return dlist[i][0]
    return ''

def progList(name,type,leftid,page,order):
    #http://video.sina.com.cn/movie/category/teleplay/index.html
    #http://video.sina.com.cn/interface/movie/category.php?category=movie&page=2&pagesize=20&liststyle=1&topid=2&leftid=movie-index
    baseurl='http://video.sina.com.cn/interface/movie/category.php?category='+type
    if page:
        currpage = int(page)
    else:
        currpage = 1
    url = baseurl + '&topid='+ order + '&leftid=' + leftid + '&page=' +str(currpage) +'&liststyle=1&pagesize=20'
    print url
    link = GetHttpData(url)
    match = re.compile('({"id".+?"})', re.DOTALL).findall(link)
    totalItems = len(match)
    orderstr=searchDict(ORDER_LIST,order)
    leftlist=leftid.split('-')
    lxstr=''
    if leftlist[0]=='type':
        lxstr='类型-'
        if leftlist[1]=='index':
            lxstr=lxstr+'全部'
        else:
            if type=='movie': lxstr=lxstr+searchDict(MOVIE_TYPE_LIST['1'],leftlist[1])
            elif type=='teleplay': lxstr=lxstr+searchDict(MOVIE_TYPE_LIST['2'],leftlist[1])
            elif type=='cartoon': lxstr=lxstr+searchDict(MOVIE_TYPE_LIST['3'],leftlist[1])
            elif type=='original': lxstr=lxstr+searchDict(MOVIE_TYPE_LIST['4'],leftlist[1])
            elif type=='arts': lxstr=lxstr+searchDict(MOVIE_TYPE_LIST['5'],leftlist[1])
            elif type=='documentary': lxstr=lxstr+'-index'
            elif type=='zt': lxstr=lxstr+searchDict(MOVIE_TYPE_LIST['6'],leftlist[1])
    elif leftlist[0]=='area':
        lxstr='地区-'
        if leftlist[1]=='index':
            lxstr=lxstr+'全部'
        else:
            lxstr=lxstr+searchDict(MOVIE_AREA_LIST,leftlist[1])
    elif leftlist[0]=='year':
        lxstr='年份-'
        if leftlist[1]=='index':
            lxstr=lxstr+'全部'
        else:
            lxstr=lxstr+searchDict(MOVIE_YEAR_LIST,leftlist[1])
    else:
        lxstr='全部'+searchDict(MOVIE_MAIN_LIST,leftlist[0])

        
    orderstr=searchDict(ORDER_LIST,order)
    
    li = xbmcgui.ListItem('类型[COLOR FFFF0000]【' + lxstr + '】[/COLOR] 排序[COLOR FFFF0000]【' + orderstr + '】[/COLOR]（按此选择）')
    u = sys.argv[0] + "?mode=3&name="+urllib.quote_plus(name)+"&type="+urllib.quote_plus(type)
    xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, True, totalItems)
    for i in range(0,len(match)):
        if type=='movie':
            match1 = re.compile('"url":"(.+?)"').search(match[i])
            p_id = match1.group(1)
        else:
            match1 = re.compile('"detail":"(.+?)"').search(match[i])
            p_id = match1.group(1)
        match1 = re.compile('"thumb":"(.+?)"').search(match[i])
        p_thumb = match1.group(1)
        match1 = re.compile('"name":"(.+?)"').search(match[i])
        p_name = match1.group(1)
        p_name=eval('u"'+p_name+'"').encode('utf-8')
        p_id=p_id.replace('\\','')
        p_thumb=p_thumb.replace('\\','')
        li = xbmcgui.ListItem(p_name, iconImage = '', thumbnailImage = p_thumb)
        isDir=False
        if type=='movie':
            u = sys.argv[0]+"?mode=10&name="+urllib.quote_plus(p_name)+"&type="+urllib.quote_plus(type)+"&url="+urllib.quote_plus('http://video.sina.com.cn'+p_id)+"&thumb="+urllib.quote_plus(p_thumb)
        else:
            isDir=True
            u = sys.argv[0]+"?mode=2&name="+urllib.quote_plus(p_name)+"&url="+urllib.quote_plus('http://video.sina.com.cn'+p_id)
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, isDir, totalItems)
    if currpage > 1:
        li = xbmcgui.ListItem('上一页')
        u = sys.argv[0]+"?mode=1&name="+urllib.quote_plus(name)+"&type="+urllib.quote_plus(type)+"&leftid="+urllib.quote_plus(leftid)+"&order="+order+"&page="+urllib.quote_plus(str(currpage-1))
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, True, totalItems)
    if len(match) > 19:
        li = xbmcgui.ListItem('下一页')
        u = sys.argv[0]+"?mode=1&name="+urllib.quote_plus(name)+"&type="+urllib.quote_plus(type)+"&leftid="+urllib.quote_plus(leftid)+"&order="+order+"&page="+urllib.quote_plus(str(currpage+1))
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, True, totalItems)
    xbmcplugin.setContent(int(sys.argv[1]), 'movies')
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

def listA(name,url):
    print name
    print url
    link = GetHttpData(url)
    match1 = re.compile('<!-- 分集点播 begin-->(.+?)<!-- 分集点播 end-->', re.DOTALL).findall(link)
    match = re.compile('<div class="pic"><a href="(.+?)".+?<img src="(.+?)".+?rel=.+?>(.+?)</a></li>', re.DOTALL).findall(match1[0])
    totalItems=len(match)
    for p_url,p_thumb,p_name  in match:
        li = xbmcgui.ListItem(name+'-'+p_name, iconImage = '', thumbnailImage = p_thumb)
        print p_url
        print p_name
        print p_thumb
        u = sys.argv[0] + "?mode=10&name="+urllib.quote_plus(name+'-'+p_name)+"&url="+urllib.quote_plus('http://video.sina.com.cn'+p_url)+"&thumb="+urllib.quote_plus(p_thumb)
        #li.setInfo(type = "Video", infoLabels = {"Title":p_name, "Director":p_director, "Genre":p_genre, "Plot":p_plot, "Year":p_year, "Cast":p_cast, "Tagline":p_tagline})
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, False, totalItems)
    xbmcplugin.setContent(int(sys.argv[1]), 'movies')
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

def listB(name,type):
    li=xbmcgui.ListItem('按类型')
    u = sys.argv[0] + "?mode=5&name="+urllib.quote_plus(name)+"&id="+urllib.quote_plus('1')+"&type="+urllib.quote_plus(type)
    xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
    li=xbmcgui.ListItem('按地区')
    u = sys.argv[0] + "?mode=5&name="+urllib.quote_plus(name)+"&id="+urllib.quote_plus('2')+"&type="+urllib.quote_plus(type)
    xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
    li=xbmcgui.ListItem('按年份')
    u = sys.argv[0] + "?mode=5&name="+urllib.quote_plus(name)+"&id="+urllib.quote_plus('3')+"&type="+urllib.quote_plus(type)
    xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
    xbmcplugin.setContent(int(sys.argv[1]), 'movies')
    xbmcplugin.endOfDirectory(int(sys.argv[1]))
        
def PlayVideo(name,type,url,thumb):
    print name
    print url
    print thumb
    link = GetHttpData(url)
    match = re.compile(' vid:\'(.+?)\'').findall(link)   
    vid=match[0]
    vidlist=vid.split('|')
    ratelist=[]
    if vidlist[1]!='0':ratelist.append(['高清',vidlist[1]])
    if vidlist[0]!='0':ratelist.append(['普通',vidlist[0]])
    if len(ratelist)==1:
        rate=ratelist[0][1]
    else:
        dialog = xbmcgui.Dialog()
        list = [x[0] for x in ratelist]
        sel = dialog.select('类型', list)
        if sel == -1:
            return
        else:
            rate=ratelist[sel][1]
    url='http://v.iask.com/v_play.php?vid='+rate+'&uid=0&pid=1000&tid=4&plid=4002&referrer=http%3A%2F%2Fvideo.sina.com.cn%2Fmovie%2Fdetail%2Fmhls&r=video.sina.com.cn'
    link = GetHttpData(url)
    match = re.compile('<url><!\[CDATA\[(.+?)\]\]></url>').findall(link)
    if match:
        playlist=xbmc.PlayList(1)
        playlist.clear()
        for i in range(len(match)):
            listitem = xbmcgui.ListItem(name, thumbnailImage = __addonicon__)
            listitem.setInfo(type="Video",infoLabels={"Title":name+" 第"+str(i+1)+"/"+str(len(match))+" 节"})
            playlist.add(match[i], listitem)
        xbmc.Player().play(playlist)
    else:
        dialog = xbmcgui.Dialog()
        ok = dialog.ok(__addonname__, '无法播放：未匹配到视频文件，请稍侯再试或联系作者')

def performChanges(name,type,id):
    change = False
    dialog = xbmcgui.Dialog()
    print '类型选择开始'
    if id=='1':
        if type=='documentary':
            leftid='documentary-index'
        else:
            if type=='movie':
               list = [x[0] for x in MOVIE_TYPE_LIST['1']]
            elif type=='teleplay':
               list = [x[0] for x in MOVIE_TYPE_LIST['2']]   
            elif type=='cartoon':
               list = [x[0] for x in MOVIE_TYPE_LIST['3']] 
            elif type=='original':
               list = [x[0] for x in MOVIE_TYPE_LIST['4']] 
            elif type=='arts':
               list = [x[0] for x in MOVIE_TYPE_LIST['5']] 
            elif type=='zt':
               list = [x[0] for x in MOVIE_TYPE_LIST['6']] 
            sel = dialog.select('类型', list)
            if sel != -1:
                if type=='movie':
                    if MOVIE_TYPE_LIST['1'][sel][1]=='全部':leftid = type+'-index'
                    else:leftid = 'type-'+MOVIE_TYPE_LIST['1'][sel][1]
                elif type=='teleplay':
                    if MOVIE_TYPE_LIST['2'][sel][1]=='全部':leftid = type+'-index'
                    else:leftid = 'type-'+MOVIE_TYPE_LIST['2'][sel][1]
                elif type=='cartoon':
                    if MOVIE_TYPE_LIST['3'][sel][1]=='全部':leftid = type+'-index'
                    else:leftid = 'type-'+MOVIE_TYPE_LIST['3'][sel][1]
                elif type=='original':
                    if MOVIE_TYPE_LIST['4'][sel][1]=='全部':leftid = type+'-index'
                    else:leftid = 'type-'+MOVIE_TYPE_LIST['4'][sel][1]
                elif type=='arts':
                    if MOVIE_TYPE_LIST['5'][sel][1]=='全部':leftid = type+'-index'
                    else:leftid = 'type-'+MOVIE_TYPE_LIST['5'][sel][1]
                elif type=='zt':
                    if MOVIE_TYPE_LIST['6'][sel][1]=='全部':leftid = type+'-index'
                    else:leftid = 'type-'+MOVIE_TYPE_LIST['6'][sel][1]
        change = True
    elif id=='2':
        list = [x[0] for x in MOVIE_AREA_LIST]
        sel = dialog.select('地区', list)
        if sel != -1:
            if MOVIE_AREA_LIST[sel][1]=='全部':leftid = type+'-index'
            else:leftid = 'area-'+MOVIE_AREA_LIST[sel][1]
            change = True
    elif id=='3':
        list = [x[0] for x in MOVIE_YEAR_LIST]
        sel = dialog.select('年份', list)
        if sel != -1:
            if MOVIE_YEAR_LIST[sel][1]=='全部':leftid = type+'-index'
            else:leftid = 'year-'+MOVIE_YEAR_LIST[sel][1]
            change = True
    
    list = [x[0] for x in ORDER_LIST]
    sel = dialog.select('排序方式', list)
    if sel != -1:
        order = ORDER_LIST[sel][1]
        change = True    
    print leftid
    print order
    print '类型选择结束'
    if change:
        progList(name,type,leftid,'1',order)
        
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
leftid=''
id = None
type = ''
cat = ''
area = ''
year = ''
order = None
page = '1'
url = ''
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
    baseurl = urllib.unquote_plus(params["baseurl"])
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
    leftid = urllib.unquote_plus(params["leftid"])
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
    progList(name,type,leftid,page,order)
elif mode == 2:
    listA(name,url)
elif mode == 3:
    listB(name,type)
elif mode == 5:
    performChanges(name,type,id)
elif mode == 10:
    PlayVideo(name,type,url,thumb)

