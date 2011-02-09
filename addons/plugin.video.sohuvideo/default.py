# -*- coding: cp936 -*-
import xbmc,xbmcgui,xbmcplugin,urllib2,urllib,re,sys
import gzip
import StringIO

#Sohu Video - by robinttt 2010.

def Roots():
	li=xbmcgui.ListItem('高清影视')
	u=sys.argv[0]+"?mode=1&name="+urllib.quote_plus('高清影视')
	xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
	li=xbmcgui.ListItem('电视节目(敬请期待)')
	u=sys.argv[0]+"?mode=40&name="+urllib.quote_plus('电视节目')
	xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
	li=xbmcgui.ListItem('视频新闻(敬请期待)')
	u=sys.argv[0]+"?mode=40&name="+urllib.quote_plus('视频新闻')
	xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)

def Channels(name):
	li=xbmcgui.ListItem(name+'>分类')
	u=sys.argv[0]+"?mode=2&name="+urllib.quote_plus(name)
	xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
	li=xbmcgui.ListItem(name+'>榜单')
	u=sys.argv[0]+"?mode=6&name="+urllib.quote_plus(name+'>榜单')
	xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)

def ListsA(name):
	li=xbmcgui.ListItem(name+'>电影分类')
	u=sys.argv[0]+"?mode=3&name="+urllib.quote_plus(name+'>电影')
	xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
	li=xbmcgui.ListItem(name+'>电视剧分类')
	u=sys.argv[0]+"?mode=3&name="+urllib.quote_plus(name+'>电视剧')
	xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
	li=xbmcgui.ListItem(name+'>纪录片分类')
	u=sys.argv[0]+"?mode=3&name="+urllib.quote_plus(name+'>纪录片')
	xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
	li=xbmcgui.ListItem(name+'>演员分类')
	u=sys.argv[0]+"?mode=4&name="+urllib.quote_plus(name+'>演员分类')
	xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
	li=xbmcgui.ListItem(name+'>个性分类')
	u=sys.argv[0]+"?mode=4&name="+urllib.quote_plus(name+'>个性分类')
	xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
	li=xbmcgui.ListItem(name+'>年份检索')
	u=sys.argv[0]+"?mode=4&name="+urllib.quote_plus(name+'>年份检索')
	xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)

def ListsB(name):
        if name=='高清影视>纪录片':
		li=xbmcgui.ListItem(name+'>类型')
		u=sys.argv[0]+"?mode=4&name="+urllib.quote_plus(name+'>类型')
		xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
		li=xbmcgui.ListItem(name+'>个性')
		u=sys.argv[0]+"?mode=4&name="+urllib.quote_plus(name+'>个性')
		xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
        else:
		li=xbmcgui.ListItem(name+'>类型')
		u=sys.argv[0]+"?mode=4&name="+urllib.quote_plus(name+'>类型')
		xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
		li=xbmcgui.ListItem(name+'>地区')
		u=sys.argv[0]+"?mode=4&name="+urllib.quote_plus(name+'>地区')
		xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)

