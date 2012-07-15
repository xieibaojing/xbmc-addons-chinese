# -*- coding: utf-8 -*-
import urllib,urllib2,re,os,xbmcplugin,xbmcgui,xbmc
import xbmcaddon
import cookielib
import ChineseKeyboard

##########################################################################
# 音悦台MV
##########################################################################
# Version 1.5.1 2012-07-15 (cmeng)
# - Playlist needs to be cleared
# - Stop xbmc from throwing error while fetching video link 
##########################################################################

__addonname__ = "音悦台MV"
__addonid__   = "plugin.video.yinyuetai"
__addon__     = xbmcaddon.Addon(id=__addonid__)
__addonicon__ = os.path.join( __addon__.getAddonInfo('path'), 'icon.png' )
__settings__  = xbmcaddon.Addon(id=__addonid__)
__icon__      = xbmc.translatePath( __settings__.getAddonInfo('icon') )
__profile__   = xbmc.translatePath( __settings__.getAddonInfo('profile') )

cookieFile    = __profile__ + 'cookies.yinyuetai'
UserAgent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'

MVR_LIST = [['MV','全部推荐MV'],['ML','内地推荐'],['HT','港台推荐'],['US','欧美推荐'],['KR','韩语推荐'],['JP','日语推荐']]
MVF_LIST = [['newRecommend','最新推荐悦单'],['newFavorite','最新收藏悦单'],['newComment','最新评论悦单'],['newCreate','最新创建悦单'],['hotView','热门播放悦单'],['hotRecommend','热门推荐悦单'],['hotFavorite','热门收藏悦单'],['hotComment','热门评论悦单'],['promo','编辑推荐悦单'],['all','全部悦单']]
MVO_LIST = [['all','全部热门'],['today','24小时热门'],['week','本周热门'],['month','本月热门']]
AREA_LIST = [['','全部地区'],['ML','内地'],['HT','港台'],['US','欧美'],['KR','韩语'],['JP','日语']]
GS_LIST = [['','全部歌手'],['Boy','男歌手'],['Girl','女歌手'],['Combo','乐队/组合']]

##################################################################################
# Routine to fetch url site data using Mozilla browser
# - delete '\r|\n|\t' for easy re.compile
# - do not delete \s <space> as some url include spaces
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
    charset=''
    req = urllib2.Request(url)
    req.add_header('User-Agent', UserAgent)
    try:
        response = opener.open(req)
    except urllib2.HTTPError, e:
        httpdata = e.read()
    except urllib2.URLError, e:
        httpdata = "IO Timeout Error"
    else:
        httpdata = response.read()
        if response.headers.get('content-encoding', None) == 'gzip':
            httpdata = gzip.GzipFile(fileobj=StringIO.StringIO(httpdata)).read()
        charset = response.headers.getparam('charset')
        cj.save(cookieFile, ignore_discard=True, ignore_expires=True)
        response.close()

    httpdata = re.sub('\r|\n|\t', '', httpdata)
    match = re.compile('<meta.+?charset=["]*(.+?)"').findall(httpdata)
    if len(match):
        charset = match[0]
    if charset:
        charset = charset.lower()
        if (charset != 'utf-8') and (charset != 'utf8'):
            httpdata = httpdata.decode(charset, 'ignore').encode('utf8', 'ignore')
    return httpdata

##################################################################################
def get_realurl(url):
    return 'http://www.yinyuetai.com' + url

##################################################################################
def get_flv_url(url):
    # http://www.flvcd.com/parse.php?flag=&format=&kw=http://3A%2F%2Fwww.yinyuetai.com%2Fvideo%2F389970&sbt=%BF%AA%CA%BCGO%21
    videoRes = int(__addon__.getSetting('video_resolution'))

    p_url = "http://www.flvcd.com/parse.php?kw="+url+"&format="+str(videoRes)
    for i in range(10): # Retry specified trials before giving up
       try:
            link = getHttpData(p_url)
            match=re.compile('下载地址：\s*<a href="(.+?)" target="_blank" class="link"').findall(link)
            if len(match): return match[0]
       except:
           pass

