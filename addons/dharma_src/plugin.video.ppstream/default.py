# -*- coding: utf-8 -*-
import xbmc, xbmcgui, xbmcplugin, xbmcaddon, urllib2, urllib, re, string, sys, os, gzip, StringIO
import ChineseKeyboard

########################################################################
# PPStream 网络电视 by robintttt/cmeng
# Version 2.0.8 2012-03-31 (cmeng)
# a. To take care main web page <tag> structure change 

# See changelog.txt for previous history
########################################################################

# Plugin constants 
__addonname__     = "PPS 网络电视"
__addonid__       = "plugin.video.ppstream"
__settings__      = xbmcaddon.Addon(id=__addonid__)
__cwd__           = xbmc.translatePath( __settings__.getAddonInfo('path') )
__addon__ = xbmcaddon.Addon(id=__addonid__)
__addonicon__ = os.path.join( __addon__.getAddonInfo('path'), 'icon.png' )

UserAgent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'
VIDEO_LIST = [['tv','电视剧'],['movie','电影'],['fun','综艺'],['anime','动漫']]
SORT_LIST = [['sum_online_sum','按观众数'],['vote_num','按评分']]
COLOR_LIST = ['[COLOR FFFF0000]','[COLOR FF00FF00]','[COLOR FFFFFF00]','[COLOR FF00FFFF]','[COLOR FFFF00FF]']
MPLAYER_LIST = [['10','PPS'],['99','SMG'],['43','优酷'],['44','土豆'],['45','奇艺'],['46','搜狐'],['47','新浪'],['48','乐视']]
     
##################################################################################
# Routine to fetech url site data using Mozilla browser
# - deletc '\r|\n|\t' for easy re.compile
# - do not delete ' ' i.e. <space> as some url include spaces
# - unicode with 'replace' option to avoid exception on some url
# - translate to utf8
##################################################################################
def getHttpData(url):
    print "getHttpData: " + url
    req = urllib2.Request(url)
    req.add_header('User-Agent', UserAgent)
    response = urllib2.urlopen(req)
    httpdata = response.read()
    response.close()
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
# 
##################################################################################
def getList(listpage):
    match0 = re.compile('<dt>按类型</dt>(.+?)</ul>', re.DOTALL).search(listpage)
    catlist = re.compile('<li><a href="/.+?/.+?/(.+?),.+?title="(.+?)">.+?</a></li>').findall(match0.group(1))
    match0 = re.compile('<dt>按国家/地区</dt>(.+?)</ul>', re.DOTALL).search(listpage)
    arealist = re.compile('<li><a href="/.+?/.+?/(.+?),.+?title="(.+?)">.+?</a></li>').findall(match0.group(1))
    match0 = re.compile('<dt>按年份</dt>(.+?)</ul>', re.DOTALL).search(listpage)
    yearlist = re.compile('<a href="/.+?/.+?/(.+?),.+?title="(.+?)">.+?</a></li>').findall(match0.group(1))

# tuple to list conversion not necessary    
#    catlist = [[x[0],x[1]] for x in catlist]
#    arealist = [[x[0],x[1]] for x in arealist]
#    yearlist = [[x[0],x[1]] for x in yearlist]
    return catlist, arealist, yearlist

##################################################################################
# Routine to fetch and build ugc filter list
# - 发布时间 (Published date)
# - 排序方式 (Order)
##################################################################################
def getListUgc(listpage):
    match0 = re.compile('<div class="sort2">发布时间:(.+?)</div>').search(listpage)
    datelist = re.compile('href="/ugc/.+?-t([0-9]+)-.+?">[ ]*(.+?)[ ]*</a>').findall(match0.group(1))
    match0 = re.compile('<div class="sort2">排序方式:(.+?)</div>').search(listpage)
    orderlist = re.compile('href="/ugc/.+?-o([0-9]+)-.+?">[ ]*(.+?)[ ]*</a>').findall(match0.group(1))
    return datelist, orderlist

