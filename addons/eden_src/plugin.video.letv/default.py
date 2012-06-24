# -*- coding: utf-8 -*-
import math
import xbmc, xbmcgui, xbmcplugin, xbmcaddon, urllib2, urllib, re, string, sys, os, gzip, StringIO
import ChineseKeyboard

########################################################################
# 乐视网(LeTv) by cmeng
########################################################################
# Version 1.0.0 2012-06-24
# a. Add in 明星 category selection
# b. Update video link decode algorithm
# c. Correct update video list error
#
# See changelog.txt for previous history
########################################################################

# Plugin constants 
__addonname__   = "乐视网 (LeTV)"
__addonid__     = "plugin.video.letv"
__addon__ = xbmcaddon.Addon(id=__addonid__)
__addonicon__   = os.path.join( __addon__.getAddonInfo('path'), 'icon.png' )
__settings__    = xbmcaddon.Addon(id=__addonid__)
__profile__     = xbmc.translatePath( __settings__.getAddonInfo('profile') )

UserAgent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'
VIDEO_LIST = [['list/c1','电影'],['list/c2','电视剧'],['list/c3','动漫'],['list/c11','综艺'],['starlist/i','明星']]
SORT_LIST = [['_o1','最新更新'],['_o3','最热播放'],['_o7','最新上映'],['_o2','最高评分']]
GENDER_LIST = [['_g-1','全部'],['_g1','男'],['_g2','女']]
COLOR_LIST = ['[COLOR FFFF0000]','[COLOR FF00FF00]','[COLOR FFFFFF00]','[COLOR FF00FFFF]','[COLOR FFFF00FF]']
     
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
# Routine to extract url ID from array based on given selected filter
# List = [['list/c1','电影'],['list/c2','电视剧']....
# list = [['_g-1','全部'],['_g1','男'],['_g2','女']]
# List = [['_o1', '最新更新'], ['_o2', '最多播放']....
# .......
##################################################################################
def fetchID(dlist, idx):
    for i in range(0, len(dlist)):
        if dlist[i][1] == idx:
            return dlist[i][0]
    return ''

##################################################################################
# Routine to fetch and build video filter list
# tuple to list conversion and strip spaces    
# - 按类型  (Categories)
# - 按地区 (Countries/Areas)
# - 按年份 (Year)
##################################################################################
def getList(listpage):
    catlist = arealist = yearlist = []
    match = re.compile('<dt>影片类型.*?</dt>(.+?)</dl>', re.DOTALL).search(listpage)
    if match is None: match = re.compile('<dt>节目类型.*?</dt>(.+?)</dl>', re.DOTALL).search(listpage)
    catlist = re.compile('href=".+?(_t[-0-9]+)_.+?>(.+?)</a>').findall(match.group(1))
    match = re.compile('<dt>地区.*?</dt>(.+?)</dl>', re.DOTALL).search(listpage)
    arealist = re.compile('href=".+?(_a[-0-9]+)_.+?>(.+?)</a>').findall(match.group(1))
    match = re.compile('<dt>上映时间.*?</dt>(.+?)</dl>', re.DOTALL).search(listpage)
    if match: yearlist = re.compile('href=".+?(_y[-0-9]+)_.+?>(.+?)</a>').findall(match.group(1))

    # tuple to list conversion and strip spaces 
    catlist  = [[x[0],x[1].strip()] for x in catlist]
    arealist = [[x[0],x[1].strip()] for x in arealist]
    yearlist = [[x[0],x[1].strip()] for x in yearlist]
    return catlist, arealist, yearlist

##################################################################################
# Routine to fetch and build video filter list for star
# - 按字母 (Alphabet)
# - 按地区 (Countries/Areas)
# - 按职业 (Profession)
# 
##################################################################################
def getListStar(listpage):
    alphabetlist = arealist = proflist = []
    match = re.compile('<dt>字母</dt>(.+?)</dl>', re.DOTALL).search(listpage)
    alphabetlist = re.compile('href=".+?(i[-1a-z]+)_.+?>(.+?)</a>').findall(match.group(1))
    match = re.compile('<dt>地区</dt>(.+?)</dl>', re.DOTALL).search(listpage)
    arealist = re.compile('href=".+?(_a[-0-9]+)_.+?>(.+?)</a>').findall(match.group(1))
    match = re.compile('<dt>职业</dt>(.+?)</dl>', re.DOTALL).search(listpage)
    proflist = re.compile('href=".+?(_w[-0-9]+)_.+?>(.+?)</a>').findall(match.group(1))

    # tuple to list conversion and strip spaces    
    alphabetlist = [[x[0],x[1].strip()] for x in alphabetlist]
    arealist = [[x[0],x[1].strip()] for x in arealist]
    proflist = [[x[0],x[1].strip()] for x in proflist]
    return alphabetlist, arealist, proflist