def ListsC(name):
	typename=name.split('>')[1]
	if typename=='纪录片':
		req = urllib2.Request('http://tv.sohu.com/real/')
	elif typename=='电视剧':
		req = urllib2.Request('http://tv.sohu.com/teleplay/')
	else:
	        req = urllib2.Request('http://tv.sohu.com/movie/')
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
	if response.headers.get('content-encoding', None) == 'gzip':
	       	link = gzip.GzipFile(fileobj=StringIO.StringIO(link)).read()
        response.close()
        link=re.sub('\r','',link)
        link=re.sub('\n','',link)
        link=re.sub('\t','',link)
        if name=='高清影视>纪录片>类型':
                match=re.compile('<div class="list clear"><h3>按类型\|</h3><ul>(.+?)</ul></div>').findall(link)
                match0=re.compile('<li><a href="(.+?)" target=_blank>(.+?)</a>').findall(match[0])
                for url1,name1 in match0:
	                li=xbmcgui.ListItem(name+'>'+name1)
	                u=sys.argv[0]+"?mode=15&name="+urllib.quote_plus(name+'>'+name1)+"&jsona="+urllib.quote_plus(name1)+"&jsonf="+urllib.quote_plus('7')+"&jsono="+urllib.quote_plus('4')+"&jsonc="+urllib.quote_plus('8')+"&jsonn="+urllib.quote_plus('1')
	                xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)

        elif name=='高清影视>纪录片>个性':
                match=re.compile('href="http://tv.sohu.com/tagreal/#key=(.+?)"').findall(link)
                for name1 in match:
	                li=xbmcgui.ListItem(name+'>'+name1)
	                u=sys.argv[0]+"?mode=15&name="+urllib.quote_plus(name+'>'+name1)+"&jsona="+urllib.quote_plus(name1)+"&jsonf="+urllib.quote_plus('22')+"&jsono="+urllib.quote_plus('4')+"&jsonc="+urllib.quote_plus('8')+"&jsonn="+urllib.quote_plus('1')
	                xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)

        elif name=='高清影视>电影>类型':
                match=re.compile('<div class="list clear"><h3>按类型\|</h3>(.+?)</div><div class=line></div>').findall(link)
                match0=re.compile("searchKey\('(.+?)'").findall(match[0])
                for name1 in match0:
	                li=xbmcgui.ListItem(name+'>'+name1)
	                u=sys.argv[0]+"?mode=5&name="+urllib.quote_plus(name+'>'+name1)+"&jsona="+urllib.quote_plus(name1)+"&jsonf="+urllib.quote_plus('7')
	                xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)

        elif name=='高清影视>电影>地区':
                match=re.compile('<div class="list clear"><h3>按地区\|</h3>(.+?)</div><div class=line></div>').findall(link)
                match0=re.compile("searchKey\('(.+?)'").findall(match[0])
                for name1 in match0:
	                li=xbmcgui.ListItem(name+'>'+name1)
	                u=sys.argv[0]+"?mode=5&name="+urllib.quote_plus(name+'>'+name1)+"&jsona="+urllib.quote_plus(name1)+"&jsonf="+urllib.quote_plus('12')
	                xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)

        elif name=='高清影视>电视剧>类型':
                match=re.compile('<div class="list clear" collection="Y"><h3>按类型\|</h3><ul>(.+?)</ul></div><div class=line></div>').findall(link)
                print match
                match0=re.compile("searchKey\('(.+?)'").findall(match[0])
                for name1 in match0:
	                li=xbmcgui.ListItem(name+'>'+name1)
	                u=sys.argv[0]+"?mode=5&name="+urllib.quote_plus(name+'>'+name1)+"&jsona="+urllib.quote_plus(name1)+"&jsonf="+urllib.quote_plus('7')
	                xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)

        elif name=='高清影视>电视剧>地区':
                match=re.compile('<div class="list clear" collection="Y"><h3>按地区\|</h3><ul>(.+?)</ul></div><div class=line></div>').findall(link)
                match0=re.compile("searchKey\('(.+?)'").findall(match[0])
                for name1 in match0:
	                li=xbmcgui.ListItem(name+'>'+name1)
	                u=sys.argv[0]+"?mode=5&name="+urllib.quote_plus(name+'>'+name1)+"&jsona="+urllib.quote_plus(name1)+"&jsonf="+urllib.quote_plus('12')
	                xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)

        elif name=='高清影视>演员分类':
                match=re.compile('<div class="list clear"><h3>按明星\|</h3>(.+?)</div><div class=line></div>').findall(link)
                match0=re.compile("searchKey\('(.+?)'").findall(match[0])
                for name1 in match0:
	                li=xbmcgui.ListItem(name+'>'+name1)
	                u=sys.argv[0]+"?mode=5&name="+urllib.quote_plus(name+'>'+name1)+"&jsona="+urllib.quote_plus(name1)+"&jsonf="+urllib.quote_plus('4')
	                xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)

        elif name=='高清影视>个性分类':
                match=re.compile('<div class="list clear c4"><h3>个性分类\|</h3><ul>(.+?)</ul></div>').findall(link)
                match0=re.compile('href="http://tv.sohu.com/tagsearch/#key=(.+?)"').findall(match[0])
                for name1 in match0:
	                li=xbmcgui.ListItem(name+'>'+name1)
	                u=sys.argv[0]+"?mode=15&name="+urllib.quote_plus(name+'>'+name1)+"&jsona="+urllib.quote_plus(name1)+"&jsonf="+urllib.quote_plus('22')+"&jsono="+urllib.quote_plus('4')+"&jsonc="+urllib.quote_plus('')+"&jsonn="+urllib.quote_plus('1')
	                xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)

        elif name=='高清影视>年份检索':
                match=re.compile('<div class="list clear"><h3>按年份\|</h3>(.+?)</div><div class=line></div>').findall(link)
                match0=re.compile("searchKey\('(.+?)'").findall(match[0])
                for name1 in match0:
	                li=xbmcgui.ListItem(name+'>'+name1)
	                u=sys.argv[0]+"?mode=5&name="+urllib.quote_plus(name+'>'+name1)+"&jsona="+urllib.quote_plus(name1)+"&jsonf="+urllib.quote_plus('15')
	                xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)

