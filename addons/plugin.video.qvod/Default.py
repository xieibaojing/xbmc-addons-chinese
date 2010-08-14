# -*- coding: utf-8 -*-
import httplib,urllib,urllib2,re,xbmcplugin,xbmcgui,xbmc,os,base64

#插件名称：快播 For TOM365 
#插件作者：Spy(十品鱼)
#插件类型：视频插件
#播 放 器：外置
#最后修改时间：2010-8-14

#这是本人的第一个XBMC插件，是参考R大的PPS、CCTV等插件学习的成果，下面的代码部分出自R大的插件，特此说明，并感谢R大的无私奉献精神。
#由于本人刚刚接触XBMC，以前也没学过PYTHON，插件如有问题，欢迎大家指正，但对因插件引起的后果，本人不承担责任，请使用者自行考虑风险是否使用本插件，谢谢。
#2010-6-10 增加了3G高清
#2010-6-8 增加QVOD资源站点
#2010-6-12 增加天天放映室 http://www.ttfdy.com/
#2010-8-14 修正QVOD资源站无法访问的问题，将站点地址更改为 http://www.qvodzy.com.cn/

#参考了以下插件：
#CCTV Video - by Robinttt 2009.
#PPS网络电视- by robinttt 2010.

def Roots():
	#列出网站清单
	#www.tom365.com
	name="Tom365"
	url="www.tom365.com"
	imgurl=os.getcwd()+'\\resources\\Default.jpg'
	addDir(name,url,1,imgurl)
	#QVOD资源站 http://www.qvodzy.me/
	name="QVOD资源站"
	url="www.qvodzy.com.cn"
	imgurl=os.getcwd()+'\\resources\\Default.jpg'
	addDir(name,url,11,imgurl)
	#3G高清http://www.720dy.com/
	name="3G高清"
	url="http://www.720dy.com/"
	imgurl=os.getcwd()+'\\resources\\Default.jpg'
	addDir(name,url,21,imgurl)
	#天天放映室http://www.ttfdy.com/
	name="天天放映室"
	url="http://www.ttfdy.com"
	imgurl=os.getcwd()+'\\resources\\Default.jpg'
	addDir(name,url,31,imgurl)
	

#======================== TOM365   Start ================
def GetType0(name):
	# mode 1 
	req=httplib.HTTPConnection("www.tom365.com")
	req.request("get", "/index.html")
	response=req.getresponse()
	link=response.read()
	response.close()
	#link=link.decode("gbk").encode("utf8")
	link=re.sub("\r|\n","",link)
	match=re.compile('<div id="nav">(.+?)</div>').findall(link)
	link=match[0]
	#跳掉首页
	link=link[10:]
	match=re.compile('<a href="(.+?)" target=_self>(.+?)</a>').findall(link)
	for url,name1 in match:
		addDir(name+">"+name1,url,2,os.getcwd()+'\\resources\\Default.jpg')

def GetList0(url,name):
	#mode 2
	req=httplib.HTTPConnection("www.tom365.com")
	req.request("get", "/"+url)
	response=req.getresponse()
	link=response.read()
	response.close()
	if isinstance(link, unicode):
		link=link.decode("gbk").encode("utf8")
	link=re.sub("\r|\n|\t","",link)
	#如果是NAME里有“下一页”，则清除掉
	#ls=name.find(">")
	#if (ls>=2):
	#	name=name[:ls]
	#print link
	name=re.sub(">首页|>上一页|>下一页|>尾页","",name)
	match=re.compile('<img border=0 height=119 src=(.+?) width=100 /></a><dl><dt><a href=(.+?) target=_blank>(.+?)</a></dt>').findall(link)
	for imgurl,url,name1 in match:
		url="movie_2004"+url[2:]
		addDir(name+">"+name1,url,3,imgurl)
	#显示上一页，下一页
	#links=link.find('pages')
	#linke=link.find('links')
	#link1=link[links:linke
	link1=re.compile('pages(.+?)links').search(link)
	if link1:
		link2=re.sub("\"","",link1.group(1))
		match=re.compile('<a href=(.+?) target=_self>(.+?)</a>').findall(link2)
		for url,name1 in match:
			addDir(name+">"+name1,"movie_2004/mlist/"+url,2,os.getcwd()+'\\resources\\Default.jpg')

