# -*- coding: utf-8 -*-
import sys
import xbmc, xbmcgui, xbmcplugin, xbmcaddon
import urllib
import urllib2, re, os, gzip, StringIO
try:
    import pycurl
except ImportError:
    pass

if sys.version_info < (2, 7):
    import simplejson
else:
    import json as simplejson
try:
    from ChineseKeyboard import Keyboard
except ImportError:
    Keyboard = xbmc.Keyboard
#import ChineseKeyboard
#from weibopy.auth import OAuthHandler
from lib.letv import playVideoLetv
from lib.qiyi import playVideoQiyi
#from weibopy.api import API
#from weibo import APIClient
RES_LIST_XUNLEI = ['normal', 'high']
# plugin modes
MODE_FIRST = 10
MODE_SECOND = 20
MODE_PLAY_YOUKU = 40
MODE_PLAY_SOHU = 50
MODE_PLAY = 30
MODE_RELATION = 60

# parameter keys
PARAMETER_KEY_MODE = "mode"

# menu item names
FIRST_SUBMENU = "HouGong1"
SECOND_SUBMENU = "Weibo Music"

# plugin handle
handle = int(sys.argv[1])

UserAgent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'
__addonid__ = "plugin.video.search"
__addon__ = xbmcaddon.Addon(id=__addonid__)
__addonicon__ = os.path.join( __addon__.getAddonInfo('path'), 'icon.png' )
# utility functions
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

def parameters_string_to_dict(parameters):
    ''' Convert parameters encoded in a URL to a dict. '''
    paramDict = {}
    if parameters:
        paramPairs = parameters[1:].split("&")
        for paramsPair in paramPairs:
            paramSplits = paramsPair.split('=')
            if (len(paramSplits)) == 2:
                paramDict[paramSplits[0]] = paramSplits[1]
    return paramDict

def addDirectoryItem(name, isFolder=True, parameters={}, thumbnail = ''):
    ''' Add a list item to the XBMC UI.'''
    li = xbmcgui.ListItem(name, thumbnailImage = thumbnail)
    url = sys.argv[0] + '?' + urllib.urlencode(parameters)
    return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=url, listitem=li, isFolder=isFolder)


# UI builder functions
def show_root_menu():
    ''' Show the plugin root menu. '''
    #name = FIRST_SUBMENU
    #keyboard = xbmc.Keyboard('','请输入搜索内容')
    keyboard = Keyboard('','请输入搜索内容')
    keyboard.doModal()
    keyword = ''
    if (keyboard.isConfirmed()):
        keyword = keyboard.getText()
        #keyword = keyword.replace(' ','%20')
        keyword = urllib.quote(keyword)
        url = "http://so.v.360.cn/index.php?kw="+keyword
        print url
        link = GetHttpData(url)
        match0 = re.compile('<ul class="gsearchlist">(.+?)</ul>', re.DOTALL).search(link)
        if match0:
            vlist = re.compile('<div class="avatar">.*?<a href="(.+?)".*?<img title="(.+?)".*?data-src="(.+?)"', re.DOTALL).findall(match0.group(1))
            for url0, name, img in vlist:
            #print url
                submenuname = name
                addDirectoryItem(name, parameters={ PARAMETER_KEY_MODE: MODE_FIRST,"url":url0,"name":submenuname }, isFolder=True, thumbnail=img)
        #addDirectoryItem(name=SECOND_SUBMENU, parameters={ PARAMETER_KEY_MODE: MODE_SECOND }, isFolder=True)
        addDirectoryItem("显示相关搜索", parameters={ PARAMETER_KEY_MODE: MODE_RELATION,"url":url }, isFolder=True)
    xbmcplugin.endOfDirectory(handle=handle, succeeded=True)
    