def ListsD(name,jsona,jsonf):
	li=xbmcgui.ListItem(name+'>最多播放')
	u=sys.argv[0]+"?mode=15&name="+urllib.quote_plus(name+'>最多播放')+"&jsona="+urllib.quote_plus(jsona)+"&jsonf="+urllib.quote_plus(jsonf)+"&jsono="+urllib.quote_plus('1')+"&jsonc="+urllib.quote_plus('')+"&jsonn="+urllib.quote_plus('1')
	xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
	li=xbmcgui.ListItem(name+'>最新发布')
	u=sys.argv[0]+"?mode=15&name="+urllib.quote_plus(name+'>最新发布')+"&jsona="+urllib.quote_plus(jsona)+"&jsonf="+urllib.quote_plus(jsonf)+"&jsono="+urllib.quote_plus('0')+"&jsonc="+urllib.quote_plus('')+"&jsonn="+urllib.quote_plus('1')
	xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
	li=xbmcgui.ListItem(name+'>相关程度')
	u=sys.argv[0]+"?mode=15&name="+urllib.quote_plus(name+'>相关程度')+"&jsona="+urllib.quote_plus(jsona)+"&jsonf="+urllib.quote_plus(jsonf)+"&jsono="+urllib.quote_plus('')+"&jsonc="+urllib.quote_plus('')+"&jsonn="+urllib.quote_plus('1')
	xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)

def SortsA(name):
	li=xbmcgui.ListItem(name+'>周期')
	u=sys.argv[0]+"?mode=7&name="+urllib.quote_plus(name+'>周期')
	xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
	li=xbmcgui.ListItem(name+'>评分')
	u=sys.argv[0]+"?mode=10&name="+urllib.quote_plus(name+'>评分')
	xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
	li=xbmcgui.ListItem(name+'>分项')
	u=sys.argv[0]+"?mode=12&name="+urllib.quote_plus(name+'>分项')
	xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)


def SortsB(name):
	li=xbmcgui.ListItem(name+'>全部')
	u=sys.argv[0]+"?mode=8&name="+urllib.quote_plus(name+'>全部')+"&url="+urllib.quote_plus('total')
	xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
	li=xbmcgui.ListItem(name+'>每周')
	u=sys.argv[0]+"?mode=8&name="+urllib.quote_plus(name+'>每周')+"&url="+urllib.quote_plus('week')
	xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
	li=xbmcgui.ListItem(name+'>每日')
	u=sys.argv[0]+"?mode=8&name="+urllib.quote_plus(name+'>每日')+"&url="+urllib.quote_plus('day')
	xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)


