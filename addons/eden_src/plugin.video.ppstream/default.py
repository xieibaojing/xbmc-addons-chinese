# -*- coding: utf-8 -*-
import xbmc, xbmcgui, xbmcplugin, xbmcaddon
import urllib2, urllib, httplib, time
import os, sys, re, string, gzip, StringIO
import cookielib
import ChineseKeyboard

if sys.version_info < (2, 7):
    import simplejson
else:
    import json as simplejson

########################################################################
# PPStream 网络电视 by cmeng
# Version 2.2.4 2013-04-20 (cmeng)
# Update scripts per site latest change
# Clean up search routine
# Use new pps4xbmc (VB2010) with enhanced features
 
# See changelog.txt for previous history
########################################################################
# Plugin constants 
__addonname__ = "PPS 网络电视"
__addonid__   = "plugin.video.ppstream"
__addon__ = xbmcaddon.Addon(id=__addonid__)
__addonicon__ = os.path.join( __addon__.getAddonInfo('path'), 'icon.png' )
__settings__  = xbmcaddon.Addon(id=__addonid__)
__profile__   = xbmc.translatePath( __settings__.getAddonInfo('profile') )
__cwd__       = xbmc.translatePath( __settings__.getAddonInfo('path') )
cookieFile = __profile__ + 'cookies.ppstream'

UserAgent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'
VIDEO_LIST = [['c_movie','电影'],['c_tv','电视剧'],['c_zy','综艺'],['c_anime','动漫']]
UGC_LIST = [['c10','原创'],['c11','音乐'],['ent','娱乐'],['life','生活'],['c4','焦点'],['game','游戏'],['c5','财经'],['c6','体育'],['auto','汽车'],['tech','科技'],['fashion','时尚'],['travel','旅游'],['mama','母婴'],['c19','教育'],['fun','搞笑'],['girl','女性'],['c22','其它'],['c24','达人秀'],['food','美食']]
SORT_LIST = [['','播放最多'],['_o_2','评分最高'],['_o_3','最近更新']]
IPD_LIST = [['ent','娱乐'],['life','生活'],['game','游戏'],['auto','汽车'],['tech','科技'],['fashion','时尚'],['travel','旅游'],['mama','母婴'],['fun','搞笑'],['girl','女性'],['food','美食']]
ISORT_DATE = [['default','全部'],['today','今日'],['week','本周'],['month','本月']]
ISORT_ORDER = [['0','默认'],['1','最近更新'],['2','播放最多']]
COLOR_LIST = ['[COLOR FFFF0000]','[COLOR FF00FF00]','[COLOR FFFFFF00]','[COLOR FF00FFFF]','[COLOR FFFF00FF]']
MPLAYER_LIST = [['10','PPS网络电视'],['99','SMG'],['43','优酷'],['44','土豆'],['45','奇艺'],['46','搜狐'],['47','新浪'],['48','乐视']]
VIDEO_RES = [["标清",'sd'],["高清",'hd'],["普通",''],["未注","null"]] 
datelist = [['t1','全部'],['t2','今日'],['t3','本周'],['t4','本月']]
orderlist = [['o1','最新发布'],['o2','最多播放'],['o3','最多评论'],['o4','最多推荐']]   
     
##################################################################################
# Routine to fetech url site data using Mozilla browser
# - deletc '\r|\n|\t' for easy re.compile
# - do not delete ' ' i.e. <space> as some url include spaces
# - unicode with 'replace' option to avoid exception on some url
# - translate to utf8
##################################################################################
def getHttpData(url):
    print "getHttpData: " + url
    # setup proxy support
    proxy = __addon__.getSetting('http_proxy')
    type = 'http'
    if proxy <> '':
        ptype = re.split(':', proxy)
        if len(ptype)<3:
            # full path requires by Python 2.4
            proxy = type + '://' + proxy 
        else: type = ptype[0]
        httpProxy = {type: proxy}
    else:
        httpProxy = {}
    proxy_support = urllib2.ProxyHandler(httpProxy)

    # setup cookie support
    cj = cookielib.MozillaCookieJar(cookieFile)
    if os.path.isfile(cookieFile):
        cj.load(ignore_discard=True, ignore_expires=True)
    else:
        if not os.path.isdir(os.path.dirname(cookieFile)):
            os.makedirs(os.path.dirname(cookieFile))
    
    # create opener for both proxy and cookie
    opener = urllib2.build_opener(proxy_support, urllib2.HTTPCookieProcessor(cj))
    #opener = urllib2.build_opener(proxy_support)
    req = urllib2.Request(url)
    req.add_header('User-Agent', UserAgent)
    
    for k in range(3): # give 3 trails to fetch url data
        try:
            response = opener.open(req)
        except urllib2.HTTPError, e:
            httpdata = e.read()
        except urllib2.URLError, e:
            httpdata = "IO Timeout Error"
        else:
            httpdata = response.read()
            response.close()
            cj.save(cookieFile, ignore_discard=True, ignore_expires=True)
            for cookie in cj:
                print cookie
            break

    httpdata = re.sub('\r|\n|\t', '', httpdata)
    match = re.compile('<meta.+?charset=["]*(.+?)"').findall(httpdata)
    if len(match):
        charset = match[0].lower()
        if (charset != 'utf-8') and (charset != 'utf8'):
            httpdata = unicode(httpdata, charset,'replace').encode('utf8')
    return httpdata

##################################################################################
# Routine to extract url ID based on given selected filter
# List = ['movie', '电影'], ['tv', '电视剧'] ...
# list = ['1', '全部'], ['2', '今日'] ...
# List = ['1', '最新发布'], ['2', '最多播放']....
# .......
##################################################################################
def fetchID(dlist, idx):
    for i in range(0, len(dlist)):
        if dlist[i][1] == idx:
            return dlist[i][0]
    return ''

##################################################################################
# Routine to fetch and build video filter list
# - 按类型  (Categories)
# - 按国家/地区 (Countries/Areas)
# - 按年份 (Year)
##################################################################################
def getList(listpage):
    catlist = arealist = yearlist = []
    match = re.compile('<dt>按类型：</dt>(.+?)</ul>').findall(listpage)
    catlist = re.compile('href="/v_list/c_[a-z]+([_st]*.*?)[_.]+.+?ml">(.+?)</a>').findall(match[0])
    
    match = re.compile('<dt>按地区：</dt>(.+?)</ul>').findall(listpage)
    arealist = re.compile('href="/v_list/c_[a-z]+([_sa]*.*?)[_.]+.+?ml">(.+?)</a>').findall(match[0])
 
    match = re.compile('<dt>按年份：</dt>(.+?)</ul>').findall(listpage)
    yearlist = re.compile('href="/v_list/c_[a-z]+([_sy]*.*?)[_.]+.+?ml">(.+?)</a>').findall(match[0])

    #print 'list...', catlist, arealist, yearlist
    return catlist, arealist, yearlist

##################################################################################
# Routine to fetch & build PPS 网络电视 main menu
# - video list as per [VIDEO_LIST]
# - ugc list as per [UGC_LIST]
# - movie, series & ugc require different sub-menu access methods
##################################################################################
def mainMenu():
    #li = xbmcgui.ListItem('[COLOR FFFF0000]PPS 网络电视:[/COLOR][COLOR FF00FF00]【请输入搜索内容】[/COLOR]')
    li = xbmcgui.ListItem('[COLOR FF00FFFF] PPS 网络电视搜索:[/COLOR][COLOR FF00FF00]【点此进行】[/COLOR]')
    u=sys.argv[0]+"?mode=31"
    xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, True)
    
    # fetch the url for video channels specified in VIDEO_LIST
    i = 0
    for id, name in VIDEO_LIST:
        i = i+1
        li = xbmcgui.ListItem(str(i)+'. '+name)
        u = sys.argv[0]+"?mode=1&name="+urllib.quote_plus(name)+"&id="+id+"&page=1"+"&cat=全部"+"&area=全部"+"&year=全部"+"&order=播放最多"
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, True)
    
    # fetch the url for ugc channels, exclude those already in VIDEO_LIST 
    for cat, name in UGC_LIST:
        if cat[0]=='c':
            morder = '最多播放'
        else:
            morder = '播放最多'
        i = i+1
        li = xbmcgui.ListItem(str(i)+'. '+name)
        u = sys.argv[0]+"?mode=11&name="+urllib.quote_plus(name)+"&id=ugc"+"&page=1"+"&cat="+cat+"&year=本周"+"&order="+morder
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, True)
        
    xbmcplugin.setContent(int(sys.argv[1]), 'movies')
    xbmcplugin.endOfDirectory(int(sys.argv[1]))  

