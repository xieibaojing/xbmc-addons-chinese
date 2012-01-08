# -*- coding: utf-8 -*-
import xbmc,xbmcgui,xbmcplugin,xbmcaddon,urllib2,urllib,re,sys,os

# 中国网络电视台点播(CNTV)
# Write by robinttt 2010.
# Update by taxigps 2011

# Plugin constants 
__addonname__ = "中国网络电视台点播(CNTV)"
__addonid__ = "plugin.video.cntv"
__addon__ = xbmcaddon.Addon(id=__addonid__)
__addonpath__ = __addon__.getAddonInfo('path')
MEDIA_PATH = xbmc.translatePath(os.path.join(__addonpath__,'resources','media'))

def GetHttpData(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    httpdata = response.read()
    response.close()
    match = re.compile('<meta http-equiv="Content-Type" content="text/html; charset=(.+?)" />').findall(httpdata)
    if len(match)>0:
        charset = match[0].lower()
        if (charset != 'utf-8') and (charset != 'utf8'):
            httpdata = unicode(httpdata, charset).encode('utf8')
    return httpdata

def Roots():
    thumb=os.path.join(MEDIA_PATH,'xiyou.png')
    li=xbmcgui.ListItem('爱西柚',iconImage='',thumbnailImage=thumb)
    u=sys.argv[0]+"?mode=1&name="+urllib.quote_plus('爱西柚')
    xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
    thumb=os.path.join(MEDIA_PATH,'bugu.png')
    li=xbmcgui.ListItem('爱布谷',iconImage='',thumbnailImage=thumb)
    u=sys.argv[0]+"?mode=8&name="+urllib.quote_plus('爱布谷')
    xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)

def BuguA(name):
    li=xbmcgui.ListItem(name+'>分类查询')
    u=sys.argv[0]+"?mode=9&name="+urllib.quote_plus(name+'>分类查询')+"&url="+urllib.quote_plus('http://bugu.cntv.cn/category/index.shtml')
    xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
    li=xbmcgui.ListItem(name+'>频道查询')
    u=sys.argv[0]+"?mode=9&name="+urllib.quote_plus(name+'>频道查询')+"&url="+urllib.quote_plus('http://bugu.cntv.cn/channel/index.shtml')
    xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
    li=xbmcgui.ListItem(name+'>活动大全')
    u=sys.argv[0]+"?mode=9&name="+urllib.quote_plus(name+'>活动大全')+"&url="+urllib.quote_plus('http://bugu.cntv.cn/specials_A-Z/index.shtml')
    xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
    li=xbmcgui.ListItem(name+'>节目大全')
    u=sys.argv[0]+"?mode=9&name="+urllib.quote_plus(name+'>节目大全')+"&url="+urllib.quote_plus('http://bugu.cntv.cn/television/index.shtml')
    xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)

def BuguB(name,url):
    link=GetHttpData(url)
    link=re.sub('\r','',link)
    link=re.sub('\n','',link)
    link=re.sub('\t','',link)
    match=re.compile('<p class="edh"(.+?)id="(.+?)">(.+?)</p>').findall(link)
    for i in range(0,len(match)):
        name1=re.sub('<a(.+?)>','',match[i][2])
        name1=re.sub('</a>','',name1)
        li=xbmcgui.ListItem(name+'>'+name1)
        u=sys.argv[0]+"?mode=10&name="+urllib.quote_plus(name+'>'+name1)+"&url="+urllib.quote_plus(url)+"&id="+urllib.quote_plus('<p class="edh"'+match[i][0]+'id="'+match[i][1]+'">'+match[i][2]+'</p>')
        xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)

def BuguC(name,url,id):
    link=GetHttpData(url)
    link=re.sub('\r','',link)
    link=re.sub('\n','',link)
    link=re.sub('\t','',link)
    match=re.compile(id+'(.+?)</table>').findall(link)
    match0=re.compile('href="(.+?)" target="_blank" class="cyan">(.+?)</a>').findall(match[0])
    for url1,name1 in match0:
        li=xbmcgui.ListItem(name+'>'+name1)
        u=sys.argv[0]+"?mode=11&name="+urllib.quote_plus(name+'>'+name1)+"&url="+urllib.quote_plus(url1)
        xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)