##################################################################################
# Routine to fetch & build PPS 网络电视 main menu
# - video list as per [VIDEO_LIST]
# - ugc list
# - movie, series & ugc require different sub-menu access methods
##################################################################################
def mainMenu():
    li = xbmcgui.ListItem('[COLOR FFFF0000]PPS 网络电视:[/COLOR][COLOR FF00FF00]【请输入搜索内容】[/COLOR]')
    u=sys.argv[0]+"?mode=31"
    xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, True)
    
    link = getHttpData('http://v.pps.tv/ugc/list-c30.html')
    match0 = re.compile('<ul class="main-nav nav-list">(.+?)</ul>', re.DOTALL).search(link)

    # fetch the url for video channels specified in VIDEO_LIST
    match = re.compile('<li class.+?><a.+?href="(.+?)"><.+?>(.+?)</span></a>').findall(match0.group(1))
    totalItems = len(match)
    i = 0
    for path, name in match:
        id = fetchID(VIDEO_LIST, name)
        if id == '': continue
        i = i + 1
        li = xbmcgui.ListItem(str(i) + '. ' + name)
        u = sys.argv[0] + "?mode=1&name=" + urllib.quote_plus(name) + "&id=" + urllib.quote_plus(id) + "&cat=" + urllib.quote_plus('全部') + "&area=" + urllib.quote_plus('全部') + "&year=" + urllib.quote_plus('全部') + "&order=" + urllib.quote_plus('按观众数')
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, True, totalItems)
    
    # fetch the url for ugc channels, exclude those already in VIDEO_LIST 
    match1 = re.compile('<ul class="ugc-cat-list">(.+?)</ul>').search(link)
    match = re.compile('<li class="ucl-item "><a class="ucl-a" href="/ugc/list-(.+?)-.+?">(.+?)<b class="b"></b></a></li>').findall(match1.group(1))
    totalItems = len(match)
    for cat, name in match:
        list = [x[1] for x in VIDEO_LIST]
        if name in list: continue # skip if already listed
        id = 'ugc'
        i = i + 1
        li = xbmcgui.ListItem(str(i) + '. ' + name)
        u = sys.argv[0] + "?mode=11&name=" + urllib.quote_plus(name) + "&id=" + urllib.quote_plus(id) + "&cat=" + urllib.quote_plus(cat) + "&year=" + urllib.quote_plus('全部') + "&order=" + urllib.quote_plus('最新发布')
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, True, totalItems)
    xbmcplugin.setContent(int(sys.argv[1]), 'movies')
    xbmcplugin.endOfDirectory(int(sys.argv[1]))  