##################################################################################
# Routine to fetch and build video filter list   
# - 年月份 (Year -Month)
##################################################################################
def getListVariety(listpage):
    datelist = []
    datelist = re.compile('<a list-month="[0-9]+?" list-year="([0-9]+?)" data-tabbtt="[0-9]+?" >(.+?)</a>', re.DOTALL).findall(listpage) 
   
    dlist = []
    plist = []
    for x in datelist:
        if x[0] not in plist:
            plist.append(x[0])
            dlist.append([x[0],'全部'])
        dlist.append([x[0],x[1]])
    datelist = dlist
    return datelist

##################################################################################
# Routine to fetch & build PPS 网络电视 main menu
# - video list as per [VIDEO_LIST]
# - ugc list
# - movie, series, star & ugc require different sub-menu access methods
##################################################################################
def mainMenu():
#    li = xbmcgui.ListItem('[COLOR FFFF0000]0. LeTV 乐视网搜索:[/COLOR][COLOR FF00FF00]【请输入搜索内容】[/COLOR]')
#    u=sys.argv[0]+"?mode=31"
#    xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, True)

    li = xbmcgui.ListItem('[COLOR FF00FF00]【LeTV 乐视网】[/COLOR]')
    u=sys.argv[0]+"?mode="
    xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, True)
    
    link = getHttpData('http://so.letv.com/list/c1_t-1_a-1_y-1_f_at_o1_p.html')
    listpage = re.compile('<div class="list_r">(.+?)<p class="foldbox on" id="tagCtr">').findall(link)[0]
    match0 = re.compile('<div class="listNav">(.+?)</ul>', re.DOTALL).findall(link)

    # fetch the url for video channels specified in VIDEO_LIST
    match = re.compile('<a href="(.+?)".+?>(.+?)</a>').findall(match0[0])
    totalItems = len(match)
    i = 0
    for path, name in match:
        id = fetchID(VIDEO_LIST, name)
        if id == '': continue
        i = i + 1
        li = xbmcgui.ListItem(str(i) + '. ' + name)
        if name == '明星':
            url = 'http://so.letv.com/starlist/i-1_w-1_a-1_g-1_p.html'
            u = sys.argv[0] + "?mode=21&name=" + urllib.quote_plus(name) + "&url=" + urllib.quote_plus(url)+ "&page=1"  + "&alphabet=全部" + "&area=全部" + "&prof=全部" + "&gender=全部"
        else:
            u = sys.argv[0] + "?mode=1&name=" + urllib.quote_plus(name) + "&id=" + urllib.quote_plus(id)+ "&page=1"  + "&cat=全部" + "&area=全部" + "&year=全部" + "&order=最新更新" + "&listpage=" + urllib.quote_plus(listpage)
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, True, totalItems)
    
    # fetch the url for ugc channels, exclude those already in VIDEO_LIST 
    for p_url, name in match:
        list = [x[1] for x in VIDEO_LIST]
        if name in list: continue # skip if already listed
        i = i + 1
        li = xbmcgui.ListItem(str(i) + '. ' + name)
        u = sys.argv[0] + "?&mode=8" + "&name=" + urllib.quote_plus(name) + "&url=" + urllib.quote_plus(p_url)
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, True, totalItems)

    xbmcplugin.setContent(int(sys.argv[1]), 'movies')
    xbmcplugin.endOfDirectory(int(sys.argv[1]))  

