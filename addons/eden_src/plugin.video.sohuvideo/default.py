# -*- coding: utf-8 -*-
import xbmc, xbmcgui, xbmcplugin, xbmcaddon, urllib2, urllib, urlparse, httplib, re, string, sys, os, gzip, StringIO, simplejson
import cookielib, time
import ChineseKeyboard
       
############################################################
# 搜狐视频(SoHu) by taxigps, 2011
############################################################
# Version 2.3.0 (2012-07-12 - cmeng)
# - Add & Update CHANNEL_LIST latest Categories and ID
# - Improve PlayVideo Reliability
# - Added new PlayVideoUgc
# - Provide video search function
# - Include Cookie support (needed by certain categories) 
# - Include Proxy support (must be transparent for video link - header)

# Version 2.1.4 (2011)
# Modified by wow1122/wht9000@gmail.com
# Modified by fxfboy@gmail.com
############################################################

# Plugin constants 
__addonname__ = "搜狐视频(SoHu)"
__addonid__   = "plugin.video.sohuvideo"
__addon__     = xbmcaddon.Addon(id=__addonid__)
__settings__  = xbmcaddon.Addon(id=__addonid__)
__profile__   = xbmc.translatePath( __settings__.getAddonInfo('profile') )
cookieFile    = __profile__ + 'cookies.sohu'

RATE_LIST = [['超清','3'], ['高清','2'], ['普通','1'], ]
CHANNEL_LIST = [['电影','100'],['电视剧','101'],['动漫','115'],['综艺','106'],['纪录片','107'],['音乐','121'],['教育','119'],['新闻 ','122'],['娱乐 ','112'],['搞笑 ','133'],['游戏','128'],['原创','124'],['体育','125'],['汽车','126'],['旅游','131'],['星尚 ','130']]
ORDER_LIST = [['','相关程度'],['5','日播放最多'],['7','周播放最多'],['1','总播放最多'],['3','最新发布'],['4','评分最高']]

LIVEID_URL = 'http://live.tv.sohu.com/live/player_json.jhtml?lid=%s&af=1&bw=531&type=1&g=8'
UserAgent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'

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
# Routine to extract url ID from array based on given selected filter
##################################################################################
def searchDict(dlist,idx):
    for i in range(0,len(dlist)):
        if dlist[i][0] == idx:
            return dlist[i][1]
    return ''

##################################################################################
# Routine to fetch and build video filter list
# tuple to list conversion and strip spaces    
# - 按类型  (Categories)
# - 按地区 (Countries/Areas)
# - 按年份 (Year)
# - etc
##################################################################################
def getcatList(listpage):
    match = re.compile('<li><span>类型：</span></li>.+?全部</a></li>(.+?)</ul>', re.DOTALL).findall(listpage)
    catlist = re.compile('p2(.+?)_p3.+?>(.+?)</a></li>', re.DOTALL).findall(match[0])
    if len(catlist)>0: catlist.insert(0,['0','全部'])
    return catlist

def getareaList(listpage):
    match = re.compile('<li><span>产地：</span></li>.+?全部</a></li>(.+?)</ul>', re.DOTALL).findall(listpage)
    arealist = re.compile('p3(_.+?)_p4.+?>(.+?)</a></li>', re.DOTALL).findall(match[0])
    if len(arealist)>0: arealist.insert(0,['0','全部'])
    return arealist

def getyearList(listpage):    
    match = re.compile('<li><span>年份：</span></li>.+?全部</a></li>(.+?)</ul>', re.DOTALL).findall(listpage)
    yearlist = re.compile('p4(.+?)_p5.+?>(.+?)</a></li>', re.DOTALL).findall(match[0])
    if len(yearlist)>0: yearlist.insert(0,['0','全部'])
    return yearlist

def getlabelList(listpage): # label & area share the same _P3   
    match = re.compile('<li><span>标签：</span></li>.+?全部</a></li>(.+?)</ul>', re.DOTALL).findall(listpage)
    arealist = re.compile('p3(_.+?)_p4.+?>(.+?)</a></li>', re.DOTALL).findall(match[0])
    if len(arealist)>0: arealist.insert(0,['0','全部'])
    return arealist

def getList16(listpage):    
    match = re.compile('<li><span>篇幅：</span></li>.+?全部</a></li>(.+?)</ul>', re.DOTALL).findall(listpage)
    pflist = re.compile('p5(.+?)_p6.+?>(.+?)</a></li>', re.DOTALL).findall(match[0])
    if len(pflist)>0: pflist.insert(0,['0','全部'])
    match = re.compile(' <li><span>年龄：</span></li>.+?全部</a></li>(.+?)</ul>', re.DOTALL).findall(listpage)
    nllist = re.compile('p6(.+?)_p7.+?>(.+?)</a></li>', re.DOTALL).findall(match[0])
    if len(nllist)>0: nllist.insert(0,['0','全部'])
    return pflist,nllist
           