##################################################################################
# Routine to fetch and build the video selection menu
# - selected page & filters (user selectable)
# - video items list
# - user selectable pages
#
# http://v.pps.tv/v_list/c_tv_st_%B0%AE%C7%E9_sa_%C4%DA%B5%D8_sy_2011_p_2.html
# c_tv: video ID 电影类型
# _st_: category 按类型
# _sa_: area 按地区
# _sy_year: period 按年份
# _o_: filter 排序方式: 众数 按评分 
#
##################################################################################
#def progListMovie(name, id, page, cat, area, year, order):
def progListMovie(name, id, page, cat, area, year, order, listpage):
    # fetch user specified url filter ID's  
    p_url = ''
    catID = areaID = yearID = ''
    if listpage is None:  # first entry
        p_url='http://v.pps.tv/v_list/'+id+'_p_1.html'
        link = getHttpData(p_url)
        
        # Extract filter list for user selection - list order valid on first entry only
        match = re.compile('<dl class="cate-panel">(.+?)</dl>').findall(link)
        listpage = match[0]
    catlist, arealist, yearlist = getList(listpage)   
 
    catID = fetchID(catlist, cat)
    areaID = fetchID(arealist, area)
    yearID = fetchID(yearlist, year)
    sortID = fetchID(SORT_LIST, order)    
    videoID = fetchID(VIDEO_LIST, name)    
                   
    # construct url based on user elected filter ID's
    url = 'http://v.pps.tv/v_list/'+videoID+catID+areaID+yearID+sortID+'_p_'+page
    url += '.html'
    if p_url <> url: # fetch http data if not first entry
        link = getHttpData(url)

    match = re.compile('<li class="p-item list-item">(.+?)</ul></li>').findall(link)                  
    totalItems = len(match)
    if re.search(cat,'全部'): cat = '全部类型'
    if re.search(area,'全部'): area = '全部地区'
    if re.search(year,'全部'): year = '全部年份'

    # Fetch & build video titles list for user selection, highlight user selected filter  
    li = xbmcgui.ListItem('[COLOR FFFF00FF]'+name+'[/COLOR]（第'+str(page)+'页）【[COLOR FFFF0000]'+cat+'[/COLOR]/[COLOR FF00FF00]'+area+'[/COLOR]/[COLOR FFFFFF00]'+year+'[/COLOR]/[COLOR FF00FFFF]'+order+'[/COLOR]】（按此选择）')
    u = sys.argv[0]+"?mode=4&name="+urllib.quote_plus(name)+"&id="+id+"&page=1"+"&cat="+cat+"&area="+area+"&year="+year+"&order="+order+"&listpage="+urllib.quote_plus(listpage)
    xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, True, totalItems)

    for i in range(0, len(match)):
        # Video & Series titles need different routines
        if name == '电影':
            mode = '10'
            match1 = re.compile('<a class="ico-item btn-syp" target="_blank" href="(.+?)">').findall(match[i])
        else:
            mode = '3'
            match1 = re.compile('<a target="_blank" href="(.+?)">').findall(match[i])

        # skip if no playback button for playing video
        if match1 == None: continue
        p_url = match1[0]
        if not re.search('http:', p_url):
            p_url = 'http://v.pps.tv'+p_url
        
        match1 = re.compile('<img class="thumb" alt="(.+?)".+?src="(.+?)"').findall(match[i])
        p_thumb = match1[0][1]
        p_name = p_list = match1[0][0]
        
        match1 = re.compile('<span class="status tr">[更新至]*(.*?)</span>').findall(match[i])
        if len(match1[0].strip()) > 0: p_list += ' [COLOR AA00FFFF]['+match1[0].strip()+'][/COLOR]'

        match1 = re.compile('<.+?class="score">(.+?)</').findall(match[i])
        if match1: p_list += ' [COLOR FFFF00FF]['+match1[0]+'][/COLOR]'
              
        match1 = re.compile('<span class="clarity-HD">(.+?)</span>').findall(match[i])
        if match1: p_list += ' [COLOR FF00FF00]['+match1[0]+'][/COLOR]'             
               
        match1 = re.compile('播放次数：(.+?)</span></li>').findall(match[i])
        if match1: p_list += ' [播放: '+match1[0]+']' #+ ' ('+p_url+')'
  
        li = xbmcgui.ListItem(str(i+1)+'. '+p_list, iconImage='', thumbnailImage=p_thumb)
        u = sys.argv[0]+"?mode="+mode+"&name="+urllib.quote_plus(p_name)+"&url="+urllib.quote_plus(p_url)+"&thumb="+urllib.quote_plus(p_thumb)
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, True, totalItems)

    # Fetch and build user selectable page number
    matchp = re.compile('<div class="page-nav">(.+?)</div>').findall(link)
    if len(matchp): 
        matchp1 = re.compile('<a href=.+?class="pn".+?>([0-9]+)</span>').findall(matchp[0])    
        if len(matchp1):
            plist=[]
            for num in matchp1:
                if num not in plist:
                    plist.append(num)
                    li = xbmcgui.ListItem("... 第"+num+"页")
                    u = sys.argv[0]+"?mode=1&name="+urllib.quote_plus(name)+"&id="+urllib.quote_plus(id)+"&cat="+urllib.quote_plus(cat)+"&area="+urllib.quote_plus(area)+"&year="+urllib.quote_plus(year)+"&order="+order+"&page="+urllib.quote_plus(str(num))+ "&listpage="+urllib.quote_plus(listpage)
                    xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, True, totalItems)        

    xbmcplugin.setContent(int(sys.argv[1]), 'movies')
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

##################################################################################
# Routine to update video list as per user selected filters
# - 按类型  (Categories)
# - 按国家/地区 (Countries/Areas)
# - 按年份 (Year)
##################################################################################
def updateListMovie(name, id, page, cat, area, year, order, listpage):
    change = False
    dialog = xbmcgui.Dialog()
    catlist, arealist, yearlist = getList(listpage)

    list = [x[1] for x in catlist]        
    sel = dialog.select('类型', list)
    if sel != -1:
        cat = catlist[sel][1]
        change = True
                    
    list = [x[1] for x in arealist]
    sel = dialog.select('地区', list)
    if sel != -1:
        area = arealist[sel][1]
        change = True
    list = [x[1] for x in yearlist]
    sel = dialog.select('年份', list)
    if sel != -1:
        year = yearlist[sel][1]
        change = True
    list = [x[1] for x in SORT_LIST]
    sel = dialog.select('排序方式', list)
    if sel != -1:
        order = SORT_LIST[sel][1]
        change = True
        
    if change: progListMovie(name, id, '1', cat, area, year, order, listpage)
    else: return(name, id, '1', cat, area, year, order, listpage)
                  
##################################################################################
# Routine to fetch and build the video series selection menu
# - selected page & filters (user selectable)
# - Video series list
# - user selectable pages