def show_first_submenu(name,url):
    ''' Show first submenu. '''
    #for i in range(0, 5):
        #name = "%s Item %d" % (FIRST_SUBMENU, i)
        #addDirectoryItem(name, isFolder=False)
    link=GetHttpData(url)
    match = re.compile('<ul.*? id="supplies".*?>(.+?)</ul>', re.DOTALL).search(link)
    if match:
        vlist = re.compile('li.*? site="(.+?)".*?<em>(.+?)</em>', re.DOTALL).findall(match.group(1))
        if not vlist:
            vlist = re.compile('<li.*? site="(.+?)">.*?<a.*?>(.+?)</a>', re.DOTALL).findall(match.group(1))
        for site, sitename in vlist:
            print site
            print sitename
            addDirectoryItem(sitename, parameters={ PARAMETER_KEY_MODE: MODE_SECOND,"url":url, "site":site, "name":name }, isFolder=True)
        #plytype="dianying"
        if not vlist:
            match1=re.compile('testSpeed.test\((.+?)\);', re.DOTALL).search(link)
            if match1:
                match11=re.compile('({.+?}}),', re.DOTALL).search(match1.group(1))
            #if match11:
                json_response = simplejson.loads(match11.group(1))
                for key in json_response.keys():
                    sitename=json_response[key]['name'].encode('utf-8')
                    site=json_response[key]['site'].encode('utf-8')
                    url=json_response[key]['link'].encode('utf-8')
                    addDirectoryItem(name+" "+sitename+"网", parameters={ PARAMETER_KEY_MODE: MODE_PLAY,"url":url,"site":site, "name":name }, isFolder=False)
            else:
                vlist = re.compile('sitename="(.+?)".*?href="(.+?)".*?<em>(.+?)</em>', re.DOTALL).findall(match.group(1))
                for site, url, sitename in vlist:
                    print "******searchplugin dianying*******"
                    addDirectoryItem(name+" "+sitename, parameters={ PARAMETER_KEY_MODE: MODE_PLAY,"url":url,"site":site, "name":name }, isFolder=False)
    else:
        match = re.compile('<div class="single gclearfix">(.*?)</div>', re.DOTALL).search(link)
        vlist = re.compile('<a class="(.*?)"><em>(.*?)</em></a>', re.DOTALL).findall(match.group(1))
        for site, sitename in vlist:
            print site
            print sitename
            sitestr = site.split('-')
            site = sitestr[1]
            print site
            addDirectoryItem(sitename, parameters={ PARAMETER_KEY_MODE: MODE_SECOND,"url":url, "site":site, "name":name }, isFolder=True)
    xbmcplugin.endOfDirectory(handle=handle, succeeded=True)

def playVideo(name,url):
    if url.find('youku') > 0:
        addDirectoryItem(name, parameters={ PARAMETER_KEY_MODE: MODE_PLAY_YOUKU,"url":url, "name":name }, isFolder=False)
    elif url.find('sohu') > 0:
        addDirectoryItem(name, parameters={ PARAMETER_KEY_MODE: MODE_PLAY_SOHU,"url":url, "name":name }, isFolder=False)
    xbmcplugin.endOfDirectory(handle=handle, succeeded=True)

def show_second_submenu(site, url, name):
    ''' Show second submenu. '''
    #for i in range(0, 10):
    #    name = "%s Item %d" % (SECOND_SUBMENU, i)
    #    addDirectoryItem(name, isFolder=False)
    link=GetHttpData(url)
    text='<div class="content" site="'+site+'".*?><div class="full gclearfix"(.+?)</div>'
    print text
    match = re.compile(text, re.DOTALL).search(link)
    if not match:
        text='<div class="list gclearfix">.*?sitename="'+site+'"(.+?)</div>\s*</div>\s*</div>'
        print text
        match = re.compile(text, re.DOTALL).search(link)
    vlist = re.compile('href="(.+?)">(.+?)</a>', re.DOTALL).findall(match.group(1))
    for url, num in vlist:
        num=num.split('<')[0]
        addDirectoryItem(name+" "+num, parameters={ PARAMETER_KEY_MODE: MODE_PLAY,"url":url, "site":site, "name":name }, isFolder=False)
    xbmcplugin.endOfDirectory(handle=handle, succeeded=True)