def getList24(listpage):
    match = re.compile('<li><span>类型：</span></li>.+?全部</a></li>(.+?)</ul>', re.DOTALL).findall(listpage)
    lxlist = re.compile('p5(.+?)_p6.+?html">(.+?)</a></li>', re.DOTALL).findall(match[0])
    if len(lxlist)>0: lxlist.insert(0,['0','全部'])
    match = re.compile('<li><span>歌手：</span></li>.+?全部</a></li>(.+?)</ul>', re.DOTALL).findall(listpage)
    gslist = re.compile('p6(.+?)_p7.+?html">(.+?)</a></li>', re.DOTALL).findall(match[0])
    if len(gslist)>0: gslist.insert(0,['0','全部'])
    match = re.compile('<li><span>语言：.+?全部</a></li>(.+?)</ul>', re.DOTALL).findall(listpage)
    yylist = re.compile('_p101_p11(.+?).html">(.+?)</a></li>', re.DOTALL).findall(match[0])
    if len(yylist)>0: yylist.insert(0,['0','全部'])
    match = re.compile('<li><span>地区：</span></li>.+?全部</a></li>(.+?)</ul>', re.DOTALL).findall(listpage)
    arealist = re.compile('p3(_.+?)_p4.+?>(.+?)</a></li>', re.DOTALL).findall(match[0])
    if len(arealist)>0: arealist.insert(0,['0','全部'])
    match = re.compile('<li><span>风格：</span></li>.+?全部</a></li>(.+?)</ul>', re.DOTALL).findall(listpage)
    fglist = re.compile('p2(.+?)_p3.+?>(.+?)</a></li>', re.DOTALL).findall(match[0])
    if len(fglist)>0: fglist.insert(0,['0','全部'])
    return lxlist,gslist,yylist,arealist,fglist

##################################################################################
# Routine to fetch & build Sohu 网络 main menu
# - Video Search
# - 电视直播
# - video list as per [CHANNEL_LIST]
##################################################################################    
def rootList():
    # force sohu to give cookie; must use cookie for some categories fast response else timeout
    #http://pv.sohu.com/suv/?t?=1342163482 447275_1920_1200?r?=
    ticks = int(time.time())
    url_cookie = 'http://pv.sohu.com/suv/?t?='+str(ticks)+'866725_1920_1080?r?='
    link = getHttpData(url_cookie)

    li = xbmcgui.ListItem('[COLOR F0F0F0F0]0. Sohu 搜库网:[/COLOR][COLOR FF00FF00]【请输入搜索内容】[/COLOR]')
    u=sys.argv[0]+"?mode=21"
    xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, True)
    
    name='电视直播'
    li=xbmcgui.ListItem('1. ' + name)
    u=sys.argv[0]+"?mode=10&name="+urllib.quote_plus(name)
    xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
    
    i = 1
    for name, id in CHANNEL_LIST:
        i += 1
        if id in ('125','130','131','133'): order = '3'
        else: order = ''        
        li=xbmcgui.ListItem(str(i) + '. ' + name)
        u=sys.argv[0]+"?mode=1&name="+urllib.quote_plus(name)+"&id="+urllib.quote_plus(id)+"&page=1"+"&cat="+"&area="+"&year=-1"+"&p5="+"&p6="+"&p11="+"&order="+order 
        xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

