# -*- coding: utf-8 -*-
import xbmc, xbmcgui, xbmcplugin, xbmcaddon, urllib2, urllib, re, string, sys, os, gzip, StringIO

# 5ivdo(5ivdo) by sand, 2012

# Plugin constants 
__addonname__ = "5ivdo(5ivdo)"
__addonid__ = "plugin.video.5ivdo"
__addon__ = xbmcaddon.Addon(id=__addonid__)
#__addonicon__ = os.path.join( __addon__.getAddonInfo('path'), 'icon.png' )



UserAgent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'
subfrom = ''
subto = ''


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


def Get5ivdoData(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', UserAgent)
    response = urllib2.urlopen(req)
    httpdata = response.read()
    httpdata = gzip.GzipFile(fileobj=StringIO.StringIO(httpdata)).read()
    response.close()
    return httpdata



def showmenu(purl):
    link = Get5ivdoData(purl)
    match = re.compile('<mode>(.+?)</mode><title>(.+?)</title><url>(.+?)</url><thumb>(.+?)</thumb>').findall(link)
    for imode, ititle, iurl,ithumb in match:
        li=xbmcgui.ListItem(ititle,iconImage = '', thumbnailImage = ithumb)
        u=sys.argv[0]+"?mode="+urllib.quote_plus(imode)+"&url="+urllib.quote_plus('http://www.5ivdo.com/' + iurl)
        xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
    xbmcplugin.endOfDirectory(int(sys.argv[1]))





def showdata(purl):
    imultesite = ''
    link = Get5ivdoData(purl)
    match0 = re.compile('<head>(.+?)</head>').search(link).group(1)
    if match0.find('multesite') > 0:
        imultesite=re.compile('<multesite>(.+?)</multesite>').findall(match0)[0]
    if imultesite == 'TRUE':
        match = re.compile('<mode>(.+?)</mode><title>(.+?)</title><url>(.+?)</url>(.+?)\n').findall(link)
        for imode, ititle, iurl ,iother in match:
            if iother.find('thumb') > 0:
                ithumb=re.compile('<thumb>(.+?)</thumb>').findall(iother)[0]
            else:
                ithumb=''
            li=xbmcgui.ListItem(ititle,iconImage = '', thumbnailImage = ithumb)
            if iother.find('matchstr') > 0:
                iimatchstr=re.compile('<matchstr>(.+?)</matchstr>').findall(iother)[0]
            else:
                iimatchstr=''
            if iother.find('mflag') > 0:
                iimflag=re.compile('<mflag>(.+?)</mflag>').findall(iother)[0]
            else:
                iimflag=''
            if iother.find('sub') > 0:
                iisub=re.compile('<sub>(.+?)</sub>').findall(iother)[0]
            else:
                iisub=''
            u=sys.argv[0]+"?name="+urllib.quote_plus(ititle)+"&mode="+urllib.quote_plus(imode)+"&matchstr="+urllib.quote_plus(iimatchstr)+"&mflag="+urllib.quote_plus(iimflag)+"&url="+urllib.quote_plus(iurl)+"&sub="+urllib.quote_plus(iisub)
            xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,False)
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
    else:
        if match0.find('matchstr') > 0:
            imatchstr=re.compile('<matchstr>(.+?)</matchstr>').findall(match0)[0]
        if match0.find('mflag') > 0:
            imflag=re.compile('<mflag>(.+?)</mflag>').findall(match0)[0]
        if match0.find('sub') > 0:
            isub=re.compile('<sub>(.+?)</sub>').findall(match0)[0]
        else:
            isub=''
        match = re.compile('<mode>(.+?)</mode><title>(.+?)</title><url>(.+?)</url><thumb>(.+?)</thumb>').findall(link)
        for imode, ititle, iurl ,ithumb in match:
            li=xbmcgui.ListItem(ititle,iconImage = '', thumbnailImage = ithumb)
            u=sys.argv[0]+"?name="+urllib.quote_plus(ititle)+"&mode="+urllib.quote_plus(imode)+"&matchstr="+urllib.quote_plus(imatchstr)+"&mflag="+urllib.quote_plus(imflag)+"&url="+urllib.quote_plus(iurl)+"&sub="+urllib.quote_plus(isub)
            xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,False)
        xbmcplugin.endOfDirectory(int(sys.argv[1]))



def rootList():
    irootfile = None
    link = GetHttpData('http://www.5ivdo.net/index.xml')
    match0 = re.compile('<config>(.+?)</config>', re.DOTALL).search(link)
    match = re.compile('<name>(.+?)</name><value>(.+?)</value>').findall(match0.group(1))
    for iname, ivalue in match:
        if iname == 'rootfile':
            irootfile = ivalue
    showmenu(irootfile) 


def urlExists(url):
    try:
        resp = urllib2.urlopen(url)
        result = True
        resp.close()
    except urllib2.URLError, e:
        result = False
    return result 


def checksub(purl,psub):
    global subfrom 
    global subto
    match = re.compile('<from>(.+?)</from><to>(.+?)</to>').findall(psub)
    for ifrom,ito in match:
        subfrom  = ifrom 
        subto = ito
        if urlExists(purl.replace(subfrom,subto)): return
    subfrom = 'ERROR'
    subto ='ERROR'


def PlayVideo(name,url,matchstr,multiflag,thumb,sub):
    link = GetHttpData(url) 
    match = re.compile(matchstr).findall(link)
    if len(match) == 0:
        dialog = xbmcgui.Dialog()
        ok = dialog.ok(__addonname__, '播放地址已失效，请换用其他网站重试。')
        return
    if len(sub) > 0:
        checksub(match[0],sub) 
    if multiflag == '1':
        listitem = xbmcgui.ListItem(name)
        if len(sub) > 0:
            xbmc.Player().play(match[0].replace(subfrom,subto)+'|User-Agent='+UserAgent, listitem)
        else:
            xbmc.Player().play(match[0]+'|User-Agent='+UserAgent, listitem)
    else:
        playlist=xbmc.PlayList(1)
        playlist.clear()
        for i in range(0,len(match)): 
            listitem = xbmcgui.ListItem(name) 
            listitem.setInfo(type="Video",infoLabels={"Title":name+" 第"+str(i+1)+"/"+str(len(match))+" 节"})
            if len(sub) > 0:
                playlist.add(match[i].replace(subfrom,subto), listitem)
            else:
                playlist.add(match[i], listitem)
        xbmc.Player().play(playlist) 




params = get_params()
mode = None
url = None
thumb = None
name = None
matchstr = None
mflag = None

try:
    thumb = urllib.unquote_plus(params["thumb"])
except:
    pass

try:
    name = urllib.unquote_plus(params["name"])
except:
    pass

try:
    matchstr = urllib.unquote_plus(params["matchstr"])
except:
    pass

try:
    mflag = urllib.unquote_plus(params["mflag"])
except:
    pass

try:
    url = urllib.unquote_plus(params["url"])
except:
    pass

try:
    mode = urllib.unquote_plus(params["mode"])
except:
    pass

try:
    sub = urllib.unquote_plus(params["sub"])
except:
    pass



if mode == None:
    rootList()
elif mode == 'menu':
    showmenu(url)
elif mode == 'data':
    showdata(url)
elif mode == 'play':
    PlayVideo(name,url,matchstr,mflag,thumb,sub)
elif mode == 'diag': 
    dialog = xbmcgui.Dialog()
    ok = dialog.ok(__addonname__, '开发阶段。')