##################################################################################
# Get imgae from local storage if available
# Fetch from Web if none found
##################################################################################
def get_Thumb(icon):
    if len(icon) < 2:
        return __icon__

    url = icon.split('?')[0]
    len_http = len(url.split('/')[2]) + 8
    pic = __profile__ + url[len_http:]

    if not os.path.isfile(pic):
        if not os.path.isdir(os.path.dirname(pic)):
            os.makedirs(os.path.dirname(pic))
        try:
            pic=urllib.urlretrieve(url, pic)[filename]
        except:
            pass
    return pic

##################################################################################
# Routine to extract url ID from array based on given selected filter
##################################################################################
def fetchID(dlist, idx):
    for i in range(0, len(dlist)):
        if dlist[i][1] == idx:
            return dlist[i][0]
    return ''

##################################################################################
def addDir(name,url,mode,pic,isDir=True,sn=''):
    if sn != '': sn=str(sn)+". "
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
    ok=True
    li=xbmcgui.ListItem(sn+name,'', pic, pic)
    li.setInfo( type="Video", infoLabels={ "Title": name } )
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=li,isFolder=isDir)
    return ok

##################################################################################
# Yinyuetai Main Menu
# 周榜 video playback can either be auto or manual via add-on setting
##################################################################################
def MainMenu(ctl):
    videoPlayback = int(__addon__.getSetting('video_playback'))
    if videoPlayback == 0:
        vlist = [x for x in ctl[None][2]]
    else:
        vlist = [x for x in ctl[1][2]]
    j=0
    for mode in vlist:
        j+=1
        name = ctl[mode][1]
        url = get_realurl(ctl[mode][2])
        isDir = ctl[mode][3]
        pic = __addonicon__
        addDir(name,url,mode,pic,isDir,j)
    xbmcplugin.setContent(int(sys.argv[1]), 'movies')
    xbmcplugin.endOfDirectory(int(sys.argv[1]))
    
##################################################################################
# http://www.yinyuetai.com/lookVideo-area/ML/4
##################################################################################
def listRecommendMV(name,cat,page):   
    # fetch user specified parameters
    if cat == None:
        cat = '全部推荐MV'
    fltrCat  = fetchID(MVR_LIST, cat)
    if page is None: page = 1
    #print 'cat,page', name, cat, page
    url = 'http://www.yinyuetai.com/lookVideo-area/'+fltrCat+'?page='+str(page)

    # Fetch & build video titles list for user selection, highlight user selected filter  
    li = xbmcgui.ListItem('[COLOR FF00FFFF]'+__addonname__+'[/COLOR]（第'+str(page)+'页）【[COLOR FFFF0000]'+cat+'[/COLOR]】（按此选择）')
    u = sys.argv[0] + "?mode=5&name="+urllib.quote_plus(name)
    xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, True)
    
    link=getHttpData(url)
    if link == None: return

    try:
        matchs=re.compile('<div class="recommend_mv_list"><ul>(.+?)</ul></div>').findall(link)
        matchli=re.compile('<li>(.+?)</li>').findall(matchs[0])
        totalItems=len(matchli)
        j=0
        for item in matchli:
            url1=re.compile('<a href="(.+?)" target="_blank"><img src="(.+?)" title="(.+?)" alt="(.+?)"/>').findall(item)
            p_url = 'http://www.yinyuetai.com' + url1[0][0]
            #p_thumb = get_Thumb(url1[0][1])
            p_thumb = url1[0][1]
            p_list = p_name = url1[0][2]
            
            artist=re.compile('--<a href="(.+?)" title="(.+?)" class="link_people"').findall(item)
            p_artist = artist[0][1]
               
            j+=1
            p_list = str(j)+'. '+p_name+' ['+p_artist +']'
            #print p_url, p_thumb, p_artist, p_list
                
            li = xbmcgui.ListItem(p_list, iconImage = '', thumbnailImage = p_thumb)
            u = sys.argv[0]+"?mode=100"+"&name="+urllib.quote_plus(p_name)+"&url="+urllib.quote_plus(p_url)+"&thumb="+urllib.quote_plus(p_thumb)
            li.setInfo(type = "Video", infoLabels = {"Title":p_name, "Artist":p_artist})
            xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, False, totalItems)
    except:
        pass
    
    # Fetch and build user selectable page number
    try:
        matchp=re.compile('<div class="page-nav">(.+?)</div>').findall(link)   
        #matchp1=re.compile('<a href="(.+?)">(.+?)</a>').findall(matchp[0])
        matchp1=re.compile('<a href=".+?>([0-9]+)</a>', re.DOTALL).findall(matchp[0])    
        plist=[str(page)]
        for num in matchp1:
            if num not in plist:
                plist.append(num)
                li = xbmcgui.ListItem("... 第" + num + "页")
                u = sys.argv[0] + "?mode=30&name="+urllib.quote_plus(name)+"&cat="+cat+"&page="+num
                xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, True)
    except:
        pass        
    xbmcplugin.setContent(int(sys.argv[1]), 'movies')
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