def SortsC(url,name):
	li=xbmcgui.ListItem(name+'>电影')
	u=sys.argv[0]+"?mode=9&name="+urllib.quote_plus(name+'>电影')+"&url="+urllib.quote_plus('http://tv.sohu.com/frag/vrs_inc/phb_mv_'+url+'_50.js')
	xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
	li=xbmcgui.ListItem(name+'>电视剧')
	u=sys.argv[0]+"?mode=9&name="+urllib.quote_plus(name+'>电视剧')+"&url="+urllib.quote_plus('http://tv.sohu.com/frag/vrs_inc/phb_tv_'+url+'_50.js')
	xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
	li=xbmcgui.ListItem(name+'>纪录片')
	u=sys.argv[0]+"?mode=9&name="+urllib.quote_plus(name+'>纪录片')+"&url="+urllib.quote_plus('http://tv.sohu.com/frag/vrs_inc/phb_doc_'+url+'_50.js')
	xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)

def SortsD(url,name):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
	if response.headers.get('content-encoding', None) == 'gzip':
        	link = gzip.GzipFile(fileobj=StringIO.StringIO(link)).read()
        response.close()
        match=re.compile('"DIRECTOR":"(.+?)"(.+?)"tv_desc":"(.+?)"(.+?)"tv_big_pic":"(.+?)"(.+?)"tv_url":"(.+?)"(.+?)"tv_name":"(.+?)"').findall(link)
        if len(match)>0:
		li=xbmcgui.ListItem('当前位置:'+name+'  TOP50')
		u=sys.argv[0]+"?mode=40&name="+urllib.quote_plus(name)
		xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
                for i in range(0,len(match)):
	        	li=xbmcgui.ListItem(str(i+1)+'.'+match[i][8],iconImage='', thumbnailImage=match[i][4])
	        	u=sys.argv[0]+"?mode=16&name="+urllib.quote_plus(match[i][8])+"&url="+urllib.quote_plus(match[i][6])+"&director="+urllib.quote_plus(match[i][0])+"&studio="+urllib.quote_plus('')+"&plot="+urllib.quote_plus(match[i][2])
	        	xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)

def SortsE(url,name):
	li=xbmcgui.ListItem(name+'>完美')
	u=sys.argv[0]+"?mode=11&name="+urllib.quote_plus(name+'>完美')+"&url="+urllib.quote_plus('4')
	xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
	li=xbmcgui.ListItem(name+'>很好')
	u=sys.argv[0]+"?mode=11&name="+urllib.quote_plus(name+'>很好')+"&url="+urllib.quote_plus('3')
	xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
	li=xbmcgui.ListItem(name+'>一般')
	u=sys.argv[0]+"?mode=11&name="+urllib.quote_plus(name+'>一般')+"&url="+urllib.quote_plus('2')
	xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
	li=xbmcgui.ListItem(name+'>烂片')
	u=sys.argv[0]+"?mode=11&name="+urllib.quote_plus(name+'>烂片')+"&url="+urllib.quote_plus('1')
	xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)