##################################################################################
# Routine to fetch and build the video selection menu
# - selected page & filters (user selectable)
# - video items list
# - user selectable pages
##################################################################################
#def progListMovie(name, id, page, cat, area, year, order):
def progListMovie(name, id, page, cat, area, year, order, listpage):
    # fetch user specified url filter ID's  
    catID = areaID = yearID = ''
    if re.search('全部',cat): catstr = ''
    else:
        catlist, arealist, yearlist = getList(listpage)
        catstr = fetchID(catlist, cat) + ','
        if catstr != None: catID = 'genre,'
        
    if re.search('全部',area): areastr = ''
    else:
        areastr = fetchID(arealist, area) + ','
        if areastr != None: areaID = 'area,'

    if re.search('全部',year): yearstr = ''
    else:
        yearstr = fetchID(yearlist, year) + ','
        if yearstr != None: yearID = 'year,'
        
    sortID = fetchID(SORT_LIST, order) + ','    
    if sortID == ',': sortID = 'sum_online_sum,'  
    videoID = fetchID(VIDEO_LIST, name)    
    if videoID == '': videoID = 'movie'
                   
    # construct url based on user elected filter ID's
    url = 'http://v.pps.tv/' + videoID + '/' + areaID + catID + yearID + 'orderby_field,asc_desc/' + areastr + catstr + yearstr + sortID + 'dec/'
    if page: currpage = int(page)
    else: currpage = 1
    url += page
    url += '.html'
    link = getHttpData(url)
    # Extract filter list for user selection - list order valid on first entry only    
    match = re.compile('<!--classification ' + name + '-->(.+?)<!--/classification-->', re.DOTALL).findall(link)
    if len(match):
        if listpage==None: listpage = match[0]
    else:
        listpage = ''        
    match = re.compile('<li class="mv-item lrBx">(.+?)</dd>', re.DOTALL).findall(link)                  
    totalItems = len(match)
    if re.search(cat,'全部'): cat = '全部类型'
    if re.search(area,'全部'): area = '全部地区'
    if re.search(year,'全部'): year = '全部年份'

    # Fetch & build video titles list for user selection, highlight user selected filter  
    li = xbmcgui.ListItem(name + '（第' + str(currpage) + '页）【[COLOR FFFF0000]' + cat + '[/COLOR]/[COLOR FF00FF00]' + area + '[/COLOR]/[COLOR FFFFFF00]' + year + '[/COLOR]/[COLOR FF00FFFF]' + order + '[/COLOR]】（按此选择）')
    u = sys.argv[0] + "?mode=4&name=" + urllib.quote_plus(name) + "&id=" + urllib.quote_plus(id) + "&cat=" + urllib.quote_plus(cat) + "&area=" + urllib.quote_plus(area) + "&year=" + urllib.quote_plus(year) + "&order=" + order + "&listpage=" + urllib.quote_plus(listpage)
    xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, True, totalItems)

    for i in range(0, len(match)):
        # Video & Series titles need different routines
        if name == '电视剧':
            mode = 3
        else:
            mode = 2

        match1 = re.compile('<a class="but" href="(.+?)" title="播放" target="PPS_PLAY">播放</a>').search(match[i])
        # No playback button for playing video
        if match1 == None: continue