def PlayVideo(name,site,url,res):
    print site
    print url
    print res
    thumb = ""
    if site=='youku':
        PlayVideoYouku(name,url,"",res)
    elif site=='tudou':
        PlayVideoTudou(name,url,"",res)
    elif site=='sohu':
        PlayVideoSohu(name,url,thumb)
    elif site=='xunlei':
        res_i=1;
        PlayVideoXunlei(name,url,thumb,res_i)
    elif site=='leshi':
        playVideoLetv(name,url)
    elif site=='fengxing':
        PlayVideoFunshion(name,url,thumb,res)
    elif site=='m1905':
        PlayVideoFunshion(name,url,thumb,res)
    elif site=='56com':
        PlayVideo56com(name,url,thumb,res)
    elif site=='pps':
        PlayVideoFunshion(name,url,thumb,res)
    elif site=='qiyi':
        playVideoQiyi(name,url,thumb,res)
    else:
        PlayVideoYouku(name,url,"",res)

def PlayVideoYouku(name,url,thumb,res):
    #res_limit = int(__addon__.getSetting('movie_res'))
    #if res > res_limit:
    #    res = res_limit
    link = GetHttpData("http://www.flvcd.com/parse.php?kw="+url+"&format="+res)
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

def PlayVideoXunlei(name,url,thumb,res):
    #res_limit = int(__addon__.getSetting('movie_res'))
    #if res > res_limit:
    #    res = res_limit
    link = GetHttpData("http://www.flvcd.com/parse.php?kw=%s&format=%s" % (url, RES_LIST_XUNLEI[res]))
    match = re.compile('<a href="(http://[^/]+/data\d/cdn_transfer/[^"]+)" target="_blank"').findall(link)
    if not match:
        link = GetHttpData("http://www.flvcd.com/parse.php?kw=%s" % (url))
        match = re.compile('<a href="(http://[^/]+/data\d/cdn_transfer/[^"]+)" target="_blank"').findall(link)
    if match:
        if len(match) > 1:
            url = 'stack://' + ' , '.join(match)
        else:
            url = match[0]
        listitem = xbmcgui.ListItem(name, thumbnailImage=thumb)
        listitem.setInfo(type="Video",infoLabels={"Title":name})
        xbmc.Player().play(url, listitem)
    else:
        dialog = xbmcgui.Dialog()
        ok = dialog.ok(__addonname__, '无法解析视频')

def PlayVideoFunshion(name,url,thumb,res):
    #res_limit = int(__addon__.getSetting('movie_res'))
    #if res > res_limit:
    #    res = res_limit
    link = GetHttpData("http://www.flvcd.com/parse.php?kw=%s&format=%s" % (url, res))
    match = re.compile('<a href="(.+?)" target="_blank" class="link"').findall(link)
    if not match:
        link = GetHttpData("http://www.flvcd.com/parse.php?kw=%s" % (url))
        match = re.compile('<a href="(.+?)" target="_blank" class="link"').findall(link)
    if match:
        if len(match) > 1:
            url = 'stack://' + ' , '.join(match)
        else:
            url = match[0]
        listitem = xbmcgui.ListItem(name, thumbnailImage=thumb)
        listitem.setInfo(type="Video",infoLabels={"Title":name})
        xbmc.Player().play(url, listitem)
    else:
        dialog = xbmcgui.Dialog()
        ok = dialog.ok(__addonname__, '无法解析视频')

def PlayVideo56com(name,url,thumb,res):
    #res_limit = int(__addon__.getSetting('movie_res'))
    #if res > res_limit:
    #    res = res_limit
    link = GetHttpData("http://www.flvcd.com/parse.php?kw=%s&format=%s" % (url, res))
    match = re.compile('<a href="(.+?)" target="_blank" class="link"').findall(link)
    if not match:
        link = GetHttpData("http://www.flvcd.com/parse.php?kw=%s" % (url))
        match = re.compile('<a href="(.+?)" target="_blank" class="link"').findall(link)
    if match:
        if len(match) > 1:
            url = 'stack://' + ' , '.join(match)
        else:
            url = match[0]
            c = pycurl.Curl()
            c.setopt(pycurl.URL, url)
            b = StringIO.StringIO()
            c.setopt(pycurl.WRITEFUNCTION, b.write)
            c.setopt(pycurl.USERAGENT, UserAgent)
            c.setopt(pycurl.HEADER, True)
            c.perform()
            html = b.getvalue()
            match = re.compile('Location: (.+?)\r', re.DOTALL).search(html)
            if match:
                url=match.group(1)
        listitem = xbmcgui.ListItem(name, thumbnailImage=thumb)
        listitem.setInfo(type="Video",infoLabels={"Title":name})
        xbmc.Player().play(url, listitem)
    else:
        dialog = xbmcgui.Dialog()
        ok = dialog.ok(__addonname__, '无法解析视频')

