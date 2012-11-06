# -*- coding: utf-8 -*-
import xbmc, xbmcgui, xbmcplugin, xbmcaddon, urllib2, urllib, re, string, sys, os, gzip, StringIO

# 5ivdo(5ivdo) by sand, 2012

# Plugin constants 
__addonname__ = "5ivdo(5ivdo)"
__addonid__ = "plugin.video.5ivdo"
__addon__ = xbmcaddon.Addon(id=__addonid__)
#__addonicon__ = os.path.join( __addon__.getAddonInfo('path'), 'icon.png' )



UserAgent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'


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
    ipara = ''
    link = Get5ivdoData(purl)
    match0 = re.compile('<head>(.+?)</head>').search(link).group(1)
    if match0.find('multesite') > 0:
        imultesite=re.compile('<multesite>(.+?)</multesite>').findall(match0)[0]
    if imultesite == 'TRUE':
        match = re.compile('<mode>(.+?)</mode><title>(.+?)</title><url>(.+?)</url>(.+?)\n').findall(link)
        for imode, ititle, iurl ,iother in match:
            ipara = ''
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
            if iother.find('prefix') > 0:
                iiprefix=re.compile('<prefix>(.+?)</prefix>').findall(iother)[0]
                ipara = ipara + "&prefix="+urllib.quote_plus(iiprefix)
            if iother.find('options') > 0:
                iioptions=re.compile('<options>(.+?)</options>').findall(iother)[0]
                ipara = ipara + "&options="+urllib.quote_plus(iioptions)
            u=sys.argv[0]+"?name="+urllib.quote_plus(ititle)+"&mode="+urllib.quote_plus(imode)+"&matchstr="+urllib.quote_plus(iimatchstr)+"&mflag="+urllib.quote_plus(iimflag)+"&url="+urllib.quote_plus(iurl)+"&sub="+urllib.quote_plus(iisub)+ipara
            xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,False)
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
    else:
        ipara = ''
        if match0.find('matchstr') > 0:
            imatchstr=re.compile('<matchstr>(.+?)</matchstr>').findall(match0)[0]
        if match0.find('mflag') > 0:
            imflag=re.compile('<mflag>(.+?)</mflag>').findall(match0)[0]
        if match0.find('sub') > 0:
            isub=re.compile('<sub>(.+?)</sub>').findall(match0)[0]
        else:
            isub=''
        if match0.find('prefix') > 0:
            iiprefix=re.compile('<prefix>(.+?)</prefix>').findall(match0)[0]
            ipara = ipara + "&prefix="+urllib.quote_plus(iiprefix)
        if match0.find('options') > 0:
            iioptions=re.compile('<options>(.+?)</options>').findall(match0)[0]
            ipara = ipara + "&options="+urllib.quote_plus(iioptions)
        match = re.compile('<mode>(.+?)</mode><title>(.+?)</title><url>(.+?)</url><thumb>(.+?)</thumb>').findall(link)
        for imode, ititle, iurl ,ithumb in match:
            li=xbmcgui.ListItem(ititle,iconImage = '', thumbnailImage = ithumb)
            u=sys.argv[0]+"?name="+urllib.quote_plus(ititle)+"&mode="+urllib.quote_plus(imode)+"&matchstr="+urllib.quote_plus(imatchstr)+"&mflag="+urllib.quote_plus(imflag)+"&url="+urllib.quote_plus(iurl)+"&sub="+urllib.quote_plus(isub) + ipara
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


def checksub(purl):
    global subfrom 
    global subto
    global sub
    match = re.compile('<from>(.+?)</from><to>(.+?)</to>').findall(sub)
    for ifrom,ito in match:
        subfrom  = ifrom 
        subto = ito
        if urlExists(purl.replace(subfrom,subto)): return
    subfrom = 'ERROR'
    subto ='ERROR'