##################################################################################
# Routine to fetch and build the video selection menu
# - selected page & filters (user selectable)
# - video items list
# - user selectable pages
# ########### url parameter decode ##############
# http://so.tv.sohu.com/list_p1100_p2_p3_p4_p5_p6_p7_p8_p9.html
# p1: 分类: 100=电影;电视剧=101;动漫=115;综艺=106 etc
# p2: 类型： 全部 爱情 动作 喜剧 科幻 战争 恐怖 风月 剧情 歌舞 动画 纪录   
# p3: 产地： 全部 华语 好莱坞 欧洲 日本 韩国 其他
# p4: 年份： 全部 2012 2011
# p5: 篇幅(动漫 )：全部 电影 连续剧 预告片 其他
# p6: 年龄(动漫 )：全部 5岁以下 5岁-12岁 13岁-18岁 18岁以上
# p7: 相关程度: 5=日播放最多;7=周播放最多;1=总播放最多;3=最新发布;4=评分最高    
# p8: 付费： 0=全部;2=免费;1=VIP;3=包月;4=点播
# p9: 状态: 2d2=全部;2d1=正片;2d3=非正片
# p10: page
# p11:
##################################################################################
def progList(name,id,page,cat,area,year,p5,p6,p11,order):
    url = 'http://so.tv.sohu.com/list_p1'+id+'_p2'+cat+'_p3'+area+'_p4'+year+'_p5'+p5+'_p6'+p6+'_p7'+order
    if name in ('电影','电视剧'):
        url +='_p82_p9_2d1'
    else:
        url +='_p8_p9'
    url += '_p10'+page+'_p11'+p11+'.html'

    currpage = int(page)
    link = getHttpData(url)
    match = re.compile('共有 <span>(.+?)</span> 个符合条件', re.DOTALL).findall(link)
    if match[0]=='0':
        dialog = xbmcgui.Dialog()
        ok = dialog.ok(__addonname__, '没有符合此条件的视频！')
    else:
        match = re.compile('c.+?[1-9]+/([0-9]+)<a href=').findall(link)
        if len(match) == 0:
            match = re.compile('c.+?[1-9]+/([0-9]+)下一页</div>').findall(link)
        totalpages = int(match[0])
            
        match = re.compile('<div class="seaKey bord clear" id="seaKey">(.+?)<div class="jumpA clear">', re.DOTALL).findall(link)
        if len(match):
            listpage = match[0]
        else:
            listpage = ''

        # match = re.compile('<div class="vInfo">(.+?)</em></p>', re.DOTALL).findall(link)
        match = re.compile('<div class="vInfo">(.+?)播 放</a>', re.DOTALL).findall(link)
        totalItems = len(match) + 1
        if currpage > 1: totalItems = totalItems + 1
        if currpage < totalpages: totalItems = totalItems + 1
        lxstr=''
        if id not in ('121','124','125','126','128','130','131','133'):
            catlist= getcatList(listpage)
            lxstr += '[COLOR FFFF0000]'
            if cat:
                lxstr += searchDict(catlist,cat)
            else:    
                lxstr += '全部类型'
            lxstr += '[/COLOR]'

        if id in ('124','125','126','128','130','131','133'):
            arealist = getlabelList(listpage)
            lxstr += '/[COLOR FF00FF00]'
            arealist= getlabelList(listpage)
            if area:
                lxstr += searchDict(arealist,area)
            else:
                lxstr += '全部标签'
            lxstr += '[/COLOR]'
        elif id in ('100','101','106'):          
            lxstr += '/[COLOR FF00FF00]'
            arealist= getareaList(listpage)
            if area:
                lxstr += searchDict(arealist,area)
            else:
                lxstr += '全部地区'
            lxstr += '[/COLOR]'

        if id=='115':
            lxstr += '/[COLOR FFFFFF00]'
            pflist,nllist=getList16(listpage)
            if p5:
                lxstr += searchDict(pflist,p5)
            else:
                lxstr += '全部篇幅'  
            lxstr += '[/COLOR]/[COLOR FF00FF00]'
            if p6:
                lxstr += searchDict(nllist,p6)
            else:
                lxstr += '全部年龄'
            lxstr += '[/COLOR]'

        if id=='121': 
            lxstr += '[COLOR FFFF0000]'
            lxlist,gslist,yylist,arealist,fglist=getList24(listpage)
            if p5:
                lxstr += searchDict(lxlist,p5)
            else:
                lxstr += '全部类型'            
            lxstr += '[/COLOR]/[COLOR FF00FF00]'
            if p6:
                lxstr += searchDict(gslist,p6)
            else:
                lxstr += '全部歌手'
            lxstr += '[/COLOR]/[COLOR FFFFFF00]'
            if p11:
                lxstr += searchDict(yylist,p11)
            else:
                lxstr += '全部语言'
            lxstr += '[/COLOR]/[COLOR FFFF5555]'
            if area:
                lxstr += searchDict(arealist,area)
            else:
                lxstr += '全部地区'
            lxstr += '[/COLOR]/[COLOR FFFF00FF]'
            if cat:
                lxstr += searchDict(fglist,cat)
            else:
                lxstr += '全部风格'
            lxstr += '[/COLOR]'
        
        if id in ('100','101','115','121'):
            lxstr += '/[COLOR FF5555FF]'
            yearlist = getyearList(listpage)
            if year=='-1':
                lxstr += '全部年份'
            elif year in ('80','90'):
                lxstr += year+'年代'
            elif year == '100':
                lxstr += '更早年代'
            else:
                lxstr += year+'年'
            lxstr += '[/COLOR]'
                
        li = xbmcgui.ListItem(name+'（第'+str(currpage)+'/'+str(totalpages)+'页）【' + lxstr + '/[COLOR FF00FFFF]' + searchDict(ORDER_LIST,order) + '[/COLOR]】（按此选择）')
        u = sys.argv[0]+"?mode=4&name="+urllib.quote_plus(name)+"&id="+id+"&cat="+cat+"&area="+area+"&year="+year+"&p5="+p5+"&p6="+p6+"&p11="+p11+"&order="+"&listpage="+urllib.quote_plus(listpage)
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, True, totalItems)

        for i in range(0,len(match)):
            match1 = re.compile('<a href="(.+?)" target="_blank">\s*<img src="(.+?)".+? target="_blank">(.+?)</a>', re.DOTALL).search(match[i])
            p_url = match1.group(1)
            p_thumb = match1.group(2)
            p_name = match1.group(3)
            match1 = re.compile('<span class="commet">\(([0-9]+)人评价\)</span><span class="grade"><font>([0-9]*)</font>([\.0-9]*).*?</span>').search(match[i])
            if match1:
                p_rating = float(match1.group(2) + match1.group(3))
                p_votes = match1.group(1)
            else:
                p_rating = 0
                p_votes = ''
            match1 = re.compile('导演：.+?</font>(.+?)</a>').search(match[i])
            if match1:
                p_director = match1.group(1)
            else:
                p_director = ''
            match1 = re.compile('<span class="show">类型：(.+?</span>)').search(match[i])
            if match1:
                match0 = re.compile('<font class="highlight"></font>([^<]+)').findall(match1.group(1))
                p_genre = ' / '.join(match0)
            else:
                p_genre = ''
            match1 = re.compile('<p class="detail">(.+?)(</p>|</b>)').search(match[i])
            if match1:
                p_plot = re.sub('<b id=.*?>','',match1.group(1))
            else:
                p_plot = ''
            match1 = re.compile('<font>年份：<a href="\?c=1&year=([0-9]+)">').search(match[i])
            if match1:
                p_year = int(match1.group(1))
            else:
                p_year = 0
 
            if id in ('101','115'):
                p_dir = True
                mode = 2
            elif id == '119': # 教育 category contains both series and movie link
                if re.search('http://tv.sohu.com/', p_url):
                    p_dir = True
                    mode = 2
                else:
                    p_dir = False
                    mode=5
            elif id in ('124','125','126','128','130','131','133'):
                p_dir = False
                mode=5
            else:
                p_dir = False
                mode = 3
            
            if match[i].find('<span class="cq_ico">')>0:
                p_name1 = p_name + ' [超清]'
                p_res = 2
            elif match[i].find('<span class="gq_ico">')>0:
                p_name1 = p_name + ' [高清]'
                p_res = 1
            else:
                p_name1 = p_name
                p_res = 0
                
            match1 = re.compile('<div class="label"><i></i><em>(.+?)</em></div>').search(match[i])
            if match1:
                label = match1.group(1)
                if '分' in label:
                    label = re.sub('分',':',label)[:-3]
                p_name1 += ' [' + label.strip(' ') + ']'
            
            
            li = xbmcgui.ListItem(str(i + 1) + '. ' + p_name1, iconImage = '', thumbnailImage = p_thumb)
            u = sys.argv[0]+"?mode="+str(mode)+"&name="+urllib.quote_plus(p_name)+"&url="+urllib.quote_plus(p_url)+"&thumb="+urllib.quote_plus(p_thumb)+"&id="+urllib.quote_plus(str(i))
            li.setInfo(type = "Video", infoLabels = {"Title":p_name, "Director":p_director, "Genre":p_genre, "Plot":p_plot, "Year":p_year, "Rating":p_rating, "Votes":p_votes})
            xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, p_dir, totalItems)
    
        # Fetch and build user selectable page number
        matchp = re.compile('<div class="jumpB clear">(.+?)</div>', re.DOTALL).findall(link)
        if len(matchp): 
            matchp1 = re.compile('<a href=".+?">([1-9]+)</a>', re.DOTALL).findall(matchp[0])
            if len(matchp1):
                plist=[str(currpage)]
                for num in matchp1:
                    if num not in plist:
                        plist.append(num)
                        li = xbmcgui.ListItem("... 第" + num + "页")
                        u=sys.argv[0]+"?mode=1&name="+urllib.quote_plus(name)+"&id="+id+"&page="+str(num)+"&cat="+cat+"&area="+area+"&year="+year+"&p5="+p5+"&p6="+p6+"&p11="+p11+"&order="+order 
                        xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, True, totalItems)        
        xbmcplugin.setContent(int(sys.argv[1]), 'movies')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