# ustr.decode('unicode-escape').encode('utf-8') 
##################################################################################
def progListSeries(name, url, thumb, episodeSel):
    # url = http://v.pps.tv/splay_156449.html
    sid = re.compile('.+?_(.+?).html').findall(url)[0]
    s_url = 'http://v.pps.tv/ugc/ajax/aj_newlongvideo.php?sid=' + sid + '&type=splay'
    link = getHttpData(s_url)   #.replace('\\/','/')
    jsd = simplejson.loads(link)
    
    # let user select series option if more than 1 series option i.e. language, HD, related info etc
    listpage = epSet = []
    for opt in jsd['series_type']:
        epSet.append(opt.encode('utf-8'))
    if len(epSet) > 1:
        episodeSel=updateListSeries(name,'1',thumb,listpage)

    epsel = 0 
    eList = ''
    for i in range(0, len(epSet)):
        eList = eList+COLOR_LIST[i%5]+epSet[i]+'[/COLOR]|'
        if epSet[i]==episodeSel: epsel = i
    if epSet: episodeSel=epSet[epsel]
    else: episodeSel=''

    li = xbmcgui.ListItem('[COLOR FFFF00FF]'+name+'[/COLOR]: [COLOR FF00FFFF](选择:'+episodeSel+')[/COLOR]【'+eList+'】（按此选择）', iconImage='', thumbnailImage=thumb)
    u = sys.argv[0]+"?mode=3&name="+urllib.quote_plus(name)+"&url="+urllib.quote_plus(url)+"&thumb="+urllib.quote_plus(thumb) 
    xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, True)
    
    # fetch and build the video series episode list
    vlist = jsd['content'][epsel]
    totalItems = len(vlist)
    if jsd['have_time'] == "yes":
        for tdate in sorted(vlist.iterkeys(), reverse=True):
            alist = vlist[tdate]
            #print 'date: ' + tdate
            for i in range(0, len(alist)):
                v_url = alist[i]['url_key']
                p_thumb =  alist[i]['cover']
                p_title =  alist[i]['title'].encode('utf-8')
                p_time = alist[i]['video_time'].encode('utf-8')
                date = alist[i]['d_echo'].encode('utf-8')
                
                p_list = p_name = date + ': ' + p_title
                p_url = 'http://v.pps.tv/play_' + v_url + '.html#from_splay'
                p_list += ' [' + p_time + '] '

                li = xbmcgui.ListItem(p_list, iconImage='', thumbnailImage=p_thumb)
                u = sys.argv[0]+"?mode=10&name="+urllib.quote_plus(p_name)+"&url="+urllib.quote_plus(p_url)
                xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, False, totalItems) 
    else:
        for i in range(0, len(vlist)):
            v_url = vlist[i]['url_key']
            p_thumb = vlist[i]['cover']
            p_title = vlist[i]['title'].encode('utf-8')
            p_time = vlist[i]['video_time'].encode('utf-8')
            p_list = p_name = '第 ' + vlist[i]['order'].encode('utf-8') + ' 集: ' + p_title

            p_url = 'http://v.pps.tv/play_' + v_url + '.html#from_splay'
            p_list += ' [' + p_time + '] '
       
            li = xbmcgui.ListItem(p_list, iconImage='', thumbnailImage=p_thumb)
            u = sys.argv[0]+"?mode=10&name="+urllib.quote_plus(p_name)+"&url="+urllib.quote_plus(p_url)
            xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, False, totalItems)

    xbmcplugin.setContent(int(sys.argv[1]), '电视剧')
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

##################################################################################
# Routine to update video series list as per user selections
# - 剧集列表 (Series Options)
##################################################################################
def updateListSeries(name, url, thumb, listpage):
    elist = listpage
    dialog = xbmcgui.Dialog()
    sel = dialog.select('剧集列表', elist)
    if sel != -1:
        epSel = elist[sel]
        # return selected value on local call
        if url=='1': return epSel
        else: progListSeries(name, url, thumb, epSel)
    else: return(name, url, thumb, '1')

##################################################################################
# Routine to fetch and build the ugc selection menu
# - selected page & filters (user selectable)
# - ugc items list
# - user selectable pages

# Ipd= http://ipd.pps.tv/fashion.html?type=video&time=week&sort=2&page=3
##################################################################################
def progListUgc(name, id, page, cat, year, order): 
    # fetch url filter ID's & Construct url based on filter ID's & selected page           
    if cat[0] == 'c':
        mf = '12'        
        dateID = fetchID(datelist, year)
        orderID = fetchID(orderlist, order)    
        url = 'http://v.pps.tv/'+id+'/list-'+cat+'-'+dateID+'-'+orderID+'-p'+page+'.html'
    else:
        mf ='13'
        dateID = fetchID(ISORT_DATE, year)
        orderID = fetchID(ISORT_ORDER, order)    
        url = 'http://ipd.pps.tv/'+cat+'.html?type=video&time='+dateID+'&sort='+orderID+'&page='+page

    link = getHttpData(url)
    # Fetch & build ugc/ipd list for user selection, highlight user selected filter      
    match = re.compile('<ul class="[ugc|r]+-list">(.+?)<div class="page.+?">').findall(link)
    match = re.compile('<li class="[ugc|r]+-item"(.+?)</li>').findall(match[0])

    totalItems = len(match)   
    li = xbmcgui.ListItem('[COLOR FFFF00FF]'+name+'[/COLOR]（第'+str(page)+'页）【[COLOR FFFFFF00]'+year+'[/COLOR]/[COLOR FF00FFFF]'+order+'[/COLOR]】（按此选择）')
    u = sys.argv[0]+"?mode="+mf+"&name="+urllib.quote_plus(name)+"&id="+id+"&cat="+cat+"&year="+year+"&order="+order
    xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, True, totalItems)
    
    playlist=xbmc.PlayList(0) # use Music playlist for temporary storage
    playlist.clear()
    for i in range(0, len(match)):
        match1 = re.compile('<a href="(.+?)"').findall(match[i])
        p_url = 'http://v.pps.tv'+match1[0]
        
        match1 = re.compile('<a href.+?title="(.+?)".*?>').findall(match[i])
        p_name = match1[0]

        match1 = re.compile('<span class="status">([:0-9]+)</span>').findall(match[i])      
        if match1: p_name += ' [COLOR FFFF00FF]['+match1[0]+'][/COLOR] '
        
        match1 = re.compile('<span class="nm">播放：</span>([0-9]+)<a.+?').findall(match[i])      
        if match1: p_name += ' [播放: '+match1[0]+']' #+' ('+p_url+')'  
          
        match1 = re.compile('<img src="(.+?)"').findall(match[i])
        p_thumb = match1[0]
        
        p_list = str(i+1)+'. '+p_name
            
        li = xbmcgui.ListItem(p_list, iconImage='', thumbnailImage=p_thumb)
        u = sys.argv[0]+"?mode=14&name="+urllib.quote_plus(p_list)+"&url="+urllib.quote_plus(p_url)+"&thumb="+urllib.quote_plus(p_thumb)
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, False, totalItems)
        playlist.add(p_url, li)

    # Fetch and build user selectable page number 
    matchp = re.compile('<div class="page.+?">(.+?)</div>').findall(link)
    if len(matchp): 
        matchp1 = re.compile('<a href=.+?class="pn".+?>([0-9]+)</span></a>').findall(matchp[0])
        if not matchp1:
            matchp1 = re.compile('<a.+?href=".+?">([0-9]+)</a>').findall(matchp[0])
        if len(matchp1):
            plist=[]
            for num in matchp1:
                if num not in plist:
                    plist.append(num)
                    li = xbmcgui.ListItem("... 第"+num+"页")
                    u = sys.argv[0]+"?mode=11&name="+urllib.quote_plus(name)+"&id="+id+"&cat="+cat+"&year="+year+"&order="+order+"&page="+str(num)
                    xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, True, totalItems) 

    xbmcplugin.setContent(int(sys.argv[1]), 'movies')
    xbmcplugin.endOfDirectory(int(sys.argv[1]))
    