#            match1 = re.compile('<div class="lbx"><a href="(.+?)"').search(match[i])
#            mode = 21
        p_id = match1.group(1)
                               
        match1 = re.compile('.+?<img src="(.+?)" class="imgs".+?').search(match[i])
        p_thumb = match1.group(1)
        match1 = re.compile('<dt class="t"><a href=".+?".+?title="(.+?)".+?</a></dt>').search(match[i])
        p_name = p_list = match1.group(1)       
        match1 = re.compile('<li>播放人次:<span class="rc">([0-9]+)</span></li>').search(match[i])
        if match1: p_list += ': ' + match1.group(1) #+ ' ('+p_id+')'
  
        li = xbmcgui.ListItem(str(i + 1) + '. ' + p_list, iconImage='', thumbnailImage=p_thumb)
        u = sys.argv[0] + "?mode=" + str(mode) + "&name=" + urllib.quote_plus(p_name) + "&id=" + urllib.quote_plus(p_id) + "&thumb=" + urllib.quote_plus(p_thumb)
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, True, totalItems)

    # Fetch and build user selectable page number
    matchp = re.compile('<div class="pagenav">(.+?)</div>', re.DOTALL).findall(link)
    if len(matchp): 
        matchp1 = re.compile('<a href=".+?">([0-9]+)</a>', re.DOTALL).findall(matchp[0])    
        if len(matchp1):
            plist=[]
            for num in matchp1:
                if num not in plist:
                    plist.append(num)
                    li = xbmcgui.ListItem("... 第" + num + "页")
                    u = sys.argv[0] + "?mode=1&name=" + urllib.quote_plus(name) + "&id=" + urllib.quote_plus(id) + "&cat=" + urllib.quote_plus(cat) + "&area=" + urllib.quote_plus(area) + "&year=" + urllib.quote_plus(year) + "&order=" + order + "&page=" + urllib.quote_plus(str(num))+ "&listpage=" + urllib.quote_plus(listpage)
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
# Routine to fetch and build the ugc selection menu
# - selected page & filters (user selectable)
# - ugc items list
# - user selectable pages
##################################################################################
def progListUgc(name, id, page, cat, year, order, datelist=[], orderlist=[]): 
    # fetch url filter ID's
    dateID = '1'
    orderID = '1'
    if len(datelist):
        dateID = fetchID(datelist, year)
        if dateID == '': dateID = '1'
        
    if len(orderlist):
        orderID = fetchID(orderlist, order)    
        if orderID == '': orderID = '1' 
                   
    # Construct url based on filter ID's & selected page           
    url = 'http://v.pps.tv/' + id + '/list-' + cat + '-t' + dateID + '-o' + orderID + '-p'
    if page:
        currpage = int(page)
    else:
        currpage = 1
    url += page
    url += '.html'
    link = getHttpData(url)
    match = re.compile('<!--ugc-tag-list-->(.+?)<!--/ugc-tag-list-->').findall(link)
    
    # Extract filter list for user selection
    match1 = re.compile('id="ugc-tag-list">(.+?)<ul class="ugc-list">').findall(match[0])
    if len(match1):
        listpage = match1[0]
    else:
        listpage = ''
          
    # Fetch & build ugc list for user selection, highlight user selected filter      
    match = re.compile('<li class="ugc-item">(.+?)</ul>').findall(match[0])
    totalItems = len(match)   
    li = xbmcgui.ListItem(name + '（第' + str(currpage) + '页）【[COLOR FFFFFF00]' + year + '[/COLOR]/[COLOR FF00FFFF]' + order + '[/COLOR]】（按此选择）')
    u = sys.argv[0] + "?mode=12&name=" + urllib.quote_plus(name) + "&id=" + urllib.quote_plus(id) + "&cat=" + urllib.quote_plus(cat) + "&year=" + urllib.quote_plus(year) + "&order=" + urllib.quote_plus(order)+ "&page=" + urllib.quote_plus(listpage)
    xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, True, totalItems)
    for i in range(0, len(match)):
        match1 = re.compile('<a href="(.+?)"').search(match[i])
        p_url = 'http://v.pps.tv' + match1.group(1)
        
        match1 = re.compile('<a href.+?title="(.+?)".*?>').search(match[i])
        p_name = p_list = match1.group(1)
        
        match1 = re.compile('<span class="nm">播放：</span>([0-9]+)<a.+?').search(match[i])      
        if match1: p_list += ': ' + match1.group(1) #+' ('+p_url+')'  
          
        match1 = re.compile('class="imgm" src="(.+?)">').search(match[i])
        p_thumb = match1.group(1)
            
        li = xbmcgui.ListItem(str(i + 1) + '. ' + p_list, iconImage='', thumbnailImage=p_thumb)
        u = sys.argv[0] + "?mode=14&name=" + urllib.quote_plus(p_name) + "&url=" + urllib.quote_plus(p_url) + "&thumb=" + urllib.quote_plus(p_thumb)
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, False, totalItems)
            
    # Fetch and build user selectable page number 
    matchp = re.compile('<div class="pagenav">(.+?)</div>').findall(link)
    if len(matchp): matchp1 = re.compile('<a href=".+?">([0-9]+)</a>').findall(matchp[0])      
    if len(matchp1):
        plist=[]
        for num in matchp1:
            if num not in plist:
                plist.append(num)
                li = xbmcgui.ListItem("... 第" + num + "页")
                u = sys.argv[0] + "?mode=11&name=" + urllib.quote_plus(name) + "&id=" + urllib.quote_plus(id) + "&cat=" + urllib.quote_plus(cat) + "&year=" + urllib.quote_plus(year) + "&order=" + order + "&page=" + urllib.quote_plus(str(num))
                xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, True, totalItems) 
    xbmcplugin.setContent(int(sys.argv[1]), 'movies')
    xbmcplugin.endOfDirectory(int(sys.argv[1]))
    
##################################################################################
# Routine to update ugc list as per user selected filters
# - 发布时间 (Published date)
# - 排序方式 (Order)
##################################################################################
def updateListUgc(name, id, listpage, cat, year, order):
    datelist, orderlist = getListUgc(listpage)
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
        progListUgc(name, id, '1', cat, year, order, datelist, orderlist)