##################################################################################
# Routine to fetch and build the video series selection menu
# - for 电视剧  & 动漫
# - selected page & filters (user selectable)
# - Video series list
# - user selectable pages
##################################################################################
def seriesList(name, id,url,thumb):
    # print 'SeriesList('+name+', '+str(id)+', '+url+', '+thumb+')'
    li = xbmcgui.ListItem('【[COLOR FFFFFF00][' + name + '][/COLOR] | [COLOR FF00FFFF][选择: ' + name + '][/COLOR]】', iconImage='', thumbnailImage=thumb)
    u = sys.argv[0]+"?mode=2&name="+urllib.quote_plus(name)+"&id="+urllib.quote_plus(id)+"&url=" + urllib.quote_plus(url)+"&thumb="+urllib.quote_plus(thumb) 
    xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, True)

    link = getHttpData(url)
    if url.find('.shtml')>0:
        match0 = re.compile('var vrs_playlist_id="(.+?)";', re.DOTALL).findall(link)
        #print 'vrs_playlist_id:' + match0.groups()
        link = getHttpData('http://hot.vrs.sohu.com/vrs_videolist.action?playlist_id='+match0[0])
        match = re.compile('"videoImage":"(.+?)",.+?"videoUrl":"(.+?)".+?"videoOrder":"(.+?)",', re.DOTALL).findall(link)
        totalItems = len(match)

        for p_thumb,p_url,p_name in match:
            li = xbmcgui.ListItem('第'+p_name+'集', iconImage = '', thumbnailImage = p_thumb)
            u = sys.argv[0] + "?mode=3&name=" + urllib.quote_plus('第'+p_name+'集') + "&url=" + urllib.quote_plus(p_url)+ "&thumb=" + urllib.quote_plus(p_thumb)
            xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, False, totalItems)       
    else:    
        match0 = re.compile('var pid=(.+?);', re.DOTALL).findall(link)
        if len(match0)>0:
            # print 'pid=' + match0[0]
            pid=match0[0].replace('"','')
            match0 = re.compile('var vid=(.+?);', re.DOTALL).findall(link)
            vid=match0[0].replace('"','')
            obtype= '2'
            link = getHttpData("http://search.vrs.sohu.com/avs_i"+vid+"_pr"+pid+"_o"+obtype+"_n_p1000_chltv.sohu.com.json")

            match = re.compile('"videoName":"(.+?)",.+?"videoUrl":"(.+?)",.+?"videoBigPic":"(.+?)",', re.DOTALL).findall(link)
            totalItems = len(match)
            i = 0
            for p_name,p_url, p_thumb  in match:
                i +=1
                li = xbmcgui.ListItem(str(i) +'. ' + p_name, iconImage = '', thumbnailImage = p_thumb)
                u = sys.argv[0] + "?mode=3&name=" + urllib.quote_plus(p_name) + "&url=" + urllib.quote_plus(p_url)+ "&thumb=" + urllib.quote_plus(p_thumb)
                xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, False, totalItems)
        else:
            match = re.compile('<a([^>]*)><IMG([^>]*)></a>',re.I).findall(link)
            thumbDict = {}
            for i in range(0, len(match)):
                p_url = re.compile('href="(.+?)"').findall(match[i][0])
                if len(p_url)>0:
                    p_url = p_url[0]
                else:
                    p_url = match[i][0]
                p_thumb = re.compile('src="(.+?)"').findall(match[i][1])
                if len(p_thumb)>0:
                    p_thumb = p_thumb[0]
                else:
                    p_thumb = match[i][1]
                thumbDict[p_url]=p_thumb
            #for img in thumbDict.items():
            url = 'http://so.tv.sohu.com/mts?c=2&wd=' + urllib.quote_plus(name.decode('utf-8').encode('gbk'))
            html = getHttpData(url)
            match =  re.compile('class="v-episode-list(.+?)<div class="v-episode-bottom">').findall(html)
            if not match:
                return
            items = re.compile('<a([^>]*)>(.+?)</a>',re.I).findall(match[0])
            totalItems = len(items)
            for item in items:
                if item[1]=='展开>>':
                    continue
                href = re.compile('href="(.+?)"').findall(item[0])
                if len(href)>0:
                    p_url = 'http://so.tv.sohu.com/' + href[0]
                    urlKey = re.compile('u=(http.+?.shtml)').search(p_url)
                    if urlKey:
                        urlKey = urllib.unquote(urlKey.group(1))
                    else:
                        urlKey = p_url
                    #print urlKey
                    p_thumb = thumb
                    try:
                        p_thumb = thumbDict[urlKey]
                    except:
                        pass
                    #title = re.compile('title="(.+?)"').findall(item)
                    #if len(title)>0:
                        #p_name = title[0]
                    p_name = name + '第' + item[1].strip() + '集'
                    li = xbmcgui.ListItem(p_name, iconImage = p_thumb, thumbnailImage = p_thumb)
                    u = sys.argv[0] + "?mode=3&name="+urllib.quote_plus(p_name)+"&id="+id+"&url="+urllib.quote_plus(p_url)+"&thumb="+urllib.quote_plus(p_thumb)
                    xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, False)
    xbmcplugin.setContent(int(sys.argv[1]), 'episodes')
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