def BuguD(name,url):
    li=xbmcgui.ListItem('当前位置：'+name)
    u=sys.argv[0]+"?mode=20&name="+urllib.quote_plus(name)
    xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
    link=GetHttpData(url)
    match=re.compile('var brief="(.+?)";').findall(link)
    plot=match[0]
    match=re.compile("new title_array\('(.+?)','(.+?)','(.+?)','(.+?)'").findall(link)
    for i in range(0,len(match)):
        li=xbmcgui.ListItem(str(i+1)+'. '+match[i][0]+'  (时长:'+match[i][2]+')',iconImage='',thumbnailImage=match[i][1])
        u=sys.argv[0]+"?mode=12&name="+urllib.quote_plus(match[i][0])+"&url="+urllib.quote_plus(match[i][3])+"&plot="+urllib.quote_plus(plot)+"&thumb="+urllib.quote_plus(match[i][1])
        xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li)

def BuguE(name,url,thumb,plot):
    playlist=xbmc.PlayList(1)
    playlist.clear()
    link=GetHttpData(url)
    match=re.compile('\("videoCenterId","(.+?)"\)').findall(link)
    url='http://vdd.player.cntv.cn/index.php?pid='+match[0]
    link=GetHttpData(url)
    match=re.compile('"chapters":\[(.+?)\]').findall(link)
    match0=re.compile('"url":"(.+?)"').findall(match[0])
    for i in range(0,len(match0)):
        listitem=xbmcgui.ListItem(name,iconImage='',thumbnailImage=thumb)
        listitem.setInfo(type="Video",infoLabels={"Title":name,"plot":plot})
        playlist.add(match0[i].replace('\\',''), listitem)
    xbmc.Player().play(playlist)

def XiyouA(name):
    li=xbmcgui.ListItem(name+'>视频')
    u=sys.argv[0]+"?mode=2&name="+urllib.quote_plus(name+'>视频')+"&category="+urllib.quote_plus('video')
    xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
    li=xbmcgui.ListItem(name+'>专辑')
    u=sys.argv[0]+"?mode=2&name="+urllib.quote_plus(name+'>专辑')+"&category="+urllib.quote_plus('plist')
    xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)

def XiyouB(name,category):
    link=GetHttpData('http://xiyou.cntv.cn/'+category+'/index-hot-week.html')
    link=re.sub('\r','',link)
    link=re.sub('\n','',link)
    link=re.sub('\t','',link)
    li=xbmcgui.ListItem(name+'>全部')
    u=sys.argv[0]+"?mode=3&name="+urllib.quote_plus(name+'>全部')+"&category="+urllib.quote_plus(category)+"&id="+urllib.quote_plus('0')
    xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
    match=re.compile('<li><a href="/'+category+'/index-hot-week-([0-9]+).html"><span class="hotspan">(.+?)</span>').findall(link)
    for id,name1 in match:
        li=xbmcgui.ListItem(name+'>'+name1)
        u=sys.argv[0]+"?mode=3&name="+urllib.quote_plus(name+'>'+name1)+"&category="+urllib.quote_plus(category)+"&id="+urllib.quote_plus(id)
        xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)

def XiyouC(name,category,id):
    li=xbmcgui.ListItem(name+'>今日')
    u=sys.argv[0]+"?mode=4&name="+urllib.quote_plus(name+'>今日')+"&category="+urllib.quote_plus(category)+"&id="+urllib.quote_plus(id)+"&type="+urllib.quote_plus('-day')
    xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
    li=xbmcgui.ListItem(name+'>本周')
    u=sys.argv[0]+"?mode=4&name="+urllib.quote_plus(name+'>本周')+"&category="+urllib.quote_plus(category)+"&id="+urllib.quote_plus(id)+"&type="+urllib.quote_plus('-week')
    xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
    li=xbmcgui.ListItem(name+'>本月')
    u=sys.argv[0]+"?mode=4&name="+urllib.quote_plus(name+'>本月')+"&category="+urllib.quote_plus(category)+"&id="+urllib.quote_plus(id)+"&type="+urllib.quote_plus('-month')
    xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
    li=xbmcgui.ListItem(name+'>全部')
    u=sys.argv[0]+"?mode=4&name="+urllib.quote_plus(name+'>全部')+"&category="+urllib.quote_plus(category)+"&id="+urllib.quote_plus(id)+"&type="+urllib.quote_plus('')
    xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)

