# -*- coding: utf-8 -*-
import xbmc, xbmcgui, xbmcplugin, xbmcaddon, urllib2, urllib, re, string, sys, os, gzip, StringIO,ChineseKeyboard

# 腾讯视频(v.qq.com) by wow1122(wht9000@gmail.com), 2011

# Plugin constants 
__addonname__ = "腾讯视频(v.qq.com)"
__addonid__ = "plugin.video.tencent"
__addon__ = xbmcaddon.Addon(id=__addonid__)
__addonicon__ = os.path.join( __addon__.getAddonInfo('path'), 'icon.png' )

UserAgent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'

ORDER_LIST = [['按更新','0'], ['按热度','1'], ['按评分','2']]
ORDER_DICT = dict(ORDER_LIST)

MOVIE_TYPE_LIST = {}
MOVIE_AREA_LIST = {}
MOVIE_YEAR_LIST = {}
MOVIE_TYPE_LIST['1'] = [['全部类型','-1'],['动作','0'],['冒险','1'],['喜剧','3'],['爱情','2'],['动画','16'],['战争','5'],['恐怖','6'],['犯罪','7'],['悬疑','8'],['惊悚','9'],['武侠','10'],['科幻','4'],['音乐','19'],['奇幻','17'],['家庭','18'],['剧情','15'],['伦理','14'],['记录','22'],['历史','13'],]
MOVIE_AREA_LIST['1'] = [['全部地区','-1'],['内地','0'],['港台','1'],['日韩','4'],['欧美','5'],['其他','9999'],]
MOVIE_YEAR_LIST['1'] = [['全部年份','-1'],['2011年','2011'],['2010年','2010'],['2009年','2009'],['2008年','2008'],['2007年','2007'],['2006年','2006'],['2005年','2005'],['2004年','2004'],['2003年','2003'],['2002年','2002'],['2001年','2001'],['其他','9999'],]
MOVIE_TYPE_LIST['2'] = [['全部类型','-1'],['偶像','1'],['喜剧','2'],['爱情','3'],['都市','4'],['古装','5'],['武侠','6'],['历史','7'],['警匪','8'],['家庭','9'],['神话','10'],['剧情','11'],['悬疑','12'],['战争','13'],['军事','14'],['犯罪','15'],['情景','16'],['TVB','17'],]
MOVIE_AREA_LIST['2'] = [['全部地区','-1'],['内地','0'],['香港','1'],['台湾','4'],['韩国','5'],['其他','9999'],]
MOVIE_YEAR_LIST['2'] = [['全部年份','-1'],['2011年','2011'],['2010年','2010'],['2009年','2009'],['2008年','2008'],['2007年','2007'],['2006年','2006'],['其他','9999'],]
MOVIE_TYPE_LIST['3'] = [['全部类型','-1'],['流行','1'],['摇滚','0'],['R&B','2'],['电子','3'],['爵士','4'],['说唱','5'],]
MOVIE_AREA_LIST['3'] = [['全部地区','-1'],['港台','0'],['内地','1'],['日韩','2'],['欧美','3'],['其他','4'],]
MOVIE_YEAR_LIST['3'] = [['全部年份','-1'],['2011年','2011'],['2010年','2010'],['2009年','2009'],['2008年','2008'],['2007年','2007'],]

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
    u=sys.argv[0]+"?mode=1&name="+urllib.quote_plus('电影')+"&type="+urllib.quote_plus('2')+"&cat="+urllib.quote_plus('-1')+"&area="+urllib.quote_plus('-1')+"&year="+urllib.quote_plus('-1')+"&order="+urllib.quote_plus('1')+"&page="+urllib.quote_plus('0')
    xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
    li=xbmcgui.ListItem('电视剧')
    u=sys.argv[0]+"?mode=1&name="+urllib.quote_plus('电视剧')+"&type="+urllib.quote_plus('3')+"&cat="+urllib.quote_plus('-1')+"&area="+urllib.quote_plus('-1')+"&year="+urllib.quote_plus('-1')+"&order="+urllib.quote_plus('1')+"&page="+urllib.quote_plus('0')
    xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