##################################################################################
# Routine to update video list as per user selected filters
# - 按类型  (Categories)
# - 按地区 (Areas)
# - 按年份 (Year)
# - 排序方式 (Selection Order) etc
##################################################################################
def performChanges(name,id,cat,area,year,p5,p6,p11,order,listpage):
    change = False
    dialog = xbmcgui.Dialog()
    if id not in ('121','124','125','126','128','130','131','133'):
        catlist= getcatList(listpage)
        if len(catlist)>0:
            list = [x[1] for x in catlist]
            sel = dialog.select('类型', list)
            if sel != -1:
                if sel == 0:
                    cat = ''
                else:
                    cat = catlist[sel][0]
                change = True
            
    if id in ('124','125','126','128','130','131','133'):
        arealist= getlabelList(listpage)
        if len(arealist)>0:
            list = [x[1] for x in arealist]
            sel = dialog.select('标签', list)
            if sel != -1:
                if sel == 0:
                    area = ''
                else:
                    area = arealist[sel][0]
                change = True       
    elif id in ('100','101','106'):
        arealist=getareaList(listpage)
        if len(arealist)>0:
            list = [x[1] for x in arealist]
            sel = dialog.select('地区', list)
            if sel != -1:
                if sel == 0:
                    area = ''
                else:
                    area = arealist[sel][0]
                change = True       
    if id=='115':
        pflist,nllist=getList16(listpage)
        if len(pflist)>0:
            list = [x[1] for x in pflist]
            sel = dialog.select('篇幅', list)
            if sel != -1:
                if sel == 0:
                    p5 = ''
                else:
                    p5 = pflist[sel][0]
                change = True 
        if len(nllist)>0:
            list = [x[1] for x in nllist]
            sel = dialog.select('年龄', list)
            if sel != -1:
                if sel == 0:
                    p6 = ''
                else:
                    p6 = nllist[sel][0]
                change = True
    if id=='121': 
        lxlist,gslist,yylist,arealist,fglist=getList24(listpage)
        if len(lxlist)>0:
            list = [x[1] for x in lxlist]
            sel = dialog.select('类型', list)
            if sel != -1:
                if sel == 0:
                    p5 = ''
                else:
                    p5 = lxlist[sel][0]
                change = True         
        if len(gslist)>0:
            list = [x[1] for x in gslist]
            sel = dialog.select('歌手', list)
            if sel != -1:
                if sel == 0:
                    p6 = ''
                else:
                    p6 = gslist[sel][0]
                change = True 
        if len(yylist)>0:
            list = [x[1] for x in yylist]
            sel = dialog.select('语言', list)
            if sel != -1:
                if sel == 0:
                    p11 = ''
                else:
                    p11 = yylist[sel][0]
                change = True 
        if len(arealist)>0:
            list = [x[1] for x in arealist]
            sel = dialog.select('地区', list)
            if sel != -1:
                if sel == 0:
                    area = ''
                else:
                    area = arealist[sel][0]
                change = True 
        if len(fglist)>0:
            list = [x[1] for x in fglist]
            sel = dialog.select('风格', list)
            if sel != -1:
                if sel == 0:
                    cat = ''
                else:
                    cat = fglist[sel][0]
                change = True 

    if id in ('100','101','115','121'):
        yearlist=getyearList(listpage)
        if len(yearlist)>0:
            list = [x[1] for x in yearlist]
            sel = dialog.select('年份', list)
            if sel != -1:
                if sel == 0:
                    year = '-1'
                else:
                    year = yearlist[sel][0]
                change = True

    list = [x[1] for x in ORDER_LIST]
    sel = dialog.select('排序方式', list)
    if sel != -1:
        order = ORDER_LIST[sel][0]
        change = True
    if change:
        progList(name,id,'1',cat,area,year,p5,p6,p11,order)