##################################################################################
# Routine to fetch and build the video selection menu
# - selected page & filters (user selectable)
# - video items list
# - user selectable pages
##################################################################################
def progListMovie(name, id, page, cat, area, year, order, listpage):
    # fetch user specified parameters  
    catlist, arealist, yearlist = getList(listpage)
    if re.search('全部',cat): cat = '全部'
    fltrCat  = fetchID(catlist, cat)
    if re.search('全部',area): area = '全部'
    fltrArea = fetchID(arealist, area)
    if re.search('全部',year): year = '全部'
    fltrYear = fetchID(yearlist, year)
    fltrAge  = '_f-1'
    fltrVer  = '_at-1'
    fltrOrder = fetchID(SORT_LIST, order) 
  
    # Video site parameters definitions:
    # [movie:] http://so.letv.com/list/c1_t-1_a-1_y-1_f_at_o1_p.html
    # c = video type (c1:电影; c2:电视剧 ; c3:动漫 ; c11:综艺 ) 
    # t = video category (t-1:all; t8:剧情)
    # a = area (a-1:all; a1:中国大陆 ...)
    # y = year (y-1:all; y2012:2012; y0:earlier)
    # [动漫:]
    # f = age group (f1:6岁以下; f2:6-12岁; f3:12-18岁; f4: 18以上)
    # at = 视频类型 (at31:TV版; at32:OVA版; at33:剧场版; at34:OAD版; at37:SP)
    # o = order (o1: 最新更新; o3: 最热播放; o7: 最新上映; o2: 最高评分)
    # p = page
    # --------------------------             
    # [ugc:] http://www.letv.com/vchannel/new_ch3_d1_p1.html
    # new_ch = ugc type (; new_ch3:娱乐 ; new_ch9:音乐 ...)
    # d1_p1 = fixed 
        
    # construct url based on user selected filter ID's
    if name == '动漫':
        url = 'http://so.letv.com/' + id + fltrCat + fltrArea +  fltrYear + fltrAge + fltrVer + fltrOrder + '_p'
    elif name == '综艺':
        url = 'http://so.letv.com/' + id + fltrCat + fltrArea + '_y_f_at' + fltrOrder + '_p'
    else:
        url = 'http://so.letv.com/' + id + fltrCat + fltrArea +  fltrYear + '_f_at' + fltrOrder + '_p'
    if page: currpage = int(page)
    else: currpage = 1
    url += page + '.html'

    link = getHttpData(url)
    # Extract filter list for user selection - list order valid on first entry only    
    match = re.compile('<div class="list_r">(.+?)<p class="foldbox on" id="tagCtr">').findall(link)[0]
    if len(match): listpage = match

    match = re.compile('<dl class="m_dl">(.+?)</dl>', re.DOTALL).findall(link)                  
    totalItems = len(match)
    if re.search(cat,'全部'): cat = '全部类型'
    if re.search(area,'全部'): area = '全部地区'
    if re.search(year,'全部'): year = '全部年份'

    # Fetch & build video titles list for user selection, highlight user selected filter  
    li = xbmcgui.ListItem(name + '（第' + str(currpage) + '页）【[COLOR FFFF0000]' + cat + '[/COLOR]/[COLOR FF00FF00]' + area + '[/COLOR]/[COLOR FFFFFF00]' + year + '[/COLOR]/[COLOR FF00FFFF]' + order + '[/COLOR]】（按此选择）')
    u = sys.argv[0] + "?mode=4&name=" + urllib.quote_plus(name) + "&id=" + urllib.quote_plus(id) + "&cat=" + urllib.quote_plus(cat) + "&area=" + urllib.quote_plus(area) + "&year=" + urllib.quote_plus(year) + "&order=" + order + "&listpage=" + urllib.quote_plus(listpage)
    xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, True, totalItems)

    for i in range(0, len(match)):
        # Movie, Video, Series & Variety titles need different routines
        if name == '电视剧':
            mode = '5'
        elif name == '动漫':
            mode = '5'
        elif name == '电影':
            mode = '10'
        elif name == '综艺':
            mode = '11'
        
        match1 = re.compile('<dt><a href="(.+?)"[ ]*title="(.+?)" target="_blank">').search(match[i])
        p_url = match1.group(1)
        p_name = p_list = match1.group(2)    
        match1 = re.compile('<imgsrc="(.+?)"alt').search(match[i])
        p_thumb = match1.group(1)
        match1 = re.compile('<dd>评价：<span class="sorce2"><i>([.0-9]+)</i>').search(match[i])
        if match1: p_list += '  [评价: ' +  match1.group(1) + ']'
  
        li = xbmcgui.ListItem(str(i + 1) + '. ' + p_list, iconImage='', thumbnailImage=p_thumb)
        u = sys.argv[0] + "?mode=" + mode + "&name=" + urllib.quote_plus(p_name) + "&url=" + urllib.quote_plus(p_url) + "&thumb=" + urllib.quote_plus(p_thumb)
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, True, totalItems)

    # Fetch and build user selectable page number
    matchp = re.compile('<div class="page">(.+?)</div>', re.DOTALL).findall(link)
    if len(matchp): 
        matchp1 = re.compile('<a href=".+?">([0-9]+)</a>', re.DOTALL).findall(matchp[0])    
        if len(matchp1):
            plist=[str(currpage)]
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
# - 按地区 (Areas)
# - 按年份 (Year)
# - 排序方式 (Selection Order)
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

    if yearlist:
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
# - for 电视剧  & 动漫
# - selected page & filters (user selectable)
# - Video series list
# - user selectable pages
##################################################################################
def progListSeries(name, url, thumb):
    link = getHttpData(url)
    
    li = xbmcgui.ListItem('【[COLOR FFFFFF00][' + name + '][/COLOR] | [COLOR FF00FFFF] [选择: ' + name + '][/COLOR]】', iconImage='', thumbnailImage=thumb)
    u = sys.argv[0]+"?mode=6&name="+urllib.quote_plus(name)+"&url="+urllib.quote_plus(url)+"&thumb="+urllib.quote_plus(thumb) 
    xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, True)
   
    # fetch and build the video series list
    match = re.compile('<div.+?data-tabct="j-tab[1-2]+_child".+?statectn="n_list[1-2]+">(.+?)</div>').findall(link)
    # special handling for '动漫'
    matchp = re.compile('<dl class="w96">(.+?)</dl>').findall(match[0])
    if len(matchp): # not the right one, so re-fetch             
        match = re.compile('<div class="list active" data-tabct="j-tab1_child">(.+?)</div>').findall(link)
    
    for j in range(0, len(match)):
        matchp = re.compile('<dl class="w120">(.+?)</dl>').findall(match[j])              
        totalItems = len(matchp)
        for i in range(0, len(matchp)):
            match1 = re.compile('<img.+?src="(.+?)"').search(matchp[i])
            p_img = match1.group(1)
            match1 = re.compile('<p class="p1">.+?href="(.+?)"[\s]*title="(.+?)">(.+?)</a></p>').search(matchp[i])
            p_url = match1.group(1)
            p_name = p_name = match1.group(2)
            sn = match1.group(3)
            p_list = sn + ': ' + p_name
                 
            li = xbmcgui.ListItem(p_list, iconImage='', thumbnailImage=p_img)
            u = sys.argv[0] + "?mode=10&name=" + urllib.quote_plus(p_name) + "&url=" + urllib.quote_plus(p_url)
            xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, False, totalItems)
    xbmcplugin.setContent(int(sys.argv[1]), name)
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
# Routine to fetch and build the video series selection menu
# - for 综艺 only
# - selected page & filters (user selectable)
# - Video series list
# - user selectable pages
##################################################################################
def progListVariety(name, url, page, year, month):
    link = getHttpData(url)
    listpage = re.compile('<div class="listPic active">(.+?)<div class="d-l"></div>').findall(link)[0]
    datelist = getListVariety(listpage)
   
    if year is None: year = datelist[0][0]
    fltrYear = '&y=' + year
    if month is None: month = datelist[0][1]
    elif re.search('全部',month): month = ''
    fltrMonth ='&m=' + month[:2]
    
    fltrPid = '&pid='+ re.split('/', url)[-1][:-5]
    if page is None: page = '1'
    fltrPage = '&b=' + page
    # http://hot.vrs.letv.com/vlist?callback=LETV.App.Detail.List.paintList&y=2011&f=1&p=1&m=12&pid=52358&b=1&s=20&o=-1&_=1340358261096
    # &y=2012: year 2012
    # &f=1
    # &p=1: 
    # &m=07: month 07=July; blank=全部
    # &pid=52358: url #####.html
    # &b=1: page #  
    # &s=20: item per page
    # &o=-1
    # &_=1340358261096:time-stamp

    # construct url based on user selected filter ID's
    p_url = 'http://hot.vrs.letv.com/vlist?callback=LETV.App.Detail.List.paintList' + fltrYear + '&f=1&p=1' + fltrMonth + fltrPid +  fltrPage + '&s=20&o=-1&_=1340358261096'
    link = getHttpData(p_url)
    if re.search(month,'全部'): month = '全部月份'

    match = re.compile('{"description".+?"name":"(.+?)".+?"viewpic":"(.+?)".+?"url":"(.+?)"').findall(link)
    totalItems = len(match)

    # Fetch & build video titles list for user selection, highlight user selected filter  
    li = xbmcgui.ListItem(name + '（第' + page + '页）【[COLOR FFFF0000]' + year + '[/COLOR] - [COLOR FF00FF00]' + month + '[/COLOR]】（按此选择）')
    u = sys.argv[0] + "?mode=12&name=" + urllib.quote_plus(name) + "&url=" + urllib.quote_plus(url) + "&page=" + page + "&year=" + year + "&month=" + month + "&listpage=" + urllib.quote_plus(listpage)
    xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, True, totalItems)
   
    # if len(match):
    for i in range(0, len(match)):
        p_name = p_list = match[i][0]
        p_img = match[i][1]
        p_url = match[i][2]
        p_list = str(i + 1) + '. ' + p_list         

        li = xbmcgui.ListItem(p_list, iconImage='', thumbnailImage=p_img)
        u = sys.argv[0] + "?mode=10&name=" + urllib.quote_plus(p_name) + "&url=" + urllib.quote_plus(p_url)
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, False, totalItems)
                                    
    # Fetch and build user selectable page number
    matchp = re.compile('LETV.App.Detail.List.paintList\({"b":([1-9]+?),"count":([0-9]+?),.+?"s":([0-9]+?),').findall(link)[0]
    page  = int(matchp[0])
    tsize = int(matchp[1])
    psize = int(matchp[2])
    if tsize > psize:
        pages = int(math.ceil(1.0 * tsize/psize))
        plist=[page]
        for num in range(pages):
            if (num+1) not in plist:
                plist.append(num)
                li = xbmcgui.ListItem("... 第" + str(num+1) + "页")
                u = sys.argv[0] + "?mode=11&name=" + urllib.quote_plus(name) + "&url=" + urllib.quote_plus(url) + "&page=" + str(num+1) + "&year=" + str(year) + "&month=" + month
                xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, True, totalItems)        

    xbmcplugin.setContent(int(sys.argv[1]), name)
    xbmcplugin.endOfDirectory(int(sys.argv[1])) 
    