##################################################################################
# Routine to update video list as per user selected filters
##################################################################################
def performChange(name,cat,page):
    change = False
    dialog = xbmcgui.Dialog()
    list = [x[1] for x in MVR_LIST]        
    sel = dialog.select('推荐MV', list)
    if sel != -1:
        name = MVR_LIST[sel][1]
        cat = MVR_LIST[sel][1]
        change = True

    if change: listRecommendMV(name,cat,1)
    else: return(name,cat,1)

##################################################################################
# http://www.yinyuetai.com/pl/playlist_newRecommend/all
def listFavouriteMV(name,cat,order,page):
    # fetch user specified parameters
    if cat == None:
        cat = '最新推荐悦单'
    fltrCat  = fetchID(MVF_LIST, cat)
    if order == None:
        order = '全部热门'
    fltrOrder  = fetchID(MVO_LIST, order)
    if page is None: page = 1
    #print 'cat,page-after', name, cat, fltrCat, order,fltrOrder, page

    if re.search('热门',cat):
        url = 'http://www.yinyuetai.com/pl/playlist_'+fltrCat+'/'+fltrOrder+'?page='+str(page)
        li = xbmcgui.ListItem('[COLOR FF00FFFF]'+__addonname__+'[/COLOR]（第'+str(page)+'页）【[COLOR FFFF0000]'+cat+'[/COLOR]/[COLOR FF00FF00]'+order+'[/COLOR]】（按此选择）')
    else:
        url = 'http://www.yinyuetai.com/pl/playlist_'+fltrCat+'?page='+str(page)
        li = xbmcgui.ListItem('[COLOR FF00FFFF]'+__addonname__+'[/COLOR]（第'+str(page)+'页）【[COLOR FFFF0000]'+cat+'[/COLOR]】（按此选择）')
  
    # Fetch & build video titles list for user selection, highlight user selected filter  
    u = sys.argv[0] + "?mode=6&name="+urllib.quote_plus(name)
    xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, True)
    
    link=getHttpData(url)
    if link == None: return
    #try:
    for i in range(1):
        matchs=re.compile('<div id="main">(.+?)</ul></div>').findall(link)
        matchli=re.compile('<div class="thumb_box">(.+?)</li>').findall(matchs[0])
        totalItems=len(matchli)
        j=0
        #print 'total', j+1, matchs, totalItems
        for item in matchli:
            match=re.compile('<a href="(.+?)" target="_blank" title="(.+?)"><img src="(.+?)"').findall(item)
            p_url = 'http://www.yinyuetai.com' + match[0][0]
            p_name = match[0][1]
            p_thumb = match[0][2]
            
            p_artist=''
            match=re.compile('target="_blank">(.+?)</a>：').findall(item)
            if len(match): p_artist = match[0]
               
            j+=1
            p_list = str(j)+'. '+p_name
            if p_artist: p_list+=' ['+p_artist +']'
            #print p_url, p_thumb, p_artist, p_list
                
            li = xbmcgui.ListItem(p_list, iconImage = '', thumbnailImage = p_thumb)
            u = sys.argv[0]+"?mode=100"+"&name="+urllib.quote_plus(p_name)+"&url="+urllib.quote_plus(p_url)+"&thumb="+urllib.quote_plus(p_thumb)
            li.setInfo(type = "Video", infoLabels = {"Title":p_name, "Artist":p_artist})
            xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, False, totalItems)
    #except:
    #    pass
    
    # Fetch and build user selectable page number
    try:
        matchp=re.compile('<div class="page-nav">(.+?)</div>').findall(link)   
        #matchp1=re.compile('<a href="(.+?)">(.+?)</a>').findall(matchp[0])
        matchp1=re.compile('<a href=".+?>([0-9]+)</a>', re.DOTALL).findall(matchp[0])    
        plist=[str(page)]
        for num in matchp1:
            if num not in plist:
                plist.append(num)
                li = xbmcgui.ListItem("... 第" + num + "页")
                u = sys.argv[0] + "?mode=31&name="+urllib.quote_plus(name)+"&cat="+cat+"&page="+num
                xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, True)
    except:
        pass        
    xbmcplugin.setContent(int(sys.argv[1]), 'movies')
    xbmcplugin.endOfDirectory(int(sys.argv[1]))
    