##################################################################################
# Routine to update ugc list as per user selected filters
# - 发布时间 (Published date)
# - 排序方式 (Order)
##################################################################################
def updateListUgc(name, id, cat, year, order):
    #datelist, orderlist = getListUgc(listpage)
    change = False
    dialog = xbmcgui.Dialog()
    list = [x[1] for x in datelist]
    sel = dialog.select('发布时间:', list)
    if sel != -1:
        year = datelist[sel][1]
        change = True

    list = [x[1] for x in orderlist]
    sel = dialog.select('排序方式', list)
    if sel != -1:
        order = orderlist[sel][1]
        change = True

    if change:
        progListUgc(name, id, '1', cat, year, order)

##################################################################################
# Routine to update ugc list as per user selected filters
# - 发布时间 (Published date)
# - 排序方式 (Order)
##################################################################################
def updateListIpd(name, id, cat, year, order):
    #datelist, orderlist = getListUgc(listpage)
    change = False
    dialog = xbmcgui.Dialog()
    list = [x[1] for x in ISORT_DATE]
    sel = dialog.select('发布时间:', list)
    if sel != -1:
        year = ISORT_DATE[sel][1]
        change = True

    list = [x[1] for x in ISORT_ORDER]
    sel = dialog.select('排序方式', list)
    if sel != -1:
        order = ISORT_ORDER[sel][1]
        change = True

    if change:
        progListUgc(name, id, '1', cat, year, order)

##################################################################################
# Routine to fetch different playback options for the selected movie
# e.g. HD(高清), languages, related info etc
##################################################################################
def getMovie(name, url, thumb):
    #url = 'http://v.pps.tv'+id
    link = getHttpData(url)
    match0 = re.compile('<ul class="new-p-list10 p-list">(.+?)</ul>').findall(link)
    if len(match0):
        j=0
        li = xbmcgui.ListItem('[COLOR FF00FFFF]【当前视频：'+name+'】[/COLOR]', iconImage='', thumbnailImage=thumb)
        u = sys.argv[0]+"?mode=40&name="+urllib.quote_plus(name)
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li)
        for k in range (0, len(match0)):
            match = re.compile('<li class="p-item.+?>(.+?)</li>').findall(match0[k])
            for i in range(0, len(match)):
                match1 = re.compile('href="(.+?)"').findall(match[i])
                p_url = match1[0]
                if not re.search('http:',p_url):
                    p_url = 'http://v.pps.tv'+p_url
                    
                match1 = re.compile('title="(.+?)"').findall(match[i])
                p_list = p_name = match1[0]
                match1 = re.compile('class="status">([:0-9]+)</span>').findall(match[i])
                if match1: p_list+=' ['+match1[0]+']'
                j=j+1
                li = xbmcgui.ListItem(str(j)+". "+p_list)
                u = sys.argv[0]+"?mode=10&name="+urllib.quote_plus(name)+"&url="+urllib.quote_plus(p_url)
                xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, False)
        xbmcplugin.endOfDirectory(int(sys.argv[1]))   

##################################################################################
# Routine to play movide video file
# Player using ppstream player
# http://active.v.pps.tv/check_play_10UIFO.js
#    match = ['pps://hwqmupwqeb6oiief2aqh2lrid7ica.pps/8bcd8aa4e01c87164d99f315a7c5b5f11c848767.pfv']
##################################################################################
def PlayVideo(name, url):
    pps4xbmc_en = __addon__.getSetting('pps4xbmc_en')
    if (pps4xbmc_en == 'false' or os.name != 'nt'):   
        playVideoUgcX(name, url, 'None')    
        return
    
    link = getHttpData(url)
    match = re.compile('p2p_src.+?"(.*?)"').findall(link)
    # match= "pps://hwshzjoqednezs5t2aqh2lrzslica.pps/f98cfd0eee8fae402f874577a4b3dad27fb48bf2.pfv?maingen=内地剧场"

    if match[0]=='': # null - try second method to fetch pps video link
        matchp = re.compile('play_(.+?).html').findall(url)

#        method not working since 14/03/2013
#        p_url = 'http://active.v.pps.tv/check_play_'+matchp[0]+'.js' 
#        link = getHttpData(p_url)
#        match = re.compile('var src="(.*?)"').findall(link)

        # http://dp.ppstream.com/get_play_url_cdn.php?sid=31K53L&flash_type=1&region=%E6%96%B0%E5%8A%A0%E5%9D%A1&operator=%E6%9C%AA%E7%9F%A5
        # link = 'http://vurl.ppstv.com/ugc/b/78/b10ceb16db9af51664f70ce29a7afae482677f6f/b10ceb16db9af51664f70ce29a7afae482677f6f.pfv?hd=0&all=0&title=新妓生传国语版-01&vtypeid=1&fd=1&ct=2869&sha=b10ceb16db9af51664f70ce29a7afae482677f6f&fid=UMJ4L7DL5DBVZQDWPYMJ6NDOK5HYZCXA&bip=http://bip.ppstream.com/U/UM/UMJ4L7DL5DBVZQDWPYMJ6NDOK5HYZCXA/UMJ4L7DL5DBVZQDWPYMJ6NDOK5HYZCXA.bip&sbest=vurl.pps.tv&tip=0&tracker=118.194.167.14,118.194.167.12'
        p_url = 'http://dp.ppstream.com/get_play_url_cdn.php?sid='+matchp[0]+'&flash_type=1&type=0'
        link = getHttpData(p_url)
        match = re.compile('(.+?)\?hd=').findall(link)
        #if match: match[0]=match[0].decode("gbk").encode("utf8")

    if match:
        v_url = match[0]
        if v_url == '':  # pps link not found, try ugc playback 
            playVideoUgcX(name, url, 'None')
        else:
            print "videolink: " + v_url
            xbmc.executebuiltin('System.ExecWait(\\"'+__cwd__+'\\resources\\player\\pps4xbmc\\" '+v_url+')')
    else: # exhausted all attempts
        dialog = xbmcgui.Dialog()
        ok = dialog.ok(__addonname__,'您当前观看的视频暂不能播放，请选择其它节目')
          
##################################################################################
# Routine to play ugc embedded swf video file
# fetch the swf file directly using one of the hardcoded link below
# http://dp.ppstream.com/get_play_url_cdn.php?sid=30NG77&flash_type=1&type=0&region=%E6%96%B0%E5%8A%A0%E5%9D%A1&operator=%E6%9C%AA%E7%9F%A5
# http://dp.ppstv.com/get_play_url_rate.php?sid=30NG77&flash_type=1&type=0
# http://dp.ppstream.com/get_play_url_rate.php?sid=30NG77&flash_type=1&type=0
# http://dp.ugc.pps.tv/get_play_url_rate.php?sid=30NG77&flash_type=1&type=0
##################################################################################
def playVideoUgc(name, url, thumb):
    videoplaycont = __addon__.getSetting('video_vplaycont')
    
    playlistA=xbmc.PlayList(0)
    playlist=xbmc.PlayList(1)
    playlist.clear()

    v_pos = int(name.split('.')[0])-1
    psize = playlistA.size()
    k=0
    
    for x in range(psize):
        if x < v_pos: continue
        p_item=playlistA.__getitem__(x)
        p_url=p_item.getfilename(x)
        p_list =p_item.getdescription(x)

        #li = xbmcgui.ListItem(p_list, iconImage = '', thumbnailImage = thumb)
        li = xbmcgui.ListItem(p_list)
        li.setInfo(type = "Video", infoLabels = {"Title":p_list})
    
        match = re.compile('play_(.+?).html').findall(p_url)
        if len(match):
             #videolink = 'http://dp.ppstv.com/get_play_url_rate.php?sid='+match[0]+'&flash_type=1&type=0'
             videolink = 'http://dp.ppstream.com/get_play_url_cdn.php?sid='+match[0]+'&flash_type=1&type=0'
             for i in range(10): # Retry specified trials before giving up (seen 9 trials max)
                try: # stop xbmc from throwing error to prematurely terminate video search
                    link = getHttpData(videolink)
                    v_url = re.compile('(.+?)\?hd=').findall(link)
                    if len(v_url):
                        v_url = v_url[0] 
                        break                        
                except:
                    pass                     
        else:
            v_url = p_url
 
        playlist.add(v_url, li, k)
        k +=1 
        if k == 1:
            xbmc.Player(1).play(playlist)
        if videoplaycont == 'false': break   

