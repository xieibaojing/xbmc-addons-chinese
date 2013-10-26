# -*- coding: utf-8 -*-
import xbmc, xbmcgui, xbmcplugin, xbmcaddon, urllib2, urllib, re, string, sys, os, gzip, StringIO
if sys.version_info < (2, 7):
    import simplejson
else:
    import json as simplejson

############################################################
# 奇艺视频(QIYI) by taxigps, 2012
############################################################

# Plugin constants 
__addonname__ = "奇艺视频(QIYI)"
__addonid__   = "plugin.video.qiyi"
__addon__     = xbmcaddon.Addon(id=__addonid__)

CHANNEL_LIST = [['电影','1'], ['电视剧','2'], ['纪录片','3'], ['动漫','4'], ['音乐','5'], ['综艺','6'], ['娱乐','7'], ['旅游','9'], ['片花','10'], ['教育','12'], ['时尚','13']]
ORDER_LIST = [['2','最新更新'], ['3','最近热播'], ['6 ','最新上映'], ['4','最受好评']]
PAYTYPE_LIST = [['','全部影片'], ['0','免费影片'], ['1','会员免费'], ['2','付费点播']]

def GetHttpData(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)')
    try:
        response = urllib2.urlopen(req)
        httpdata = response.read()
        if response.headers.get('content-encoding', None) == 'gzip':
            httpdata = gzip.GzipFile(fileobj=StringIO.StringIO(httpdata)).read()
        charset = response.headers.getparam('charset')
        response.close()
    except:
        xbmc.log( "%s: %s (%d) [%s]" % (
            __addonname__,
            sys.exc_info()[ 2 ].tb_frame.f_code.co_name,
            sys.exc_info()[ 2 ].tb_lineno,
            sys.exc_info()[ 1 ]
            ), level=xbmc.LOGERROR)
        return ''
    match = re.compile('<meta http-equiv=["]?[Cc]ontent-[Tt]ype["]? content="text/html;[\s]?charset=(.+?)"').findall(httpdata)
    if len(match)>0:
        charset = match[0]
    if charset:
        charset = charset.lower()
        if (charset != 'utf-8') and (charset != 'utf8'):
            httpdata = httpdata.decode(charset, 'ignore').encode('utf8', 'ignore')
    return httpdata
   
def urlExists(url):
    try:
        resp = urllib2.urlopen(url)
        result = True
        resp.close()
    except:
        result = False
    return result

def selResolution(items):
    ratelist = []
    for i in range(0,len(items)):
        if items[i] == 96: ratelist.append([4, '极速', i])    # 清晰度设置值, 清晰度, match索引
        if items[i] == 1: ratelist.append([3, '流畅', i])
        if items[i] == 2: ratelist.append([2, '高清', i])
        if items[i] == 3: ratelist.append([1, '超清', i])
    ratelist.sort()
    if len(ratelist) > 1:
        resolution = int(__addon__.getSetting('resolution'))
        if resolution == 0:    # 每次询问点播视频清晰度
            dialog = xbmcgui.Dialog()
            list = [x[1] for x in ratelist]
            sel = dialog.select('清晰度（低网速请选择低清晰度）', list)
            if sel == -1:
                return -1
        else:
            sel = 0
            while sel < len(ratelist)-1 and resolution > ratelist[sel][0]: sel =  sel + 1
    else:
        sel = 0
    return ratelist[sel][2]

def PlayVideo(name,id,thumb):
    id = id.split(',')
    if len(id) == 1:
        url = 'http://cache.video.qiyi.com/avlist/%s/' % (id[0])
        link = GetHttpData(url)
        data = link[link.find('=')+1:]
        json_response = simplejson.loads(data)
        tvId = str(json_response['data']['vlist'][0]['id'])
        videoId = json_response['data']['vlist'][0]['vid'].encode('utf-8')
    else:
        tvId = id[0]
        videoId = id[1]

    playmode = int(__addon__.getSetting('playmode'))
    if playmode == 0:   # 连续播放模式
        url = 'http://cache.video.qiyi.com/m/' + tvId + '/' + videoId + '/'
        link = GetHttpData(url)
        match1 = re.compile('var ipadUrl=({.*})', re.DOTALL).search(link)
        if match1:
            data = unicode(match1.group(1), 'utf-8', errors='ignore')
            json_response = simplejson.loads(data)
            mtl = json_response['data']['mtl']
            sel = selResolution([x['vd'] for x in mtl])
            if sel == -1:
                return
            listitem = xbmcgui.ListItem(name, thumbnailImage = thumb)
            xbmc.Player().play(mtl[sel]['m3u'], listitem)
    else:               # 分段播放模式
        #url = 'http://cache.video.qiyi.com/v/' + videoId + '/' + pid + '/' + ptype + '/'
        url = 'http://cache.video.qiyi.com/v/' + tvId + '/' + videoId
        link = GetHttpData(url)
        match1 = re.compile('<data version="(\d+)">([^<]+)</data>').findall(link)
        sel = selResolution([int(x[0]) for x in match1])
        if sel == -1:
            return
        if match1[sel][1] != videoId:
            #url = 'http://cache.video.qiyi.com/v/' + match1[sel][1] + '/' + pid + '/' + ptype + '/'
            url = 'http://cache.video.qiyi.com/v/' + tvId + '/' + match1[sel][1]
            link = GetHttpData(url)

        match=re.compile('<file>(.+?)</file>').findall(link)
        playlist=xbmc.PlayList(1)
        playlist.clear()
        listitem = xbmcgui.ListItem(name, thumbnailImage = thumb)
        listitem.setInfo(type="Video",infoLabels={"Title":name+" 第"+str(1)+"/"+str(len(match))+" 节"})
        filepart = '/'.join(match[0].split('/')[-3:])
        if urlExists('http://qiyi.soooner.com/videos2/'+filepart):
            baseurl = 'http://qiyi.soooner.com/videos2/'
        elif urlExists('http://qiyi.soooner.com/videos/'+filepart):
            baseurl = 'http://qiyi.soooner.com/videos/'
        else:
            dialog = xbmcgui.Dialog()
            ok = dialog.ok(__addonname__, '未能获取视频地址')
            return
        playlist.add(baseurl+filepart, listitem = listitem)
        for i in range(1,len(match)):
            listitem=xbmcgui.ListItem(name, thumbnailImage = thumb)
            listitem.setInfo(type="Video",infoLabels={"Title":name+" 第"+str(i+1)+"/"+str(len(match))+" 节"})
            filepart = '/'.join(match[i].split('/')[-3:])
            playlist.add(baseurl+filepart, listitem = listitem)
        xbmc.Player().play(playlist)

def playVideoQiyi(name,url,thumb,res):
    link = GetHttpData(url)
    tvid = re.compile('data-drama-tvid="(.+?)"', re.DOTALL).search(link)
    vid=re.compile('data-drama-vid="(.+?)"', re.DOTALL).search(link)
    id = tvid.group(1)+','+vid.group(1)
    print 'qiyi: id = '+id
    PlayVideo(name,id,thumb)

