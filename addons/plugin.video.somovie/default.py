# -*- coding: utf-8 -*-
import xbmc,xbmcgui,xbmcplugin,urllib2,urllib,re,sys,os,datetime,time

#由于目前XBMC暂不支持中文输入，所以通过google查询的提示功能，将常用拼音或简拼翻译成中文名
#支持PPStream、QVOD、中国电信天翼NetITV、搜狐高清视频、广西宽频网（联通）的影片搜索，若网站支持也可以查到演员、简介等相关视频
#使用前需保证上述视频插件已经安装，并且插件目录名未做修改。
# - by visualcjy@21cn.com 20100725. 首发于http://bbs.htpc1.com
# - 20110129 修改适应google搜索的变化

class SmartRedirectHandler(urllib2.HTTPRedirectHandler):    
    def http_error_301(self, req, fp, code, msg, headers): 
        result = urllib2.HTTPRedirectHandler.http_error_301(
            self, req, fp, code, msg, headers)             
        result.status = code
        return result 
    def http_error_302(self, req, fp, code, msg, headers):  
        result = urllib2.HTTPRedirectHandler.http_error_302(
            self, req, fp, code, msg, headers)             
        result.status = code
        return result

def Roots():
	li=xbmcgui.ListItem("查询中文名称（Google翻译）...")
	u=sys.argv[0]+"?mode=0&name="+urllib.quote_plus("中文")+"&url="
	xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
	li=xbmcgui.ListItem("查询英文名称（含数字）...")
	u=sys.argv[0]+"?mode=0&name="+urllib.quote_plus("英文")+"&url="
	xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
	li=xbmcgui.ListItem("..返回根目录")
	u=""
	xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)

def SearchSite(name,url):
	#dialog = xbmcgui.Dialog()
	li=xbmcgui.ListItem("搜索PPS")
	u='plugin://plugin.video.ppstream/'+"?mode=14&name="+urllib.quote_plus("搜索PPS : "+name)+"&url=http://kan.pps.tv/search/"+urllib.quote_plus(name.decode("utf8").encode("gb2312"))+"/1.html"
	#ok=dialog.ok(name,name.decode("utf8").encode("gb2312"))
	xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
	li=xbmcgui.ListItem("搜索QVOD")
	u=sys.argv[0]+'?mode=2&url='+urllib.quote_plus('search.asp?keyword='.decode("utf8").encode("gbk")+name.decode("utf8").encode("gbk"))+'&name='+urllib.quote_plus("搜索QVOD > "+name)
	xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
	li=xbmcgui.ListItem("搜索天翼NetITV")
	u=sys.argv[0]+'?mode=6&name='+urllib.quote_plus(name)+'&url='+"http://search.netitv.com/searchServlet.xo"+urllib.quote_plus("?k="+name)
	xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
	li=xbmcgui.ListItem("搜索SohuVideo")
	u=sys.argv[0]+'?mode=4&name='+urllib.quote_plus(name)+'&url='+urllib.quote_plus("mts?wd="+name.decode("utf8").encode("gbk"))
	xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
	li=xbmcgui.ListItem("搜索广西宽频网")
	#u='plugin://plugin.video.powerstream/'+"?mode=6&name="+urllib.quote_plus("搜索广西宽频网: "+name)+"&url="+urllib.quote_plus("http://vod.gxbbn.cn/vod_detail.php?keyword="+name.decode("utf8").encode("gb2312"))
	u=sys.argv[0]+"?mode=5&name="+urllib.quote_plus("搜索广西宽频网: "+name)+"&url="+urllib.quote_plus("http://vod.gxbbn.cn/vod_detail.php?keyword="+name.decode("utf8").encode("gb2312"))
	xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
	li=xbmcgui.ListItem("搜索YouKu")
	u=sys.argv[0]+'?mode=7&name='+urllib.quote_plus(name)+'&url='+urllib.quote_plus(name)
	xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
	li=xbmcgui.ListItem("..返回根目录")
	u=""
	xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)

def SearchYouKu(name,url):
	url="http://www.soku.com/search_video/q_"+url
	req = urllib2.Request(url)
	print url
	req.add_header("User-Agent", "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Trident/4.0)")
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	link=link.replace(" ","")
	link=re.sub("\r|\n|\t","",link)
	li=xbmcgui.ListItem("搜索YouKu >"+name)
	u=sys.argv[0]+"?mode=40&name="+urllib.quote_plus(name)
	xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,False)
	match=re.compile('<ulclass="show"><liclass="show_link"><a([^>]*)></a></li><liclass="show_img"><imgsrc="([^"]*)"').findall(link)
	for url2,img in match:
		title=re.compile('title="([^"]*)"').findall(url2)[0]
		url3=re.compile('id_(.+?).html').findall(url2)[0]		
		li=xbmcgui.ListItem(">"+title,title,img,img)
		u='plugin://plugin.video.youku/'+'?mode=16&name='+urllib.quote_plus(title)+'&url='+urllib.quote_plus(url3)
		xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)