##################################################################################
# Routine to update video list as per user selected filters
##################################################################################
def performChangeFavourite(name,cat,order,page):
    change = False
    dialog = xbmcgui.Dialog()
    list = [x[1] for x in MVF_LIST]        
    sel = dialog.select('悦单', list)
    if sel != -1:
        cat = MVF_LIST[sel][1]
        change = True

    if re.search('热门',cat):
        list = [x[1] for x in MVO_LIST]        
        sel = dialog.select('排序方式', list)
        if sel != -1:
           order = MVO_LIST[sel][1]
           change = True

    if change: listFavouriteMV(name,cat,order,1)
    else: return(name,cat,order,1)

##################################################################################
# http://www.yinyuetai.com/fanAll?area=ML&property=Girl&enName=F&page=1
##################################################################################
def listArtist(name,area,geshou,fname,thumb,page):
    # fetch user specified parameters
    if area == None:
        area = '全部地区'
    fltrArea  = fetchID(AREA_LIST, area)
    if geshou == None:
        geshou = '全部歌手'
    fltrGeshou  = fetchID(GS_LIST, geshou)
    if page is None: page = 1
    print 'area...', name, area, geshou, fname, page

    # Fetch & build video titles list for user selection, highlight user selected filter  
    url = 'http://www.yinyuetai.com/fanAll?area='+fltrArea+'&property='+fltrGeshou+'&page='+str(page)
    if fname:
        url += '&enName='+fname
        li = xbmcgui.ListItem('[COLOR FF00FFFF]'+__addonname__+'[/COLOR]（第'+str(page)+'页）【[COLOR FFFF0000]'+area+'[/COLOR]/[COLOR FF00FF00]'+geshou+'[/COLOR]/[COLOR FFFF5555]姓:'+fname+'[/COLOR]】（按此选择）')
    else:
        fname=''
        li = xbmcgui.ListItem('[COLOR FF00FFFF]'+__addonname__+'[/COLOR]（第'+str(page)+'页）【[COLOR FFFF0000]'+area+'[/COLOR]/[COLOR FF00FF00]'+geshou+'[/COLOR]】（按此选择）')
    u = sys.argv[0] + "?mode=7&name="+urllib.quote_plus(name)
    xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, True)    
    
    link=getHttpData(url)
    if link == None: return
    
    #for j in range(1):
    try:
        match=re.compile('<span class="groupcover"(.+?)</li>').findall(link)
        totalItems = len(match)
        for i in range(0, len(match)):
            match1 = re.compile('fanid=.+?<a href="(.+?)"').search(match[i])
            p_url1 = match1.group(1)
            artistid = p_url1.split('/')[2]
            p_url = 'http://www.yinyuetai.com/fanclub/mv-all/'+artistid+'/toNew'
        
            match1 = re.compile('<img.+?src="(.+?)"/>').search(match[i])
            p_thumb = match1.group(1)          

            match1 = re.compile('<div class="info">.+?<a href="(.+?)"').search(match[i])
            p_url2 = match1.group(1)

            match1 = re.compile('class="song" title="(.+?)">').search(match[i])
            p_name = match1.group(1)
               
            p_list = str(i+1)+'. '+p_name
            p_name += ' [COLOR FFFF5555]['+area+'/'+geshou+'][/COLOR]'
            #print p_url, p_thumb, p_artist, p_list
                
            li = xbmcgui.ListItem(p_list, iconImage = '', thumbnailImage = p_thumb)  #name,area,geshou,fname,page
            u = sys.argv[0]+"?mode=33"+"&name="+urllib.quote_plus(p_name)+"&url="+urllib.quote_plus(p_url)+"&thumb="+urllib.quote_plus(p_thumb)+"&page=1"
            li.setInfo(type = "Video", infoLabels = {"Title":p_name})
            xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, True, totalItems)
    except:
        pass    
   
    # Fetch and build user selectable page number
    #for j in range(1):
    try:
        matchp=re.compile('<div class="page-nav">(.+?)</div>').findall(link)   
        matchp1=re.compile('<a href=".+?>([0-9]+)</a>', re.DOTALL).findall(matchp[0])    
        plist=[str(page)]
        for num in matchp1:
            if num not in plist:
                plist.append(num)
                li = xbmcgui.ListItem("... 第" + num + "页")
                u = sys.argv[0]+"?mode=32"+"&name="+urllib.quote_plus(p_name)+"&area="+area+"&gehou="+geshou+"&fname="+fname+"&thumb="+urllib.quote_plus(p_thumb)+"&page="+num
                xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, True)
    except:
        pass        
    xbmcplugin.setContent(int(sys.argv[1]), 'movies')
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