##################################################################################
# Routine to play ugc embedded swf video file
# fetch the swf file directly using one of the hardcoded link below
# http://dp.ppstream.com/get_play_url_cdn.php?sid=30NG77&flash_type=1&type=0&region=%E6%96%B0%E5%8A%A0%E5%9D%A1&operator=%E6%9C%AA%E7%9F%A5
# http://dp.ppstv.com/get_play_url_rate.php?sid=30NG77&flash_type=1&type=0
# http://dp.ppstream.com/get_play_url_rate.php?sid=30NG77&flash_type=1&type=0
# http://dp.ugc.pps.tv/get_play_url_rate.php?sid=30NG77&flash_type=1&type=0
##################################################################################
def playVideoUgcX(name, url, thumb): 
    match = re.compile('play_(.+?).html').findall(url)
    #videolink = 'http://dp.ppstv.com/get_play_url_rate.php?sid='+match[0]+'&flash_type=1&type=0'
    videolink = 'http://dp.ppstream.com/get_play_url_cdn.php?sid='+match[0]+'&flash_type=1&type=0'
    link = getHttpData(videolink)   
    if (link):
        match = re.compile('(.+?)\?hd=').findall(link)
        playlist=xbmc.PlayList(1)
        playlist.clear()
        listitem = xbmcgui.ListItem(name, thumbnailImage = thumb)
        listitem.setInfo(type="Video",infoLabels={"Title":name})
        playlist.add(match[0], listitem)
        xbmc.Player().play(playlist)       
    else:
        dialog = xbmcgui.Dialog()
        ok = dialog.ok(__addonname__,'您当前观看的视频暂不能播放，请选择其它节目')        
            
##################################################################################
# Get user input for PPS site search
        #keyword = "恋爱季节"
        #keyword = "我们约会吧" 
        #keyword = "风声传奇"
##################################################################################
def searchPPS():
    result=''
    keyboard = ChineseKeyboard.Keyboard('','请输入搜索内容')
#    keyboard = xbmc.Keyboard('','请输入搜索内容')
    xbmc.sleep( 1500 )
    keyboard.doModal()
    if (keyboard.isConfirmed()):
        keyword = keyboard.getText()

        keyword = "恋爱季节"
        url='http://so.pps.tv/search?k='+urllib.quote(keyword)+'&from=1'
        ppsSearchList(keyword,url,'1')
    else: return
        
##################################################################################
# Routine to search PPS site based on user given keyword for:
# a. video episode List for each found provider
# b. movie from each found provider
# c. ugc for each found provider
##################################################################################
def ppsSearchList(name, url, page): 
    p_url = url+'&page='+str(page)
    link = getHttpData(p_url)
    li = xbmcgui.ListItem('[COLOR FFFF0000]当前搜索: 第'+str(page)+'页[/COLOR][COLOR FFFFFF00] ('+name+')[/COLOR]【[COLOR FF00FF00]'+'请输入新搜索内容'+'[/COLOR]】')
    u = sys.argv[0]+"?mode=31&name="+urllib.quote_plus(name)+"&url="+urllib.quote_plus(url)+"&page="+urllib.quote_plus(page)
    xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, True)
    
    n = 0
    #############################################################
    # Episode Listing for each found related episode title
    #############################################################
    match = re.compile('<!--rp-tv rp-item-->(.+?)<!--/rp-tv rp-item-->').findall(link)
    if match:
        match_ep = re.compile('<div class="rp-tv rp rp-item">(.+?)<!--/drama-set-->').findall(link)
        if len(match_ep):
            for k in range(0, len(match_ep)):
                match1 = re.compile('<h2.+?><a href="(.+?)" target="_blank"><span>(.+?)</span></a>').findall(match_ep[k])
                #p_url = match1[0][0]
                p_list = p_name = match1[0][1]
                    
                match1 = re.compile('<img src="(.+?)"').findall(match_ep[k])
                p_thumb = match1[0]
                
                # Construct an array for the found episode listing for fast response - sub menu
                match_ep1 = re.compile('<li class="dc-item"><a href="(.+?)".+?><span class="s">(.+?)</span></a>').findall(match_ep[k])
                if len(match_ep1):
                    p_url = match_ep1[0][1] + ': ' + match_ep1[0][0]
                    for k in range(1, len(match_ep1)):
                        p_url += ',' + match_ep1[k][1] + ': ' + match_ep1[k][0]
                
#                match1 = re.compile('class="status">([:0-9]+)</span>').findall(match_ep[k])
#                if match1: p_list+=' ['+match1[0]+']'
                n += 1
                p_list = str(n)+". [COLOR FF00FF00]电视剧:[/COLOR] "+p_name
                li = xbmcgui.ListItem(p_list, iconImage='', thumbnailImage=p_thumb)
                u = sys.argv[0]+"?mode=33&name="+urllib.quote_plus(p_name)+"&url="+urllib.quote_plus(p_url)
                xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, True)

    #############################################################
    # Moive Listing for each found related movie title
    #############################################################
    match = re.compile('<!--rp-movie rp-item-->(.+?)<!--/rp-ipd rp-item-->').findall(link)
    if match:
        match_mv = re.compile('<div class="rp-movie rp rp-item">(.+?)</ul>').findall(link)
        if len(match_mv):
            for k in range(0, len(match_mv)):
                match1 = re.compile('<h2.+?><a href="(.+?)" target="_blank"><span>(.+?)</span></a>').findall(match_mv[k])
                p_url = match1[0][0]
                p_list = p_name = match1[0][1]
                    
                match1 = re.compile('<img src="(.+?)"').findall(match_mv[k])
                p_thumb = match1[0]
                
