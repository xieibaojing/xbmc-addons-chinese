# -*- coding: utf-8 -*-
import xbmc, xbmcgui, xbmcplugin, xbmcaddon, urllib2, urllib, re, string, sys, os, gzip, StringIO
import math, os.path, httplib, time
import cookielib
import ChineseKeyboard

########################################################################
# 搜库 -太极拳(Soku) by cmeng
########################################################################
# Version 1.0.1 2012-07-09
# a. Share common routine
# b. Improve some UI display

# See changelog.txt for previous history
########################################################################

# Plugin constants 
__addonname__   = "搜库-太极拳(Soku)"
__addonid__     = "plugin.video.soku"
__addon__ = xbmcaddon.Addon(id=__addonid__)
__addonicon__   = os.path.join( __addon__.getAddonInfo('path'), 'icon.png' )
__settings__    = xbmcaddon.Addon(id=__addonid__)
__profile__     = xbmc.translatePath( __settings__.getAddonInfo('profile') )
cookieFile = __profile__ + 'cookies.soku'

UserAgent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'
TC_LIST =['24式太极拳','42式太极拳','杨式太极拳','陈式太极拳','陈氏太极拳','太极拳','太极拳实战','太极拳教学视频','太极拳教学视频完整版']

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
        response.close()
        cj.save(cookieFile, ignore_discard=True, ignore_expires=True)

    httpdata = re.sub('\r|\n|\t', '', httpdata)
    match = re.compile('<meta.+?charset=["]*(.+?)"').findall(httpdata)
    if len(match):
        charset = match[0].lower()
        if (charset != 'utf-8') and (charset != 'utf8'):
            httpdata = unicode(httpdata, charset,'replace').encode('utf8')
    return httpdata

##################################################################################
# Main menu - 搜库网络 (Soku) 
##################################################################################
def mainMenu():   
    li = xbmcgui.ListItem('[COLOR F0F0F0F0]0. Soku 搜库网:[/COLOR][COLOR FF00FF00]【请输入搜索内容】[/COLOR]')
    u=sys.argv[0]+"?mode=31"
    xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, True)
    
    # compile the url for video specified in TC_LIST
    p_url = 'http://www.soku.com/search_video/q_' #+'太极拳_orderby_1_page_1'
    totalItem = len(TC_LIST)
    for i in range(0, totalItem):
        name = TC_LIST[i]
        url = p_url + urllib.quote(name)
        li = xbmcgui.ListItem(str(i+1) + '. ' + name)
        u = sys.argv[0] + "?mode=32&name=" + name + "&url=" + urllib.quote_plus(url)+ "&page=1"
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, True,   totalItem)
    xbmcplugin.setContent(int(sys.argv[1]), 'movies')
    xbmcplugin.endOfDirectory(int(sys.argv[1]))  