#    li=xbmcgui.ListItem('综艺')
#    u=sys.argv[0]+"?mode=1&name="+urllib.quote_plus('综艺')+"&type="+urllib.quote_plus('http://v.qq.com/variety/latest/1_1.html')
#    xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
    li=xbmcgui.ListItem('音乐')
    u=sys.argv[0]+"?mode=1&name="+urllib.quote_plus('音乐')+"&type="+urllib.quote_plus('4')+"&cat="+urllib.quote_plus('-1')+"&area="+urllib.quote_plus('-1')+"&year="+urllib.quote_plus('-1')+"&order="+urllib.quote_plus('1')+"&page="+urllib.quote_plus('0')
    xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
    li=xbmcgui.ListItem('娱乐')
    u=sys.argv[0]+"?mode=1&name="+urllib.quote_plus('娱乐')+"&type="+urllib.quote_plus('6')+"&cat="+urllib.quote_plus('-1')+"&area="+urllib.quote_plus('-1')+"&year="+urllib.quote_plus('-1')+"&order="+urllib.quote_plus('1')+"&page="+urllib.quote_plus('0')
    xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
    li=xbmcgui.ListItem('体育')
    u=sys.argv[0]+"?mode=1&name="+urllib.quote_plus('体育')+"&type="+urllib.quote_plus('5')+"&cat="+urllib.quote_plus('-1')+"&area="+urllib.quote_plus('-1')+"&year="+urllib.quote_plus('-1')+"&order="+urllib.quote_plus('1')+"&page="+urllib.quote_plus('0')
    xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
    li=xbmcgui.ListItem('新闻')
    u=sys.argv[0]+"?mode=1&name="+urllib.quote_plus('新闻')+"&type="+urllib.quote_plus('7')+"&cat="+urllib.quote_plus('-1')+"&area="+urllib.quote_plus('-1')+"&year="+urllib.quote_plus('-1')+"&order="+urllib.quote_plus('1')+"&page="+urllib.quote_plus('0')
    xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
    li=xbmcgui.ListItem('财经')
    u=sys.argv[0]+"?mode=1&name="+urllib.quote_plus('财经')+"&type="+urllib.quote_plus('8')+"&cat="+urllib.quote_plus('-1')+"&area="+urllib.quote_plus('-1')+"&year="+urllib.quote_plus('-1')+"&order="+urllib.quote_plus('1')+"&page="+urllib.quote_plus('0')
    xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
    li=xbmcgui.ListItem('搜索')
    u=sys.argv[0]+"?mode=6&name="+urllib.quote_plus('搜索')+"&type="+urllib.quote_plus('8')+"&cat="+urllib.quote_plus('-1')+"&area="+urllib.quote_plus('-1')+"&year="+urllib.quote_plus('-1')+"&order="+urllib.quote_plus('1')+"&page="+urllib.quote_plus('0')
    xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
    xbmcplugin.endOfDirectory(int(sys.argv[1]))
    
def searchDict(dlist,idx):
    for i in range(0,len(dlist)):
        if dlist[i][1] == idx:
            return dlist[i][0]
    return ''

