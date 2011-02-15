# -*- coding: cp936 -*-
import urllib,urllib2,re,os,xbmcplugin,xbmcgui,xbmc

#音悦台MV- by skyemperor 2011.
#Version 1.0.0  2011-2-12

def Root(ctl):
    for i in ctl[None][2]:
        addDir(ctl[i][1],get_realurl(ctl[i][2]),i,'')
    
def SubTree(ctl,mode,lists):
    addDir('当前位置：'+ctl[mode][1],get_realurl(ctl[mode][2]),mode,'')
    for i in lists:
        addDir(ctl[i][1],get_realurl(ctl[i][2]),i,'')


def RecommendMV(url,name,mode):
    addDir(u'当前位置：推荐MV'.encode('utf8'),url,mode,'')
    link=get_content(url)
    if link == None:
        return
    link=re.sub(' ','',link)
    match=re.compile('<inputtype="radio"id="(.+?)"name=\'area\'onclick="javascript:document.location=\'(.+?)\'"value="(.+?)"').findall(link)
    for id,url1,name1 in match:
        addDir(name1,get_realurl(url1),mode+1,'')

def ListRecommendMV(url,name,mode):
    link=get_content(url)
    if link == None:
        return
    match0=re.compile('<div class="page-nav">(.+?)</div>').findall(link)
    match1=re.compile('<a href="(.+?)">(.+?)</a>').findall(match0[0])
    cur=url.split('/')
    curpos=cur[len(cur)-1]
    if curpos.isdigit():
        curpos=cur[len(cur)-2]
    if curpos=='MV':
        curpos=u'全部MV'.encode('utf8')
    elif curpos=='CN':
        curpos=u'华语MV'.encode('utf8')
    elif curpos=='US':
        curpos=u'欧美MV'.encode('utf8')
    elif curpos=='JK':
        curpos=u'日韩MV'.encode('utf8')
    if match0 != []:
        curpage=re.compile('<span>(.+?)</span>').findall(match0[0])
        addDir(u'当前位置：推荐MV>'.encode('utf8')+curpos+u' 第'.encode('utf8')+curpage[0]+u'页'.encode('utf8'),url,mode,'')
    else:
        addDir(u'当前位置：推荐MV>'.encode('utf8')+curpos,url,mode,'')

    match=re.compile('<div class="info"><div class="title"><a href="(.+?)" title="(.+?)" target="_blank" class="song_name">(.+?)</a>--<a href="(.+?)" title="(.+?)" class="link_people" target="_blank">').findall(link)
    for url1,title,title1,fanclub,artist in match:
        addLink(title,artist,get_realurl(url1),255,'')
    for pageurl,pagenum in match1:
        if pagenum.isdigit():
            addDir(u'..第'.encode('utf8')+pagenum+u'页'.encode('utf8'),get_realurl(pageurl),mode,'')
        else:
           addDir(u'..'.encode('utf8')+pagenum,get_realurl(pageurl),mode,'')
    
def AllMV(url,name,mode):
    addDir(u'当前位置：全部MV'.encode('utf8'),url,mode,'')
    link=get_content(url)
    if link == None:
        return
    match=re.compile('<li title="(.+?)"><a href="(.+?)"(.+?)>(.+?)</a></li>').findall(link)
    for title,url1,cur,name1 in match:
        addDir(u'全部MV>'.encode('utf8')+name1,get_realurl(url1),mode+1,'')