##################################################################################
# Routine to fetch and build the video series selection menu
# - for 电视剧  & 动漫
# - selected page & filters (user selectable)
# - Video series list
# - user selectable pages
##################################################################################
def progListSeries(name, url, thumb, page):
    link = getHttpData(url)
    
    #li = xbmcgui.ListItem('【[COLOR FFFFFF00][' + name + '][/COLOR] | [COLOR FF00FFFF] [选择: ' + name + '][/COLOR]】', iconImage='', thumbnailImage=thumb)
    li = xbmcgui.ListItem(name + '（第' + str(page) + '页）[COLOR FF00FFFF]选择:【' + name + '】[/COLOR]')
    u = sys.argv[0]+"?mode=5&name="+urllib.quote_plus(name)+"&url="+urllib.quote_plus(url)+"&thumb="+urllib.quote_plus(thumb) 
    xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, True)
   
    # fetch and build the video series list
    matchp=re.compile('<div class="items">(.+?)<!-- .items -->').findall(link)
    match = re.compile('<ul class="v">(.+?)</ul>').findall(matchp[0]) 
    totalItems = len(match)

    for i in range(0, len(match)):
        p_url = re.compile('href="(.+?)"').search(match[i]).group(1)
                    
        p_name = p_list = re.compile('title="(.+?)"').search(match[i]).group(1)
        match1 = re.compile('<li class="v_thumb"><.+?src="(.+?)"').search(match[i])
        p_thumb = match1.group(1).strip(' ')
               
        p_ishd = re.compile('<li class="v_ishd"><span ([^>]*)></span>').findall(match[i])
        if len(p_ishd) > 0:
            if p_ishd[0].find('ico__SD') > 0:
                p_list += ' [超清]'
            elif p_ishd[0].find('ico__HD') > 0:
                p_list += ' [高清]'
            else:
                p_res = 0

        match1 = re.compile('<li class="v_time"><span.+?>([:0-9]+)</span>').search(match[i])
        if match1:
            p_time = match1.group(1)
            p_list += ' [' + p_time + ']'
        p_list = str(i+1) + ': ' + p_list

        #print "url,name,thumb,time, plist", str(i) , p_url, p_name, p_thumb, p_time, p_list

        li = xbmcgui.ListItem(p_list, iconImage=p_thumb, thumbnailImage=p_thumb)
        u = sys.argv[0] + "?mode=10&name=" + urllib.quote_plus(p_name) + "&url=" + urllib.quote_plus(p_url) + "&thumb=" + urllib.quote_plus(p_thumb)
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, False, totalItems)
            
    # Fetch and build user selectable page number
    matchp = re.compile('<div class="qPager"><div.+?/div>(.+?)</div>').findall(link)[0]
    if len(matchp): 
        matchp1 = re.compile('<li><a onclick=.+?href="(.+?)">([1-9]+)</a>').findall(matchp) 
        print matchp, matchp1
        if len(matchp1):
            plist=[str(page)]
            for p_url, num in matchp1:
                if num not in plist:
                    plist.append(num)
                    url = 'http://www.youku.com' + p_url
                    li = xbmcgui.ListItem("... 第" + num + "页")
                    u = sys.argv[0] + "?mode=5&name=" + urllib.quote_plus(name) + "&url=" + urllib.quote_plus(url)+ urllib.quote_plus(p_url) + "&thumb=" + urllib.quote_plus(p_thumb) + "&page=" + str(num)
                    xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, True, totalItems)   
    
    #http://www.youku.com/show_eplist/showid_z2274a0d0b67d11e0a046_type_pic_from_ajax_page_2.html?__rt=1&__ro=eplist
    xbmcplugin.setContent(int(sys.argv[1]), 'movie')
    xbmcplugin.endOfDirectory(int(sys.argv[1]))
  
#################################################################################
# Get user input for Soku site search
##################################################################################
def searchSoku():
    result=''
    keyboard = ChineseKeyboard.Keyboard('','请输入搜索内容')
    xbmc.sleep( 1500 )
    keyboard.doModal()
    if (keyboard.isConfirmed()):
        keyword = keyboard.getText()
        p_url = 'http://www.soku.com/search_video/q_'
        url = p_url + urllib.quote(keyword)
        sokuSearchList(keyword,url,'1')
    else: return
        
