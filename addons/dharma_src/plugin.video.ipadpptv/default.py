# -*- coding: utf-8 -*-
import xbmc, xbmcgui, xbmcplugin, xbmcaddon, urllib2, urllib, re, string, sys, os, gzip, StringIO

# PPTV IPAD专区视频(ipad.pptv.com) by wow1122(wht9000@gmail.com), 2011

# Plugin constants 
__addonname__ = "PPTV IPAD专区视频(ipad.pptv.com)"
__addonid__ = "plugin.video.ipadpptv"
__addon__ = xbmcaddon.Addon(id=__addonid__)
__addonicon__ = os.path.join( __addon__.getAddonInfo('path'), 'icon.png' )

#UserAgent = 'Mozilla/5.0(iPad; U; CPU iPhone OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B314 Safari/531.21.10'
UserAgent = 'Mozilla/5.0(iPad; U; CPU OS 4_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8F191 Safari/6533.18.5'

def GetHttpData(url):
	print "GetHttpData %s " % url
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
    
def searchDict(dlist,idx):
    for i in range(0,len(dlist)):
        if dlist[i][0] == idx:
            return dlist[i][1]
    return ''
    
def getList(listpage):
    catlist = re.compile('<a href="(.+?).htm" title="(.+?)"', re.DOTALL).findall(listpage)
    return catlist 
         
def rootList():
    li=xbmcgui.ListItem('新上线')
    u=sys.argv[0]+"?mode=1&name="+urllib.quote_plus('新上线')+"&type="+urllib.quote_plus('new')+"&cat="+urllib.quote_plus('')+"&page="+urllib.quote_plus('1')
    xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
    li=xbmcgui.ListItem('电影')
    u=sys.argv[0]+"?mode=1&name="+urllib.quote_plus('电影')+"&type="+urllib.quote_plus('movie')+"&cat="+urllib.quote_plus('')+"&page="+urllib.quote_plus('1')
    xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
    li=xbmcgui.ListItem('电视剧')
    u=sys.argv[0]+"?mode=1&name="+urllib.quote_plus('电视剧')+"&type="+urllib.quote_plus('tv')+"&cat="+urllib.quote_plus('')+"&page="+urllib.quote_plus('1')
    xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
    li=xbmcgui.ListItem('动漫')
    u=sys.argv[0]+"?mode=1&name="+urllib.quote_plus('动漫')+"&type="+urllib.quote_plus('cartoon')+"&cat="+urllib.quote_plus('')+"&page="+urllib.quote_plus('1')
    xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
    li=xbmcgui.ListItem('综艺')
    u=sys.argv[0]+"?mode=1&name="+urllib.quote_plus('综艺')+"&type="+urllib.quote_plus('show')+"&cat="+urllib.quote_plus('')+"&page="+urllib.quote_plus('1')
    xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
    li=xbmcgui.ListItem('资讯')
    u=sys.argv[0]+"?mode=1&name="+urllib.quote_plus('资讯')+"&type="+urllib.quote_plus('info')+"&cat="+urllib.quote_plus('')+"&page="+urllib.quote_plus('1')
    xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
    li=xbmcgui.ListItem('体育')
    u=sys.argv[0]+"?mode=1&name="+urllib.quote_plus('体育')+"&type="+urllib.quote_plus('sport')+"&cat="+urllib.quote_plus('')+"&page="+urllib.quote_plus('1')
    xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
    li=xbmcgui.ListItem('游戏')
    u=sys.argv[0]+"?mode=1&name="+urllib.quote_plus('游戏')+"&type="+urllib.quote_plus('game')+"&cat="+urllib.quote_plus('')+"&page="+urllib.quote_plus('1')
    xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
    xbmcplugin.endOfDirectory(int(sys.argv[1]))
    
def progList(name,type,cat,page):
    if cat.find('_')==-1:
        url = 'http://ipad.pptv.com/'+type+'_p'+page+'.htm'
    else:
        url = 'http://ipad.pptv.com/'+cat+'_p'+page+'.htm'
    link = GetHttpData(url)
    print "progList %s " % url
    match = re.compile('<dt>类型：</dt>(.+?)</dl>', re.DOTALL).findall(link)
    if len(match):
        listpage = match[0]
    else:
        listpage = ''
    catlist=getList(listpage)
    if cat.find('_')==-1:
        catstr='全部'
    else:
        clist=cat.split('_')
        if len(clist)==2:
           catstr = searchDict(catlist,cat)
        else:
           print cat[:-6]
           catstr = searchDict(catlist,cat[:-6])
           match = re.compile('<dt>全部子分类：</dt>(.+?)</dd>',re.DOTALL).findall(link)
           if match:
                match1 = re.compile('class="now">(.+?)</a>').findall(match[0])
                catstr = catstr+'-'+match1[0]
                
    match = re.compile('<li>(.+?)</li>', re.DOTALL).findall(link)
    totalItems = len(match)           

    li = xbmcgui.ListItem('类型[COLOR FFFF0000]【' + catstr + '】[/COLOR] （按此选择）')
    u = sys.argv[0] + "?mode=5&name="+urllib.quote_plus(name)+"&type="+urllib.quote_plus(type)+"&cat="+urllib.quote_plus(cat)+"&page="+urllib.quote_plus(listpage)
    xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, True, totalItems)
                

    for i in range(0,len(match)):
        match1 = re.compile('<a href="(.+?)" title="(.+?)" class="img"><img src="(.+?)" width=', re.DOTALL).findall(match[i])
        for p_id,p_name,p_thumb in match1:
            li = xbmcgui.ListItem(p_name, iconImage = '', thumbnailImage = p_thumb)
            u = sys.argv[0]+"?mode=2&name="+urllib.quote_plus(p_name)+"&url="+urllib.quote_plus('http://ipad.pptv.com/'+p_id)+"&thumb="+urllib.quote_plus(p_thumb)
            xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, True, totalItems)

    match = re.compile('<nav class="pageNum c_b">(.+?)</nav>', re.DOTALL).findall(link)
    match1= re.compile('<a class="" href=".+?">(.+?)</a>', re.DOTALL).findall(match[0])
    totalpages=match1[len(match1)-2]
    currpage=int(page)
    if currpage > 1:
        li = xbmcgui.ListItem('上一页')
        u = sys.argv[0]+"?mode=1&name="+urllib.quote_plus(name)+"&type="+urllib.quote_plus(type)+"&cat="+urllib.quote_plus(cat)+"&page="+urllib.quote_plus(str(currpage-1))
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, True, totalItems)
    if currpage < totalpages:
        li = xbmcgui.ListItem('下一页')
        u = sys.argv[0]+"?mode=1&name="+urllib.quote_plus(name)+"&type="+urllib.quote_plus(type)+"&cat="+urllib.quote_plus(cat)+"&page="+urllib.quote_plus(str(currpage+1))
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, True, totalItems)
    xbmcplugin.setContent(int(sys.argv[1]), 'movies')
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