#################################################################################
# Get user input for Sohu site search
##################################################################################
def searchSohu():
    result=''
    keyboard = ChineseKeyboard.Keyboard('','请输入搜索内容')
    xbmc.sleep( 1500 )
    keyboard.doModal()
    if (keyboard.isConfirmed()):
        keyword = keyboard.getText()
        p_url = 'http://so.tv.sohu.com/mts?chl=&tvType=-2&wd='
        url = p_url + urllib.quote_plus(keyword.decode('utf-8').encode('gb2312'))
        sohuSearchList(keyword,url,'1')
    else: return
        
##################################################################################
# Routine to search Sohu site based on user given keyword for:
# http://so.tv.sohu.com/mts?chl=&tvType=-2&wd=love&whole=1&m=1&box=1&c=100&o=1&p=2
# c: 类型：''=全部 100=电影 101=电视剧 106=综艺 121=音乐 122=新闻 112=娱乐 0=其它 
# o:排序方式： ''=相关程度 1=最多播放 3=最新发布
##################################################################################
def sohuSearchList(name, url, page):
    # construct url based on user selected item
    p_url = url + '&fee=0&whole=1&m=1&box=1&p=' + page
    link = getHttpData(p_url)

    li = xbmcgui.ListItem('[COLOR FFFF0000]当前搜索: 第' + page + '页[/COLOR][COLOR FFFFFF00] (' + name + ')[/COLOR]【[COLOR FF00FF00]' + '请输入新搜索内容' + '[/COLOR]】')
    u = sys.argv[0] + "?mode=21&name=" + urllib.quote_plus(name) + "&url=" + urllib.quote_plus(url) + "&page=" + urllib.quote_plus(page)
    xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, True)
    
    #########################################################################
    # Video listing for all found related episode title
    #########################################################################
    match = re.compile('</span> 共找到(.+?)个').search(link)
    if match: totalItems = int(match.group(1))
    else: totalItems = 0;
    if totalItems == 0:
        li=xbmcgui.ListItem('抱歉，没有找到[COLOR FFFF0000] '+name+' [/COLOR]的相关视频')
        xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,False)
    else:
        matchp=re.compile('<div class=["clear list_pack"|"list_pack clear"]+>(.+?)播 放 </a>').findall(link)
        k = 0
        for i in range(0, len(matchp)):
            vlink = matchp[i]    
            if vlink.find('<em class="pay"></em>')>0: continue

            match1 = re.compile('href="(.+?)"').findall(vlink)
            p_url = 'http://so.tv.sohu.com' + match1[0]

            match1 = re.compile('alt="(.+?)"').search(vlink)
            p_name = match1.group(1)
            
            match1 = re.compile('src="(.+?)"').search(vlink)
            p_thumb = match1.group(1)

            match1 = re.compile("<b class='gq_ico'></b>(.+?)</span>").search(vlink)
            if match1:
                label = match1.group(1)
                if '分' in label:
                    label = re.sub('分',':',label)[:-3]
                p_label = ' [' + label.strip(' ') + ']'
            else:
                p_label =''

            p_type = ''
            isTeleplay = False
            match1 = re.compile('<span class="type">(.+?)</span>').search(vlink)
            if match1:
                p_type = match1.group(1)
            if p_type=='[电视剧]':
                isTeleplay = True
                mode = '2'
                p_type='【[COLOR FF00FF00]电视剧[/COLOR]】'
            elif p_type=='[电影]':
                p_type='【[COLOR FF00FF00]电影[/COLOR]】'
                mode ='3'
            else:
                p_type = ' ' + p_type
                mode ='3'
 
            k+=1 
            p_list = str(k) + ': ' + p_name + p_type + p_label
            li = xbmcgui.ListItem(p_list, iconImage=p_thumb, thumbnailImage=p_thumb)
            u = sys.argv[0] + "?mode=" + mode + "&name=" + urllib.quote_plus(p_name) + "&id=101" + "&url=" + urllib.quote_plus(p_url) + "&thumb=" + urllib.quote_plus(p_thumb)
  
            if isTeleplay:
                xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, True, totalItems)       
            else:
                xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, False, totalItems)
 
    # Fetch and build user selectable page number
    matchp = re.compile('<div class="jumpB clear">(.+?)</div>', re.DOTALL).findall(link)
    if len(matchp): 
        matchp1 = re.compile('<a href=".+?">([1-9]+)</a>', re.DOTALL).findall(matchp[0])
        if len(matchp1):
            plist=[str(currpage)]
            for num in matchp1:
                if num not in plist:
                    plist.append(num)
                    li = xbmcgui.ListItem("... 第" + num + "页")
                    u = sys.argv[0] + "?mode=22&name=" + urllib.quote_plus(name) + "&url=" + urllib.quote_plus(url) + "&page=" + str(num)
                    xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, True, totalItems)        
    xbmcplugin.setContent(int(sys.argv[1]), 'movies')
    xbmcplugin.endOfDirectory(int(sys.argv[1]))
 