def SortsF(url,name):
	li=xbmcgui.ListItem(name+'>全部')
	u=sys.argv[0]+"?mode=15&name="+urllib.quote_plus(name+'>全部')+"&jsona="+urllib.quote_plus(url)+"&jsonf="+urllib.quote_plus('16')+"&jsono="+urllib.quote_plus('3')+"&jsonc="+urllib.quote_plus('')+"&jsonn="+urllib.quote_plus('1')
	xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
	li=xbmcgui.ListItem(name+'>电影')
	u=sys.argv[0]+"?mode=15&name="+urllib.quote_plus(name+'>电影')+"&jsona="+urllib.quote_plus(url)+"&jsonf="+urllib.quote_plus('16')+"&jsono="+urllib.quote_plus('3')+"&jsonc="+urllib.quote_plus('1')+"&jsonn="+urllib.quote_plus('1')
	xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
	li=xbmcgui.ListItem(name+'>电视剧')
	u=sys.argv[0]+"?mode=15&name="+urllib.quote_plus(name+'>电视剧')+"&jsona="+urllib.quote_plus(url)+"&jsonf="+urllib.quote_plus('16')+"&jsono="+urllib.quote_plus('3')+"&jsonc="+urllib.quote_plus('2')+"&jsonn="+urllib.quote_plus('1')
	xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
	li=xbmcgui.ListItem(name+'>纪录片')
	u=sys.argv[0]+"?mode=15&name="+urllib.quote_plus(name+'>纪录片')+"&jsona="+urllib.quote_plus(url)+"&jsonf="+urllib.quote_plus('16')+"&jsono="+urllib.quote_plus('3')+"&jsonc="+urllib.quote_plus('8')+"&jsonn="+urllib.quote_plus('1')
	xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)

def SortsG(url,name):
	li=xbmcgui.ListItem(name+'>导演')
	u=sys.argv[0]+"?mode=13&name="+urllib.quote_plus(name+'>导演')+"&url="+urllib.quote_plus('219')
	xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
	li=xbmcgui.ListItem(name+'>演员')
	u=sys.argv[0]+"?mode=13&name="+urllib.quote_plus(name+'>演员')+"&url="+urllib.quote_plus('220')
	xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
	li=xbmcgui.ListItem(name+'>剧情')
	u=sys.argv[0]+"?mode=13&name="+urllib.quote_plus(name+'>剧情')+"&url="+urllib.quote_plus('221')
	xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
	li=xbmcgui.ListItem(name+'>画面')
	u=sys.argv[0]+"?mode=13&name="+urllib.quote_plus(name+'>画面')+"&url="+urllib.quote_plus('222')
	xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
	li=xbmcgui.ListItem(name+'>音乐')
	u=sys.argv[0]+"?mode=13&name="+urllib.quote_plus(name+'>音乐')+"&url="+urllib.quote_plus('223')
	xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)

def SortsH(url,name):
	li=xbmcgui.ListItem(name+'>全部')
	u=sys.argv[0]+"?mode=14&name="+urllib.quote_plus(name+'>全部')+"&url="+urllib.quote_plus('http://tv.sohu.com/frag/vrs_inc/phb_score_'+url+'_50.js')
	xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
	li=xbmcgui.ListItem(name+'>电影')
	u=sys.argv[0]+"?mode=14&name="+urllib.quote_plus(name+'>电影')+"&url="+urllib.quote_plus('http://tv.sohu.com/frag/vrs_inc/phb_score_mv_'+url+'_50.js')
	xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
	li=xbmcgui.ListItem(name+'>电视剧')
	u=sys.argv[0]+"?mode=14&name="+urllib.quote_plus(name+'>电视剧')+"&url="+urllib.quote_plus('http://tv.sohu.com/frag/vrs_inc/phb_score_tv_'+url+'_50.js')
	xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)