def XiyouD(name,category,id,type):
    li=xbmcgui.ListItem(name+'>播放最多')
    u=sys.argv[0]+"?mode=5&name="+urllib.quote_plus(name+'>播放最多')+"&category="+urllib.quote_plus(category)+"&id="+urllib.quote_plus(id)+"&type="+urllib.quote_plus(type)+"&handler="+urllib.quote_plus('-hot')+"&page="+urllib.quote_plus('1')
    xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
    li=xbmcgui.ListItem(name+'>收藏最多')
    u=sys.argv[0]+"?mode=5&name="+urllib.quote_plus(name+'>收藏最多')+"&category="+urllib.quote_plus(category)+"&id="+urllib.quote_plus(id)+"&type="+urllib.quote_plus(type)+"&handler="+urllib.quote_plus('-fav')+"&page="+urllib.quote_plus('1')
    xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
    if category=='video':
        li=xbmcgui.ListItem(name+'>评论最多')
        u=sys.argv[0]+"?mode=5&name="+urllib.quote_plus(name+'>评论最多')+"&category="+urllib.quote_plus(category)+"&id="+urllib.quote_plus(id)+"&type="+urllib.quote_plus(type)+"&handler="+urllib.quote_plus('-comment')+"&page="+urllib.quote_plus('1')
        xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
        li=xbmcgui.ListItem(name+'>顶的最多')
        u=sys.argv[0]+"?mode=5&name="+urllib.quote_plus(name+'>顶的最多')+"&category="+urllib.quote_plus(category)+"&id="+urllib.quote_plus(id)+"&type="+urllib.quote_plus(type)+"&handler="+urllib.quote_plus('-dig')+"&page="+urllib.quote_plus('1')
        xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
    li=xbmcgui.ListItem(name+'>最近更新')
    u=sys.argv[0]+"?mode=5&name="+urllib.quote_plus(name+'>最近更新')+"&category="+urllib.quote_plus(category)+"&id="+urllib.quote_plus(id)+"&type="+urllib.quote_plus(type)+"&handler="+urllib.quote_plus('-new')+"&page="+urllib.quote_plus('1')
    xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)

def XiyouE(name,category,handler,id,type,page):
    tmp='Ajax'+category+handler
    url='http://xiyou.cntv.cn/'+category+'/index'+handler+type+'-'+id+'-'+page+'.html'
    link=GetHttpData(url)
    link=re.sub('\r','',link)
    link=re.sub('\n','',link)
    link=re.sub('\t','',link)
    link=re.sub(' ','',link)

    li=xbmcgui.ListItem('当前位置：'+name+' 【第'+page+'页】')
    u=sys.argv[0]+"?mode=20"
    xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
    #获取当前列表
    if category=='video':
        match0=re.compile('<ulclass="video"><liclass="vimg"><atitle="(.+?)"href="(.+?)"target="_blank"><img.*?lazy-src="(.+?)"alt=".+?"></a><spanclass="vtime">(.+?)</span><spanid="(.+?)"').findall(link)
        for i in range(0,len(match0)):
            li=xbmcgui.ListItem(str(i+1)+'.'+match0[i][0],iconImage='',thumbnailImage=match0[i][2])
            u=sys.argv[0]+"?mode=7&name="+urllib.quote_plus(match0[i][0])+"&id="+urllib.quote_plus(match0[i][4])+"&thumb="+urllib.quote_plus(match0[i][2])+"&duration="+urllib.quote_plus(match0[i][3])
            xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li)
    else:
        match0=re.compile('<ulclass="video"><liclass="vimg"><atitle="(.+?)"href="(.+?)"target="_blank"><img.*?lazy-src="(.+?)"alt=".+?"></a>').findall(link)
        for i in range(0,len(match0)):
            li=xbmcgui.ListItem(str(i+1)+'.'+match0[i][0],iconImage='',thumbnailImage=match0[i][2])
            u=sys.argv[0]+"?mode=6&name="+urllib.quote_plus(name+'>'+match0[i][0])+"&url="+urllib.quote_plus('http://xiyou.cntv.cn'+match0[i][1])
            xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
    #获取其他页码
    match=re.compile('<divclass="page">(.+?)</div>').findall(link)
    if len(match)>0:
        match0=re.compile('<ahref="/'+category+'/index'+handler+type+'-'+id+'-([0-9]+).html"class="(.+?)">(.+?)</a>').findall(match[0])
        for i in range(0,len(match0)):
            if match0[i][1]=='fsize12' or match0[i][1]=='prev_page' or match0[i][1]=='next_page':
                li=xbmcgui.ListItem('..'+match0[i][2])
                u=sys.argv[0]+"?mode=5&name="+urllib.quote_plus(name)+"&category="+urllib.quote_plus(category)+"&id="+urllib.quote_plus(id)+"&type="+urllib.quote_plus(type)+"&handler="+urllib.quote_plus(handler)+"&page="+urllib.quote_plus(match0[i][0])
                xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
            elif match0[i][1]!='current_page':
                li=xbmcgui.ListItem('..第'+match0[i][2]+'页')
                u=sys.argv[0]+"?mode=6&name="+urllib.quote_plus(name)+"&category="+urllib.quote_plus(category)+"&id="+urllib.quote_plus(id)+"&type="+urllib.quote_plus(type)+"&handler="+urllib.quote_plus(handler)+"&page="+urllib.quote_plus(match0[i][0])
                xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)