def SearchSohu(name,url):
	req = urllib2.Request("http://so.tv.sohu.com/"+url)
	req.add_header("User-Agent", "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Trident/4.0)")
	response = urllib2.urlopen(req)
	link=response.read()
	dialog = xbmcgui.Dialog()
	response.close()
	#link=link.decode("gbk","ignore").encode("utf8")
	link=re.sub("\r|\n|\t","",link)
	li=xbmcgui.ListItem("搜索Sohu >"+name)
	u=sys.argv[0]+"?mode=40&name="+urllib.quote_plus(name)
	xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,False)
	match=re.compile(' href="([^"]*)" title="(.+?)">([^<]*)</a></li>').findall(link)
	for url2,name1,name2 in match:
		#ok=dialog.ok(name1,url)
		li=xbmcgui.ListItem(">"+name2)
		u=sys.argv[0]+'?mode=4&url='+urllib.quote_plus(url2)+'&name='+urllib.quote_plus("搜索Sohu >"+name+">"+name2.decode("gbk").encode("utf8"))
		xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)

def SearchSohuList(name,url):
	#dialog = xbmcgui.Dialog()
	#ok=dialog.ok(name,url)
	req = urllib2.Request("http://so.tv.sohu.com/"+url)
	req.add_header("User-Agent", "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Trident/4.0)")
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	#link=link.decode("gbk","ignore").encode("utf8")
	li=xbmcgui.ListItem("搜索Sohu >"+name)
	u=sys.argv[0]+"?mode=40&name="+urllib.quote_plus(name)
	xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,False)
	link=re.sub("\r|\n|\t","",link)
	match=re.compile('<a class="img" href="([^"]*)" title="(.+?)" target="_blank"><img src="(.+?)" alt="(.+?)" width="120">').findall(link)
	#ok=dialog.ok(name,"find "+str(len(match)))
	for url2,name1,img,name2 in match:
		#ok=dialog.ok(name1,url)
		li=xbmcgui.ListItem(">"+name2,name1,img,img)
		u='plugin://plugin.video.sohuvideo/'+'?mode=16&url=http://so.tv.sohu.com'+urllib.quote_plus(url2)+'&name='+urllib.quote_plus(name2)+"&director=&studio=&plot="
		xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)

def SearchQVod(url,name):
	#dialog = xbmcgui.Dialog()
	req = urllib2.Request("http://www.qvodzy.me/"+url)
	req.add_header("User-Agent", "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Trident/4.0)")
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	link=link.decode("gbk","ignore").encode("utf8")
	link=re.sub("\r|\n","",link)
	#如果是NAME里有“下一页”，则清除掉
	name=re.sub(">首页|>上一页|>下一页|>尾页","",name)
	#ok=dialog.ok(name,url)
	li=xbmcgui.ListItem(name)
	u=sys.argv[0]+"?mode=40&name="+urllib.quote_plus(name)
	xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,False)
	match=re.compile('<td height="20"><a href=(.+?) target="_blank">(.+?)</a></td>').findall(link)
	#ok=dialog.ok(name,"find "+str(len(match)))
	for i in range(0,len(match)):
		#ok=dialog.ok(name1,url)
		url=match[i][0]
		name1=match[i][1]
		li=xbmcgui.ListItem(str(i+1)+". "+name1)
		u='plugin://plugin.video.qvod/'+'?mode=13&url=/'+urllib.quote_plus(url.decode("utf8").encode("gbk"))+'&name='+urllib.quote_plus("搜索QVOD: ".decode("utf8").encode("gbk")+name.decode("utf8").encode("gbk"))+'&imgurl='
		xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)

def SearchPowerStream(name,url):
	dialog = xbmcgui.Dialog()
	#ok=dialog.ok(name,url)
	url=url.replace("&amp;","&")
	req=urllib2.Request(url)
	req.add_header("User-Agent","Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Trident/4.0)")
	response=urllib2.urlopen(req)
	link=response.read()
	response.close()
	link=re.sub("\r","",link)
	link=re.sub("\n","",link)
	link=re.sub("\t","",link)
	li=xbmcgui.ListItem(name)
	u=sys.argv[0]+"?mode=100&name="+urllib.quote_plus(name)
	xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,False)
	match=re.compile('<table width="173" height="250" border="0"(.+?)<a name="leaveword').findall(link)
	for i in range(0,len(match)):
		match1=re.compile('<span><font color="">(.+?)</font>').findall(match[i])
		name2=match1[0]
		match1=re.compile('<img src="([^"]*)" width="171" height="250').findall(match[i])
		img2=match1[0]
		li=xbmcgui.ListItem(str(i+1)+". "+name2,img2,img2)
		u=sys.argv[0]+"?mode=40&name="+urllib.quote_plus(name)+">"+"&url="
		#ok=dialog.ok(name,"here3")
		xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,False)
		match1=re.compile(' href="([^"]*)" class="red" target="_blank">(.+?)</a>').findall(match[i])
		for url2,name2 in match1:
			li=xbmcgui.ListItem("-->"+name2.decode("gb2312").encode("utf8"))
			u='plugin://plugin.video.powerstream/'+"?mode=7&name="+urllib.quote_plus(name)+">"+"&url="+urllib.quote_plus(url2)
			xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
		match1=re.compile('\[<a href="([^"]*)" (.+?)993300">(.+?)</font></a>').findall(match[i])
		for url2,temp,area in match1:
			li=xbmcgui.ListItem("-->"+area.decode("gb2312").encode("utf8"))
			u='plugin://plugin.video.powerstream/'+"?mode=7&name="+urllib.quote_plus(name)+">"+"&url="+urllib.quote_plus(url2)
			xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)