##################################################################################
# http://www.yinyuetai.com/fanAll?area=ML&property=Girl&page=1
# http://www.yinyuetai.com/fanclub/27
##################################################################################
def listArtistMV(name,url,thumb,page):
    # fetch user specified parameters
    if page is None: page = 1
    p_url = url+'/?page='+str(page)
    
    print 'url', url, p_url
    li = xbmcgui.ListItem('[COLOR FF00FFFF]'+__addonname__+'[/COLOR]（第'+str(page)+'页）【[COLOR FF00FF00]'+name+'[/COLOR]】')
    # Fetch & build video titles list for user selection, highlight user selected filter  
    u = sys.argv[0] + "?mode=33&name="+urllib.quote_plus(name)+"&url="+urllib.quote_plus(p_url)+"&thumb="+urllib.quote_plus(thumb)+"&page="+str(page)
    xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, True)

    link=getHttpData(p_url)
    if link == None: return

    #for i in range(1):
    try:
        vlist=re.compile('<div class="mv_list"><ul>(.+?)</ul></div>').findall(link)
        match=re.compile('<div class="thumb"><a target="_blank" title="(.+?)" href="(.+?)"><img.+?src="(.+?)"').findall(vlist[0])    
        totalItems=len(match)
        j=0
        artist=re.compile('<h1>(.+?)</h1>').findall(link)
        p_artist = artist[0]
        for p_name,p_url,p_thumb in match:
            j+=1
            p_url = 'http://www.yinyuetai.com' + p_url              
            p_list = str(j)+'. '+p_name+' ['+p_artist +']'
            #print p_url, p_thumb, p_artist, p_list
                
            li = xbmcgui.ListItem(p_list, iconImage = '', thumbnailImage = p_thumb)
            u = sys.argv[0]+"?mode=100"+"&name="+urllib.quote_plus(p_name)+"&url="+urllib.quote_plus(p_url)+"&thumb="+urllib.quote_plus(p_thumb)
            li.setInfo(type = "Video", infoLabels = {"Title":p_list, "Artist":p_artist})
            xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, False, totalItems)
    except:
        pass

    # Fetch and build user selectable page number
    try:
        matchp=re.compile('<div class="page-nav">(.+?)</div>').findall(link)   
        #matchp1=re.compile('<a href="(.+?)">(.+?)</a>').findall(matchp[0])
        matchp1=re.compile('<a href=".+?>([0-9]+)</a>', re.DOTALL).findall(matchp[0])    
        plist=[str(page)]
        for num in matchp1:
            if num not in plist:
                plist.append(num)
                li = xbmcgui.ListItem("... 第" + num + "页")
                u = sys.argv[0]+"?mode=33"+"&name="+urllib.quote_plus(name)+"&url="+urllib.quote_plus(url)+"&thumb="+urllib.quote_plus(thumb)+"&page="+num
                xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, True)
    except:
        pass        
    xbmcplugin.setContent(int(sys.argv[1]), 'movies')
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

