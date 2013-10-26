# -*- coding: utf-8 -*-
import xbmc, xbmcgui, xbmcplugin, xbmcaddon, urllib2, urllib, re, string, sys, os, gzip, StringIO
import math, os.path, httplib, time
import cookielib

if sys.version_info < (2, 7):
    import simplejson
else:
    import json as simplejson

########################################################################
# 乐视网(LeTv) by cmeng
########################################################################
# Version 1.2.7 2013-04-07 (cmeng)
# - fix script error in progListVariety (use simplejson)
# - enhance menu list information display

# See changelog.txt for previous history
########################################################################

# Plugin constants 
__addonname__   = "乐视网 (LeTV)"
__addonid__     = "plugin.video.letv"
__addon__ = xbmcaddon.Addon(id=__addonid__)
__addonicon__   = os.path.join( __addon__.getAddonInfo('path'), 'icon.png' )
__settings__    = xbmcaddon.Addon(id=__addonid__)
__profile__     = xbmc.translatePath( __settings__.getAddonInfo('profile') )
cookieFile = __profile__ + 'cookies.letv'

UserAgent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'
VIDEO_LIST = [['list/c1','电影'],['list/c2','电视剧'],['list/c3','动漫'],['list/c11','综艺'],['starlist/i','明星']]
VIDEO_RES = [["标清",'sd'],["高清",'hd'],["普通",''],["未注","null"]]
SORT_LIST = [['_o1','最新更新'],['_o3','最热播放'],['_o7','最新上映'],['_o2','最高评分']]
GENDER_LIST = [['_g-1','全部'],['_g1','男'],['_g2','女']]
COLOR_LIST = ['[COLOR FFFF0000]','[COLOR FF00FF00]','[COLOR FFFFFF00]','[COLOR FF00FFFF]','[COLOR FFFF00FF]']
CLASS_MODE = [['10','电影'],['5','电视剧'],['5','动漫'],['11','综艺'],['21','明星'],['11','娱乐'],['10','音乐']]

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
            break

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
# LeTV Video Link Decode Algorithm & Player
# Extract all the video list and start playing first found valid link
# User may press <SPACE> bar to select video resolution for playback
##################################################################################
def playVideoLetv(name,url):
    VIDEO_CODE=[['bHY=','bHY/'],['dg==','dj9i'],['dg==','dTgm'],['Zmx2','Zmx2']]
    videoRes = 1#int(__addon__.getSetting('video_resolution'))
    link = getHttpData(url)

    match = re.compile('{v:\[(.+?)\]').findall(link)
    #print match
    # link[0]:"标清-SD" ; link[1]:"高清-HD"
    if match:
        matchv = re.compile('"(.+?)"').findall(match[0])
        if matchv:
            playlist=xbmc.PlayList(1)
            playlist.clear()
            if videoRes == 1: # Play selected HD and fallback to SD if HD failed
                vlist = reversed(range(len(matchv)))
            else: # Play selected SD and HD as next item in playlist
                vlist = range(len(matchv))
                
            for j in vlist:
                if matchv[j] == "": continue
                #algorithm to generate the video link code
                vidx = matchv[j].find('MT')
                vidx = -1 # force to start at 24
                if vidx < 0:
                    vid = matchv[j][24:+180]  # extract max VID code length
                else:
                    vid = matchv[j][vidx:+180]
                    
                for k in range(0, len(VIDEO_CODE)):
                    vidcode = re.split(VIDEO_CODE[k][1], vid)
                    if len(vidcode) > 1 :                 
                        vid = vidcode[0] + VIDEO_CODE[k][0]
                        break
                    
                # fail to decipher, use alternate method to play    
                if len(vidcode) == 1:
                    #print 'vidcode: ', vidcode
                    #print "Use alternative player"
                    playVideo(name,url,videoRes)
                    return
                #else:                        
                p_url = 'http://g3.letv.cn/vod/v1/' + vid + '?format=1&b=388&expect=3&host=www_letv_com&tag=letv&sign=free'
                link = getHttpData(p_url)
                link = link.replace("\/", "/")
                match = re.compile('{.+?"location": "(.+?)" }').findall(link)
                if match:
                    for i in range(len(match)):
                        p_name = name +' ['+ VIDEO_RES[j][0] +']' 
                        listitem = xbmcgui.ListItem(p_name, thumbnailImage = __addonicon__)
                        listitem.setInfo(type="Video",infoLabels={"Title":p_name})
                        playlist.add(match[i], listitem)
                        break # skip the rest if any (1 of 3) video links access successful
                    break # play user selected video resolution only
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
def playVideo(name,url,videoRes):
    p_url = "http://www.flvcd.com/parse.php?kw="+url+"&format="+str(videoRes)
    for i in range(10): # Retry specified trials before giving up (seen 9 trials max)
       try: # stop xbmc from throwing error to prematurely terminate video search
            link = getHttpData(p_url)
            match=re.compile('下载地址：\s*<a href="(.+?)" target="_blank" class="link"').findall(link)
            if len(match): break
       except:
           pass   
    
    if len(match):
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
# Continuous Player start playback from user selected video
# User backspace to previous menu will not work - playlist = last selected
##################################################################################
def playVideoUgc(name,url,thumb):
    videoRes = int(__addon__.getSetting('video_resolution'))
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
        
        if re.search('http://www.letv.com/', p_url):  #fresh search
            f_url = "http://www.flvcd.com/parse.php?kw="+p_url+"&format="+str(videoRes)
            for i in range(10): # Retry specified trials before giving up (seen 9 trials max)
                try: # stop xbmc from throwing error to prematurely terminate video search
                    link = getHttpData(f_url)
                    v_url=re.compile('下载地址：\s*<a href="(.+?)" target="_blank" class="link"').findall(link)
                    if len(v_url):
                        v_url = v_url[0] 
                        break
                except:
                    pass   

            if v_url == None: continue
            print "url: ", v_url
            playlistA.remove(p_url) # remove old url
            playlistA.add(v_url, li, x)  # keep a copy of v_url in Audio Playlist
        else:
            v_url = p_url
            
        playlist.add(v_url, li, k)
        k +=1 

        if k == 1:
            xbmc.Player(1).play(playlist)
        if videoplaycont == 'false': break
           
##################################################################################    
# Routine to extra parameters from xbmc
##################################################################################
