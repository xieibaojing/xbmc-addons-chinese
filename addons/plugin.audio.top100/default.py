# -*- coding: utf-8 -*-

#author: sAGiTTaR
#e-mail: plestoon@gmail.com
#release: 1.1.3 2010-8-18

import xbmc, xbmcgui, xbmcplugin
import urllib, httplib
import re

root_catigories = [('排行榜', 'topcatigories'),
                   ('艺术家', 'artistregions')]

top_catigories = [('热力新歌TOP1000', 'http://www.top100.cn/hot/allsong.shtml'),
                  ('华语流行TOP1000', 'http://www.top100.cn/hot/allsong-inland.shtml'),
                  ('港台流行TOP1000', 'http://www.top100.cn/hot/allsong-hongkong.shtml'),
                  ('日韩流行TOP1000', 'http://www.top100.cn/hot/allsong-japankorea.shtml'),
                  ('欧美流行TOP1000', 'http://www.top100.cn/hot/allsong-europ.shtml'),
                  ('其它流行TOP1000', 'http://www.top100.cn/hot/allsong-other.shtml')]

artist_catigories = [('大陆',[('大陆男艺术家', 'http://www.top100.cn/artist/index-inland-male.shtml'),
                              ('大陆女艺术家', 'http://www.top100.cn/artist/index-inland-female.shtml'),
                              ('大陆乐队组合', 'http://www.top100.cn/artist/index-inland-group.shtml')]),
                     ('港台',[('港台男艺术家', 'http://www.top100.cn/artist/index-hongkong-male.shtml'),
                              ('港台女艺术家', 'http://www.top100.cn/artist/index-hongkong-female.shtml'),
                              ('港台乐队组合', 'http://www.top100.cn/artist/index-hongkong-group.shtml')]),
                     ('日韩',[('日韩男艺术家', 'http://www.top100.cn/artist/index-japankorea-male.shtml'),
                              ('日韩女艺术家', 'http://www.top100.cn/artist/index-japankorea-female.shtml'),
                              ('日韩乐队组合', 'http://www.top100.cn/artist/index-japankorea-group.shtml')]),
                     ('欧美',[('欧美男艺术家', 'http://www.top100.cn/artist/index-europ-male.shtml'),
                              ('欧美女艺术家', 'http://www.top100.cn/artist/index-europ-female.shtml'),
                              ('欧美乐队组合', 'http://www.top100.cn/artist/index-europ-group.shtml')]),
                     ('其它',[('其他男艺术家', 'http://www.top100.cn/artist/index-other-male.shtml'),
                              ('其他女艺术家', 'http://www.top100.cn/artist/index-other-female.shtml'),
                              ('其他乐队组合', 'http://www.top100.cn/artist/index-other-group.shtml')])]


def getRoot(params):
    items = []
    for cat in root_catigories:
        item = xbmcgui.ListItem(cat[0])
        url = '%s?cmd=listdir&type=%s' % (sys.argv[0], cat[1])
        items.append((url, item, True))
    return items

def getTopCatigories(params):
    items = []
    for cat in top_catigories:
        item = xbmcgui.ListItem(cat[0])
        url = '%s?cmd=listdir&type=topgroups&url=%s' % (sys.argv[0], cat[1])
        items.append((url, item, True))
    return items

def getTopGroups(params):
    items = []
    for i in range(10):
        item = xbmcgui.ListItem('%d - %d' % ((i * 100) + 1, (i * 100) + 100))
        url = '%s?cmd=listdir&type=topsongs&url=%s&group=%s' % (sys.argv[0], params['url'].replace('.shtml', '-%d.shtml' % (i + 1)), i)
        items.append((url, item, True))
    return items        