def ShowMov0(url,name,imgurl):
	#mode 3
	req=httplib.HTTPConnection("www.tom365.com")
	req.request("get", "/"+url)
	response=req.getresponse()
	link=response.read()
	response.close()
	if isinstance(link, unicode):
		link=link.decode("gbk").encode("utf8")
	link=re.sub("\r","",link)
	link=re.sub("\n","",link)
	link=re.sub("\t","",link)
	link=re.sub('"_blank"','_blank',link)
	match=re.compile('p2p\.htm\?(.+?)" target=_blank>\[(.+?)\]</a>').findall(link)
	for url,name1 in match:
		jsname=url.split("?")
		# jsname[2]是JS的名字
		req=httplib.HTTPConnection("www.tom365.com")
		req.request("get", "/jsever/"+str(jsname[2])+".js?t=200.js")
		response=req.getresponse()
		link2=response.read()
		response.close()
		match=re.compile('QVOD="(.+?)"').findall(link2)
		serverip=match[0]
		addDir(name+">"+u"第".encode('utf8')+name1+u"集".encode('utf8'),serverip+jsname[0],10000,imgurl)
	#QVOD地址，直接获取
	match=re.compile('index/vod\.htm\?(.+?)" target=_blank>\[(.+?)\]</a>').findall(link)
	for url,name1 in match:
		addDir(name+"> "+u"备用第".encode('utf8')+name1+u"集".encode('utf8'),"qvod://"+url,10000,imgurl)
		#图片从上级得到，不再抓取
#=========== TOM365 End ===========

#======================== QVOD资源站   Start ================
def GetType1(name):
	# mode 1 
	req = urllib2.Request("http://www.qvodzy.com.cn")
	req.add_header("User-Agent", "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3")
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	link=link.decode("gbk","ignore").encode("utf8")
	link=re.sub("\r|\n","",link)
	match=re.compile('<a href="(.+?)" class="bai">(.+?)</a>').findall(link)
	if len(match)>0:
		#跳掉首页
		del match[0]
		for url,name1 in match:
			addDir(name+">"+name1,url,12,os.getcwd()+'\\resources\\Default.jpg')
	else:
		dialog = xbmcgui.Dialog()
		ok=dialog.ok(name, u'网站可能无法访问！请直接用浏览器访问'.encode('utf8'),'http://www.qvodzy.com.cn')


def GetList1(url,name):
	#mode 12
	req = urllib2.Request("http://www.qvodzy.com.cn/"+url)
	req.add_header("User-Agent", "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3")
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	link=link.decode("gbk","ignore").encode("utf8")
	link=re.sub("\r|\n","",link)
	#如果是NAME里有“下一页”，则清除掉
	name=re.sub(">首页|>上一页|>下一页|>尾页","",name)
	match=re.compile('<td height="20"><a href="(.+?)" target="_blank">(.+?)</a></td>').findall(link)
	for url,name1 in match:
		addDir(name+">"+name1,url,13)
	#显示上一页，下一页
	#match=re.compile('总共 <span class="STYLE1">(.+?)</span>').search(link)
	#print match.group()
	#总共 match.group(1) 部影片
	#name1=">总共 "+match.group(1)+" 部影片"
	#li=xbmcgui.ListItem(name+name1, iconImage="DefaultFolder.png", thumbnailImage="DefaultFolder.png")
	#li.setInfo( type="Video", infoLabels={ "Title": name1 } )
	#xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url="",listitem=li)
	match=re.compile('><td width="46%" align="center" colspan="2">(.+?)</td></tr>    </table></td>  </tr>').search(link)
	match2=re.compile('<a href="(.+?)">(.+?)</a>').findall(match.group(1))
	for url,name1 in match2:
		addDir(name+">"+name1,url,12)

def ShowMov1(url,name,imgurl):
	#mode 13
	req = urllib2.Request("http://www.qvodzy.com.cn"+url)
	req.add_header("User-Agent", "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3")
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	link=link.decode("gbk","ignore").encode("utf8")
	link=re.sub("\r|\n","",link)
	match=re.compile('valign="middle"><img src="(.+?)" width="250" height="350"').search(link)
	imgurl=match.group(1)
	match=re.compile('qvod://(.+?)</a>').findall(link)
	for url in match:
		name2=url.split(r"|")
		addDir(name2[2],"qvod://"+url,10000,imgurl)