def XiyouF(name,url):
    li=xbmcgui.ListItem('当前位置：'+name)
    u=sys.argv[0]+"?mode=20"
    xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
    link=GetHttpData(url)
    link=re.sub('\r','',link)
    link=re.sub('\n','',link)
    link=re.sub('\t','',link)
    link=re.sub(' ','',link)
    match=re.compile('<ulclass="video"><liclass="vimg"><ahref="(.+?)"title="(.+?)"><img.*?lazy-src="(.+?)"/></a><spanclass="vtime">(.+?)</span><spanclass="vadd"id="(.+?)"').findall(link)
    for i in range(0,len(match)):
        li=xbmcgui.ListItem(str(i+1)+'.'+match[i][1],iconImage='',thumbnailImage=match[i][2])
        u=sys.argv[0]+"?mode=7&name="+urllib.quote_plus(match[i][1])+"&id="+urllib.quote_plus(match[i][4])+"&thumb="+urllib.quote_plus(match[i][2])+"&duration="+urllib.quote_plus(match[i][3])
        xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li)

def XiyouG(name,id,thumb,duration):
    url='http://xiyou.cntv.cn/interface/index?videoId='+id
    link=GetHttpData(url)
    match=re.compile('"videoFilePath":"(.+?)#').findall(link)
    path=match[0].replace('\\','')+'_001.mp4'
    li=xbmcgui.ListItem(name,iconImage='',thumbnailImage=thumb)
    li.setInfo(type="Video",infoLabels={"Title":name,"Duration":duration})
    xbmc.Player().play(path, li)

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

params=get_params()

mode=None
name=None
url=None
category=None
id=None
type=None
handler=None
page=None
thumb=None
director=None
studio=None
plot=None
duration=None


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
try:
    category=urllib.unquote_plus(params["category"])
except:
    pass
try:
    id=urllib.unquote_plus(params["id"])
except:
    pass
try:
    type=urllib.unquote_plus(params["type"])
except:
    pass
try:
    handler=urllib.unquote_plus(params["handler"])
except:
    pass
try:
    page=urllib.unquote_plus(params["page"])
except:
    pass
try:
    director=urllib.unquote_plus(params["director"])
except:
    pass
try:
    studio=urllib.unquote_plus(params["studio"])
except:
    pass
try:
    plot=urllib.unquote_plus(params["plot"])
except:
    pass
try:
    thumb=urllib.unquote_plus(params["thumb"])
except:
    pass
try:
    duration=urllib.unquote_plus(params["duration"])
except:
    pass


if mode==None:
    name=''
    Roots()
elif mode==1:
    XiyouA(name)
elif mode==2:
    XiyouB(name,category)
elif mode==3:
    XiyouC(name,category,id)
elif mode==4:
    XiyouD(name,category,id,type)
elif mode==5:
    XiyouE(name,category,handler,id,type,page)
elif mode==6:
    XiyouF(name,url)
elif mode==7:
    XiyouG(name,id,thumb,duration)
elif mode==8:
    BuguA(name)
elif mode==9:
    BuguB(name,url)
elif mode==10:
    BuguC(name,url,id)
elif mode==11:
    BuguD(name,url)
elif mode==12:
    BuguE(name,url,plot,thumb)

xbmcplugin.endOfDirectory(int(sys.argv[1]))