def ListAllMV(url,name,mode):
    link=get_content(url)
    if link == None:
        return
    #match=re.compile('<div class="thumb"><a href="(.+?)" target="_blank" class="img"><img src="(.+?)\?t=(.+?)" alt="(.+?)"/>').findall(link)
    #for url1,img,time,title in match:
    #        addLink(title,'','http://www.yinyuetai.com'+url1,255,'http://www.yinyuetai.com'+img)
    curpos1=re.compile('<a href="(.+?)" class="current">(.+?)</a>').findall(link)
    curpos2=re.compile('<li title="(.+?)"><a href="(.+?)" class="current">(.+?)</a></li>').findall(link)
    match0=re.compile('<div class="page-nav">(.+?)</div>').findall(link)
    match=re.compile('<div class="title"><a href="(.+?)" title="(.+?)" target="_blank">(.+?)</a></div><div class="artis">--<a href="(.+?)" title="(.+?)" class="link_people" target="_blank">').findall(link)
    if match0 != []:
        curpage=re.compile('<span>(.+?)</span>').findall(match0[0])
        addDir(u'当前位置：'.encode('utf8')+curpos1[0][1]+'>'+curpos2[0][2]+u' 第'.encode('utf8')+curpage[0]+u'页'.encode('utf8'),url,mode,'')
    else:
        addDir(u'当前位置：'.encode('utf8')+curpos1[0][1]+'>'+curpos2[0][2]+name,url,mode,'')
    for url1,title,title1,fanclub,artist in match:
        addLink(title,artist,get_realurl(url1),255,'')
    if match0 != []:
        match1=re.compile('<a href="(.+?)">(.+?)</a>').findall(match0[0])
        for pageurl,pagenum in match1:
            if pagenum.isdigit():
                addDir(u'..第'.encode('utf8')+pagenum+u'页'.encode('utf8'),get_realurl(pageurl),mode,'')
            else:
                addDir(u'..'.encode('utf8')+pagenum,get_realurl(pageurl),mode,'')

def get_playlistpage(url,name,mode):
    link=get_content(url)
    if link == None:
        return
    match0=re.compile('<div class="page-nav">(.+?)</div>').findall(link)
    match=re.compile('<div class="thumb"><a href="(.+?)" target="_blank" title="(.+?)"><img src="(.+?)" alt="(.+?)"><span></span></a></div>').findall(link)
    curpos='当前位置：' + name
    if len(match0) > 0:
        curpage=re.compile('<span>(.+?)</span>').findall(match0[0])
        if len(curpage) > 0:
            curpos = curpos + ' 第' + curpage[0] + '页'
    addDir(curpos,url,mode,'')
    for url1,title,img,title1 in match:
        addDir(title,get_realurl(url1),256,get_realurl(img))
    if len(match0)>0:
        match1=re.compile('<a href="(.+?)" >(.+?)</a>').findall(match0[0])
        for pageurl,pagenum in match1:
            if pagenum.isdigit():
                addDir(u'..第'.encode('utf8')+pagenum+u'页'.encode('utf8'),get_realurl(pageurl),mode,'')
            else:
                addDir(u'..'.encode('utf8')+pagenum,get_realurl(pageurl),mode,'')
        match2=re.compile('<span class="separator">...</span>(.+?)</a><a href="(.+?)" class="nextpage">').findall(match0[0])
        for temp,nextpageurl in match2:
            addDir(u'..下一页'.encode('utf8'),get_realurl(nextpageurl),mode,'')

def ShowPlayList(url,name,mode,handle):
    link=get_content(url)
    if link == None:
        return
    pltitle=re.compile('<h2>(.+?)</h2>').findall(link)
    match0=re.compile('<div id="videoList" class="hidden">(.+?)</div><div class="subNav">').findall(link)
    match1=re.compile('<div>(.+?)</div>').findall(match0[0])
    if len(pltitle)>0:
        addDir(u'悦单名称：'.encode('utf8')+pltitle[0],url,mode,'')
    addDir(u'收录歌曲数：'.encode('utf8')+len(match1).__str__()+u'首'.encode('utf8'),url,mode,'')
    for match2 in match1:
        match=re.compile('<span name="(.+?)">(.+?)</span>').findall(match2)
        addLink(match[1][1],match[3][1],get_realurl('/video/'+match[0][1]),handle,get_realurl(match[4][1]))

