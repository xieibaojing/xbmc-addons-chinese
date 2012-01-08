# -*- coding: utf-8 -*-
import urllib,urllib2,re,xbmcplugin,xbmcgui,xbmc,os

# OpenV(天线高清)
# write by robinttt, 2010
# update by taxigps, 2011

def GetHttpData(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    httpdata = response.read()
    response.close()
    return httpdata

def CATEGORIES():
    addDir('电影','http://www.openv.com/fl_list.php?t=3',1,'')
    addDir('电视剧','http://www.openv.com/fl_list.php?t=2',1,'')
    addDir('电视节目','http://www.openv.com/fl_list.php?t=1',1,'')
    addDir('新闻','http://www.openv.com/fl_list.php?t=4',1,'')

def Channels(url,name):
    link = GetHttpData(url)
    link = link.replace('\r','').replace('\n','').replace('\t','').replace(' ','')
    match = re.compile('<divclass="gyong_top">(.+?)</div>').findall(link)
    for i in range(0,len(match)):
        addDir(name+'>'+match[i],url,2,'')

def ChannelsA(url,name):
    name0 = name.split('>')[1]
    link = GetHttpData(url)
    link = link.replace('\r','').replace('\n','').replace('\t','').replace(' ','')
    match = re.compile('<divclass="gyong_top">'+name0+'</div>(.+?)</ul>').findall(link)
    match0 = re.compile('<ahref="(.+?)">(.+?)</a>').findall(match[0])
    for url1,name1 in match0:
        addDir(name+'>'+name1,'http://www.openv.com/'+url1,3,'')

def Lists(url,name):
    link = GetHttpData(url)
    link = link.replace('\r','').replace('\n','').replace('\t','').replace(' ','')
    addDir('当前位置：'+name,'',20,'')
    match = re.compile('<divclass="gongyong_mid1">(.+?)</ul>').findall(link)
    match0 = re.compile('<ahref="(.+?)"target="_hdplay"><imgalt="(.+?)"src="(.+?)"').findall(match[0])
    for i in range(0,len(match0)):
        if match0[i][0].find('tv_show')==-1:
            ids = match0[i][0].split('-')
            id = ids[1].replace('.html','')
            addLink(str(i+1)+'.'+match0[i][1],'http://casting.openv.com/PLGS/plgs.php?pid='+id,5,match0[i][2])
        else:
            addDir(str(i+1)+'.'+match0[i][1],'http://www.openv.com/'+match0[i][0],6,match0[i][2])
    match = re.compile('<divclass="page">(.+?)</div>').findall(link)
    match0 = re.compile('href="(.+?)">(.+?)</a>').findall(match[0])
    for url1,name1 in match0:
        if url1.find('"class="nob')==-1:
            addDir('第'+name1+'页','http://www.openv.com/'+url1,3,'')
        else:
            url1 = url1.replace('"class="nob','')
            addDir(name1,'http://www.openv.com/'+url1,3,'')

def ListsA(url,name):
    names=name.split('.')
    name=names[1]
    link = GetHttpData(url)
    link = link.replace('\r','').replace('\n','').replace('\t','').replace(' ','')
    match = re.compile('<divclass="gongyong_bfjuji"><divclass="img"><imgsrc="(.+?)"').findall(link)
    thumb = match[0]
    match = re.compile('<divclass="b">剧情简介：</div><div>(.+?)</div>').findall(link)
    plot = match[0]
    match = re.compile('<div>导演：(.+?)</div>').findall(link)
    director = match[0]
    match = re.compile('<div>主演：(.+?)</div>').findall(link)
    cast = match[0].replace('/',' ').split()
    match = re.compile('<div>首播时间：([0-9]+)').findall(link)
    if len(match) == 0:
        year = 0
    else:
        year = int(match[0])
    match = re.compile('<divclass="ct">(.+?)</ul>').findall(link)
    match0 = re.compile('href="tv_play-(.+?).html">(.+?)</a>').findall(match[0])
    for i in range(0,len(match0)):
        name1 = name+'【'+match0[i][1]+'】'
        li = xbmcgui.ListItem(name1, iconImage = '', thumbnailImage = thumb)
        li.setInfo(type = "Video", infoLabels = {"Title":name1, "Director":director, "Cast":cast, "Plot":plot, "Year":year})
        u = sys.argv[0] + "?mode=5&name=" + urllib.quote_plus(name1) + "&url=" + urllib.quote_plus('http://casting.openv.com/PLGS/plgs.php?pid='+match0[i][0])
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li)
        #addLink(name+'【'+match0[i][1]+'】','http://casting.openv.com/PLGS/plgs.php?pid='+match0[i][0],5,'')

def PlayVideo(url,name):
    playlist = xbmc.PlayList(1)
    playlist.clear()
    link = GetHttpData(url)
    match = re.compile('<flvpath>(.+?)</flvpath>').findall(link)
    for i in range(0,len(match)):
        listitem = xbmcgui.ListItem(name)
        listitem.setInfo(type="Video",infoLabels={"Title":name})
        playlist.add(match[i], listitem)
    xbmc.Player().play(playlist)

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

def addLink(name,url,mode,iconimage):
    u = sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
    ok = True
    liz = xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name } )
    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz)
    return ok

def addDir(name,url,mode,iconimage):
    u = sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
    ok=True
    liz = xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name } )
    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
    return ok

params=get_params()
url=None
name=None
mode=None

try:
    url=urllib.unquote_plus(params["url"])
except:
    pass
try:
    name=urllib.unquote_plus(params["name"])
except:
    pass
try:
    mode=int(params["mode"])
except:
    pass

if mode==None:
    CATEGORIES()

elif mode==1:
    Channels(url,name) 
 
elif mode==2:
    ChannelsA(url,name)
      
elif mode==3:
    Lists(url,name)

elif mode==5:
    PlayVideo(url,name)

elif mode==6:
    ListsA(url,name)

elif mode==7:
    ListsB(url,name)

xbmcplugin.endOfDirectory(int(sys.argv[1]))