def SortsI(url,name):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
	if response.headers.get('content-encoding', None) == 'gzip':
        	link = gzip.GzipFile(fileobj=StringIO.StringIO(link)).read()
        response.close()
        match=re.compile('"DIRECTOR":"(.+?)"(.+?)"tv_comment":"(.+?)","MAIN_ACTOR":"(.+?)","tv_score":"(.+?)"(.+?)"tv_big_pic":"(.+?)"(.+?)"tv_url":"(.+?)","tv_name":"(.+?)"').findall(link)
        if len(match)>0:
		li=xbmcgui.ListItem('当前位置:'+name+'  TOP50')
		u=sys.argv[0]+"?mode=40&name="+urllib.quote_plus(name)
		xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
        	for i in range(0,len(match)):
	  	        li=xbmcgui.ListItem(str(i+1)+'.'+match[i][9]+' ('+match[i][4][0:3]+'分)',iconImage='', thumbnailImage=match[i][6])
	  	     	u=sys.argv[0]+"?mode=16&name="+urllib.quote_plus(match[i][9])+"&url="+urllib.quote_plus(match[i][8])+"&director="+urllib.quote_plus(match[i][0])+"&studio="+urllib.quote_plus(match[i][3])+"&plot="+urllib.quote_plus(match[i][2])
	   	    	xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)

def MovieList(name,jsona,jsonf,jsono,jsonc,jsonn):
        if name.find('年份检索')!=-1 or name.find('评分')!=-1:
                url='http://search.vrs.sohu.com/video_f'+jsonf+'_o'+jsono+'_c'+jsonc+'_s_n'+jsonn+'_p15_chltv.sohu.com_k'+jsona+'.json'
        else:
                name1=''
                for item in jsona.decode('gbk'):
                       name1=name1+"%25u"+"%X"%ord(item)
                       url='http://search.vrs.sohu.com/video_f'+jsonf+'_o'+jsono+'_c'+jsonc+'_s_n'+jsonn+'_p15_chltv.sohu.com_k'+name1+'.json'
        #dialog = xbmcgui.Dialog()
        #ok=dialog.ok(name,url)
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
	if response.headers.get('content-encoding', None) == 'gzip':
        	link = gzip.GzipFile(fileobj=StringIO.StringIO(link)).read()
        response.close()
        match=re.compile('"totalCount":(.+?),"').findall(link)
        paget=abs(int(match[0])/-15)
        if paget>0:
            li=xbmcgui.ListItem('当前位置:'+name+'  第'+jsonn+'/'+str(paget)+'页')
            u=sys.argv[0]+"?mode=40&name="+urllib.quote_plus(name)
            xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
        if int(jsonn)>1:
            li=xbmcgui.ListItem('..第一页')
            u=sys.argv[0]+"?mode=15&name="+urllib.quote_plus(name)+"&jsona="+urllib.quote_plus(jsona)+"&jsonf="+urllib.quote_plus(jsonf)+"&jsono="+urllib.quote_plus(jsono)+"&jsonc="+urllib.quote_plus(jsonc)+"&jsonn="+urllib.quote_plus('1')
            xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
            li=xbmcgui.ListItem('..上一页')
            u=sys.argv[0]+"?mode=15&name="+urllib.quote_plus(name)+"&jsona="+urllib.quote_plus(jsona)+"&jsonf="+urllib.quote_plus(jsonf)+"&jsono="+urllib.quote_plus(jsono)+"&jsonc="+urllib.quote_plus(jsonc)+"&jsonn="+urllib.quote_plus(str(int(jsonn)-1))
            xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
        if int(jsonn)<paget:
            li=xbmcgui.ListItem('..下一页')
            u=sys.argv[0]+"?mode=15&name="+urllib.quote_plus(name)+"&jsona="+urllib.quote_plus(jsona)+"&jsonf="+urllib.quote_plus(jsonf)+"&jsono="+urllib.quote_plus(jsono)+"&jsonc="+urllib.quote_plus(jsonc)+"&jsonn="+urllib.quote_plus(str(int(jsonn)+1))
            xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
            li=xbmcgui.ListItem('..最后页')
            u=sys.argv[0]+"?mode=15&name="+urllib.quote_plus(name)+"&jsona="+urllib.quote_plus(jsona)+"&jsonf="+urllib.quote_plus(jsonf)+"&jsono="+urllib.quote_plus(jsono)+"&jsonc="+urllib.quote_plus(jsonc)+"&jsonn="+urllib.quote_plus(str(paget))
            xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
        match=re.compile('[^=]\{([^\}].+?)\}').findall(link.decode("gbk").encode("utf8"))
        #ok=dialog.ok(name,str(len(match)))
        for i in range(0,len(match)):
            match0=re.compile('"videoName":"(.+?)",').findall(match[i])
            if len(match0)>0:
                name1=match0[0].decode("utf8").encode("gbk")
            match0=re.compile('"videoScore":(.+?),').findall(match[i])
            if len(match0)>0:
                score=match0[0]
            match0=re.compile('"videoSmallPic":"(.+?)",').findall(match[i])
            if len(match0)>0:
                iconimg=match0[0]
            match0=re.compile('"videoBigPic":"(.+?)",').findall(match[i])
            if len(match0)>0:
                timg=match0[0]
            match0=re.compile('"videoUrl":"(.+?)",').findall(match[i])
            if len(match0)>0:
                url2=match0[0]
            match0=re.compile('"videoDirector":"(.+?)",').findall(match[i])
            if len(match0)>0:
                director=match0[0]
            match0=re.compile('"videoActor":"(.+?)",').findall(match[i])
            if len(match0)>0:
                actor=match0[0]
            match0=re.compile('"videoAlbumContCategory":"(.+?)",').findall(match[i])
            if len(match0)>0:
                category=match0[0]
            #score=str(match0[19][1])
            #iconimg=match0[23][1].replace('"',"")
            #timg=match0[17][1].replace('"',"")
            li=xbmcgui.ListItem(str(i+1)+'.'+name1+' ('+score[0:3]+'分)',"",iconimg,timg)
            u=sys.argv[0]+"?mode=16&name="+urllib.quote_plus(name1)+"&url="+urllib.quote_plus(url2)+"&director="+urllib.quote_plus(director)+"&studio="+urllib.quote_plus(actor)+"&plot="+urllib.quote_plus(category)
            xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)