def get_artistpage(url,name,mode,handle):
    link=get_content(url)
    if link == None:
        return
    match0=re.compile('<div class="page-nav">(.+?)</div>').findall(link)
    matchA=re.compile('<div class="letterCategory">(.+?)</div>').findall(link)
    match=re.compile('<span class="groupcover"><a href="(.+?)" target="_blank"><img src="(.+?)"/></a></span><div class="info"><a href="(.+?)" target="_blank" class="song" title="(.+?)">').findall(link)
    curpos='当前位置：' + name
    if len(matchA) > 0:
        curletter=re.compile('<a href="(.+?)" class="current">(.+?)</a>').findall(matchA[0])
        if len(curletter) > 0:
            curpos = curpos + '>' + curletter[0][1]
    if len(match0) > 0:
        curpage=re.compile('<span>(.+?)</span>').findall(match0[0])
        if len(curletter) > 0:
            curpos = curpos + ' 第' + curpage[0] + '页'
    addDir(curpos,url,mode,'')
    for url1,img,url2,title in match:
        artistid = url1.split('/')[2]
        addDir(title,get_realurl('/fanclub/mv-all/'+artistid+'/toNew'),handle,get_realurl(img))
    if len(matchA) > 0:
        matchB=re.compile('<a href="(.+?)" >(.+?)</a>').findall(matchA[0])
        for letterurl,letter in matchB:
            addDir(letter,get_realurl(letterurl),mode,'')
    if len(match0) > 0:
        match1=re.compile('<a href="(.+?)">(.+?)</a>').findall(match0[0])
        for pageurl,pagenum in match1:
            if pagenum.isdigit():
                addDir(u'..第'.encode('utf8')+pagenum+u'页'.encode('utf8'),get_realurl(pageurl),mode,'')
            else:
                addDir(u'..'.encode('utf8')+pagenum,get_realurl(pageurl),mode,'')
        match2=re.compile('<span class="separator">...</span>(.+?)</a><a href="(.+?)" class="nextpage">').findall(match0[0])
        for temp,nextpageurl in match2:
            addDir(u'..下一页'.encode('utf8'),get_realurl(nextpageurl),mode,'')

def ShowArtistMV(url,name,mode,handle):
    link=get_content(url)
    if link == None:
        return
    artist=re.compile('<h1>(.+?)</h1>').findall(link)
    match0=re.compile('<div class="page-nav">(.+?)</div>').findall(link)
    curpos=u'当前位置：歌手>'.encode('utf8')+name
    if len(artist) > 0:
        curpos=curpos+artist[0]
    if len(match0) > 0:
        curpage=re.compile('<span>(.+?)</span>').findall(match0[0])
        if len(curpage) > 0:
            curpos = curpos + u' 第'.encode('utf8') + curpage[0] + u'页'.encode('utf8')
    addDir(curpos,url,mode,'')
    match=re.compile('<div class="thumb"><a target="_blank" title="(.+?)" href="(.+?)"><img src="(.+?)" alt=""/>').findall(link)
    for title,url1,imgurl in match:
        addLink(title,artist[0],get_realurl(url1),handle,get_realurl(imgurl))
    if len(match0) > 0:
        match1=re.compile('<a href="(.+?)">(.+?)</a>').findall(match0[0])
        for pageurl,pagenum in match1:
            if pagenum.isdigit():
                addDir(u'..第'.encode('utf8')+pagenum+u'页'.encode('utf8'),get_realurl(pageurl),mode,'')
            else:
                addDir(u'..'.encode('utf8')+pagenum,get_realurl(pageurl),mode,'')

def PlayMV(url,name,artist):
    playlist=xbmc.PlayList(0)
    playlist.clear()
    link=get_content('http://www.flvcd.com/parse.php?kw='+url)
    if link == None:
        return
    link=re.sub(" ","",link)
    match=re.compile('下载地址：<ahref="(.+?)"target="_blank"class="link"').findall(link)
    for flvLink in match:
        listitem=xbmcgui.ListItem(name)
        listitem.setInfo(type="Video",infoLabels={"Title":name,"Artist":artist})
        playlist.add(flvLink, listitem)
    xbmc.Player().play(playlist)