def ListA(name,url,thumb):
    link = GetHttpData(url)
    match = re.compile('var PlayList = \["(.+?)"\];').findall(link)   
    vid=match[0]
    print vid
    if len(vid)==32:
        PlayVideo(name,vid,thumb)
    else:
        ListB(name,url,thumb)

    
def ListB(name,url,thumb):
    link = GetHttpData(url)
    match = re.compile('var PlayList = \["(.+?)"\];').findall(link)  
    vid=match[0]
    vidlist=vid.split('","')
    match= re.compile('<a href="#" onclick=.+?>(.+?)</a>').findall(link) 
    for i in range(len(vidlist)):
        print match[i]
        li = xbmcgui.ListItem(match[i], iconImage = '', thumbnailImage = thumb)
        u = sys.argv[0]+"?mode=10&name="+urllib.quote_plus(match[i])+"&url="+urllib.quote_plus(vidlist[i])+"&thumb="+urllib.quote_plus(thumb)
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, False, len(vidlist))
    xbmcplugin.setContent(int(sys.argv[1]), 'movies')
    xbmcplugin.endOfDirectory(int(sys.argv[1]))
    
def PlayVideo(name,url,thumb):
    link = GetHttpData('http://ipad.pptv.com/api/ipad/list.js?cb=load.cbs.cb_1&md5='+url)
    print 'http://ipad.pptv.com/api/ipad/list.js?cb=load.cbs.cb_1&md5='+url
    print "PlayVideo link %s " % link
    match = re.compile('"m3u":"(.+?)","').findall(link)   
    url=match[0].replace('\\', '')
    print url
    host=url.replace('http://','')
    host='http://'+host.split('/')[0]+'/'
    #print host
    link = GetHttpData(url)
    #print link
    #EXTINF:10,
    match = re.compile('(/.+?.ts)').findall(link)    
    playlist=xbmc.PlayList(1)
    playlist.clear()
    for i in range(0,len(match)):
        listitem = xbmcgui.ListItem(name, thumbnailImage = __addonicon__)
        listitem.setInfo(type="Video",infoLabels={"Title":name+" 第"+str(i+1)+"/"+str(len(match))+" 节"})
        #listitem.setInfo(type="Video",infoLabels={"Title":name})
        fileurl = match[i]
        if fileurl.find('/') == 0:
            fileurl = fileurl[1:len(fileurl)]
        fileurl = fileurl.replace('_0_10.','_0_0.')
        playlist.add(host+fileurl, listitem)
        break  #只执行1次
    print playlist
    xbmc.Player().play(playlist)

def performChanges(name,type,page,cat):
    catlist = getList(page)
    change = False
    dialog = xbmcgui.Dialog()
    if len(catlist)>0:
        list = [x[1] for x in catlist]
        sel = dialog.select('类型', list)
        if sel != -1:
            cat = catlist[sel][0]
            change = True
            if cat.find('_')!=-1:
                link = GetHttpData('http://ipad.pptv.com/'+cat+'_p1.htm')
                match = re.compile('<dt>全部子分类：</dt>(.+?)</dd>', re.DOTALL).findall(link)
                if match:
                    catlist = re.compile('<a href="(.+?).htm" title="(.+?)"').findall(match[0])
                    if len(catlist)>0:
                        list = [x[1] for x in catlist]
                        dialog = xbmcgui.Dialog()
                        sel = dialog.select('子分类', list)
                        if sel != -1:
                            if catlist[sel][1]!='全部':
                                cat = catlist[sel][0]
    if change:
        progList(name,type,cat,'1')
    
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
url = ''
thumb = None
type = ''
cat = ''
page = ''
try:
    thumb = urllib.unquote_plus(params["thumb"])
except:
    pass
try:
    url = urllib.unquote_plus(params["url"])
except:
    pass
try:
    type = urllib.unquote_plus(params["type"])
except:
    pass 
try:
    cat = urllib.unquote_plus(params["cat"])
except:
    pass
try:
    page = urllib.unquote_plus(params["page"])
except:
    pass    
try:
    name = urllib.unquote_plus(params["name"])
except:
    pass
try:
    mode = int(params["mode"])
except:
    pass

if mode != None:
    print 'params mode %d' % mode

if mode == None:
    rootList()
elif mode == 1:
    progList(name,type,cat,page)
elif mode == 2:
    ListA(name,url,thumb)
elif mode == 5:
    performChanges(name,type,page,cat)
elif mode == 10:
    PlayVideo(name,url,thumb)