#                match1 = re.compile('class="status">([:0-9]+)</span>').findall(match_mv[k])
#                if match1: p_list+=' ['+match1[0]+']'

                n += 1
                p_list = str(n)+". [COLOR FF00FFFF]电影:[/COLOR] "+p_name
                li = xbmcgui.ListItem(p_list, iconImage='', thumbnailImage=p_thumb)
                u = sys.argv[0]+"?mode=10&name="+urllib.quote_plus(p_name)+"&url="+urllib.quote_plus(p_url)
                xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, False)
  
    #############################################################
    # ugc-list for related title unpack
    #############################################################
    #matchp = re.compile('<ul class="ugc-list">(.+?)<div class="pagenav2">').findall(link)
    matchp = re.compile('<ul class="p-list.+?">(.+?)<div class="page-nav">').findall(link)
    if len(matchp):
        # Fetch & build ugc list for user selection, highlight user selected filter      
        match = re.compile('<li class="p-item">(.+?)</li>').findall(matchp[0])
        if len(match):
            n += 1
            totalItems = len(match)

            for i in range(0, len(match)):      
                match1 = re.compile('<div class="t"><a href="(.+?)" target="_blank">(.+?)</a>').findall(match[i])
                p_url = match1[0][0]
                p_name = p_list = match1[0][1]

                match1 = re.compile('<span class="status">([:0-9]+)</span>').findall(match[i])      
                if match1: p_list += ' [COLOR FFFF00FF]['+match1[0]+'][/COLOR] '

                match1 = re.compile('<span class="nm">播放：</span>([0-9]+)<a class=').findall(match[i])      
                if match1: p_list += ' [播放: '+match1[0]+']'
          
                match1 = re.compile('<img lazy_src=.+?src="(.+?)"').findall(match[i])
                p_thumb = match1[0]
        
                li = xbmcgui.ListItem(str(n+i)+". "+p_list, iconImage="", thumbnailImage=p_thumb)
                u = sys.argv[0]+"?mode=15&name="+urllib.quote_plus(p_name)+"&url="+urllib.quote_plus(p_url)+"&thumb="+urllib.quote_plus(p_thumb)
                xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, False, totalItems)

    if n==0:
        dialog = xbmcgui.Dialog()
        ok = dialog.ok(__addonname__, '抱歉，未能找到与 "'+name+'" 相关的视频')

    else:  
        # Fetch and build user selectable page number 
        matchp = re.compile('<div class="page-nav">(.+?)</div>').findall(link)
        if len(matchp): 
            matchp1 = re.compile('<a.+?href=.+?><span class="sp">([0-9]+)</span></a>').findall(matchp[0])       
            if len(matchp1):
                plist=[]
                for num in matchp1:
                    if num not in plist:
                        plist.append(num)
                        li = xbmcgui.ListItem("... 第"+num+"页")
                        u = sys.argv[0]+"?mode=32&name="+urllib.quote_plus(name)+"&url="+urllib.quote_plus(url)+"&page="+urllib.quote_plus(str(num))
                        xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, True) 
        xbmcplugin.setContent(int(sys.argv[1]), 'movies')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
        # xbmc.executebuiltin('Container.Refresh')

##################################################################################
# Routine to display episode listing
##################################################################################
def episodeList(name, url):
 # url is a list of url for each episode
    li = xbmcgui.ListItem('[COLOR FFFF00FF]'+name+'[/COLOR]')
    u = sys.argv[0]+"?mode=33"+"&name="+urllib.quote_plus(name)+"&url="+urllib.quote_plus(url)
    xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, True)

    url_list = url.split(",")
    for i in range(0, len(url_list)): 
        p_url = url_list[i].split(": ")[1]
        p_name = url_list[i].split(": ")[0] + ': ' + name 
        li = xbmcgui.ListItem(p_name)
        u = sys.argv[0]+"?mode=10&name="+urllib.quote_plus(p_name)+"&url="+urllib.quote_plus(p_url)
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, False)
    xbmcplugin.setContent(int(sys.argv[1]), 'episodes')
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

##################################################################################
# Routine to search PPS site based on user given keyword for:
# a. video episode List for each found provider
# b. movie from each found provider
# c. ugc for each found provider
##################################################################################
def ppsSearchListx(name, url, page): 
    p_url = url+'&page='+str(page)
    link = getHttpData(p_url)
    li = xbmcgui.ListItem('[COLOR FFFF0000]当前搜索: 第'+str(page)+'页[/COLOR][COLOR FFFFFF00] ('+name+')[/COLOR]【[COLOR FF00FF00]'+'请输入新搜索内容'+'[/COLOR]】')
    u = sys.argv[0]+"?mode=31&name="+urllib.quote_plus(name)+"&url="+urllib.quote_plus(url)+"&page="+urllib.quote_plus(page)
    xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, True)
    
    #########################################################################
    # Video Episode/Movie listing for each found related episode title
    #########################################################################
    n = 0
    match_ml = re.compile('<li class="sr-item"(.+?)<div class="sr-cell">').findall(link)
    if len(match_ml):
        for x in range(0, len(match_ml)): 
            # Find the episode title & its list of the provider sites 
            match_t = re.compile('<em class="keyword">(.+?)</em>').findall(match_ml[x])
            keyword = match_t[0]

            ## matchp = re.compile('<div class="mv-play-drop">(.+?)</div>').findall(match_ml[x])
            match1 = re.compile('class="drop-trigger v-offer v-pps">(.+?)<em>').findall(match_ml[x])
            if match1==None: continue # Proceed only if provider sites found
            # Extract each provider and its episode list
            match_ep = re.compile('<ul class="mv-episode [_site1|_expand_site1].+?>(.+?)</ul').findall(match_ml[x])
            # Fetch & build the episode list for each site provider 
            for j in range(0, len(match1)): 
#                 p_name = match1[j][1] + " - " + keyword
                 p_name = match1[0] + " - " + keyword
                 epSite = "_site"+match1[j][0]
                 
                 #############################################################
                 # Episode Listing for each found related episode title
                 #############################################################
                 if match_ep:
                     # Combine all the episode listing groups based on given site provider
                     epList = ""
                     for k in range(0, len(match_ep)):
                         #if re.search(epSite, match_ep[k]): (22/02/2013 - only pps available)
                             epList += match_ep[k]

                     # Construct an array for the found episode listing for fast response - sub menu
                     match_ep1 = re.compile('<li class="epis-item.+?href="(.+?)".+?>([0-9]+)</a>').findall(epList)
                     if len(match_ep1):
                         p_list = match_ep1[0][1] + ': ' + match_ep1[0][0]
                         for k in range(1, len(match_ep1)):
                             p_list += ',' + match_ep1[k][1] + ': ' + match_ep1[k][0]

                         n += 1
                         li = xbmcgui.ListItem(str(n)+". 电视剧: "+p_name)
                         u = sys.argv[0]+"?mode=33&name="+urllib.quote_plus(p_name)+"&url="+urllib.quote_plus(p_list)
                         xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, True)

                 #############################################################
                 # Moive Listing for each found related movie title
                 #############################################################
                     else:       
#                     match_mp = re.compile('<ul class=".+?new-mv-episode(.+?)</ul').findall(match_ml[x])
#                     print 'match_mp', match_mp
#                     # Find the direct playback video link for the site provider
#                     for k in range(0, len(match_mp)):
#                         if re.search(epSite, match_mp[k])== None: continue
#                         match_mp1 = re.compile('<a href="(.+?)">').findall(match_mp[k])
                         match_mp1 = re.compile('<div class="mv-play-only"><a href="(.+?)"').findall(match_ml[x])
                         p_url = match_mp1[0]
                         n += 1
 
#                         mode = fetchID(MPLAYER_LIST,match1[j][1])
                         mode = fetchID(MPLAYER_LIST,match1[0])
                         #print 'mode', match1[0], mode
                         if mode=='': mode = '99' # player not implemented

                         li = xbmcgui.ListItem(str(n)+". 电影: "+p_name)
                         u = sys.argv[0]+"?mode="+mode+"&name="+urllib.quote_plus(p_name)+"&url="+urllib.quote_plus(p_url)
                         xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, False)
 
    #############################################################
    # ugc-list for related title unpack
    #############################################################
    n += 1
    matchp = re.compile('<ul class="ugc-list">(.+?)<div class="pagenav2">').findall(link)
    if len(matchp) == 0: return
    
    # Fetch & build ugc list for user selection, highlight user selected filter      
    match = re.compile('<li class="ugc-item">(.+?)</ul>').findall(matchp[0])
    if len(match) == 0: return
    totalItems = len(match)

    for i in range(0, len(match)):      
        match1 = re.compile('<div class="t"><a href="(.+?)" target="_blank">(.+?)</a>').findall(match[i])
        p_url = match1[0][0]
        p_name = p_list = match1[0][1]

        match1 = re.compile('<span class="status">([:0-9]+)</span>').findall(match[i])      
        if match1: p_list += ' ['+match1[0]+'] '

        match1 = re.compile('<span class="nm">播放：</span>([0-9]+)<a class=').findall(match[i])      
        if match1: p_list += ' [播放: '+match1[0]+']'
          
        match1 = re.compile('<img src=.+?lazy_src="(.+?)" class="imgm"').findall(match[i])
        p_thumb = match1[0]
        
        li = xbmcgui.ListItem(str(n+i)+". "+p_list, iconImage="", thumbnailImage=p_thumb)
        u = sys.argv[0]+"?mode=15&name="+urllib.quote_plus(p_name)+"&url="+urllib.quote_plus(p_url)+"&thumb="+urllib.quote_plus(p_thumb)
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, False, totalItems)
            
    # Fetch and build user selectable page number 
    matchp = re.compile('<div class="pagenav2">(.+?)</div>').findall(link)
    if len(matchp): 
        matchp1 = re.compile('<a.+?href=".+?">([0-9]+)</a>').findall(matchp[0])       
        if len(matchp1):
            plist=[]
            for num in matchp1:
                if num not in plist:
                    plist.append(num)
                    li = xbmcgui.ListItem("... 第"+num+"页")
                    u = sys.argv[0]+"?mode=32&name="+urllib.quote_plus(name)+"&url="+urllib.quote_plus(url)+"&page="+urllib.quote_plus(str(num))
                    xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, True) 
    xbmcplugin.setContent(int(sys.argv[1]), 'movies')
    xbmcplugin.endOfDirectory(int(sys.argv[1]))
    # xbmc.executebuiltin('Container.Refresh')