def progList(name,type,page,cat,area,year,order):
    baseurl='http://sns.video.qq.com/fcgi-bin/txv_lib?'
    if page:
        currpage = int(page)
    else:
        currpage = 0
    url = baseurl + 'mi_mtype='+type+'&mi_type='+cat+ '&mi_area=' +area+ '&mi_year=' + year + '&mi_sort=1&mi_show_type=0&mi_pagenum=' +str(currpage) +'&mi_pagesize=30&otype=xml&mi_online=1&mi_index_type=0'
    print url
    link = GetHttpData(url)
    match = re.compile('<total>(.+?)</total>', re.DOTALL).findall(link)
    alltotalItems=match[0]
    if int(alltotalItems)%30 > 0:
        totalpages=int(alltotalItems)/30+1
    else:
        totalpages=int(alltotalItems)/30
    match = re.compile('(<movies>.+?</movies>)', re.DOTALL).findall(link)
    totalItems = len(match)
    print '页数：'+str(totalpages)
    print '每页个数：'+str(totalItems)
    if currpage > 1: totalItems = totalItems + 1
    if currpage < totalpages: totalItems = totalItems + 1
    if type in ['2','3','4']:
        if cat == '-1':
            catstr = '全部类型'
        else:
            if type=='2':catstr = searchDict(MOVIE_TYPE_LIST['1'],cat)
            elif type=='3':catstr = searchDict(MOVIE_TYPE_LIST['2'],cat)
            elif type=='4':catstr = searchDict(MOVIE_TYPE_LIST['3'],cat)
        if area == '-1':
            areastr = '全部地区'
        else:
            if type=='2':areastr = searchDict(MOVIE_AREA_LIST['1'],area)
            elif type=='3':areastr = searchDict(MOVIE_AREA_LIST['2'],area)
            elif type=='4':areastr = searchDict(MOVIE_AREA_LIST['3'],area)
        if year == '-1':
            yearstr = '全部年份'
        else:
            if type=='2':yearstr = searchDict(MOVIE_YEAR_LIST['1'],year)
            elif type=='3':yearstr = searchDict(MOVIE_YEAR_LIST['2'],year)
            elif type=='4':yearstr = searchDict(MOVIE_YEAR_LIST['3'],year)
        orderstr=searchDict(ORDER_LIST,order)
        li = xbmcgui.ListItem('类型[COLOR FFFF0000]【' + catstr + '】[/COLOR] 地区[COLOR FFFF0000]【' + areastr + '】[/COLOR] 年份[COLOR FFFF0000]【' + yearstr + '】[/COLOR] 排序[COLOR FFFF0000]【' + orderstr + '】[/COLOR]（按此选择）')
        u = sys.argv[0] + "?mode=5&name="+urllib.quote_plus(name)+"&type="+type+"&cat="+urllib.quote_plus(cat)+"&area="+urllib.quote_plus(area)+"&year="+urllib.quote_plus(year)+"&order="+order+"&page="+urllib.quote_plus(page)
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, True, totalItems)
    for i in range(0,len(match)):
        match1 = re.compile('<cover_id>(.+?)</cover_id>').search(match[i])
        if type=='4':
            p_id = match1.group(1)
            match1 = re.compile('<actor>(.+?)</actor>').search(match[i])
            p_actor =match1.group(1)
            p_actor1=p_actor.split(';')[1]
        else:
            p_id = match1.group(1)[0]+'/'+match1.group(1)+'.html'
        match1 = re.compile('<pic_url>(.+?)</pic_url>').search(match[i])
        p_thumb = match1.group(1)
        match1 = re.compile('<title>(.+?)</title>').search(match[i])
        p_name = match1.group(1)
        if type=='4':
            li = xbmcgui.ListItem(p_actor1+'-'+p_name, iconImage = '', thumbnailImage = p_thumb)
        else:
            li = xbmcgui.ListItem(p_name, iconImage = '', thumbnailImage = p_thumb)
        u = sys.argv[0]+"?mode=10&name="+urllib.quote_plus(p_name)+"&type=2&url="+urllib.quote_plus('http://v.qq.com/cover/'+p_id)+"&thumb="+urllib.quote_plus(p_thumb)
        isDir=False
        if type=='3':
            u = sys.argv[0]+"?mode=2&name="+urllib.quote_plus(p_name)+"&url="+urllib.quote_plus('http://v.qq.com/cover/'+p_id)+"&thumb="+urllib.quote_plus(p_thumb)
            isDir=True
        if type=='4':
            u = sys.argv[0]+"?mode=3&name="+urllib.quote_plus(p_actor1+'-'+p_name)+"&url="+urllib.quote_plus(p_id)+"&thumb="+urllib.quote_plus(p_thumb)
        #li.setInfo(type = "Video", infoLabels = {"Title":p_name, "Director":p_director, "Genre":p_genre, "Plot":p_plot, "Year":p_year, "Cast":p_cast, "Tagline":p_tagline})
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, isDir, totalItems)

    order='1'
    cat='-1'
    area='-1'
    year='-1'
    if currpage > 1:
        li = xbmcgui.ListItem('上一页')
        u = sys.argv[0]+"?mode=1&name="+urllib.quote_plus(name)+"&type="+urllib.quote_plus(type)+"&baseurl="+urllib.quote_plus(baseurl)+"&cat="+urllib.quote_plus(cat)+"&area="+urllib.quote_plus(area)+"&year="+urllib.quote_plus(year)+"&order="+order+"&page="+urllib.quote_plus(str(currpage-1))
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, True, totalItems)
    if currpage < totalpages:
        li = xbmcgui.ListItem('下一页')
        u = sys.argv[0]+"?mode=1&name="+urllib.quote_plus(name)+"&type="+urllib.quote_plus(type)+"&baseurl="+urllib.quote_plus(baseurl)+"&cat="+urllib.quote_plus(cat)+"&area="+urllib.quote_plus(area)+"&year="+urllib.quote_plus(year)+"&order="+order+"&page="+urllib.quote_plus(str(currpage+1))
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, True, totalItems)
    xbmcplugin.setContent(int(sys.argv[1]), 'movies')
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