##################################################################################
# Routine to update video list as per user selected filters
# - for 综艺
# - 按年份 (Year)
##################################################################################
def updateListVariety(name, url, page, year, month, listpage):
    change = False
    dialog = xbmcgui.Dialog()
    datelist = getListVariety(listpage)
    list = []
    # extract unique year list
    for x in datelist:
        if x[0] not in list: list.append(x[0])
    sel = dialog.select('年份', list)
    if sel != -1:
        year = list[sel]
        change = True

    list = [x[1] for x in datelist if x[0] == year]        
    sel = dialog.select('月份', list)
    if sel != -1:
        month = list[sel]
        change = True

    if change: progListVariety(name, url, '1', year, month)
    else: return(name, url, '1', year, month)

##################################################################################
# Routine to display Singer list for selection
# - for 明星
# - selected page & filters
# - Video series list
# - user selectable pages 
##################################################################################
def progListStar(name, url, page, alphabet, area, prof, gender):
    link = getHttpData(url)
    # Extract filter list for user selection - list order valid on first entry only
    listpage = re.compile('<div class="list_r">(.+?)<p class="foldbox on" id="tagCtr">').findall(link)[0]

    # fetch user specified parameters
    alphabetlist, arealist, proflist = getListStar(listpage)
    if re.search('全部',alphabet): alphabet = '全部'
    fltrAlphabet = fetchID(alphabetlist, alphabet)
    if re.search('全部',area): area = '全部'
    fltrArea = fetchID(arealist, area)
    if re.search('全部',prof): prof = '全部'
    fltrProf = fetchID(proflist, prof)
    if re.search('全部',gender): gender = '全部'
    fltrGender = fetchID(GENDER_LIST, gender) 
  
    # Video site parameters definitions:
    # [明星:] http://so.letv.com/starlist/i-1_w-1_a-1_g-1_p1.html
    # i = alphabet (a~z; i-1:all) 
    # w = profession category (w-1:all; w1~8:演员;导演;主持人;歌手;编剧;摄像;制片人;讲师)
    # a = area (a-1:all; a1:中国大陆 ...)
    # g = gender (g-1:all; g1:男; g2:女)
    # p = page number
            
    # construct url based on user selected filter ID's
    url = 'http://so.letv.com/starlist/' + fltrAlphabet + fltrProf + fltrArea + fltrGender + '_p'
    if page: currpage = int(page)
    else: currpage = 1
    url += page + '.html'

    if re.search(alphabet,'全部'): alphabet = '全部字母'
    if re.search(area,'全部'): area = '全部地区'
    if re.search(prof,'全部'): prof = '全部职业'
    if re.search(gender,'全部'): gender = '全部性别'

    link = getHttpData(url)
    match = re.compile('<dl class="StarDL">(.+?)</dl>', re.DOTALL).findall(link)                  
    totalItems = len(match)

    # Fetch & build video titles list for user selection, highlight user selected filter  
    li = xbmcgui.ListItem(name + '（第' + str(currpage) + '页）【[COLOR FFFF0000]' + alphabet + '[/COLOR]/[COLOR FF00FF00]' + area + '[/COLOR]/[COLOR FFFFFF00]' + prof + '[/COLOR]/[COLOR FF00FFFF]' + gender + '[/COLOR]】（按此选择）')
    u = sys.argv[0] + "?mode=22&name=" + urllib.quote_plus(name) + "&url=" + urllib.quote_plus(url) + "&alphabet=" + urllib.quote_plus(alphabet) + "&area=" + urllib.quote_plus(area) + "&prof=" + urllib.quote_plus(prof) + "&gender=" + gender + "&listpage=" + urllib.quote_plus(listpage)
    xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, True, totalItems)

    for i in range(0, len(match)):
        match1 = re.compile('<img src="(.+?)"').search(match[i])
        p_thumb = match1.group(1)
        match1 = re.compile('<dd class="tit"><a href="(.+?)".+?>(.+?)</a>').search(match[i])
        p_url = match1.group(1)
        p_name = p_list = match1.group(2)    
        match1 = re.compile('<dd>(职业：.+?)</dd>').search(match[i])
        p_prof = match1.group(1)
 
        p_title=''
        match1 = re.compile('<a href=.+?title=.+?target=.+?>(《.+?》)</a>').findall(match[i])
        for title in match1: p_title += title
        p_list += ' ~ [' + p_prof +'] ' + p_title
 
        li = xbmcgui.ListItem(str(i + 1) + '. ' + p_list, iconImage='', thumbnailImage=p_thumb)
        u = sys.argv[0] + "?mode=23" + "&name=" + urllib.quote_plus(p_name) + "&url=" + urllib.quote_plus(p_url) + "&thumb=" + urllib.quote_plus(p_thumb)
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, True, totalItems)

    # Fetch and build user selectable page number
    matchp = re.compile('<div class="page">(.+?)</div>', re.DOTALL).findall(link)
    if len(matchp): 
        matchp1 = re.compile('<a href=".+?">([0-9]+)</a>', re.DOTALL).findall(matchp[0])    
        if len(matchp1):
            plist=[str(currpage)]
            for num in matchp1:
                if num not in plist:
                    plist.append(num)
                    li = xbmcgui.ListItem("... 第" + num + "页")
                    u = sys.argv[0] + "?mode=21&name=" + urllib.quote_plus(name) + "&url=" + urllib.quote_plus(url) + "&page=" + num + "&alphabet=" + alphabet + "&area=" + area + "&prof=" + prof + "&gender=" + gender
                    xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, True, totalItems)        

    xbmcplugin.setContent(int(sys.argv[1]), 'movies')
    xbmcplugin.endOfDirectory(int(sys.argv[1]))
    