def get_realurl(url):
    return 'http://www.yinyuetai.com'+url

def get_content(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    try:
        response = urllib2.urlopen(req)
    except:
        return None
    link=response.read()
    response.close()
    link=re.sub('\r|\n|\t','',link)
    return link    
           
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

def addLink(name,artist,url,mode,iconimage):
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&artist="+urllib.quote_plus(artist)
    pic=iconimage.split('?')
    ok=True
    li=xbmcgui.ListItem(name+u' 【'.encode('utf8')+artist+u'】'.encode('utf8'),'',pic[0],pic[0])
    li.setInfo( type="Video", infoLabels={ "Title": name,"Artist": artist } )
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=li)
    return ok

def addDir(name,url,mode,iconimage):
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
    ok=True
    li=xbmcgui.ListItem(name, iconImage=os.getcwd()+'\\icon.gif', thumbnailImage=iconimage)
    li.setInfo( type="Video", infoLabels={ "Title": name } )
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=li,isFolder=True)
    return ok
  

params=get_params()
url=None
name=None
mode=None
artist=None

try:
    url=urllib.unquote_plus(params["url"])
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
    mode=int(params["mode"])
except:
    pass

ctl = {
            None : ('Root(ctl)','音悦台MV',(32,44,3,5,6,7,43)),
            1    : ('RecommendMV(url,name,mode)','推荐MV','/lookVideo'),
            2    : ('ListRecommendMV(url,name,mode)','推荐MV'),
            3    : ('AllMV(url,name,mode)','全部MV','/lookAllVideo'),
            4    : ('ListAllMV(url,name,mode)','全部MV'),
            5    : ('get_playlistpage(url,ctl[mode][1],mode)','全部悦单','/pl/playlist_all'),
            6    : ('SubTree(ctl,mode,(8,13,18,23))','热门悦单','/pl/playlist_hot'),
            7    : ('get_playlistpage(url,ctl[mode][1],mode)','编辑推荐悦单','/pl/playlist_promo'),
            8    : ('SubTree(ctl,mode,(9,10,11,12))','热门评论悦单','/pl/playlist_hotComment'),
            9    : ('get_playlistpage(url,ctl[mode][1],mode)','24小时热门评论悦单','/pl/playlist_hotComment/today'),
            10   : ('get_playlistpage(url,ctl[mode][1],mode)','本周热门评论悦单','/pl/playlist_hotComment/week'),
            11   : ('get_playlistpage(url,ctl[mode][1],mode)','本月热门评论悦单','/pl/playlist_hotComment/month'),
            12   : ('get_playlistpage(url,ctl[mode][1],mode)','全部热门评论悦单','/pl/playlist_hotComment/all'),
            13   : ('SubTree(ctl,mode,(14,15,16,17))','热门收藏悦单','/pl/playlist_hotFavorite'),
            14   : ('get_playlistpage(url,ctl[mode][1],mode)','24小时热门收藏悦单','/pl/playlist_hotFavorite/today'),
            15   : ('get_playlistpage(url,ctl[mode][1],mode)','本周热门收藏悦单','/pl/playlist_hotFavorite/week'),
            16   : ('get_playlistpage(url,ctl[mode][1],mode)','本月热门收藏悦单','/pl/playlist_hotFavorite/month'),
            17   : ('get_playlistpage(url,ctl[mode][1],mode)','全部热门收藏悦单','/pl/playlist_hotFavorite/all'),
            18   : ('SubTree(ctl,mode,(19,20,21,22))','热门推荐悦单','/pl/playlist_hotRecommend'),
            19   : ('get_playlistpage(url,ctl[mode][1],mode)','24小时热门推荐悦单','/pl/playlist_hotRecommend/today'),
            20   : ('get_playlistpage(url,ctl[mode][1],mode)','本周热门推荐悦单','/pl/playlist_hotRecommend/week'),
            21   : ('get_playlistpage(url,ctl[mode][1],mode)','本月热门推荐悦单','/pl/playlist_hotRecommend/month'),
            22   : ('get_playlistpage(url,ctl[mode][1],mode)','全部热门推荐悦单','/pl/playlist_hotRecommend/all'),
            23   : ('SubTree(ctl,mode,(24,25,26,27))','热门播放悦单','/pl/playlist_hotView'),
            24   : ('get_playlistpage(url,ctl[mode][1],mode)','24小时热门播放悦单','/pl/playlist_hotView/today'),
            25   : ('get_playlistpage(url,ctl[mode][1],mode)','本周热门播放悦单','/pl/playlist_hotView/week'),
            26   : ('get_playlistpage(url,ctl[mode][1],mode)','本月热门播放悦单','/pl/playlist_hotView/month'),
            27   : ('get_playlistpage(url,ctl[mode][1],mode)','全部热门播放悦单','/pl/playlist_hotView/all'),
            28   : ('get_playlistpage(url,ctl[mode][1],mode)','最新推荐悦单','/pl/playlist_newRecommend'),
            29   : ('get_playlistpage(url,ctl[mode][1],mode)','最新收藏悦单','/pl/playlist_newFavorite'),
            30   : ('get_playlistpage(url,ctl[mode][1],mode)','最新评论悦单','/pl/playlist_newComment'),
            31   : ('get_playlistpage(url,ctl[mode][1],mode)','最新创建悦单','/pl/playlist_newCreate'),
            32   : ('SubTree(ctl,mode,(33,34,35,36,37,38,39,40,41,42))','歌手','/fanAll'),
            33   : ('get_artistpage(url,ctl[mode][1],mode,257)','全部歌手','/fanAll'),
            34   : ('get_artistpage(url,ctl[mode][1],mode,257)','华语男歌手','/fanAll?area=CN&property=Boy'),
            35   : ('get_artistpage(url,ctl[mode][1],mode,257)','华语女歌手','/fanAll?area=CN&property=Girl'),
            36   : ('get_artistpage(url,ctl[mode][1],mode,257)','华语乐队/组合','/fanAll?area=CN&property=Combo'),
            37   : ('get_artistpage(url,ctl[mode][1],mode,257)','日韩男歌手','/fanAll?area=JK&property=Boy'),
            38   : ('get_artistpage(url,ctl[mode][1],mode,257)','日韩女歌手','/fanAll?area=JK&property=Girl'),
            39   : ('get_artistpage(url,ctl[mode][1],mode,257)','日韩乐队/组合','/fanAll?area=JK&property=Combo'),
            40   : ('get_artistpage(url,ctl[mode][1],mode,257)','欧美男歌手','/fanAll?area=US&property=Boy'),
            41   : ('get_artistpage(url,ctl[mode][1],mode,257)','欧美女歌手','/fanAll?area=US&property=Girl'),
            42   : ('get_artistpage(url,ctl[mode][1],mode,257)','欧美乐队/组合','/fanAll?area=US&property=Combo'),
            43   : ('SubTree(ctl,mode,(28,29,30,31))','最新悦单','/pl/playlist_new'),
            44   : ('SubTree(ctl,mode,(45,46,47,48))','推荐MV','/lookVideo'),
            45   : ('ListRecommendMV(url,name,mode)','全部推荐MV','/lookVideo-area/MV'),
            46   : ('ListRecommendMV(url,name,mode)','华语推荐MV','/lookVideo-area/CN'),
            47   : ('ListRecommendMV(url,name,mode)','欧美推荐MV','/lookVideo-area/US'),
            48   : ('ListRecommendMV(url,name,mode)','日韩推荐MV','/lookVideo-area/JK'),
            255  : ('PlayMV(url,name,artist)','播放MV'),
            256  : ('ShowPlayList(url,name,mode,255)','显示悦单'),
            257  : ('ShowArtistMV(url,name,mode,255)','显示歌手MV')
      }
exec(ctl[mode][0])
#xbmcplugin.setPluginCategory(int(sys.argv[1]), ctl[mode][1])
xbmcplugin.endOfDirectory(int(sys.argv[1]))