def SearchNetITV(name,url):
	dialog = xbmcgui.Dialog()
	if url.find("&p=")==-1:
		url=url+"&p=1&ps=12&cid=&s="+"s"+"&bit=0&exch=true&snew=1"
	req=urllib2.Request(url)
	req.add_header("User-Agent","Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Trident/4.0)")
	response=urllib2.urlopen(req)
	link=response.read()
	response.close()
	link=re.sub("\r|\n|\t","",link)
	match=re.compile('<div class="number">([^<]*)</div>').findall(link)
	if len(match)>0:
		sNum=match[0]
	else:
		sNum="(找到0条记录)"
	TotalNum=int(re.sub("\D","",sNum))
	addItem(sys.argv[0]+"?mode=100&name="+urllib.quote_plus("查询NetITV >"+name),name+sNum,"")
	match=re.compile('<input name="txt_movie_page" id="txt_movie_page" value="([^"]*)" readonly />').findall(link)
	if len(match)>0:
		current=int(match[0])
	else:
		current=1
	pages=int(TotalNum/12)
	if pages*12<TotalNum:
		pages=pages+1
	#ok=dialog.ok(name,str(pages))
	if current>1:
		url2=url+"&p="+str(current-1)+"&ps=12&cid=&s=s&bit=0&exch=true&snew=1"
		addDir(sys.argv[0]+"?mode=6&name="+urllib.quote_plus(name),">上一页","")
	if current<pages:
		url2=url+"&p="+str(current+1)+"&ps=12&cid=&s=s&bit=0&exch=true&snew=1"
		addDir(sys.argv[0]+"?mode=6&name="+urllib.quote_plus(name),">下一页","")
	match=re.compile('<a href="elivemovie://(.+?)/"  title="([^<]*)"   class="program-pic" ><img src="([^<]*)"  alt="([^<]*)"/></a>').findall(link)
	i=0
	for url2,title,img,t2 in match:
		i=i+1
		addDir('plugin://plugin.video.netitv/'+"?mode=5&name="+urllib.quote_plus(title)+"&url="+urllib.quote_plus(url2),title,img)
	
		
def addDir(u,li,img):
	l=xbmcgui.ListItem(li,img,img)
	xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,l,True)

def addItem(u,li,img):
	l=xbmcgui.ListItem(li,img,img)
	xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,l,False)

	
def Search(name,url):
	if name=='中文':
		kb=xbmc.Keyboard('','输入所查影片中文信息-拼音或简拼(拼音首字母)',False)
		kb.doModal()
		kw=kb.getText()
		url="http://www.google.com.hk/search?hl=zh-CN&source=hp&btnG=&aq=f&aqi=&aql=&oq=&gs_rfai=&num=1&q="+kw
		url=url.replace("&amp;","&")
		cookieprocessor = urllib2.HTTPCookieProcessor() 
		opener = urllib2.build_opener(SmartRedirectHandler, cookieprocessor)
		req=urllib2.Request(url)
		req.add_header("User-Agent","Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3")
		req.add_header("Referer","www.google.cn")
		urllib2.install_opener(opener) 
		response =urllib2.urlopen(req)
		link=response.read()
		response.close()
		link=re.sub("\r|\n|\t","",link)
		match=re.compile("class=spell><em>(.+?)</em>").findall(link)
		for i in range(0,len(match)/2):
			li=xbmcgui.ListItem(match[i])
			u=sys.argv[0]+"?mode=1&name="+urllib.quote_plus(match[i])+"&url="
			xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)		
	else:
		kb=xbmc.Keyboard('','输入所查影片英文信息(含数字)',False)
		kb.doModal()
		kw=kb.getText()
		li=xbmcgui.ListItem(kw)
		u=sys.argv[0]+"?mode=1&name="+urllib.quote_plus(kw)+"&url="
		xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)		



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
type=None


try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        type=urllib.unquote_plus(params["type"])
except:
        pass
try:
        mode=int(params["mode"])
except:
        pass



if mode==None or name==None:
	name=''
	Roots()
elif mode==0:
	Search(name,url)
elif mode==1:
	SearchSite(name,url)
elif mode==2:
	SearchQVod(url,name)
elif mode==3:
	SearchSohu(name,url)
elif mode==4:
	SearchSohuList(name,url)
elif mode==5:
	SearchPowerStream(name,url)
elif mode==6:
	SearchNetITV(name,url)
elif mode==7:
	SearchYouKu(name,url)

xbmcplugin.setPluginCategory(int(sys.argv[1]), name )
xbmcplugin.endOfDirectory(int(sys.argv[1]))

    