##################################################################################
# Routine to display episode listing
##################################################################################
def episodeListx(name, url):
 # url is a list of url for each episode
    
    li = xbmcgui.ListItem('[COLOR FFFF00FF]'+name+'[/COLOR]')
    u = sys.argv[0]+"?mode=33"+"&name="+urllib.quote_plus(name)+"&url="+urllib.quote_plus(url)
    xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, True)

    site = name.split(" - ")[0]
    mode = fetchID(MPLAYER_LIST,site)
    if mode=='': mode = '99' # player not implemented
    t_name = name.split(" - ")[1]
    
    url_list = url.split(",")
    for i in range(0, len(url_list)): 
        p_url = url_list[i].split(" ")[1]
#        p_name = name+": 第"+str(i+1)+"集"
        p_name = url_list[i].split(" ")[0] + ' ' + t_name 
        li = xbmcgui.ListItem(p_name)
        u = sys.argv[0]+"?mode="+ mode +"&name="+urllib.quote_plus(p_name)+"&url="+urllib.quote_plus(p_url)
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, False)
    xbmcplugin.setContent(int(sys.argv[1]), 'episodes')
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

##################################################################################
# Youku Video Player
##################################################################################
def PlayVideoYouku(name, url):
    link = getHttpData("http://www.flvcd.com/parse.php?kw="+url+"&format=high")
    match = re.compile('"(http://f.youku.com/player/getFlvPath/.+?)" target="_blank"').findall(link)
    if len(match)>0:
        playlist=xbmc.PlayList(1)
        playlist.clear()
        for i in range(0,len(match)):
            p_name = name+" 第"+str(i+1)+"节"
            listitem = xbmcgui.ListItem(p_name, thumbnailImage = __addonicon__)
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

##################################################################################
# Todou Video Player
##################################################################################
def PlayVideoTudou(name,url):
    thumb=""
    #http://www.tudou.com/programs/view/WCtPhTFE5Os/
    match = re.compile('http://www.tudou.com/playlist/p/a[0-9]+i([0-9]+).html').findall(url)
    url = 'http://v2.tudou.com/v?it='+match[0]
    link = getHttpData(url)
    match = re.compile('(http://.+?)</f>').findall(link)
    if match:
        listitem = xbmcgui.ListItem(name, thumbnailImage = thumb)
        #listitem.setInfo(type = "Video", infoLabels = {"Title":name, "Director":director, "Plot":plot, "Year":int(year)})
        xbmc.Player().play(match[0]+'|User-Agent='+UserAgent, listitem)
    else:
        dialog = xbmcgui.Dialog()
        ok = dialog.ok(__addonname__, '抱歉! 由于版权原因, 非大陆地区 - 节目暂时不提供观看')

##################################################################################
# Qiyi Video Player
##################################################################################
def PlayVideoQiyi(name,url):
    if url.find('http://cache.video.qiyi.com/v/') == -1:
        link = getHttpData(url)
        url = getPlayURL(link)
    link = getHttpData(url)
    thumb=""
    match=re.compile('<file>http://data.video.qiyi.com/videos/([^/]+?)/(.+?)</file>').findall(link)
    playlist=xbmc.PlayList(1)
    playlist.clear()
    if urlExists('http://qiyi.soooner.com/videos2/'+match[0][0]+'/'+match[0][1]):
        baseurl = 'http://qiyi.soooner.com/videos2/'
    else:
        baseurl = 'http://qiyi.soooner.com/videos/'
    for i in range(0,len(match)):
        p_name = name+" 第"+str(i+1)+"节"
        listitem=xbmcgui.ListItem(p_name, thumbnailImage = thumb)
        listitem.setInfo(type="Video",infoLabels={"Title":name+" 第"+str(i+1)+"/"+str(len(match))+" 节"})
        playlist.add(baseurl+match[i][0]+'/'+match[i][1], listitem = listitem)
    xbmc.Player().play(playlist)

##################################################################################
# Qiyi Video Player support functions
##################################################################################
def getPlayURL(html):
    match1 = re.compile('pid : "(.+?)",//').findall(html)
    if len(match1) > 0:
        pid = match1[0]
        match1 = re.compile('ptype : "(.+?)",//').findall(html)
        ptype = match1[0]
        match1 = re.compile('videoId : "(.+?)",//').findall(html)
        videoId = match1[0]
        url = 'http://cache.video.qiyi.com/v/'+videoId+'/'+pid+'/'+ptype+'/'
    else:
        url = ''
    return url

def urlExists(url):
    try:
        resp = urllib2.urlopen(url)
        result = True
        resp.close()
    except urllib2.URLError, e:
        result = False
    return result

##################################################################################
# Sohu Video Player
##################################################################################
def PlayVideoSohu(name,url):
    thumb=""   
    link = getHttpData(url)
    match1 = re.compile('var vid="(.+?)";').search(link)
    if not match1:
        match1 = re.compile('<a href="(http://[^/]+/[0-9]+/[^\.]+.shtml)" target="?_blank"?><img').search(link)
        if match1:
            PlayVideoSohu(name,match1.group(1),thumb)
        return
    p_vid = match1.group(1)
    if p_vid.find(',') > 0 : p_vid = p_vid.split(',')[0]

    ### Fetch video resolution supported for user selection
    link = getHttpData('http://hot.vrs.sohu.com/vrs_flash.action?vid='+p_vid)
    match = re.compile('"norVid":(.+?),"highVid":(.+?),"superVid":(.+?),').search(link)
    if not match:
       dialog = xbmcgui.Dialog()
       ok = dialog.ok(__addonname__,'您当前选择的节目暂不能播放，请选择其它节目')   
       return
    ratelist=[]
    if match.group(3)!='0':ratelist.append(['超清','3'])
    if match.group(2)!='0':ratelist.append(['高清','2'])
    if match.group(1)!='0':ratelist.append(['流畅','1'])

    dialog = xbmcgui.Dialog()
    list = [x[0] for x in ratelist]
    if len(ratelist)==1:
        rate=ratelist[0][1]
    else:
        sel = dialog.select('视频率 (请选择低视频-流畅如网络缓慢)', list)
        if sel == -1:
            return
        else:
            rate=ratelist[sel][1]
    
    if match.group(int(rate))<>str(p_vid):
        link = getHttpData('http://hot.vrs.sohu.com/vrs_flash.action?vid='+match.group(int(rate)))
    match = re.compile('"tvName":"(.+?)"').findall(link)
    if not match:
       res = ratelist[3-int(rate)][0]
       dialog = xbmcgui.Dialog()
       ok = dialog.ok(__addonname__,'您当前选择的视频: ['+ res +'] 暂不能播放，请选择其它视频')       
       return
    name = match[0]
    match = re.compile('"clipsURL"\:\["(.+?)"\]').findall(link)
    paths = match[0].split('","')
    match = re.compile('"su"\:\["(.+?)"\]').findall(link)
    newpaths = match[0].split('","')
    playlist = xbmc.PlayList(1)
    playlist.clear()
    for i in range(0,len(paths)):
        p_url = 'http://data.vod.itc.cn/?prot=2&file='+paths[i].replace('http://data.vod.itc.cn','')+'&new='+newpaths[i]
        link = getHttpData(p_url)
        key=link.split('|')[3]
        url=link.split('|')[0].rstrip("/")+newpaths[i]+'?key='+key
        title = name+" 第"+str(i+1)+"/"+str(len(paths))+"节"
        listitem=xbmcgui.ListItem(title,thumbnailImage=thumb)
        listitem.setInfo(type="Video",infoLabels={"Title":title})
        playlist.add(url, listitem)
    # start play only after all video queue is completed. otherwise has problem on slow network
    xbmc.Player().play(playlist)