##################################################################################
# Routine to update video list as per user selected filters
# - for 明星
# - 按字母  (Categories)
# - 按地区 (Areas)
# - 按职业 (Professional)
# - 按性别 (Gender)
##################################################################################
def updateListStar(name, url, page, alphabet, area, prof, gender, listpage):
    change = False
    dialog = xbmcgui.Dialog()
    alphabetlist, arealist, proflist = getListStar(listpage)

    list = [x[1] for x in alphabetlist]
    sel = dialog.select('字母', list)
    if sel != -1:
        alphabet = alphabetlist[sel][1]
        change = True                   
    list = [x[1] for x in arealist]
    sel = dialog.select('地区', list)
    if sel != -1:
        area = arealist[sel][1]
        change = True
    list = [x[1] for x in proflist]
    sel = dialog.select('职业', list)
    if sel != -1:
        prof = proflist[sel][1]
        change = True
    list = [x[1] for x in GENDER_LIST]
    sel = dialog.select('性别', list)
    if sel != -1:
        gender = GENDER_LIST[sel][1]
        change = True
        
    if change: progListStar(name, url, '1', alphabet, area, prof, gender)
    else: return(name, url, '1', alphabet, area, prof, gender)        
          
##################################################################################
# Routine to extract video series selection menu for user playback
# - for 明星
##################################################################################
def progListStarVideo(name, url, thumb):
    link = getHttpData(url)
    
    li = xbmcgui.ListItem('【[COLOR FFFFFF00][' + name + '][/COLOR] | [COLOR FF00FFFF] [选择: ' + name + '][/COLOR]】', iconImage='', thumbnailImage=thumb)
    u = sys.argv[0]+"?mode=6&name="+urllib.quote_plus(name)+"&url="+urllib.quote_plus(url)+"&thumb="+urllib.quote_plus(thumb) 
    xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, True)
   
    matchp = []
    # fetch and build the video series list
    match = re.compile('<div class="video">.+?<div class="list">(.+?)</div>').findall(link)
    matchv = re.compile('<dl class="w96">(.+?)</dl>').findall(match[0])
    matchp.append(matchv)
       
    match = re.compile('<div class="newMusic">.+?<div class="list">(.+?)</div>').findall(link)
    for j in range(0, len(match)):
        matchm = re.compile('<dl class="w140">(.+?)</dl>').findall(match[j])              
        matchp.append(matchm)    
    
    for j in range(0, len(matchp)):
        totalItems = len(matchp[j])
        for i in range(0, len(matchp[j])):
            match1 = re.compile('<dt><a target="_blank" href="(.+?)"[\s]*title="(.+?)"><img.+?src="(.+?)"').search(matchp[j][i])
            p_url = match1.group(1)
            p_name = p_name = match1.group(2)
            p_img = match1.group(3)
            p_list = str(j) + str(i+1) + ': ' + p_name
                 
            li = xbmcgui.ListItem(p_list, iconImage='', thumbnailImage=p_img)
            u = sys.argv[0] + "?mode=10&name=" + urllib.quote_plus(p_name) + "&url=" + urllib.quote_plus(p_url)
            xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, False, totalItems)
    xbmcplugin.setContent(int(sys.argv[1]), name)
    xbmcplugin.endOfDirectory(int(sys.argv[1]))
       