##################################################################################
# Routine to fetch and build the video series selection menu
# - selected page & filters (user selectable)
# - Video series list
# - user selectable pages
##################################################################################
def progListSeries(name, id, thumb, episodeSel):
    url = 'http://v.pps.tv' + id
    link = getHttpData(url)
    episodeList = re.compile('<!--episode-list-->(.+?)<!--/episode-list-->').findall(link)
    listpage = episodeList[0]
               
    episodeSet = re.compile('class="dra-version".+?<h[0-9]>(.+?)</h[0-9]>').findall(episodeList[0])
    if len(episodeSet):
        # let user select series option if on first time entry i.e. language, HD, related info etc
        if episodeSel=='1' and len(episodeSet)>1: episodeSel=updateListSeries(name,'1',thumb,listpage)
        epsel = 0 
        eList = ''
        for i in range(0, len(episodeSet)):
            if episodeSet[i]==episodeSel: 
                epsel = i
            eList = eList + COLOR_LIST[i] + episodeSet[i] + '[/COLOR]|'
        episodeSel=episodeSet[epsel]
        
    li = xbmcgui.ListItem("[选择:"+episodeSel+"] " + eList + '（按此选择）', iconImage='', thumbnailImage=thumb)
    u = sys.argv[0]+"?mode=6&name="+urllib.quote_plus(name)+"&id="+urllib.quote_plus(id)+"&thumb="+urllib.quote_plus(thumb)+"&page="+urllib.quote_plus(listpage) 
    xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, True)
    
    # fetch and build the video series list  / related info list
    match = re.compile('<div id="tag-[0-9]+" class="dra-version">(.+?)</ul>').findall(episodeList[0])
#    if len(match):
    for j in range(0,len(match)):
        if re.search('>'+episodeSel+'<',match[j]) == None: continue
        matchp = re.compile('<li id=(.+?)</li>').findall(match[j])                  
        totalItems = len(matchp)
        for i in range(0, len(matchp)):
            match1 = re.compile('<a.+?href="(.+?)"').search(matchp[i])
            if match1 == None: continue
            p_url = 'http://v.pps.tv' + match1.group(1)
            match1 = re.compile('title="(.+?)".*?>(.+?)</a>').search(matchp[i])           
            sn = re.sub(' ','',match1.group(2))
            p_name = match1.group(1)
            p_list = sn + ': ' + p_name   #+' ('+p_url+')'
 
            li = xbmcgui.ListItem(p_list, iconImage='', thumbnailImage='')
            u = sys.argv[0] + "?mode=10&name=" + urllib.quote_plus(p_name) + "&url=" + urllib.quote_plus(p_url)
            xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, False, totalItems)
        break
    xbmcplugin.setContent(int(sys.argv[1]), '电视剧')
    xbmcplugin.endOfDirectory(int(sys.argv[1]))
           
##################################################################################
# Routine to update video series list as per user selections
# - 剧集列表 (Series Options)
##################################################################################
def updateListSeries(name, id, thumb, listpage):   
    elist = re.compile('class="dra-version".+?<h[0-9]>(.+?)</h[0-9]>').findall(listpage)
    dialog = xbmcgui.Dialog()
    sel = dialog.select('剧集列表', elist)
    if sel != -1:
        epSel = elist[sel]
        # return selected value on local call
        if id=='1': return epSel
        else: progListSeries(name, id, thumb, epSel)
    else: return(name, id, thumb, '1')

##################################################################################
# Routine to play TV series video file
# Player using ppstream player
##################################################################################
def PlaySeries(name, url, thumb):
    link = getHttpData(url)
    xbmc.executebuiltin('System.ExecWait(\\"' + __cwd__ + '\\resources\\player\\pps4xbmc\\" ' + url + ')')
 
##################################################################################
# Routine to play movide video file
# Player using ppstream player
##################################################################################
def PlayVideo(name, url):
    link = getHttpData(url)
    match0 = re.compile('<!--播放相关js-->.+?src="(.+?)".+?</script>').findall(link)
    match1 = getHttpData(match0[0])