#================= QVOD资源站 End ===========

#======================== 3G高清 www.720dy.com   Start ================
def GetType2(name,url):
	# mode 21 
	req = urllib2.Request(url)
	req.add_header("User-Agent", "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3")
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	link=re.sub("\r|\n|\"|\'","",link)
	#print link
	match=re.compile('(?i)<li class=>(.+?)</div>').search(link)
	if match:
		link=match.group(1)
		match=re.compile('<a href=(.+?)>(.+?)</a>').findall(link)
		for url,name1 in match:
			addDir(name+">"+name1,url,22,os.getcwd()+'\\resources\\Default.jpg')

def GetList2(url,name):
	#mode 22
	req = urllib2.Request("http://www.720dy.com"+url)
	req.add_header("User-Agent", "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3")
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	#link=link.decode("gbk","ignore").encode("utf8")
	link=re.sub("\r|\n","",link)
	#print link
	#如果是NAME里有“下一页”，则清除掉
	name=re.sub(">首页|>上一页|>下一页|>尾页","",name)
	match=re.compile('<li> <a href="(.+?)" target="_blank"> <img src="(.+?)" alt="(.+?)"').findall(link)
	for url,imgurl,name1 in match:
		addDir(name+">"+name1,url,23,'http://www.720dy.com'+imgurl)
	#显示上一页，下一页
	match=re.compile('<div class="page clear">(.+?)</div>').search(link)
	match2=re.compile('<a href="(.+?)" class="pagegbk">(.+?)</a>').findall(match.group(1))
	for url,name1 in match2:
		addDir(name+">"+name1,url,22)

def ShowMov2(url,name,imgurl):
	#mode 23
	req = urllib2.Request("http://www.720dy.com"+url)
	req.add_header("User-Agent", "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3")
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	link=re.sub("\r|\n","",link)
	match=re.compile('<div class="vpl">(.+?)</div>').search(link)
	if match:
		link=match.group(1)
		match=re.compile('<a href="(.+?)" target="_blank">(.+?)</a>').findall(link)
		for url,name2 in match:
			addDir(name+">"+name2,url,24,imgurl)
	else:
		dialog = xbmcgui.Dialog()
		ok=dialog.ok(name, u'没有发现播放地址！请直接用浏览器访问：'.encode('utf8'),'http://www.720dy.com'+url)
	
def ShowMov2_1(url,name,imgurl):
	#mode 24
	req = urllib2.Request("http://www.720dy.com"+url)
	req.add_header("User-Agent", "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3")
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	link=re.sub("\r|\n","",link)
	link=urllib.unquote(link)
	match=re.compile('var pp_url="(.+?)"').search(link)
	if match:
		movurl=match.group(1)
		match=re.compile('qvod://(.+?)$').search(movurl)
		url=match.group(1)
		addDir("播放："+name,"qvod://"+url,10000,imgurl)
	else:
		dialog = xbmcgui.Dialog()
		ok=dialog.ok(name, u'没有发现播放地址！请直接用浏览器访问：'.encode('utf8'),'http://www.720dy.com'+url)
	

#================= 3G高清 www.720dy.com End ===========

#======================== 天天放映室 http://www.ttfdy.com Start ================
def GetType3(name,url):
	# mode 31 
	req = urllib2.Request(url)
	req.add_header("User-Agent", "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3")
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	link=link.decode("gbk").encode("utf8")
	link=re.sub("\r|\n|\"","",link)
	match=re.compile('pptv_menuLink c_b(.+?)class=pptv_ico>').search(link)
	if match:
		link1=match.group(1)
		match=re.compile('(?i)<a href=(.+?)><STRONG>(.+?)</STRONG></A>').findall(link1)
		if len(match)>0:
			for url,name1 in match:
				url=re.sub("\.\.","",url)
				ls=url.find("title")
				if ls>0:
					url=url[:ls]
				addDir(name+">"+name1,url,32,os.getcwd()+'\\resources\\Default.jpg')
		else:
			dialog = xbmcgui.Dialog()
			ok=dialog.ok(name, u'网站可能无法访问！请直接用浏览器访问'.encode('utf8'),url)
	else:
		dialog = xbmcgui.Dialog()
		ok=dialog.ok(name, u'网站可能无法访问！请直接用浏览器访问'.encode('utf8'),url)