##################################################################################
# Routine to fetch and build the ugc selection menu
# - for categories not in VIDEO_LIST
# - selected page & filters (user selectable)
# - ugc items list
# - user selectable pages
##################################################################################
def progListUgc(name, url):
    link = getHttpData(url)
    match = re.compile('<div class="soyall">(.+?)<div class="clear">').findall(link)
    currpage = re.compile('.+?_p([0-9]+).html').findall(url)[0]
        
    # Fetch & build ugc list for user selection      
    match = re.compile('<dl class="tvinfo2 top10">(.+?)</dl>').findall(match[0])
    totalItems = len(match)   
    li = xbmcgui.ListItem(name + '（第' + str(currpage) + '页）[COLOR FF00FFFF]【' + name + '】[/COLOR]')
    u = sys.argv[0] + "?mode=8&name=" + urllib.quote_plus(name) + "&url=" + urllib.quote_plus(url)
    xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, True, totalItems)
 
    for i in range(0, len(match)):
        match1 = re.compile('<dt><a target="_blank" title="(.+?)" href="(.+?)">').search(match[i])
        p_name = p_list = match1.group(1)
        p_url = match1.group(2)
        
        match1 = re.compile('<dd>(片长：[:0-9]+)[ ]*</dd>').search(match[i])      
        if match1: p_list += '  [' + match1.group(1) + ']' 
          
        match1 = re.compile('<img alt=.+?src="(.+?)"></a></dt>').search(match[i])
        p_thumb = match1.group(1)
            
        li = xbmcgui.ListItem(str(i + 1) + '. ' + p_list, iconImage='', thumbnailImage=p_thumb)
        u = sys.argv[0] + "?mode=10&name=" + urllib.quote_plus(p_name) + "&url=" + urllib.quote_plus(p_url) + "&thumb=" + urllib.quote_plus(p_thumb)
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, False, totalItems)
            
    # Fetch and build user selectable page number 
    matchp = re.compile('<div class="page">(.+?)</div>').findall(link)
    if len(matchp): matchp1 = re.compile('<a href="(.+?)">([0-9]+)</a>').findall(matchp[0])      
    if len(matchp1):
        plist=[]
        for url, num in matchp1:
            if num not in plist:
                plist.append(num)
                li = xbmcgui.ListItem("... 第" + num + "页")
                u = sys.argv[0] + "?mode=8&name=" + urllib.quote_plus(name) + "&url=" + urllib.quote_plus(url)
                xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, True, totalItems) 
    xbmcplugin.setContent(int(sys.argv[1]), 'movie')
    xbmcplugin.endOfDirectory(int(sys.argv[1]))
  