def getTopSongs(params):
    items = []    
    f = urllib.urlopen(params['url'])
    data = f.read()
    pattern = '<ul class="sli.*>\r\n(.*\r\n)+? +</ul>'
    matches = re.finditer(pattern, data)
    i = int(params['group']) * 100
    for match in matches:
        item = xbmcgui.ListItem()
        pattern = '<li class="l5"><a href="javascript:.*openPlayer\(\'(.+)\'\);".*\r\n( +title=".+">\r\n)? +(.+)</a>'
        m1 = re.search(pattern, match.group(0))
        title = m1.group(3).strip()
        pattern = '<a target=\'_blank\'.*?>(.+?)</a>'
        m2 = re.findall(pattern, match.group(0))
        artist = '/'.join(m2)
        label = ''
        if params['cmd'] == 'listdir':
            label = '%d. %s - %s' % (i + 1, artist, title)
        elif params['cmd'] == 'queueall':
            label = '%s - %s' % (artist, title)
        item.setLabel(label)
        url = '%s?cmd=play&id=%s&title=%s&artist=%s' % (sys.argv[0], m1.group(1), title, artist)
        item.setProperty('IsPlayable', 'true')
        item.setInfo('music', {'title': title, 'artist': artist})
        item.addContextMenuItems([('添加所有歌曲到播放列表', 'XBMC.RunPlugin(%s?cmd=queueall&type=topsongs&url=%s&group=%s)' % (sys.argv[0], params['url'], params['group']),)])
        items.append((url, item, False))
        i += 1
    return items

def getArtistRegions(params):
    items = []
    for idx, region in enumerate(artist_catigories):
        item = xbmcgui.ListItem(region[0])
        url = '%s?cmd=listdir&type=artistcatigories&idx=%s' % (sys.argv[0], idx)
        items.append((url, item, True))
    return items

def getArtistCatigories(params):
    items = []
    for cat in artist_catigories[int(params['idx'])][1]:
        item = xbmcgui.ListItem(cat[0])
        url = '%s?cmd=listdir&type=artistgroups&url=%s' % (sys.argv[0], cat[1])
        items.append((url, item, True))
    return items

def getArtistGroups(params):
    items = []
    
    item = xbmcgui.ListItem('热门歌手')
    url = '%s?cmd=listdir&type=artists&url=%s&group=%s' % (sys.argv[0], params['url'], 'hot')
    items.append((url, item, True))
    
    f = urllib.urlopen(params['url'])
    data = f.read()
    pattern = 'style="" href="#(.+?)"'
    matches = re.finditer(pattern, data)
    for match in matches:
        artist_group = match.group(1)
        item = xbmcgui.ListItem(artist_group)
        url = '%s?cmd=listdir&type=artists&url=%s&group=%s' % (sys.argv[0], params['url'], artist_group)
        items.append((url, item, True))        
    return items

def getArtists(params):
    items = []
    f = urllib.urlopen(params['url'])
    data = f.read()

    if params['group'] == 'hot':
        pattern = '<li class="l2"><a href="(.+)" target="_blank" class="a3">(.+)</a></li>'
    else:
        pattern = '<dl class="fnav">\r\n(.*\r\n){2}.*<div>%s</div>\r\n(.*\r\n)+? +</dl>' % params['group']
        match = re.search(pattern, data)
        data = match.group(0)
        pattern = '<a href="(.+)" target="_blank" class="a3">(.+)</a>'
    matches = re.finditer(pattern, data)
    for match in matches:
        artist_home = 'http://www.top100.cn%s' % match.group(1)[2:]
        item = xbmcgui.ListItem(match.group(2))
        url = '%s?cmd=listdir&type=artisthome&url=%s' % (sys.argv[0], artist_home)
        items.append((url, item, True))    
    return items

def getArtistHome(params):
    items = []
    
    item = xbmcgui.ListItem('热门单曲')
    url = '%s?cmd=listdir&type=artistsongs&url=%s' % (sys.argv[0], params['url'])
    items.append((url, item, True))

    item = xbmcgui.ListItem('专辑列表')
    url = '%s?cmd=listdir&type=artistalbums&url=%s' % (sys.argv[0], params['url'].replace('info', 'album'))
    items.append((url, item, True))

    return items

def getArtistAlbums(params):
    items = []

    f = urllib.urlopen(params['url'])
    data = f.read()

    pattern = '<li class="l1"><a href=\'(.+)\' target="_blank" title="(.+)">.+</a></li>\r\n'
    matches = re.finditer(pattern, data)
    for match in matches:
        album_url = 'http://www.top100.cn%s' % match.group(1)[2:]
        item = xbmcgui.ListItem(match.group(2))
        url = '%s?cmd=listdir&type=artistsongs&url=%s' % (sys.argv[0], album_url)
        items.append((url, item, True))

    pattern = '<a href="(/artist/album-\w+-\d+\.shtml)" class="nextlink"><span>后页</span></a>'
    matches = re.finditer(pattern, data)
    for match in matches:
        params['url'] = 'http://www.top100.cn%s' % match.group(1)
        items.extend(getArtistAlbums(params))

    return items