##################################################################################
# Sohu Video Link Decode Algorithm & Player
# Extract all the video list and start playing first found valid link
# User may press <SPACE> bar to select video resolution for playback
##################################################################################
def PlayVideoSohu(name,url,thumb):
    level = 1#int(__addon__.getSetting('resolution'))
    site = 0#int(__addon__.getSetting('videosite'))

    link = GetHttpData(url)
    match1 = re.compile('var vid="(.+?)";').search(link)
    if not match1:
        match1 = re.compile('<a href="(http://[^/]+/[0-9]+/[^\.]+.shtml)" target="?_blank"?><img').search(link)
        if match1:
            PlayVideoSohu(name,match1.group(1),thumb)
        return
    p_vid = match1.group(1)
    if p_vid.find(',') > 0 : p_vid = p_vid.split(',')[0]
       
    p_url = 'http://hot.vrs.sohu.com/vrs_flash.action?vid='+ p_vid
    link = GetHttpData(p_url)
    match = re.compile('"norVid":(.+?),"highVid":(.+?),"superVid":(.+?),').search(link)
    if not match:
       dialog = xbmcgui.Dialog()
       ok = dialog.ok(__addonname__,'您当前选择的节目暂不能播放，请选择其它节目')   
       return    
    ratelist=[]
    if match.group(3)!='0':ratelist.append(['超清','3'])
    if match.group(2)!='0':ratelist.append(['高清','2'])
    if match.group(1)!='0':ratelist.append(['流畅','1'])
    if level == 3 :
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
    else:
        rate = int(ratelist[0][1])
        if rate > level + 1:
            rate = level + 1
    if match.group(int(rate))<>str(p_vid):
        link = GetHttpData('http://hot.vrs.sohu.com/vrs_flash.action?vid='+match.group(int(rate)))
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
    if not match:
       res = ratelist[3-int(rate)][0]
       dialog = xbmcgui.Dialog()
       ok = dialog.ok(__addonname__,'您当前选择的视频: ['+ res +'] 暂不能播放，请选择其它视频')       
       return
    newpaths = match[0].split('","')
    
    urls = []
    for i in range(0,len(paths)):
        p_url = 'http://data.vod.itc.cn/?prot=2&file='+paths[i].replace('http://data.vod.itc.cn','')+'&new='+newpaths[i]
        link = GetHttpData(p_url)
        
        # http://newflv.sohu.ccgslb.net/|623|116.14.234.161|Googu7gm-8WjRTd5ZfBVPIfrtRtLE5Cn|1|0
        key=link.split('|')[3]
        if site == 0:
            url = link.split('|')[0].rstrip("/")+newpaths[i]+'?key='+key
        else:
            url = 'http://new.sohuv.dnion.com'+newpaths[i]+'?key='+key
        urls.append(url)
    stackurl = 'stack://' + ' , '.join(urls)
    listitem = xbmcgui.ListItem(name,thumbnailImage=thumb)
    listitem.setInfo(type="Video",infoLabels={"Title":name})
    xbmc.Player().play(stackurl, listitem)

def PlayTudou(name,iid,thumb):
    url = 'http://v2.tudou.com/v2/cdn?id=%s' % (iid)
    link = GetHttpData(url)
    match = re.compile('<f.+?brt="(\d+)"[^>]*>(.+?)</f>', re.DOTALL).findall(link)
    match.sort(reverse=True)
    listitem = xbmcgui.ListItem(name,thumbnailImage=thumb)
    listitem.setInfo(type="Video",infoLabels={"Title":name})
    xbmc.Player().play('%s|User-Agent=%s' % (match[0][1], UserAgent), listitem)