def MovieId(name,url,director,studio,plot):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
	#网易使用gzip返回数据
	if response.headers.get('content-encoding', None) == 'gzip':
        	link = gzip.GzipFile(fileobj=StringIO.StringIO(link)).read()
        response.close()
        link=re.sub(' ','',link)
        match=re.compile('varvid="(.+?)";').findall(link)
        vid=match[0]
        match=re.compile('varpid="(.+?)";').findall(link)
        pid=match[0]
        link=re.sub("\r","",link)
        link=re.sub("\n","",link)
        link=re.sub("\t","",link)
	desc=directory=actor=category=""
        match=re.compile('<divid="introID"><P>(.+?)<SCRIPTtype=text/javascript>(.+?)</SCRIPT>').findall(link)
        if len(match)>0:
                desc=match[0][0]
                match0=re.compile('VRS_DIRECTOR="(.+?)";').findall(match[0][1])
                if len(match0)>0:
                    director=match0[0]
                match0=re.compile('VRS_ACTOR="(.+?)";').findall(match[0][1])
                if len(match0)>0:
                    actor=match0[0]
                match0=re.compile('VRS_CATEGORY="(.+?)";').findall(match[0][1])
                if len(match0)>0:
                    category=match0[0]
        url='http://hot.vrs.sohu.com/vrs_videolist.action?vid='+vid+'&pid='+pid
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
	li=xbmcgui.ListItem('当前影视名称:'+name)
	u=sys.argv[0]+"?mode=40&name="+urllib.quote_plus(name)
	xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,False)
        match=re.compile('"videoImage":"(.+?)"(.+?)"videoId":(.+?),"(.+?)"videoName":"(.+?)"').findall(link)
        if len(match)>0:
                for i in range(0,len(match)):
                        if name==match[i][4]:
                                li=xbmcgui.ListItem('播放 >> '+str(i+1)+'.'+match[i][4],match[i][0],match[i][0])
                                li.setInfo(type="Video",infoLabels={"Title":match[i][4],"Director":director,"Studio":studio,"Plot":plot})
                  	        u=sys.argv[0]+"?mode=17&name="+urllib.quote_plus(match[i][4])+"&url="+urllib.quote_plus(match[i][2])+"&thumb="+urllib.quote_plus(match[i][0])+"&director="+urllib.quote_plus(director)+"&studio="+urllib.quote_plus(studio)+"&plot="+urllib.quote_plus(plot)
	                        xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li)  
	else:
                li=xbmcgui.ListItem('播放 >> '+name)
      	        u=sys.argv[0]+"?mode=17&name="+urllib.quote_plus(name)+"&url="+urllib.quote_plus(vid)+"&thumb=&director=&studio=&plot="
                xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li)  
	li=xbmcgui.ListItem('内容简介:')
	u=sys.argv[0]+"?mode=40&name="+urllib.quote_plus(name)
	xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,False)
	li=xbmcgui.ListItem("---"+desc)
	u=sys.argv[0]+"?mode=40&name="+urllib.quote_plus(name)
	xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,False)
        li=xbmcgui.ListItem('导演：'+director)
        u=sys.argv[0]+"?mode=40&name="+urllib.quote_plus(name)
        xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,False)
        li=xbmcgui.ListItem('主演：'+actor)
        u=sys.argv[0]+"?mode=40&name="+urllib.quote_plus(name)
        xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,False)
        li=xbmcgui.ListItem('分类：'+category)
        u=sys.argv[0]+"?mode=40&name="+urllib.quote_plus(name)
        xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,False)
                        