##################################################################################
# Routine to update video list as per user selected filters
##################################################################################
def performChangeGs(name,area,geshou,fname,thumb,page):
    change = False
    dialog = xbmcgui.Dialog()
    list = [x[1] for x in AREA_LIST]        
    sel = dialog.select('地区', list)
    if sel != -1:
        area = AREA_LIST[sel][1]
        change = True

    list = [x[1] for x in GS_LIST]        
    sel = dialog.select('歌手', list)
    if sel != -1:
       geshou = GS_LIST[sel][1]
       change = True

    list = [chr(i) for i in xrange(ord('A'),ord('Z')+1)]
    list.insert(0,'全部')      
    sel = dialog.select('姓', list)
    if sel != -1:
       fname = list[sel]
       if fname=='全部': fname=''
       change = True

    if change:listArtist(name,area,geshou,fname,thumb,1)
    else: return(name,area,geshou,fname,thumb,1)

##################################################################################
#####################To be clear up later ########################################

##################################################################################
def AllMV(url,name,mode):
    addDir('[COLOR FF00FFFF]'+'当前位置：全部MV'+'[/COLOR]',url,mode,'')
    link=getHttpData(url)
    if link == None: return
    match=re.compile('<li title="(.+?)"><a href="(.+?)"(.+?)>(.+?)</a></li>').findall(link)
    total=len(match)
    if total:
        j=0
        for title,url1,cur,name in match:
            j+=1
            mode = 4
            p_url = 'http://www.yinyuetai.com' + url1
            isDir = True
            addDir('全部MV>'+name,p_url,mode,'',isDir,j)

##################################################################################
def ListAllMV(url,name,mode):
    link=getHttpData(url)
    if link == None: return
    curpos1=re.compile('<a href="(.+?)" class="current">(.+?)</a>').findall(link)
    curpos2=re.compile('<li title="(.+?)"><a href="(.+?)" class="current">(.+?)</a></li>').findall(link)
    match0=re.compile('<div class="page-nav">(.+?)</div>').findall(link)
    try:
        curpage=re.compile('<span>(.+?)</span>').findall(match0[0])
        addDir('[COLOR FF00FFFF]'+'当前位置：'+curpos1[0][1]+' [/COLOR]>[COLOR FF00FF00] '+curpos2[0][2]+':[/COLOR] [第'+curpage[0]+'页]'+'',url,mode,'',True)
    except:
        addDir('[COLOR FF00FFFF]'+'当前位置：'+curpos1[0][1]+' [/COLOR]>[COLOR FF00FF00] '+curpos2[0][2]+name+'[/COLOR]',url,mode,'',True)
        pass
    try:
        matchs=re.compile('<div class="mv_list"><ul>(.+?)</ul></div>').findall(link)
        matchli=re.compile('<div class="thumb">(.+?)</div></li>').findall(matchs[0])
        totalItems=len(matchli)
        j=0
        for item in matchli:
            title=re.compile('<div class="title"><a href="(.+?)" title="(.+?)" target="_blank"').findall(item)
            p_name = title[0][1]
            p_url = 'http://www.yinyuetai.com' + title[0][0]
            
            img=re.compile('<img src="(.+?)"').findall(item)
            p_thumb = img[0]
 
            artist=re.compile('<div class="artis">--<a href="(.+?)" title="(.+?)" class="link_people"').findall(item)
            p_artist = artist[0][1]
            
            j+=1
            p_list = str(j)+'. '+p_name+' ['+p_artist +']'
            #print p_url, p_thumb, p_artist, p_list
                
            li = xbmcgui.ListItem(p_list, iconImage = '', thumbnailImage = p_thumb)
            u = sys.argv[0]+"?mode=100"+"&name="+urllib.quote_plus(p_name)+"&url="+urllib.quote_plus(p_url)+"&thumb="+urllib.quote_plus(p_thumb)
            li.setInfo(type = "Video", infoLabels = {"Title":p_list, "Artist":p_artist})
            xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, False, totalItems)
    except:
        pass
    try:
        match1=re.compile('<a href="(.+?)">(.+?)</a>').findall(match0[0])
        for pageurl,pagenum in match1:
            if pagenum.isdigit():
                addDir('..第'+pagenum+'页',get_realurl(pageurl),mode,'')
            else:
                addDir('..'+pagenum,get_realurl(pageurl),mode,'')
    except:
        pass
                    