##################################################################################
# Sohu Video Link Decode Algorithm & Player
# Extract all the video list and start playing first found valid link
# User may press <SPACE> bar to select video resolution for playback
##################################################################################
def PlayVideo(name,url,thumb):
    level = int(__addon__.getSetting('resolution'))
    site = int(__addon__.getSetting('videosite'))

    link = getHttpData(url)
    match1 = re.compile('var vid="(.+?)";').search(link)
    if not match1:
        match1 = re.compile('<a href="(http://[^/]+/[0-9]+/[^\.]+.shtml)" target="?_blank"?><img').search(link)
        if match1:
            PlayVideo(name,match1.group(1),thumb)
        return
    p_vid = match1.group(1)
    if p_vid.find(',') > 0 : p_vid = p_vid.split(',')[0]
       
    p_url = 'http://hot.vrs.sohu.com/vrs_flash.action?vid='+ p_vid
    link = getHttpData(p_url)
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
        link = getHttpData('http://hot.vrs.sohu.com/vrs_flash.action?vid='+match.group(int(rate)))
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
    
    playlist = xbmc.PlayList(1)
    playlist.clear()
    for i in range(0,len(paths)):
        p_url = 'http://data.vod.itc.cn/?prot=2&file='+paths[i].replace('http://data.vod.itc.cn','')+'&new='+newpaths[i]
        link = getHttpData(p_url)
        
        # http://newflv.sohu.ccgslb.net/|623|116.14.234.161|Googu7gm-8WjRTd5ZfBVPIfrtRtLE5Cn|1|0
        key=link.split('|')[3]
        url=link.split('|')[0].rstrip("/")+newpaths[i]+'?key='+key
        title = name+" 第"+str(i+1)+"/"+str(len(paths))+"节"
        listitem=xbmcgui.ListItem(title,thumbnailImage=thumb)
        listitem.setInfo(type="Video",infoLabels={"Title":title})
        #print 'i, link, key, url, title', i, link, key, url, title
        
        for trial in range(10): # give 10 trials to retrive Location on busy network
           if site == 0:
                parsedurl = urlparse.urlparse(url)
                httpConn = httplib.HTTPConnection(parsedurl[1])
                httpConn.connect()
                httpConn.request('HEAD', parsedurl[2])
           else:
                httpConn = httplib.HTTPConnection("new.sohuv.dnion.com")
                httpConn.request('HEAD', newpaths[i]+'?key='+key)
                
           response = httpConn.getresponse()
           #print 'trial, site, urlheader', trial, site, response.getheaders()
           if response.getheader('Location') <> None: break
           else: site = not site # try the other site if failed
        httpConn.close()
        playlist.add(url, listitem)
        if i == 0: 
            xbmc.Player().play(playlist)