def MoviePlay(name,url,thumb,director,studio,plot):
        url='http://hot.vrs.sohu.com/vrs_flash.action?vid='+url
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('"clipsURL"\:\["(.+?)"\]').findall(link)
        paths=match[0].split('","')
        playlist=xbmc.PlayList(1)
        playlist.clear()
        for i in range(0,len(paths)):
	        listitem=xbmcgui.ListItem(name,thumb,thumb)
                listitem.setInfo(type="Video",infoLabels={"Title":name,"Director":director,"Studio":studio,"Plot":plot})
                playlist.add(paths[i], listitem)
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

params=get_params()
mode=None
name=None
url=None
thumb=None
jsona=None
jsonf=None
jsono=None
jsonc=None
jsonn=None
director=None
studio=None
plot=None


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
        jsona=urllib.unquote_plus(params["jsona"])
except:
        pass
try:
        jsonf=urllib.unquote_plus(params["jsonf"])
except:
        pass
try:
        jsono=urllib.unquote_plus(params["jsono"])
except:
        pass
try:
        jsonc=urllib.unquote_plus(params["jsonc"])
except:
        pass
try:
        jsonn=urllib.unquote_plus(params["jsonn"])
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


if mode==None:
	name=''
	Roots()

elif mode==1:
	Channels(name)

elif mode==2:
	ListsA(name)

elif mode==3:
	ListsB(name)

elif mode==4:
	ListsC(name)

elif mode==5:
	ListsD(name,jsona,jsonf)

elif mode==6:
	SortsA(name)

elif mode==7:
	SortsB(name)

elif mode==8:
	SortsC(url,name)

elif mode==9:
	SortsD(url,name)

elif mode==10:
	SortsE(url,name)

elif mode==11:
	SortsF(url,name)

elif mode==12:
	SortsG(url,name)

elif mode==13:
	SortsH(url,name)

elif mode==14:
	SortsI(url,name)

elif mode==15:
	MovieList(name,jsona,jsonf,jsono,jsonc,jsonn)

elif mode==16:
	MovieId(name,url,director,studio,plot)

elif mode==17:
	MoviePlay(name,url,thumb,director,studio,plot)

xbmcplugin.setPluginCategory(int(sys.argv[1]), name )
xbmcplugin.endOfDirectory(int(sys.argv[1]))

    