##################################################################################
##################################################################################
def showFocusMV(url,name,mode):
    curpos = '当前位置：'+name
    addDir('[COLOR FF00FFFF]'+curpos+'[/COLOR]', url, mode,'',True)
    link=getHttpData(url)
    if link == None: return
    matchs=re.compile('<div class="mv_list"><ul>(.+?)</ul></div>').findall(link)
    if len(matchs):
        matchli=re.compile('<div class="thumb">(.+?)</div></li>').findall(matchs[0])
        totalItems=len(matchli)
        if totalItems:
            j=0
            for item in matchli:
                matchp=re.compile('<div class="title"><a href="(.+?)" title="(.+?)" target="_blank" class="song">').findall(item)
                p_list = p_name = matchp[0][1]
                p_url = 'http://www.yinyuetai.com' + matchp[0][0]              

                artist=re.compile('--<a href="(.+?)" title="(.+?)" class="artist" target="_blank">').findall(item)
                p_artist = artist[0][1]
      
                img=re.compile('<img src="(.+?)"').findall(item)
                p_thumb = img[0]
                
                j+=1
                p_list = str(j)+'. '+p_name+' ['+p_artist+']'
                
                li = xbmcgui.ListItem(p_list, iconImage = '', thumbnailImage = p_thumb)
                u = sys.argv[0]+"?mode=100"+"&name="+urllib.quote_plus(p_name)+"&url="+urllib.quote_plus(p_url)+"&thumb="+urllib.quote_plus(p_thumb)
                li.setInfo(type = "Video", infoLabels = {"Title":p_list, "Artist":p_artist})
                xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, False, totalItems)
        xbmcplugin.setContent(int(sys.argv[1]), 'movies')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

##################################################################################
def playFocusMV(url,name,mode):
    link=getHttpData(url)
    if link == None: return
    matchs=re.compile('<div class="mv_list"><ul>(.+?)</ul></div>').findall(link)
    if len(matchs):
        matchli=re.compile('<div class="thumb">(.+?)</div></li>').findall(matchs[0])
        if len(matchli):
            j = 0
            playlist=xbmc.PlayList(1)
            playlist.clear()
            for item in matchli:
                matchp=re.compile('<div class="title"><a href="(.+?)" title="(.+?)" target="_blank" class="song">').findall(item)
                p_name = matchp[0][1]
                p_url = 'http://www.yinyuetai.com' + matchp[0][0]              

                artist=re.compile('--<a href="(.+?)" title="(.+?)" class="artist" target="_blank">').findall(item)
                p_artist = artist[0][1]

                img=re.compile('<img src="(.+?)"').findall(item)
                p_thumb = img[0]
                
                v_url = get_flv_url(p_url)
                if v_url == None: continue
                print 'v_url: ' + v_url,
                j += 1
                p_list = str(j)+'. '+p_name+' ['+p_artist+']'
                
                listitem = xbmcgui.ListItem(p_list, iconImage = '', thumbnailImage = p_thumb)
                listitem.setInfo(type="Video",infoLabels={"Title":p_list})
                playlist.add(v_url, listitem)
                if j == 1: xbmc.Player().play(playlist)

##################################################################################
def playVideo(name,url):
    v_url = get_flv_url(url)
    if v_url:
        playlist=xbmc.PlayList(1)
        #if not xbmc.Player(1).isPlayingVideo:
        playlist.clear()
        #print 'newplaylist', playlist
        listitem = xbmcgui.ListItem(name, thumbnailImage = __addonicon__)
        listitem.setInfo(type="Video",infoLabels={"Title":name})
        playlist.add(v_url, listitem)
        xbmc.Player().play(playlist)
    else:
        if link.find('该视频为加密视频')>0:
            dialog = xbmcgui.Dialog()
            ok = dialog.ok(__addonname__, '无法播放：该视频为加密视频')
        elif link.find('解析失败，请确认视频是否被删除')>0:
            dialog = xbmcgui.Dialog()
            ok = dialog.ok(__addonname__, '无法播放：该视频或为收费节目')