##################################################################################
# Sohu Video Link Decode Algorithm & Player
# Extract all the video list and start playing first found valid link
# User may press <SPACE> bar to select video resolution for playback
# Only one video resoluton is provided
#
# http://my.tv.sohu.com/u/vw/26542854  
# http://my.tv.sohu.com/videinfo.jhtml?m=viewnew&vid=26542854&af=1&bw=722&g=8&referer=http://my.tv.sohu.com/u/vw/26542854&t=0.2265001619234681  
# http://61.135.183.46/?prot=2&file=g17.f.video.sohu.com/88868f4eae2219b1f9a25647ea2096cf0edd71e6c7e0ca374ab14196b3a7f556bf224dbb2f617a53.mp4&new=/196/48/VVPoipyoBwvOyxtNf3MNj7.mp4&t=0.30849113827571273
# http://newflv.sohu.ccgslb.net/196/238/YNWLzmwirSzs4IOUZM80Z.mp4?key=lyaN5VbuiPJ0ZzhxmcnKugDllMHEkGpX
# http://127.0.0.1:8828/notify_buffer?uuid=3d168a12-6299-62c7-d197-79f38ede6b9e&r=0.7472089589573443
##################################################################################
def PlayVideoUgc(name,url,thumb):
    site = int(__addon__.getSetting('videosite'))
    p_vid = url.split('/')[-1]
      
    p_url = 'http://my.tv.sohu.com/videinfo.jhtml?m=viewnew&vid='+ p_vid
    link = getHttpData(p_url)
 
    match = re.compile('"clipsURL"\:\["(.+?)"\]').findall(link)
    paths = match[0].split('","')
    match = re.compile('"su"\:\["(.*?)"\]').findall(link)
    if not match:
       dialog = xbmcgui.Dialog()
       ok = dialog.ok(__addonname__,'您当前选择的视频: ['+ name +'] 暂不能播放，请选择其它视频')       
       return
    newpaths = match[0].split('","')
    
    match = re.compile('"allot":"(.+?)"').findall(link)
    if match and len(match[0]) > 5:
        p_url = 'http://' + match[0]+ '/?prot=2&file='
    else: # link contains direct item to play
        url = 'http://'
    
    playlist = xbmc.PlayList(1)
    playlist.clear()
    for i in range(0,len(paths)):
        if newpaths[i] == '':
            url += paths[i]
            title = name+" 第"+str(i+1)+"/"+str(len(paths))+"节"
            listitem=xbmcgui.ListItem(title,thumbnailImage=thumb)
            listitem.setInfo(type="Video",infoLabels={"Title":title})
        else:
            p_url += paths[i]+'&new='+newpaths[i]
            link = getHttpData(p_url)
        
            key=link.split('|')[3]
            url=link.split('|')[0].rstrip("/")+newpaths[i]+'?key='+key
            title = name+" 第"+str(i+1)+"/"+str(len(paths))+"节"
            listitem=xbmcgui.ListItem(title,thumbnailImage=thumb)
            listitem.setInfo(type="Video",infoLabels={"Title":title})
        
            for trial in range(10): # give 10 trials to retrive Location on busy network
               if site == 0:
                    parsedurl = urlparse.urlparse(url)
                    httpConn = httplib.HTTPConnection(parsedurl[1])
                    httpConn.connect()
                    httpConn.request('HEAD', parsedurl[2])
               else:
                    httpConn = httplib.HTTPConnection("new.sohuv.dnion.com")
                    httpConn.request('HEAD', newpaths[i]+'?key='+key)
                
               response = httpConn.getresponse()
               if response.getheader('Location') <> None: break
               else: site = not site # try the other site if failed
            httpConn.close()

        playlist.add(url, listitem)
        if i == 0: 
            xbmc.Player().play(playlist)

##################################################################################
# Sohu 电视直播 Menu List
##################################################################################
def LiveChannel(name):
    url = 'http://live.tv.sohu.com'
    link = getHttpData(url)
    match = re.compile('var data1 = ({.+?});').findall(link)
    if match:
        parsed_json = simplejson.loads(match[0])
        totalItems = len(parsed_json['data'])
        i = 0
        for item in parsed_json['data']:
            p_name = item['name'].encode('utf-8')
            p_thumb = item['bigPic'].encode('utf-8')
            id = str(item['tvId'])
            i += 1
            li = xbmcgui.ListItem(str(i)+ '. ' + p_name, iconImage = '', thumbnailImage = p_thumb)
            u = sys.argv[0] + "?mode=11&name=" + urllib.quote_plus(p_name) + "&id=" + urllib.quote_plus(id)+ "&thumb=" + urllib.quote_plus(p_thumb)
            xbmcplugin.addDirectoryItem(int(sys.argv[1]), u, li, False, totalItems)
    xbmcplugin.setContent(int(sys.argv[1]), 'movies')
    xbmcplugin.endOfDirectory(int(sys.argv[1]))
    
##################################################################################
# Sohu 电视直播 Player
##################################################################################
def LivePlay(name,id,thumb):
    link = getHttpData(LIVEID_URL % (id))
    parsed_json = simplejson.loads(link)
    url = 'http://' + parsed_json['data']['clipsURL'][0].encode('utf-8')
    li = xbmcgui.ListItem(name,iconImage='',thumbnailImage=thumb)
    xbmc.Player().play(url, li)

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
mode = None
name = None
id = None
cat = ''
area = ''
year = ''
order = ''
page = ''
p5 = ''
p6 = ''
p11 = ''
listpage = ''
url = None
thumb = None

try:
    thumb = urllib.unquote_plus(params["thumb"])
except:
    pass
try:
    url = urllib.unquote_plus(params["url"])
except:
    pass
try:
    page = urllib.unquote_plus(params["page"])
except:
    pass
try:
    listpage = urllib.unquote_plus(params["listpage"])
except:
    pass
try:
    p5 = urllib.unquote_plus(params["p5"])
except:
    pass
try:
    p6 = urllib.unquote_plus(params["p6"])
except:
    pass
try:
    p11 = urllib.unquote_plus(params["p11"])
except:
    pass
try:
    order = urllib.unquote_plus(params["order"])
except:
    pass
try:
    year = urllib.unquote_plus(params["year"])
except:
    pass
try:
    area = urllib.unquote_plus(params["area"])
except:
    pass
try:
    cat = urllib.unquote_plus(params["cat"])
except:
    pass
try:
    id = urllib.unquote_plus(params["id"])
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

if mode == None:
    rootList()
elif mode == 1:
    progList(name,id,page,cat,area,year,p5,p6,p11,order)
elif mode == 2:
    seriesList(name,id,url,thumb)
elif mode == 3:
    PlayVideo(name,url,thumb)
elif mode == 4:
    performChanges(name,id,cat,area,year,p5,p6,p11,order,listpage)
elif mode == 5:
    PlayVideoUgc(name,url,thumb)

elif mode == 10:
    LiveChannel(name)
elif mode == 11:
    LivePlay(name,id,thumb)
     
elif mode == 21:
    searchSohu()
elif mode == 22:
    sohuSearchList(name, url, page)