#    match = re.compile("ppspowerplayer.setencsrc\('(.+?)'\)").findall(match1)
    match = re.compile('var encsrc="(.+?)"').findall(match1)
    if len(match):  
        url = match[0]
        xbmc.executebuiltin('System.ExecWait(\\"' + __cwd__ + '\\resources\\player\\pps4xbmc\\" ' + url + ')')
    else:
        dialog = xbmcgui.Dialog()
        ok = dialog.ok(__addonname__,'您当前观看的视频暂不能播放，请选择其它节目')
        
##################################################################################
# Routine to play ugc embedded swf video file
# fetch the swf file directly using one of the hardcoded link below
# http://dp.ppstv.com/get_play_url_rate.php?sid=30NG77&flash_type=1&type=0
# http://dp.ppstream.com/get_play_url_rate.php?sid=30NG77&flash_type=1&type=0
# http://dp.ugc.pps.tv/get_play_url_rate.php?sid=30NG77&flash_type=1&type=0
##################################################################################
def playVideoUgc(name, url, thumb): 
    match = re.compile('play_(.+?).html').findall(url)
    videolink = 'http://dp.ppstv.com/get_play_url_rate.php?sid='+match[0]+'&flash_type=1&type=0'
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
# Routine to fetch different playback options for the selected movie
# e.g. HD(高清), languages, related info etc
##################################################################################
def getMovie(name, id, thumb):
    url = 'http://v.pps.tv' + id
    link = getHttpData(url)
    match0 = re.compile('js-list[0-9]*?(.+?)</ul>').findall(link)
    if len(match0):
        j=0
        li = xbmcgui.ListItem("当前视频：" + name, iconImage='', thumbnailImage=thumb)
        u = sys.argv[0] + "?mode=40&name=" + urllib.quote_plus(name)
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li)
        for k in range (0, len(match0)):
            match = re.compile('<li id(.+?)</li>').findall(match0[k])
            for i in range(0, len(match)):
                match1 = re.compile('href="\.{0,1}?(.+?)"').search(match[i])
                p_url = match1.group(1)
                match1 = re.compile('title="(.+?)"').search(match[i])
                p_name = match1.group(1)
                j=j+1
                url = "http://v.pps.tv" + p_url
                li = xbmcgui.ListItem(str(j) + ". " + p_name)
                u = sys.argv[0] + "?mode=10&name=" + urllib.quote_plus(name) + "&url=" + urllib.quote_plus(url)
                xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, False)
        xbmcplugin.endOfDirectory(int(sys.argv[1]))   


##################################################################################
# Get user input for PPS site search
##################################################################################
def searchPPS():
    result=''
    keyboard = ChineseKeyboard.Keyboard('','请输入搜索内容')
#    keyboard = xbmc.Keyboard('','请输入搜索内容')
    xbmc.sleep( 1500 )
    keyboard.doModal()
    if (keyboard.isConfirmed()):
        keyword = keyboard.getText()

        ### Chinese String for testing without chinesekeyboard
        ### 夏家三千金 不能说的秘密  步步惊心 爱情公寓 三国高清版 金陵十三钗
        #keyword = '爱情公寓'

        url='http://so.pps.tv/search?q=' + keyword + '&from=1'
        page='1'
        ppsSearchList(keyword,url,page)
    else: return
        