##################################################################################
def get_params():
    param=[]
    paramstring=sys.argv[2]
    if len(paramstring)>=2:
        params=sys.argv[2]
        cleanedparams=params.replace('?','')
        if (params[len(params)-1]=='/'):
            params=params[0:len(params)-2]
        pairsofparams=cleanedparams.split('&')
        param={}
        for i in range(len(pairsofparams)):
            splitparams={}
            splitparams=pairsofparams[i].split('=')
            if (len(splitparams))==2:
                param[splitparams[0]]=splitparams[1]
    return param

##################################################################################

params=get_params()
url=None
name=None
mode=None
artist=None
page=None
area=None
geshou=None
cat=None
order=None
fname=None
thumb=None

try:
    mode=int(params["mode"])
except:
    pass
try:
    url=urllib.unquote_plus(params["url"])
except:
    pass
try:
    thumb=urllib.unquote_plus(params["thumb"])
except:
    pass
try:
    name=urllib.unquote_plus(params["name"])
except:
    pass
try:
    artist=urllib.unquote_plus(params["artist"])
except:
    pass
try:
    area=urllib.unquote_plus(params["area"])
except:
    pass
try:
    geshou=urllib.unquote_plus(params["geshou"])
except:
    pass
try:
    cat=urllib.unquote_plus(params["cat"])
except:
    pass
try:
    order=urllib.unquote_plus(params["order"])
except:
    pass
try:
    page=urllib.unquote_plus(params["page"])
except:
    pass
try:
    fname=urllib.unquote_plus(params["fname"])
except:
    pass
ctl = {
            None : ('MainMenu(ctl)','音悦台MV',(80,81,82,83,84,85,30,31,32)),
            1    : ('MainMenu(ctl)','音悦台MV',(70,71,72,73,74,75,30,31,32)),
            4    : ('ListAllMV(url,name,mode)','全部MV'),

            5    : ('performChange(name,cat,page)',''),
            6    : ('performChangeFavourite(name,cat,order,page)',''),
            7    : ('performChangeGs(name,area,geshou,fname,thumb,page)',''),

            30   : ('listRecommendMV(name,cat,page)','推荐MV','/lookVideo-area/MV',True),   
            31   : ('listFavouriteMV(name,cat,order,page)','推荐悦单','/pl/playlist_newRecommend',True), 
            32   : ('listArtist(name,area,geshou,fname,thumb,page)','歌手','/fanAll',True),
            33   : ('listArtistMV(name,url,thumb,page)','显示歌手MV','/fanAll',True),
            
            70   : ('playFocusMV(url,name,mode)','MV周榜','/index/MV',False),
            71   : ('playFocusMV(url,name,mode)','内地周榜','/index-ml',False),
            72   : ('playFocusMV(url,name,mode)','港台周榜','/index-ht',False),
            73   : ('playFocusMV(url,name,mode)','欧美周榜','/index-us',False),
            74   : ('playFocusMV(url,name,mode)','韩国周榜','/index-kr',False),
            75   : ('playFocusMV(url,name,mode)','日本周榜','/index-jp',False),            

            80   : ('showFocusMV(url,name,mode)','MV周榜','/index/MV',True),
            81   : ('showFocusMV(url,name,mode)','内地周榜','/index-ml',True),
            82   : ('showFocusMV(url,name,mode)','港台周榜','/index-ht',True),
            83   : ('showFocusMV(url,name,mode)','欧美周榜','/index-us',True),
            84   : ('showFocusMV(url,name,mode)','韩国周榜','/index-kr',True),
            85   : ('showFocusMV(url,name,mode)','日本周榜','/index-jp',True),            

            91   : ('AllMV(url,name,mode)','全部MV','/lookAllVideo',True),  # temporary remove seems nothing
            100  : ('playVideo(name,url)',''),
      }
#print 'ctlmode', ctl[mode][0]
exec(ctl[mode][0])
#xbmcplugin.setPluginCategory(int(sys.argv[1]), ctl[mode][1])
#xbmcplugin.endOfDirectory(int(sys.argv[1]))