def listA(name,url,thumb):
    print name
    print url
    print thumb
    link = GetHttpData(url)
    if link.find('sv=""') > 0 :
        match = re.compile('</i><a target="_self".+?id="(.+?)"  title="(.+?)"', re.DOTALL).findall(link)
        totalItems=len(match)
        for p_url,p_name  in match:
            li = xbmcgui.ListItem(p_name, iconImage = '', thumbnailImage = thumb)
            u = sys.argv[0] + "?mode=10&name="+urllib.quote_plus(p_name)+"&type=3&url="+urllib.quote_plus(p_url)+"&thumb="+urllib.quote_plus(thumb)
            #li.setInfo(type = "Video", infoLabels = {"Title":p_name, "Director":p_director, "Genre":p_genre, "Plot":p_plot, "Year":p_year, "Cast":p_cast, "Tagline":p_tagline})
            xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, False, totalItems)
    else:
        match = re.compile('</i><a target="_self".+?title="(.+?)".+?sv="(.+?)"', re.DOTALL).findall(link)
        totalItems=len(match)
        print str(totalItems)
        for p_name,p_url  in match:
            li = xbmcgui.ListItem(p_name, iconImage = '', thumbnailImage = thumb)
            u = sys.argv[0] + "?mode=10&name="+urllib.quote_plus(p_name)+"&type=3&url="+urllib.quote_plus(p_url)+"&thumb="+urllib.quote_plus(thumb)
            #li.setInfo(type = "Video", infoLabels = {"Title":p_name, "Director":p_director, "Genre":p_genre, "Plot":p_plot, "Year":p_year, "Cast":p_cast, "Tagline":p_tagline})
            xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, False, totalItems)
    xbmcplugin.setContent(int(sys.argv[1]), 'movies')
    xbmcplugin.endOfDirectory(int(sys.argv[1]))
    
def PlayVideo(name,type,url,thumb):
    print name
    print url
    print thumb
    if type=='2':
        link = GetHttpData(url)
        match = re.compile('vid:"(.+?)"').findall(link)   
        vid=match[0]
        vidlist=vid.split('|')
    elif type=='3':
        vidlist=url.split('|')
    print vidlist
    if len(vidlist)>0:
        playlist=xbmc.PlayList(1)
        playlist.clear()
        for i in range(len(vidlist)):
            listitem = xbmcgui.ListItem(name, thumbnailImage = __addonicon__)
            listitem.setInfo(type="Video",infoLabels={"Title":name+" 第"+str(i+1)+"/"+str(len(vidlist))+" 节"})
            link = GetHttpData('http://vv.video.qq.com/geturl?otype=xml&platform=1&format=2&&vid='+vidlist[i])
            match = re.compile('<url>(.+?)</url>').findall(link)
            playlist.add(match[0], listitem)
        xbmc.Player().play(playlist)
    else:
        dialog = xbmcgui.Dialog()
        ok = dialog.ok(__addonname__, '无法播放：未匹配到视频文件，请稍侯再试或联系作者')

def PlayMv(name,url,thumb):
    print name
    print url
    print thumb
    link = GetHttpData('http://vv.video.qq.com/geturl?otype=xml&platform=1&format=2&&vid='+url)
    match = re.compile('<url>(.+?)</url>').findall(link)
    xbmc.Player().play(match[0])