##################################################################################
# Routine to search PPS site based on user given keyword for:
# a. video episode List for each found provider
# b. movie from each found provider
# c. ugc for each found provider
##################################################################################
def ppsSearchList(name, url, page): 
    if page:
        currpage = int(page)
    else:
        currpage = 1
    
    p_url = url.replace(" ","%20") + '&page=' + str(currpage)
    link = getHttpData(p_url)
    li = xbmcgui.ListItem('[COLOR FFFF0000]当前搜索: 第' + str(currpage) + '页[/COLOR][COLOR FFFFFF00] (' + name + ')[/COLOR]【[COLOR FF00FF00]' + '请输入新搜索内容' + '[/COLOR]】')
    u = sys.argv[0] + "?mode=31&name=" + urllib.quote_plus(name) + "&url=" + urllib.quote_plus(url) + "&page=" + urllib.quote_plus(page)
    xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, True)
    
    #########################################################################
    # Video Episode/Movie listing for each found related episode title
    #########################################################################
    n = 0
    match_ml = re.compile('<li class="sr-item.+?">(.+?)<div class="sr-cell">').findall(link)
    if len(match_ml):
        for x in range(0, len(match_ml)): 
            # Find the episode title & its list of the provider sites 
            match_t = re.compile('<a data-click-stat=.+?class="keyword">(.+?)</a>').findall(match_ml[x])
            keyword = match_t[0].replace('</em>','')

            ## matchp = re.compile('<div class="mv-play-drop">(.+?)</div>').findall(match_ml[x])
            match1 = re.compile('<li.+?data-video-type="([0-9]+)".+?title=.+?>(.+?)<em>.+?</li>').findall(match_ml[x])
            if match1==None: continue # Proceed only if provider sites found
            # Extract each provider and its episode list
            match_ep = re.compile('<ul class="mv-episode(.+?)</ul').findall(match_ml[x])

            # Fetch & build the episode list for each site provider 
            for j in range(0, len(match1)): 
                 p_name = match1[j][1]+ " - " + keyword
                 epSite = "_site" + match1[j][0]
                 
                 #############################################################
                 # Episode Listing for each found related episode title
                 #############################################################
                 if match_ep:
                     # Combine all the episode listing groups based on given site provider
                     epList = ""
                     for k in range(0, len(match_ep)):
                         if re.search(epSite, match_ep[k]):
                             epList += match_ep[k] 
                     # Construct the array for the found episode listing for fast response
                     match_ep1 = re.compile('<a class="epis-a" href="(.+?)" target="_blank" title=.+?>([0-9]+)</a>').findall(epList)
                     p_list = match_ep1[0][0]
                     for k in range(1, len(match_ep1)):
                         p_list += "," + match_ep1[k][0]

                     n += 1
                     li = xbmcgui.ListItem(str(n) + ". 电视剧: " + p_name)
                     u = sys.argv[0] + "?mode=33&name=" + urllib.quote_plus(p_name) + "&url=" + urllib.quote_plus(p_list)
                     xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, True)

                 #############################################################
                 # Moive Listing for each found related movie title
                 #############################################################
                 else:       
                     match_mp = re.compile('<ul class="new-mv-episode(.+?)</ul').findall(match_ml[x])
                     
                     # Find the video link for the site provider
                     for k in range(0, len(match_mp)):
                         if re.search(epSite, match_mp[k])== None: continue
                         match_mp1 = re.compile('<a class="epis-a" href="(.+?)" target="_blank".+?</a>').findall(match_mp[k])
                         p_url = match_mp1[0]
                         n += 1
 
                         mode = fetchID(MPLAYER_LIST,match1[j][1])
                         if mode=='': mode = '99' # player not implemented

                         li = xbmcgui.ListItem(str(n) + ". 电影: " + p_name)
                         u = sys.argv[0] + "?mode=" + mode + "&name=" + urllib.quote_plus(p_name) + "&url=" + urllib.quote_plus(p_url)
                         xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, False)
 
    #############################################################
    # ugc-list for related title unpack
    #############################################################
    n += 1
    matchp = re.compile('<ul class="ugc-list">(.+?)<!--/ugc-search-results-->').findall(link)
    if len(matchp) == 0: return
    
    # Fetch & build ugc list for user selection, highlight user selected filter      
    match = re.compile('<li class="ugc-item">(.+?)</ul>').findall(matchp[0])
    if len(match) == 0: return
    totalItems = len(match)

    for i in range(0, len(match)):      
        match1 = re.compile('<div class="t"><a href="(.+?)" target="_blank" title="(.+?)">').search(match[i])
        p_url = match1.group(1)
        p_name = p_list = match1.group(2)

        match1 = re.compile('<span class="nm">播放：</span>([0-9]+)<a class=').search(match[i])      
        if match1: p_list += ': ' + match1.group(1)
          
        match1 = re.compile('<img src=.+?lazy_src="(.+?)" class="imgm"').search(match[i])
        p_thumb = match1.group(1)
              
        li = xbmcgui.ListItem(str(n + i) + ". " + p_list, iconImage="", thumbnailImage=p_thumb)
        u = sys.argv[0] + "?mode=14&name=" + urllib.quote_plus(p_name) + "&url=" + urllib.quote_plus(p_url) + "&thumb=" + urllib.quote_plus(p_thumb)
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
                    li = xbmcgui.ListItem("... 第" + num + "页")
                    u = sys.argv[0] + "?mode=32&name=" + urllib.quote_plus(name) + "&url=" + urllib.quote_plus(url) + "&page=" + urllib.quote_plus(str(num))
                    xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, True) 
    xbmcplugin.setContent(int(sys.argv[1]), 'movies')
    xbmcplugin.endOfDirectory(int(sys.argv[1]))
    # xbmc.executebuiltin('Container.Refresh')