def PlayVideoTudou(name,url,thumb,res):
    link = GetHttpData(url)
    match = re.compile('itemData=\{(.+?)\};', re.DOTALL).search(link)
    if match:
        iid = ''
        vcode = ''
        #llist = ''
        # 解析土豆视频id (iid)
        match1 = re.compile('iid: (\d+)').search(match.group(1))
        if match1:
            iid = match1.group(1)
        # 解析优酷视频id (vcode)
        match1 = re.compile("vcode: '([^']+)'").search(match.group(1))
        if match1:
            vcode = match1.group(1)
        lang_select = 0#int(__addon__.getSetting('lang_select')) # 默认|每次选择|自动首选
        if lang_select != 0:
            # 解析优酷多语种id
            match1 = re.compile("\{id: \d+, vcode: '([^']+)', lan: '([^']+)'\}").findall(link)
            if match1:
                #llist =  '; '.join(['%s=%s' % (x[1],x[0]) for x in match1])
                if lang_select == 1:
                    list = [x[1] for x in match1]
                    sel = xbmcgui.Dialog().select('选择语言', list)
                    if sel ==-1:
                        return
                    vcode = match1[sel][0]
                    name = '%s（%s）' % (name, match1[sel][1])
                else:
                    lang_prefer = __addon__.getSetting('lang_prefer') # 国语|粤语
                    for i in range(0,len(match1)):
                        if match1[i][1] == lang_prefer:
                            vcode = match1[i][0]
                            name = '%s（%s）' % (name, match1[i][1])
                            break
        #ok = xbmcgui.Dialog().ok(__addonname__, 'iid=%s, vcode=%s' % (iid,vcode), llist)
        if (not vcode) and iid:
            PlayTudou(name,iid,thumb)
            return
        if vcode:
            url = 'http://v.youku.com/v_show/id_%s.html' % (vcode)
    PlayVideoYouku(name,url,thumb,res)

def show_relation(url):
    link = GetHttpData(url)
    match0 = re.compile('<ul class="gshortvideolist gclearfix">(.+?)</ul>', re.DOTALL).search(link)
    if match0:
        vlist = re.compile('<li>.*?<a sitename="(.+?)" href="(.+?)".*?title="(.+?)".*?data-src="(.+?)".*?<em>(.+?)</em>\s*<ins>(.+?)</ins>.*?</li>', re.DOTALL).findall(match0.group(1))
        for site, url, name, img, sitename, instime in vlist:
        #print url
            submenuname = name
            addDirectoryItem(name+" "+instime+" "+sitename, parameters={ PARAMETER_KEY_MODE: MODE_PLAY,"url":url, "site":site, "name":submenuname }, isFolder=False, thumbnail=img)
    xbmcplugin.endOfDirectory(handle=handle, succeeded=True)

# parameter values
params = parameters_string_to_dict(sys.argv[2])
mode = int(params.get(PARAMETER_KEY_MODE, "0"))
url = urllib.unquote_plus(params.get("url","0"))
name = urllib.unquote_plus(params.get("name","0"))
site = urllib.unquote_plus(params.get("site","0"))
res='super'
#print "##########################################################"
print("Mode: %s %s %s" % (mode,url,name))
print("Mode: %s %s %s" % (sys.argv[0],sys.argv[1],sys.argv[2]))
#print "##########################################################"

# Depending on the mode, call the appropriate function to build the UI.
if not sys.argv[2]:
    # new start
    ok = show_root_menu()
elif mode == MODE_FIRST:
    ok = show_first_submenu(name,url)
elif mode == MODE_SECOND:
    ok = show_second_submenu(site,url,name)
elif mode == MODE_PLAY:
    ok = PlayVideo(name,site,url,res)
elif mode == MODE_PLAY_YOUKU:
    ok = PlayVideoYouku(name,url,"",res)
elif mode == MODE_PLAY_SOHU:
    ok = PlayVideoSohu(name,url,"")
elif mode == MODE_RELATION:
    ok = show_relation(url)