def getArtistSongs(params):
    items = []    
    f = urllib.urlopen(params['url'])
    data = f.read()
    pattern = '<ul class="sl".*\r\n(.*\r\n)+? +</ul>'
    matches = re.finditer(pattern, data)
    for i, match in enumerate(matches):
        item = xbmcgui.ListItem()
        pattern = '<li class="l3"><a  href="javascript:page.common.openPlayer\(\'(.+)\'\);".*>(.+)</a>'
        m1 = re.search(pattern, match.group(0))
        title = m1.group(2).strip()
        pattern = '<a target=\'_blank\'.*?>(.+?)</a>'
        m2 = re.findall(pattern, match.group(0))
        artist = '/'.join(m2)
        label = ''
        if params['cmd'] == 'listdir':
            label = '%d. %s - %s' % (i + 1, artist, title)
        elif params['cmd'] == 'queueall':
            label = '%s - %s' % (artist, title)
        item.setLabel(label)
        url = '%s?cmd=play&id=%s&title=%s&artist=%s' % (sys.argv[0], m1.group(1), title, artist)
        item.setProperty('IsPlayable', 'true')
        item.setInfo('music', {'title': title, 'artist': artist})
        item.addContextMenuItems([('添加所有歌曲到播放列表', 'XBMC.RunPlugin(%s/?cmd=queueall&type=artistsongs&url=%s)' % (sys.argv[0], params['url']),)])
        items.append((url, item, False))
    return items

def play(params):
    domain = 'www.top100.cn'
    url = '/download/download.aspx?Productid=%s' % params['id'][1:]
    
    conn = httplib.HTTPConnection(domain)
    conn.request('GET', url)
    res = conn.getresponse()
    data = res.read()
    pattern = '<a href="http://www.top100.cn(.+?)".*>下载</a>'
    m = re.search(pattern, data)

    referer = 'http://%s%s' % (domain, url)
    headers = {'Referer':referer}
    conn.request('HEAD', m.group(1), headers=headers)
    res = conn.getresponse()

    for header in res.getheaders():
        if header[0] == 'location':
            item = xbmcgui.ListItem()
            item.setInfo('music', {'title': params['title'], 'artist': params['artist']})
            item.setPath(header[1])
            xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)

def queueAll(params):
    playlist = xbmc.PlayList(xbmc.PLAYLIST_MUSIC)
    if params['type'] == 'topsongs':
        items = getTopSongs(params)
    elif params['type'] == 'artistsongs':
        items = getArtistSongs(params)
    for item in items:
        playlist.add(item[0], item[1])

def getDirectoryItems(params):
    type = params['type']
    
    if type == 'root':
        return getRoot(params)    
    elif type == 'topcatigories':
        return getTopCatigories(params)
    elif type == 'topgroups':
        return getTopGroups(params)
    elif type == 'topsongs':
        return getTopSongs(params)
    elif type == 'artistregions':
        return getArtistRegions(params)
    elif type == 'artistcatigories':
        return getArtistCatigories(params)
    elif type == 'artistgroups':
        return getArtistGroups(params)
    elif type == 'artists':
        return getArtists(params)
    elif type == 'artisthome':
        return getArtistHome(params)
    elif type == 'artistsongs':
        return getArtistSongs(params)
    elif type == 'artistalbums':
        return getArtistAlbums(params)
    else:
        return []

def listDirectory(params):
    items = getDirectoryItems(params)
    xbmcplugin.addDirectoryItems(int(sys.argv[1]), items, len(items))
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

def parseParams(str):
    result = {}
    if not str:
        result['cmd'] = 'listdir'
        result['type'] = 'root'
        return result
    for param in str[1:].split('&'):
        key = param.split('=')[0]
        value = param.split('=')[1]
        result[key] = value
    return result

params = parseParams(sys.argv[2])

cmd = params['cmd']
if cmd == 'listdir':
    listDirectory(params)
elif cmd == 'play':
    play(params)
elif cmd == 'queueall':
    queueAll(params)