##################################################################################
# Routine to display episode listing
##################################################################################
def episodeList(name, url):
 # url is a list of url for each episode
    site = name.split(" - ")[0]  
    mode = fetchID(MPLAYER_LIST,site)
    if mode=='': mode = '99' # player not implemented
    url_list = url.split(",")
    for i in range(0, len(url_list)): 
        p_url = url_list[i]
        p_name = name + ": 第" + str(i+1) + "集"
        li = xbmcgui.ListItem(p_name)
        u = sys.argv[0] + "?mode="+ mode +"&name=" + urllib.quote_plus(p_name) + "&url=" + urllib.quote_plus(p_url)
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
        url = 'http://cache.video.qiyi.com/v/' + videoId + '/' + pid + '/' + ptype + '/'
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
# LETV Video Player - Under Development
# Add all the video resolution items & links in playlist for auto/user selection
# a. Press space bar, then scroll to the required item
# b. Press Enter play
# c. Press Stop to end playlist
##################################################################################
def PlayVideoLetv(name,url):
    VIDEORES=["高清","标清","流畅"]  
    playlist=xbmc.PlayList(1)
    playlist.clear()
    
    link = getHttpData(url)
    matchv = re.compile('{v:\["(.+?)","(.+?)"\],p:""}').findall(link)
    for j in reversed(range(len(matchv[0]))):
        #algorithm to generate the video link code
        vid = matchv[0][j][24:56]  # extract 32-Bytes VID code
        if matchv[0][j][56:60] == "dj9i":
            vid += "dg=="
        elif matchv[0][j][56:60] == "bHY/":
            vid += "bHY="
        elif matchv[0][j][52:56] == "bHY/":
            vid = vid[:-1] + "="
        url = 'http://g3.letv.cn/vod/v1/' + vid + '?format=1&b=843&expect=3&host=www_letv_com'
        link = getHttpData(url)
        link = link.replace("\/", "/")
        match = re.compile('{.+?"location": "(.+?)" }').findall(link)
        if match:
            for i in range(len(match)):
                p_name = name+' "'+VIDEORES[i]+'"' 
                listitem = xbmcgui.ListItem(p_name, thumbnailImage = __addonicon__)
                listitem.setInfo(type="Video",infoLabels={"Title":p_name})
                playlist.add(match[i], listitem)
        else:
            dialog = xbmcgui.Dialog()
            ok = dialog.ok(__addonname__, '无法播放：未匹配到视频文件，请稍侯再试')  
    xbmc.Player().play(playlist)

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
    getMovie(name, id, thumb)
elif mode == 3:
    progListSeries(name, id, thumb, page)
elif mode == 4:
    updateListMovie(name, id, page, cat, area, year, order, listpage)
elif mode == 6:
    updateListSeries(name, id, thumb, page)
elif mode == 10:
    PlayVideo(name, url)
    
elif mode == 11:
    progListUgc(name, id, page, cat, year, order)
elif mode == 12:
    updateListUgc(name, id, page, cat, year, order) 
elif mode == 14:
    playVideoUgc(name, url, thumb)    
    
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
       