##################################################################################
# Routine to search Soku site based on user given keyword for:
##################################################################################
def sokuSearchList(name, url, page):
    # construct url based on user selected item
    # 'http://www.soku.com/search_video/q_太极拳_orderby_1_page_1'    
    p_url = url + '_orderby_1_page_' + page + '.htm'
    link = getHttpData(p_url)

    li = xbmcgui.ListItem('[COLOR FFFF0000]当前搜索: 第' + page + '页[/COLOR][COLOR FFFFFF00] (' + name + ')[/COLOR]【[COLOR FF00FF00]' + '请输入新搜索内容' + '[/COLOR]】')
    u = sys.argv[0] + "?mode=31&name=" + urllib.quote_plus(name) + "&url=" + urllib.quote_plus(url) + "&page=" + urllib.quote_plus(page)
    xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, True)
    
    #########################################################################
    # Video listing for all found related episode title
    #########################################################################
    match = re.compile('<div class="stat">共找到(.+?)个结果</div>').search(link)
    if match: totalItems = int(match.group(1))
    else: totalItems = 0;
    if totalItems == 0:
        li=xbmcgui.ListItem('抱歉，没有找到[COLOR FFFF0000] '+name+' [/COLOR]的相关视频')
        xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,False)
    else:
        #addItem('', '第'+str(currpage)+'/'+str(totalpages)+'页,【优酷站内搜索"[COLOR FFFF0000]'+name+'[/COLOR]",共找到'+str(totalItems)+'个视频】', getPluginIcon(plugin))
        # 2011/11/28 update start (Added the direct search result)
        matchp=re.compile('<div class="item[s]*">(.+?)<!--\s*item[s]* end\s*-->').findall(link)

        k = 0
        for j in range(0, len(matchp)):
            item = matchp[j]
            #v_link = re.compile('<li class="base_name">(.+?)</li>').findall(item)[0]
            #v_link = re.compile('href="([^"]*)"').findall(v_link)[0]
            #if (v_link.find('http://www.youku.com') < 0): continue

            if (item.find('<div class="tv">') > -1):
                p_type = 'tv'
                mode = '5'
            elif (item.find('<div class="movie">') > -1):
                p_type = 'movie'
                mode = '10'
            else:
                p_type = 'other'
                mode = '10'
        
            match = re.compile('<ul class="v">(.+?)</ul>').findall(matchp[j]) 
            if len(match) ==0:
                match = re.compile('<ul class="p pv">(.+?)</ul>').findall(matchp[j])
            totalItems = len(match)

            for i in range(0, len(match)):
                p_url = re.compile('href="(.+?)"').search(match[i]).group(1)
                if p_url.split('/')[0] <> 'http:':
                    p_url = 'http://www.soku.com' + p_url
                #p_id = p_url.split('/')[-1].split('.')[0][3:]
                    
                p_name = p_list = re.compile('title="(.+?)"').search(match[i]).group(1)
                match1 = re.compile('<li class="[vp]+_thumb"><.+?src="(.+?)"').search(match[i])
                p_thumb = match1.group(1).strip(' ')
                
                if p_type=='tv':
                    p_list += '【电视剧】'
                elif p_type=='movie': 
                    p_list += '【电影】'
                
                p_ishd = re.compile('<li class="[vp]+_ishd"><span ([^>]*)></span>').findall(match[i])
                if len(p_ishd) > 0:
                    if p_ishd[0].find('ico__SD') > 0:
                        p_list += ' [超清]'
                    elif p_ishd[0].find('ico__HD') > 0:
                        p_list += ' [高清]'
                    else:
                        p_res = 0

                match1 = re.compile('<li class="v_time"><span.+?>([:0-9]+)</span>').search(match[i])
                if match1:
                    p_time = match1.group(1)
                    p_list += ' [' + p_time + ']'
                    
                match1 = re.compile('<li class="v_stat"><label>播放:</label><span.+?">([,0-9]+)</span>').search(match[i])
                if match1:
                    p_stat = match1.group(1)
                    p_list += ' [播放:' +  p_stat + ']'

                k +=1
                p_list = str(k) + ': ' + p_list
                #p_list = str(j) + str(i+1) + ': ' + p_list
                #print "url,id,name,thumb,time, plist, ptype", str(j) + str(i) , p_url, p_id, p_name, p_thumb, p_time, p_list, p_type

                li = xbmcgui.ListItem(p_list, iconImage=p_thumb, thumbnailImage=p_thumb)
                u = sys.argv[0] + "?mode=" + mode + "&name=" + urllib.quote_plus(p_name) + "&url=" + urllib.quote_plus(p_url) + "&thumb=" + urllib.quote_plus(p_thumb)+ "&page=" + urllib.quote_plus(page)
                if mode=='10':
                    xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, False, totalItems)
                else:
                    xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, True, totalItems)
 
    # Fetch and build user selectable page number
    matchp = re.compile('<div class="pager">(.+?)</div>').findall(link)
    if len(matchp): 
        matchp1 = re.compile('<a href=.+?>([1-9]+)</a>').findall(matchp[0])    
        if len(matchp1):
            plist=[str(page)]
            for num in matchp1:
                if num not in plist:
                    plist.append(num)
                    li = xbmcgui.ListItem("... 第" + num + "页")
                    u = sys.argv[0] + "?mode=32&name=" + urllib.quote_plus(name) + "&url=" + urllib.quote_plus(url) + "&page=" + str(num)
                    xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, True, totalItems)        

    xbmcplugin.setContent(int(sys.argv[1]), 'movies')
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

##################################################################################
# Youku Video Link Decode Algorithm & Player
##################################################################################
def PlayVideo(name,url):
    RES_LIST = ['normal', 'high', 'super']
    videoRes = int(__addon__.getSetting('video_resolution'))

    link = getHttpData("http://www.flvcd.com/parse.php?kw="+url+"&format="+RES_LIST[videoRes])
    match = re.compile('"(http://f.youku.com/player/getFlvPath/.+?)" target="_blank"').findall(link)
    if len(match)>0:
        playlist=xbmc.PlayList(1)
        playlist.clear()
        for i in range(0,len(match)):
            listitem = xbmcgui.ListItem(name, thumbnailImage = __addonicon__)
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
page = '1'
thumb = None
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
    page = urllib.unquote_plus(params["page"])
except:
    pass
try:
    thumb = urllib.unquote_plus(params["thumb"])
except:
    pass
try:
    mode = int(params["mode"])
except:
    pass

if mode == None:
    mainMenu()
elif mode == 5:
    progListSeries(name, url, thumb, page)
elif mode == 10:
    PlayVideo(name,url)

elif mode == 31:
    searchSoku()
elif mode == 32:
    sokuSearchList(name, url, page)

       