def GetList3(url,name):
	#mode 32
	req = urllib2.Request(url)
	req.add_header("User-Agent", "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3")
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	link=link.decode("gbk").encode("utf8")
	link=re.sub("\r|\n|\t|\"|\'","",link)
	link=re.sub("/>",">",link)
	#如果是NAME里有“下一页”，则清除掉
	name=re.sub(">首页|>上一页|>下一页|>尾页","",name)
	match=re.compile('(?i)class=movie_li_1 c_b(.+?)class=page_num>').search(link)
	if match:
		link1=match.group(1)
		match=re.compile('(?i)<dt><a href=(.+?) target=(.+?)title=(.+?)><img src=(.+?) >').findall(link1)
		for url,ls,name1,imgurl in match:
			addDir(name+">"+name1,url,33,imgurl)
		#显示上一页，下一页
		print link
		match=re.compile('(?i)<DIV class=page_num>(.+?)</DIV><DIV class=movie_li_1 c_b>').search(link)
		if match:
			match1=match.group(1)
			match1=re.sub("<span(.+?)/span","",match1)
			match2=re.compile('(?i)a href=(.+?)title=(.+?)class=PageBox>').findall(match1)
			for url,name1 in match2:
				addDir(name+">"+name1,url,32)

def ShowMov3(url,name,imgurl):
	#mode 33
	req = urllib2.Request(url)
	req.add_header("User-Agent", "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3")
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	link=link.decode("gbk").encode("utf8")
	link=re.sub("\r|\n|\"","",link)
	match=re.compile('/qplayer.html?(.+?) target=_blank>(.+?)</a>').findall(link)
	if len(match)>0:
		for url,name1 in match:
			url=urllib.unquote(url)
			url1=eval("u'"+url.replace("%","\\")+"'")
			url=url1.split(r"?")
			addDir(url[2]+url[3],url[4],10000,imgurl)
	else:
		dialog = xbmcgui.Dialog()
		ok=dialog.ok(u"未能找到Qvod地址！".encode('utf8'),u"该网站有的电影只提供的了GVOD地址。".encode('utf8'))
	
#================= 天天放映室 http://www.ttfdy.com End ===========

#========== 公共函数区 开始 ==============
def QvodPlay(url):
	#mode 10000
	if (os.name == 'nt'):
		xbmc.executebuiltin('System.ExecWait(\\"'+ os.getcwd()+'\\resources\\player\\qvod4xbmc\\" '+url+')')
	else:
		xbmc.executebuiltin('System.ExecWait(\\"'+ os.getcwd()+'\\resources\\player\\qvod4xbmc\\" '+url+')')

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

def addDir(name,url,mode,iconimage=os.getcwd()+'\\resources\\Default.jpg'):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setInfo( type="Video", infoLabels={ "Title": name } )
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
	return ok

#========== 公共函数区 结束 ==============

#========== 主程序 开始 ===============
params=get_params()
url=None
name=None
mode=None
iconimage=None
burl=None
isdebug=True
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
	iconimage=urllib.unquote_plus(params["iconimage"])
except:
	pass
if isdebug:
	print "Mode: "+str(mode)
	print "URL: "+str(url)
	print "Name: "+str(name)
	print "iconimage: "+str(iconimage)
if mode==None:
	Roots()
elif mode==1:
	#===TOM365
	GetType0(name)
elif mode==2:
	GetList0(url,name)
elif mode==3:
	ShowMov0(url,name,iconimage)
elif mode==11:
	#==QVOD资源站
	GetType1(name)
elif mode==12:
	GetList1(url,name)
elif mode==13:
	ShowMov1(url,name,iconimage)
elif mode==21:
	#==3G高清 www.720dy.com
	GetType2(name,url)
elif mode==22:
	GetList2(url,name)
elif mode==23:
	ShowMov2(url,name,iconimage)
elif mode==24:
	ShowMov2_1(url,name,iconimage)
elif mode==31:
	#== 天天放映室 http://www.ttfdy.com/
	GetType3(name,url)
elif mode==32:
	GetList3('http://www.ttfdy.com'+url,name)
elif mode==33:
	ShowMov3('http://www.ttfdy.com'+url,name,iconimage)
elif mode==34:
	ShowMov3_1('http://www.ttfdy.com'+url,name,iconimage)

elif mode==10000:
	QvodPlay(url)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
#========= 主程序 结束 =========