def SearchVideo(name,type,url,thumb):
		kb=xbmc.Keyboard('','输入所查影片中文信息-拼音或简拼(拼音首字母)',False)
		kb.doModal()
		kw=kb.getText() 
		
    #li=xbmcgui.ListItem("搜索结果")
    #u=""
    #xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
    #keyboard = ChineseKeyboard.Keyboard('缺省输入字串','中文输入窗标题')
    #keyboard.doModal()
    #if (keyboard.isConfirmed()):
        #input_string = keyboard.getText()
        #link = GetHttpData('http://v.qq.com/search.html?pagetype=3&ms_key='+input_string)
        #match = re.compile('<img src="(.+?)".+?playid="(.+?)">(.+?)</a>.+?([.+?])', re.DOTALL).findall(link)
        #totalItems=len(match)
        #for p_thumb,p_vid,p_name,p_type  in match:
            #li = xbmcgui.ListItem(p_name, iconImage = '', thumbnailImage = p_thumb)
            #print p_url
            #u = sys.argv[0] + "?mode=10&name="+urllib.quote_plus(p_name)+"&type=3&url="+urllib.quote_plus(p_url)+"&thumb="+urllib.quote_plus(p_thumb)
            #li.setInfo(type = "Video", infoLabels = {"Title":p_name, "Director":p_director, "Genre":p_genre, "Plot":p_plot, "Year":p_year, "Cast":p_cast, "Tagline":p_tagline})
            #xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, False, totalItems)
        #xbmcplugin.setContent(int(sys.argv[1]), 'movies')
        #xbmcplugin.endOfDirectory(int(sys.argv[1]))        
        
        
def performChanges(name,type,page,cat,area,year,order):
    change = False
    dialog = xbmcgui.Dialog()
    if type=='2':
       list = [x[0] for x in MOVIE_TYPE_LIST['1']]
    elif type=='3':
       list = [x[0] for x in MOVIE_TYPE_LIST['2']]   
    elif type=='4':
       list = [x[0] for x in MOVIE_TYPE_LIST['3']] 
    sel = dialog.select('类型', list)
    if sel != -1:
        if type=='2':
           cat = MOVIE_TYPE_LIST['1'][sel][1]
        elif type=='3':
           cat = MOVIE_TYPE_LIST['2'][sel][1]  
        elif type=='4':
           cat = MOVIE_TYPE_LIST['3'][sel][1] 
        change = True
    if type=='2':
        list = [x[0] for x in MOVIE_AREA_LIST['1']]
    elif type=='3':
        list = [x[0] for x in MOVIE_AREA_LIST['2']]        
    elif type=='4':
        list = [x[0] for x in MOVIE_AREA_LIST['3']]   
    sel = dialog.select('地区', list)
    if sel != -1:
        if type=='2':
           area = MOVIE_AREA_LIST['1'][sel][1]
        elif type=='3':
           area = MOVIE_AREA_LIST['2'][sel][1]        
        elif type=='4':
           area = MOVIE_AREA_LIST['3'][sel][1]  
        change = True
    if type=='2':
        list = [x[0] for x in MOVIE_YEAR_LIST['1']]
    elif type=='3':
        list = [x[0] for x in MOVIE_YEAR_LIST['2']]        
    elif type=='4':
        list = [x[0] for x in MOVIE_YEAR_LIST['3']]
    sel = dialog.select('地区', list)
    if sel != -1:
        if type=='2':
           year = MOVIE_YEAR_LIST['1'][sel][1]
        elif type=='3':
           year = MOVIE_YEAR_LIST['2'][sel][1]        
        elif type=='4':
           year = MOVIE_YEAR_LIST['3'][sel][1]  
        change = True
    list = [x[0] for x in ORDER_LIST]
    sel = dialog.select('排序方式', list)
    if sel != -1:
        order = ORDER_LIST[sel][1]
        change = True

    if change:
        progList(name,type,'0',cat,area,year,order)

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
    progList(name,type,page,cat,area,year,order)
elif mode == 2:
    listA(name,url,thumb)
elif mode == 3:
    PlayMv(name,url,thumb)
elif mode == 5:
    performChanges(name,type,page,cat,area,year,order)
elif mode == 6:
    SearchVideo(name,type,url,thumb)
elif mode == 10:
    PlayVideo(name,type,url,thumb)