#################################################################################
# Get user input for LeTV site search
##################################################################################
def searchLetv():
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
# Routine to search LeTV site based on user given keyword for:
# a. video episode List for each found provider
# b. movie from each found provider
# c. ugc for each found provider
##################################################################################
def letvSearchList(name, url, page): 
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
    match = re.compile('{v:(.+?),p:""}').findall(link)[0]
    matchv = re.compile('"(.+?)"').findall(match)
    if matchv:
       for j in range(len(matchv)):
            if matchv[j] == "": continue
            #algorithm to generate the video link code
            vid = matchv[j][24:]  # extract max VID code size
            vidcode = re.split('dj9i', vid)
            if vidcode:                 
                vid = vidcode[0] + "dg=="
            else:
                vidcode = re.split('bHY/', vid)
                if vidcode:                 
                    vid = vidcode[0] + "bHY="
                else:
                    vidcode = re.split('Zmx2', vid)
                    if vidcode:                 
                        vid = vidcode[0] + "Zmx2"

            url = 'http://g3.letv.cn/vod/v1/' + vid + '?format=1&b=388&expect=3&host=www_letv_com&tag=letv&sign=free'
            link = getHttpData(url)
            link = link.replace("\/", "/")
            match = re.compile('{.+?"location": "(.+?)" }').findall(link)
            if match:
                for i in range(len(match)):
                    p_name = name +' ['+ VIDEORES[i] +']' 
                    listitem = xbmcgui.ListItem(p_name, thumbnailImage = __addonicon__)
                    listitem.setInfo(type="Video",infoLabels={"Title":p_name})
                    playlist.add(match[i], listitem)