def sohuPlayVideo(pname,purl,pthumb):
    link = GetHttpData(purl)
    match = re.compile('"clipsURL"\:\["(.+?)"\]').findall(link)
    if len(match) == 0:
        dialog = xbmcgui.Dialog()
        ok = dialog.ok(__addonname__, '无法播放，请换用其他网站重试。')
        return
    paths = match[0].split('","')
    match = re.compile('"su"\:\["(.+?)"\]').findall(link)
    if len(match) == 0:
        dialog = xbmcgui.Dialog()
        ok = dialog.ok(__addonname__, '无法播放，请换用其他网站重试。')
        return
    newpaths = match[0].split('","')
    playlist=xbmc.PlayList(1) 
    playlist.clear()
    for i in range(0,len(paths)):
        p_url = 'http://data.vod.itc.cn/?prot=2&file='+paths[i].replace('http://data.vod.itc.cn','')+'&new='+newpaths[i]
        link = GetHttpData(p_url)
        # http://newflv.sohu.ccgslb.net/|623|116.14.234.161|Googu7gm-8WjRTd5ZfBVPIfrtRtLE5Cn|1|0
        key=link.split('|')[3]
        url=link.split('|')[0].rstrip("/")+newpaths[i]+'?key='+key
        title = pname+" 第"+str(i+1)+"/"+str(len(paths))+"节"
        listitem=xbmcgui.ListItem(title)
        listitem.setInfo(type="Video",infoLabels={"Title":title})
        playlist.add(url, listitem)    
    xbmc.Player().play(playlist)



def PlayVideo(name,url,matchstr,multiflag,thumb,pmod):
    if pmod.find('RAW') >0:
        playlist=xbmc.PlayList(1)  
        playlist.clear() 
        listitem = xbmcgui.ListItem(name) 
        listitem.setInfo(type="Video",infoLabels={"Title":name})
        playlist.add(url, listitem)
        xbmc.Player().play(playlist)
    elif pmod.find('SOHU') >0: 
        sohuPlayVideo(name,url,thumb)
    else:
        playlist=xbmc.PlayList(1)  
        playlist.clear() 
        link = GetHttpData(url) 
        match = re.compile(matchstr).findall(link)
        if len(match) == 0:
            dialog = xbmcgui.Dialog()
            ok = dialog.ok(__addonname__, '播放地址已失效，请换用其他网站重试。')
            return
        for i in range(0,len(match)): 
            if multiflag == '1' and i < len(match) -1: continue
            listitem = xbmcgui.ListItem(name) 
            if multiflag == '1':
                listitem.setInfo(type="Video",infoLabels={"Title":name})
            else:
                listitem.setInfo(type="Video",infoLabels={"Title":name+" 第"+str(i+1)+"/"+str(len(match))+" 节"})
            purl=match[i]
            if pmod.find('SUB') > 0:
                if i==0: checksub(match[i]) 
                purl = purl.replace(subfrom,subto)
            if pmod.find('PRE') > 0:
                purl = prefix + purl
            playlist.add(purl, listitem)
        xbmc.Player().play(playlist)
    



params = get_params()
mode = None
url = None
thumb = None
name = None
matchstr = None
mflag = None
subfrom = None
subto = None
sub = None
prefix = None
options = None
pmod = '|'

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

try:
    prefix = urllib.unquote_plus(params["prefix"])
except:
    pass

try:
    options = urllib.unquote_plus(params["options"])
except:
    pass




if mode == None:
    rootList()
elif mode == 'menu':
    showmenu(url)
elif mode == 'data':
    showdata(url)
elif mode == 'play':
    if options: pmod = pmod + options
    if sub: pmod = pmod + '|SUB'
    if prefix: pmod = pmod + '|PRE'
    PlayVideo(name,url,matchstr,mflag,thumb,pmod) 
elif mode == 'diag':
    dialog = xbmcgui.Dialog()
    ok = dialog.ok(__addonname__, '开发阶段。')