##################################################################################
# Sina Video Player
##################################################################################
def PlayVideoSina(name,url):
    link = getHttpData(url)
    match = re.compile(' vid:\'(.+?)\',').findall(link)   
    vid=match[0]
    vidlist=vid.split('|')
    #vidlist[0]=普通; vidlist[1]=清晰
    url='http://v.iask.com/v_play.php?vid='+vidlist[1]+'&uid=0&pid=1000&tid=4&plid=4002&referrer=http%3A%2F%2Fvideo.sina.com.cn%2Fmovie%2Fdetail%2Fmhls&r=video.sina.com.cn'
    link = getHttpData(url)
    match = re.compile('<url><!\[CDATA\[(.+?)\]\]></url>').findall(link)
    if match:
        playlist=xbmc.PlayList(1)
        playlist.clear()
        for i in range(len(match)):
            p_name = name+" 第"+str(i+1)+"节"
            listitem = xbmcgui.ListItem(p_name, thumbnailImage = __addonicon__)
            listitem.setInfo(type="Video",infoLabels={"Title":name+" 第"+str(i+1)+"/"+str(len(match))+" 节"})
            playlist.add(match[i], listitem)
        xbmc.Player().play(playlist)
    else:
        dialog = xbmcgui.Dialog()
        ok = dialog.ok(__addonname__, '无法播放：未匹配到视频文件，请稍侯再试')

##################################################################################
# LeTV Video Link Decode Algorithm & Player
# Extract all the video list and start playing first found valid link
# User may press <SPACE> bar to select video resolution for playback
##################################################################################
def PlayVideoLetv(name,url):
    VIDEO_CODE=[['bHY=','bHY/'],['dg==','dj9i'],['dg==','dTgm'],['Zmx2','Zmx2']]
    link = getHttpData(url)

    match = re.compile('{v:(.+?),p:""}').findall(link)
    # link[0]:"标清-SD" ; link[1]:"高清-HD"
    if match:
        matchv = re.compile('"(.+?)"').findall(match[0])
        if matchv:
            playlist=xbmc.PlayList(1)
            playlist.clear()
            # Play HD and fallback to SD if HD failed
            vlist = reversed(range(len(matchv)))
            for j in vlist:
                if matchv[j] == "": continue
                #algorithm to generate the video link code
                vidx = matchv[j].find('MT')
                vidx = -1 # force to start at 24
                if vidx < 0:
                    vid = matchv[j][24:]  # extract max VID code length
                else:
                    vid = matchv[j][vidx:]
                for k in range(0, len(VIDEO_CODE)):
                    vidcode = re.split(VIDEO_CODE[k][1], vid)
                    if len(vidcode) > 1 :                 
                        vid = vidcode[0]+VIDEO_CODE[k][0]
                        break
                url = 'http://g3.letv.cn/vod/v1/'+vid+'?format=1&b=388&expect=3&host=www_letv_com&tag=letv&sign=free'
                link = getHttpData(url)
                link = link.replace("\/", "/")
                match = re.compile('{.+?"location": "(.+?)" }').findall(link)
                if match:
                    for i in range(len(match)):
                        p_name = name +' ['+ VIDEO_RES[j][0] +']' 
                        listitem = xbmcgui.ListItem(p_name, thumbnailImage = __addonicon__)
                        listitem.setInfo(type="Video",infoLabels={"Title":p_name})
                        playlist.add(match[i], listitem)
                        break # skip the rest if any (1 of 3) video links access successful
                else:
                    dialog = xbmcgui.Dialog()
                    ok = dialog.ok(__addonname__, '无法播放：未匹配到视频文件，请选择其它视频')  
            xbmc.Player().play(playlist)
        else:
            dialog = xbmcgui.Dialog()
            ok = dialog.ok(__addonname__, '无法播放：需收费，请选择其它视频')  
    else:
        dialog = xbmcgui.Dialog()
        match = re.compile('<dd class="ddBtn1">.+?title="(.+?)" class="btn01">').findall(link)
        if match and match[0] == "点播购买":
            ok = dialog.ok(__addonname__, '无法播放：需收费，请选择其它视频')
        else:
            ok = dialog.ok(__addonname__, '无法播放：未匹配到视频文件，请选择其它视频')    

##################################################################################
# Unimplmented video player message display
##################################################################################    
def searchUndefined(name,url):
    dialog = xbmcgui.Dialog()
    ok = dialog.ok(__addonname__,'抱歉! 此视频播放还未推出\nSorry! Video player not implemented.')             

##################################################################################
# Routine to fetch video info only (no implemented), no video for playback.
##################################################################################    
def getInfo(name, id, thumb):
    dialog = xbmcgui.Dialog()
    ok = dialog.ok(__addonname__,'您当前观看的视频暂不能播放，请选择其它节目')             
                              
##################################################################################
# Routine to extra parameters from xbmc
##################################################################################
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
listpage = None
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
    listpage = urllib.unquote_plus(params["listpage"])
except:
    pass
try:
    mode = int(params["mode"])
except:
    pass

if mode == None:
    mainMenu()
elif mode == 1:
    progListMovie(name, id, page, cat, area, year, order, listpage)
elif mode == 2:
    getMovie(name, url, thumb)
elif mode == 3:
    progListSeries(name, url, thumb, page)
elif mode == 4:
    updateListMovie(name, id, page, cat, area, year, order, listpage)
elif mode == 6:
    updateListSeries(name, url, thumb, listpage)
elif mode == 10:
    PlayVideo(name, url)
    
elif mode == 11:
    progListUgc(name, id, page, cat, year, order)
elif mode == 12:
    updateListUgc(name, id, cat, year, order) 
elif mode == 13:
    updateListIpd(name, id, cat, year, order) 
elif mode == 14:
    playVideoUgc(name, url, thumb)    
elif mode == 15:
    playVideoUgcX(name, url, thumb)    
elif mode == 16:
    playVideoIpd(name, url, thumb)    
    
elif mode == 21:
    getInfo(name, id, thumb)

elif mode == 31:
    searchPPS()
elif mode == 32:
    ppsSearchList(name, url, page)
elif mode == 33:
    episodeList(name,url)

elif mode == 42:
    PlayVideoSmgbb(name,url)
elif mode == 43:
    PlayVideoYouku(name,url)
elif mode == 44:
    PlayVideoTudou(name,url)
elif mode == 45:
    PlayVideoQiyi(name,url)
elif mode == 46:
    PlayVideoSohu(name,url)
elif mode == 47:
    PlayVideoSina(name,url)
elif mode == 48:
    PlayVideoLetv(name,url)

elif mode == 99:
    searchUndefined(name, url)
       