#                break # proceed if only first video link access failed
            else:
                dialog = xbmcgui.Dialog()
                ok = dialog.ok(__addonname__, '无法播放：未匹配到视频文件，请稍侯再试')  
       xbmc.Player().play(playlist)
    else:
       dialog = xbmcgui.Dialog()
       ok = dialog.ok(__addonname__, '无法播放：需付款费，请选择其它视频')  

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
    ok = dialog.ok(__addonname__,'抱歉! 此视频播放还未完成，请选择其它节目')             
                              
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
url = None
name = None
id = None
page = '1'
cat = None
area = None
year = None
month = None
order = None
thumb = None
listpage = None
alphabet = None
prof = None
gender = None
mode = None

try:
    url = urllib.unquote_plus(params["url"])
except:
    pass
try:
    name = urllib.unquote_plus(params["name"])
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
    cat = urllib.unquote_plus(params["cat"])
except:
    pass
try:
    area = urllib.unquote_plus(params["area"])
except:
    pass
try:
    year = urllib.unquote_plus(params["year"])
except:
    pass
try:
    month = urllib.unquote_plus(params["month"])
except:
    pass
try:
    order = urllib.unquote_plus(params["order"])
except:
    pass
try:
    alphabet = urllib.unquote_plus(params["alphabet"])
except:
    pass
try:
    prof = urllib.unquote_plus(params["prof"])
except:
    pass
try:
    gender = urllib.unquote_plus(params["gender"])
except:
    pass
try:
    thumb = urllib.unquote_plus(params["thumb"])
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
elif mode == 4:
    updateListMovie(name, id, page, cat, area, year, order, listpage)
elif mode == 5:
    progListSeries(name, url, thumb)
elif mode == 6:
    updateListSeriess(name, id, thumb, page)
elif mode == 8:
    progListUgc(name, url)
elif mode == 10:
    PlayVideoLetv(name,url)
  
elif mode == 11:
    progListVariety(name, url, page, year, month)
elif mode == 12:
    updateListVariety(name, url, page, year, month, listpage)
   
elif mode == 21:
    progListStar(name, url, page, alphabet, area, prof, gender)
elif mode == 22:
    updateListStar(name, url, page, alphabet, area, prof, gender, listpage)
elif mode == 23:
    progListStarVideo(name, url, thumb)

elif mode == 31:
    searchLetv()
elif mode == 32:
    letvSearchList(name, url, page)
elif mode == 33:
    episodeList(name,url)

elif mode == 50:
    getInfo(name, id, thumb)

elif mode == 99:
    searchUndefined(name, url)
       