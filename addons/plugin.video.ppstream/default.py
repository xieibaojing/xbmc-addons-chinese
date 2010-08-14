# -*- coding: utf-8 -*-
import xbmc,xbmcgui,xbmcplugin,urllib2,urllib,re,sys,os

#PPS网络电视- by robinttt 2010.

def Roots():
	li=xbmcgui.ListItem("PPS看看")
	u=sys.argv[0]+"?mode=1&name="+urllib.quote_plus("PPS看看")
	xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
	li=xbmcgui.ListItem("影视百科")
	u=sys.argv[0]+"?mode=16&name="+urllib.quote_plus("影视百科")
	xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)

def Kankan(name):
	li=xbmcgui.ListItem(name+">分类")
	u=sys.argv[0]+"?mode=2&name="+urllib.quote_plus(name+">分类")
	xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
	li=xbmcgui.ListItem(name+">地区")
	u=sys.argv[0]+"?mode=5&name="+urllib.quote_plus(name+">地区")
	xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
	li=xbmcgui.ListItem(name+">年份")
	u=sys.argv[0]+"?mode=8&name="+urllib.quote_plus(name+">年份")
	xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
	li=xbmcgui.ListItem(name+">明星")
	u=sys.argv[0]+"?mode=9&name="+urllib.quote_plus(name+">明星")
	xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
	li=xbmcgui.ListItem(name+">综合")
	u=sys.argv[0]+"?mode=11&name="+urllib.quote_plus(name+">综合")
	xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)

def KankanA(name):
	li=xbmcgui.ListItem(name+">电影")
	u=sys.argv[0]+"?mode=3&name="+urllib.quote_plus(name+">电影")+"&url="+urllib.quote_plus("http://kan.pps.tv/movie_index.html")
	xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
	li=xbmcgui.ListItem(name+">电视")
	u=sys.argv[0]+"?mode=3&name="+urllib.quote_plus(name+">电视")+"&url="+urllib.quote_plus("http://kan.pps.tv/tv_index.html")
	xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
	li=xbmcgui.ListItem(name+">动漫")
	u=sys.argv[0]+"?mode=3&name="+urllib.quote_plus(name+">动漫")+"&url="+urllib.quote_plus("http://kan.pps.tv/anime_index.html")
	xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
	li=xbmcgui.ListItem(name+">综艺")
	u=sys.argv[0]+"?mode=3&name="+urllib.quote_plus(name+">综艺")+"&url="+urllib.quote_plus("http://kan.pps.tv/arts_index.html")
	xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)

def KankanA0(name,url):
        req = urllib2.Request(url)
        req.add_header("User-Agent", "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3")
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        link=re.sub("\r","",link)
        link=re.sub("\n","",link)
        link=re.sub("\t","",link)
        match=re.compile("<dt>"+u"按类型".encode("gbk")+"</dt>(.+?)</dd>").findall(link)
        match0=re.compile('href="/nlist/(.+?)/1.html">(.+?)</a>').findall(match[0])
        for url1,name1 in match0:
	        li=xbmcgui.ListItem(name+">"+name1.decode("gbk").encode("utf8"))
	        u=sys.argv[0]+"?mode=4&name="+urllib.quote_plus(name+">"+name1.decode("gbk").encode("utf8"))+"&url="+urllib.quote_plus(url1)
	        xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)

def KankanA1(name,url):
	li=xbmcgui.ListItem(name+">最新更新")
	u=sys.argv[0]+"?mode=13&name="+urllib.quote_plus(name+">最新更新")+"&url="+urllib.quote_plus("http://kan.pps.tv/nlist/"+url+"/1.html")
	xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
	li=xbmcgui.ListItem(name+">播放最多")
	u=sys.argv[0]+"?mode=13&name="+urllib.quote_plus(name+">播放最多")+"&url="+urllib.quote_plus("http://kan.pps.tv/nlist_v5_play_num/"+url+"/1.html")
	xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)

def KankanB(name):
	li=xbmcgui.ListItem(name+">欧美")
	u=sys.argv[0]+"?mode=6&name="+urllib.quote_plus(name+">欧美")
	xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
	li=xbmcgui.ListItem(name+">日韩")
	u=sys.argv[0]+"?mode=6&name="+urllib.quote_plus(name+">日韩")
	xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
	li=xbmcgui.ListItem(name+">中国")
	u=sys.argv[0]+"?mode=6&name="+urllib.quote_plus(name+">中国")
	xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
	li=xbmcgui.ListItem(name+">港台")
	u=sys.argv[0]+"?mode=6&name="+urllib.quote_plus(name+">港台")
	xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)

def KankanB0(name):
        if name=="PPS看看>地区>欧美":
        	li=xbmcgui.ListItem(name+">欧美电影")
        	u=sys.argv[0]+"?mode=7&name="+urllib.quote_plus(name+">欧美电影")+"&url="+urllib.quote_plus("movie_bk_europe")
        	xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
		li=xbmcgui.ListItem(name+">美国电影")
		u=sys.argv[0]+"?mode=14&name="+urllib.quote_plus(name+">美国电影")+"&url="+urllib.quote_plus("http://kan.pps.tv/movie_region/%C3%C0%B9%FA_1.html")
		xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)        
		li=xbmcgui.ListItem(name+">法国电影")
		u=sys.argv[0]+"?mode=14&name="+urllib.quote_plus(name+">法国电影")+"&url="+urllib.quote_plus("http://kan.pps.tv/movie_region/%B7%A8%B9%FA_1.html")
		xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True) 
		li=xbmcgui.ListItem(name+">英国电影")
		u=sys.argv[0]+"?mode=14&name="+urllib.quote_plus(name+">英国电影")+"&url="+urllib.quote_plus("http://kan.pps.tv/movie_region/%D3%A2%B9%FA_1.html")
		xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)   
		li=xbmcgui.ListItem(name+">德国电影")
		u=sys.argv[0]+"?mode=14&name="+urllib.quote_plus(name+">德国电影")+"&url="+urllib.quote_plus("http://kan.pps.tv/movie_region/%B5%C2%B9%FA_1.html")
		xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True) 
        	li=xbmcgui.ListItem(name+">欧美电视")
        	u=sys.argv[0]+"?mode=7&name="+urllib.quote_plus(name+">欧美电视")+"&url="+urllib.quote_plus("tv_bk_europe")
        	xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
        	li=xbmcgui.ListItem(name+">欧美动漫")
        	u=sys.argv[0]+"?mode=7&name="+urllib.quote_plus(name+">欧美动漫")+"&url="+urllib.quote_plus("anime_bk_europe")
        	xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
        	li=xbmcgui.ListItem(name+">欧美综艺")
        	u=sys.argv[0]+"?mode=7&name="+urllib.quote_plus(name+">欧美综艺")+"&url="+urllib.quote_plus("arts_bk_europe")
        	xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
        elif name=="PPS看看>地区>日韩":
        	li=xbmcgui.ListItem(name+">日韩电影")
        	u=sys.argv[0]+"?mode=7&name="+urllib.quote_plus(name+">日韩电影")+"&url="+urllib.quote_plus("movie_bk_japan")
        	xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
		li=xbmcgui.ListItem(name+">日本电影")
		u=sys.argv[0]+"?mode=14&name="+urllib.quote_plus(name+">日本电影")+"&url="+urllib.quote_plus("http://kan.pps.tv/movie_region/%C8%D5%B1%BE_1.html")
		xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)        
		li=xbmcgui.ListItem(name+">韩国电影")
		u=sys.argv[0]+"?mode=14&name="+urllib.quote_plus(name+">韩国电影")+"&url="+urllib.quote_plus("http://kan.pps.tv/movie_region/%BA%AB%B9%FA_1.html")
		xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)    
        	li=xbmcgui.ListItem(name+">日韩电视")
        	u=sys.argv[0]+"?mode=7&name="+urllib.quote_plus(name+">日韩电视")+"&url="+urllib.quote_plus("tv_bk_japan")
        	xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
        	li=xbmcgui.ListItem(name+">日韩动漫")
        	u=sys.argv[0]+"?mode=7&name="+urllib.quote_plus(name+">日韩动漫")+"&url="+urllib.quote_plus("anime_bk_japan")
        	xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
        	li=xbmcgui.ListItem(name+">日韩综艺")
        	u=sys.argv[0]+"?mode=7&name="+urllib.quote_plus(name+">日韩综艺")+"&url="+urllib.quote_plus("arts_bk_japan")
        	xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
        elif name=="PPS看看>地区>中国":
        	li=xbmcgui.ListItem(name+">中国电影")
        	u=sys.argv[0]+"?mode=7&name="+urllib.quote_plus(name+">中国电影")+"&url="+urllib.quote_plus("movie_bk_mainland")
        	xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
        	li=xbmcgui.ListItem(name+">中国电视")
        	u=sys.argv[0]+"?mode=7&name="+urllib.quote_plus(name+">中国电视")+"&url="+urllib.quote_plus("tv_bk_mainland")
        	xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
        	li=xbmcgui.ListItem(name+">中国动漫")
        	u=sys.argv[0]+"?mode=7&name="+urllib.quote_plus(name+">中国动漫")+"&url="+urllib.quote_plus("anime_bk_mainland")
        	xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
        	li=xbmcgui.ListItem(name+">中国综艺")
        	u=sys.argv[0]+"?mode=7&name="+urllib.quote_plus(name+">中国综艺")+"&url="+urllib.quote_plus("arts_bk_mainland")
        	xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
        elif name=="PPS看看>地区>港台":
  		li=xbmcgui.ListItem(name+">香港电影")
		u=sys.argv[0]+"?mode=6&name="+urllib.quote_plus(name+">香港电影")+"&url="+urllib.quote_plus("http://kan.pps.tv/movie_region/%CF%E3%B8%DB_1.html")
		xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)        
		li=xbmcgui.ListItem(name+">台湾电影")
		u=sys.argv[0]+"?mode=6&name="+urllib.quote_plus(name+">台湾电影")+"&url="+urllib.quote_plus("http://kan.pps.tv/movie_region/%CC%A8%CD%E5_1.html")
		xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True) 
        	li=xbmcgui.ListItem(name+">港台电影")
        	u=sys.argv[0]+"?mode=7&name="+urllib.quote_plus(name+">港台电影")+"&url="+urllib.quote_plus("movie_bk_hongkong")
        	xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
        	li=xbmcgui.ListItem(name+">港台电视")
        	u=sys.argv[0]+"?mode=7&name="+urllib.quote_plus(name+">港台电视")+"&url="+urllib.quote_plus("tv_bk_hongkong")
        	xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)

def KankanB1(name,url):
	li=xbmcgui.ListItem(name+">最新更新")
	u=sys.argv[0]+"?mode=13&name="+urllib.quote_plus(name+">最新更新")+"&url="+urllib.quote_plus("http://kan.pps.tv/"+url+"_new_1.html")
	xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
	li=xbmcgui.ListItem(name+">播放最多")
	u=sys.argv[0]+"?mode=13&name="+urllib.quote_plus(name+">播放最多")+"&url="+urllib.quote_plus("http://kan.pps.tv/"+url+"_play_num_1.html")
	xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
	li=xbmcgui.ListItem(name+">评分最高")
	u=sys.argv[0]+"?mode=13&name="+urllib.quote_plus(name+">评分最高")+"&url="+urllib.quote_plus("http://kan.pps.tv/"+url.replace("_bk","")+"_paihan_1.html")
	xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)

def KankanC(name):
        for i in range(1998,2010):
	        li=xbmcgui.ListItem(name+">"+str(i))
	        u=sys.argv[0]+"?mode=14&name="+urllib.quote_plus(name+">"+str(i))+"&url="+urllib.quote_plus("http://kan.pps.tv/movie_year/"+str(i)+"_1.html")
	        xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)

def KankanD(name):
	li=xbmcgui.ListItem(name+">热门")
	u=sys.argv[0]+"?mode=10&name="+urllib.quote_plus(name+">热门")+"&url="+urllib.quote_plus("http://kan.pps.tv/people_index.html")
	xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
        for i in range(65,91):
	        li=xbmcgui.ListItem(name+">"+chr(i))
	        u=sys.argv[0]+"?mode=10&name="+urllib.quote_plus(name+">"+chr(i))+"&url="+urllib.quote_plus("http://kan.pps.tv/star_list/"+chr(i).lower()+"-1.html")
	        xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
	li=xbmcgui.ListItem(name+">其他")
	u=sys.argv[0]+"?mode=10&name="+urllib.quote_plus(name+">其他")+"&url="+urllib.quote_plus("http://kan.pps.tv/star_list/*-1.html")
	xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)

def KankanD0(name,url):
        req = urllib2.Request(url)
        req.add_header("User-Agent", "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3")
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        link=re.sub("\r","",link)
        link=re.sub("\n","",link)
        link=re.sub("\t","",link)
        matchp=re.compile('<div class="pageNav">(.+?)</div>').findall(link)
        matchp1=re.compile('<span>(.+?)</span>').findall(matchp[0])
	li=xbmcgui.ListItem(name+" "+matchp1[0].decode("gbk").encode("utf8"))
	u=sys.argv[0]+"?mode=40&name="+urllib.quote_plus(name)
	xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li)        
        match=re.compile('<div class="pltr">(.+?)<img src="(.+?)"(.+?)<span>(.+?)</span><a  href="(.+?)" >(.+?)</a></dt>').findall(link)
        for i in range(0,len(match)):
	        li=xbmcgui.ListItem(str(i+1)+"."+match[i][5].decode("gbk").encode("utf8")+"  ("+match[i][3].decode("gbk").encode("utf8")+")",match[i][1].replace(" ","%20"),match[i][1].replace(" ","%20"))
	        u=sys.argv[0]+"?mode=13&name="+urllib.quote_plus(match[i][5].decode("gbk").encode("utf8")+"的相关视频")+"&url="+urllib.quote_plus(match[i][4])
	        xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
        matchp2=re.compile('href="(.+?)">(.+?)</a>').findall(matchp[0].replace(" ","").replace("&lt;&lt;","").replace("&gt;&gt;",""))
        for url1,name1 in matchp2:
                if name1.find(u"页".encode("gbk"))==-1: name1="第"+name1.decode("gbk").encode("utf8")+"页"
	        li=xbmcgui.ListItem(".."+name1)
	        u=sys.argv[0]+"?mode=10&name="+urllib.quote_plus(name)+"&url="+urllib.quote_plus("http://kan.pps.tv"+url1)
	        xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)

def KankanE(name):
        req = urllib2.Request("http://kan.pps.tv/movie_index.html")
        req.add_header("User-Agent", "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3")
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        link=re.sub("\r","",link)
        link=re.sub("\n","",link)
        link=re.sub("\t","",link)
        match=re.compile('href="/olist/(.+?)/1.html">(.+?)</a></li>').findall(link)
        for url1,name1 in match:
	        li=xbmcgui.ListItem(name+">"+name1.decode("gbk").encode("utf8"))
	        u=sys.argv[0]+"?mode=12&name="+urllib.quote_plus(name+">"+name1.decode("gbk").encode("utf8"))+"&url="+urllib.quote_plus(url1)
	        xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)

def KankanE0(name,url):
	li=xbmcgui.ListItem(name+">最新更新")
	u=sys.argv[0]+"?mode=13&name="+urllib.quote_plus(name+">最新更新")+"&url="+urllib.quote_plus("http://kan.pps.tv/olist/"+url+"/1.html")
	xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
	li=xbmcgui.ListItem(name+">播放最多")
	u=sys.argv[0]+"?mode=13&name="+urllib.quote_plus(name+">播放最多")+"&url="+urllib.quote_plus("http://kan.pps.tv/olist_v5_play_num/"+url+"/1.html")
	xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)


def KankanList0(name,url):
        req = urllib2.Request(url)
        req.add_header("User-Agent", "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3")
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        link=re.sub('\s','',link)
        matchp=re.compile('<divclass="pageNav">(.+?)</div>').findall(link)
        matchp1=re.compile('<span>(.+?)</span>').findall(matchp[0])
	li=xbmcgui.ListItem(name+" "+matchp1[0].decode("gbk").encode("utf8"))
	u=sys.argv[0]+"?mode=40&name="+urllib.quote_plus(name)
	xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li)        

        match=re.compile('<divclass="pltr"><divclass="img"><ahref="(.+?)"target="_blank"><imgsrc="(.+?)"alt="(.+?)"/></a></div><dlclass="tr"><dt><span>(.+?)</span>').findall(link)
        for i in range(0,len(match)):
                img=match[i][1][0:len(match[i][1])-12]+"%20"+match[i][1][len(match[i][1])-12:len(match[i][1])]
		li=xbmcgui.ListItem(str(i+1)+"."+match[i][2].decode("gbk").encode("utf8")+"  ("+match[i][3].decode("gbk").encode("utf8")+")",img,img)
		u=sys.argv[0]+"?mode=15&name="+urllib.quote_plus(match[i][2].decode("gbk").encode("utf8"))+"&url="+urllib.quote_plus("http://kan.pps.tv"+match[i][0])
		xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)     

        matchp2=re.compile('href="(.+?)">(.+?)</a>').findall(matchp[0].replace(" ","").replace("&lt;&lt;","").replace("&gt;&gt;",""))
        for url1,name1 in matchp2:
                if name1.find(u"页".encode("gbk"))==-1: name1="第"+name1.decode("gbk").encode("utf8")+"页"
	        li=xbmcgui.ListItem(".."+name1)
	        u=sys.argv[0]+"?mode=13&name="+urllib.quote_plus(name)+"&url="+urllib.quote_plus(url1)
	        xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)


def KankanList1(name,url):
        req = urllib2.Request(url)
        req.add_header("User-Agent", "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3")
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        link=re.sub("\r","",link)
        link=re.sub("\n","",link)
        link=re.sub("\t","",link)
        matchp=re.compile('<div class="pageNav">(.+?)</div>').findall(link)
        matchp1=re.compile('<span>(.+?)</span>').findall(matchp[0])
	li=xbmcgui.ListItem(name+" "+matchp1[0].decode("gbk").encode("utf8"))
	u=sys.argv[0]+"?mode=40&name="+urllib.quote_plus(name)
	xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li)        
        match=re.compile('<div class="pltr">(.+?)<img src="(.+?)"(.+?)<span>(.+?)</span><a href="(.+?)" target="_blank">(.+?)</a></dt>').findall(link)
        for i in range(0,len(match)):
	        li=xbmcgui.ListItem(str(i+1)+"."+match[i][5].decode("gbk").encode("utf8")+"  ("+match[i][3].decode("gbk").encode("utf8")+")",match[i][1].replace(" ","%20"),match[i][1].replace(" ","%20"))
	        u=sys.argv[0]+"?mode=15&name="+urllib.quote_plus(match[i][5].decode("gbk").encode("utf8"))+"&url="+urllib.quote_plus("http://kan.pps.tv"+match[i][4])
	        xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
        matchp2=re.compile('href="(.+?)">(.+?)</a>').findall(matchp[0].replace(" ","").replace("&lt;&lt;","").replace("&gt;&gt;",""))
        for url1,name1 in matchp2:
                if name1.find(u"页".encode("gbk"))==-1: name1="第"+name1.decode("gbk").encode("utf8")+"页"
	        li=xbmcgui.ListItem(".."+name1)
	        u=sys.argv[0]+"?mode=14&name="+urllib.quote_plus(name)+"&url="+urllib.quote_plus(url1)
	        xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)

def KankanList2(name,url):
        if url.find("http://kan.pps.tv/play_list_v5_")==-1:
                req = urllib2.Request(url)
                req.add_header("User-Agent", "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3")
                response = urllib2.urlopen(req)
                link=response.read()
                response.close()
                link=re.sub("\r","",link)
                link=re.sub("\n","",link)
                link=re.sub("\t","",link)
                if link.find('<iframe src="http://kan.pps.tv/play_list_v5_')==-1:
	                li=xbmcgui.ListItem("当前视频："+name)
	                u=sys.argv[0]+"?mode=40&name="+urllib.quote_plus(name)
	                xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li)  
                        match=re.compile("plist\[(.+?)\]\='(.+?)\|\|\|(.+?)\|\|\|(.+?)';").findall(link)
                        for i in range(0,len(match)):
	                        li=xbmcgui.ListItem(str(i+1)+"."+match[i][1].decode("gbk").encode("utf8"))
	                        u=sys.argv[0]+"?mode=23&name="+urllib.quote_plus(name)+"&url="+urllib.quote_plus(match[i][2])
	                        xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li)
                else:
	                li=xbmcgui.ListItem("当前视频："+name+" 第1页")
	                u=sys.argv[0]+"?mode=40&name="+urllib.quote_plus(name)
	                xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li)  
                        match=re.compile("http://kan.pps.tv/play/(.+?).html").findall(url)
                        url1=match[0].split("_")[1]
                        req = urllib2.Request("http://kan.pps.tv/play_list_v5_"+url1+"/1.html")
                        req.add_header("User-Agent", "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3")
                        response = urllib2.urlopen(req)
                        link=response.read()
                        response.close()
                        link=re.sub("\r","",link)
                        link=re.sub("\n","",link)
                        link=re.sub("\t","",link)
                        link=re.sub(" ","",link)
                        match=re.compile('<liid="li(.+?)class="mc">(.+?)</a><ahref="(.+?)"').findall(link)
                        for i in range(0,len(match)):
	                        li=xbmcgui.ListItem(str(i+1)+"."+match[i][1].decode("gbk").encode("utf8"))
	                        u=sys.argv[0]+"?mode=23&name="+urllib.quote_plus(name)+"&url="+urllib.quote_plus(match[i][2])
	                        xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li)
                        matchp=re.compile('<divclass="pageNav">(.+?)</div>').findall(link)
                        matchp0=re.compile('href="(.+?)">(.+?)</a>').findall(matchp[0])
                        for url1,name1 in matchp0:
	                        li=xbmcgui.ListItem("..第"+name1.decode("gbk").encode("utf8")+"页")
	                        u=sys.argv[0]+"?mode=15&name="+urllib.quote_plus(name)+"&url="+urllib.quote_plus(url1)
	                        xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
        else:
                req = urllib2.Request(url)
                req.add_header("User-Agent", "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3")
                response = urllib2.urlopen(req)
                link=response.read()
                response.close()
                link=re.sub("\r","",link)
                link=re.sub("\n","",link)
                link=re.sub("\t","",link)
                link=re.sub(" ","",link)
                matchp=re.compile('<divclass="pageNav">(.+?)</div>').findall(link)
                matchp0=re.compile('<spanclass="cur">(.+?)</span>').findall(matchp[0])
	        li=xbmcgui.ListItem("当前视频："+name+" 第"+matchp0[0].decode("gbk").encode("utf8")+"页")
	        u=sys.argv[0]+"?mode=40&name="+urllib.quote_plus(name)
	        xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li)  
                match=re.compile('<liid="li(.+?)class="mc">(.+?)</a><ahref="(.+?)"').findall(link)
                for i in range(0,len(match)):
	                li=xbmcgui.ListItem(str(i+1)+"."+match[i][1].decode("gbk").encode("utf8"))
	                u=sys.argv[0]+"?mode=23&name="+urllib.quote_plus(name)+"&url="+urllib.quote_plus(match[i][2])
	                xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li)
                matchp0=re.compile('href="(.+?)">(.+?)</a>').findall(matchp[0])
                for url1,name1 in matchp0:
	                li=xbmcgui.ListItem("..第"+name1.decode("gbk").encode("utf8")+"页")
	                u=sys.argv[0]+"?mode=15&name="+urllib.quote_plus(name)+"&url="+urllib.quote_plus(url1)
	                xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)


def Baike(name):
	li=xbmcgui.ListItem(name+">电影")
	u=sys.argv[0]+"?mode=17&name="+urllib.quote_plus(name+">电影")+"&url="+urllib.quote_plus("http://bk.pps.tv/navi_cate/2.html")
	xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
	li=xbmcgui.ListItem(name+">电视")
	u=sys.argv[0]+"?mode=17&name="+urllib.quote_plus(name+">电视")+"&url="+urllib.quote_plus("http://bk.pps.tv/navi_cate/61.html")
	xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
	li=xbmcgui.ListItem(name+">动漫")
	u=sys.argv[0]+"?mode=17&name="+urllib.quote_plus(name+">动漫")+"&url="+urllib.quote_plus("http://bk.pps.tv/navi_cate/110.html")
	xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
	li=xbmcgui.ListItem(name+">综艺")
	u=sys.argv[0]+"?mode=17&name="+urllib.quote_plus(name+">综艺")+"&url="+urllib.quote_plus("http://bk.pps.tv/navi_cate/109.html")
	xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
	li=xbmcgui.ListItem(name+">人物")
	u=sys.argv[0]+"?mode=17&name="+urllib.quote_plus(name+">人物")+"&url="+urllib.quote_plus("http://bk.pps.tv/navi_cate/1.html")
	xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)

def BaikeA(name,url):
        req = urllib2.Request(url)
        req.add_header("User-Agent", "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3")
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        link=re.sub("\r","",link)
        link=re.sub("\n","",link)
        link=re.sub("\t","",link)
        link=re.sub(" ","",link)
        match=re.compile('<h1id="element(.+?)">'+u'按'.encode('gbk')+'(.+?)'+u'查询'.encode('gbk')+'</h1>').findall(link)
        for i in range(0,len(match)):
	        li=xbmcgui.ListItem(name+">"+match[i][1].decode("gbk").encode("utf8"))
	        u=sys.argv[0]+"?mode=18&name="+urllib.quote_plus(name+">"+match[i][1].decode("gbk").encode("utf8"))+"&url="+urllib.quote_plus(url)+"&type="+urllib.quote_plus('<h1id="element'+match[i][0]+'">'+u'按'.encode('gbk')+match[i][1]+u'查询'.encode('gbk')+'</h1>')
	        xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)

def BaikeB(name,url,type):
        req = urllib2.Request(url)
        req.add_header("User-Agent", "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3")
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        link=re.sub("\r","",link)
        link=re.sub("\n","",link)
        link=re.sub("\t","",link)
        link=re.sub(" ","",link)
        match=re.compile(type+'(.+?)</div>').findall(link)
        match0=re.compile('href="http://bk.pps.tv/class(.+?)">(.+?)</a>').findall(match[0])
        for url1,name1 in match0:
	        li=xbmcgui.ListItem(name+">"+name1.decode("gbk").encode("utf8"))
	        u=sys.argv[0]+"?mode=19&name="+urllib.quote_plus(name+">"+name1.decode("gbk").encode("utf8"))+"&url="+urllib.quote_plus(url1)
	        xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)

def BaikeC(name,url):
	li=xbmcgui.ListItem(name+">按评分")
	u=sys.argv[0]+"?mode=20&name="+urllib.quote_plus(name+">按评分")+"&url="+urllib.quote_plus("http://bk.pps.tv/class"+url)
	xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
	li=xbmcgui.ListItem(name+">按更新")
	u=sys.argv[0]+"?mode=20&name="+urllib.quote_plus(name+">按更新")+"&url="+urllib.quote_plus("http://bk.pps.tv/update"+url)
	xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)

def BaikeD(name,url):
        req = urllib2.Request(url)
        req.add_header("User-Agent", "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3")
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        link=re.sub("\r","",link)
        link=re.sub("\n","",link)
        link=re.sub("\t","",link)

        matchp=re.compile('<div class="pagenav(.+?)</div>').findall(link)
        matchp0=re.compile('<span class="on">(.+?)</span>').findall(matchp[0])
        if len(matchp0)>0:
		li=xbmcgui.ListItem("当前位置："+name+"  第"+matchp0[0].decode("gbk").encode("utf8")+"页")
		u=sys.argv[0]+"?mode=40&name="+urllib.quote_plus(name)
		xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li)
        else:
		li=xbmcgui.ListItem("当前位置："+name+"  第1页")
		u=sys.argv[0]+"?mode=40&name="+urllib.quote_plus(name)
		xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li)

        match=re.compile('<dt><span style="float:right;" title="(.+?)"(.+?)href="(.+?)"(.+?)</a>(.+?)src="(.+?)"').findall(link)
        for i in range(0,len(match)):
                li=xbmcgui.ListItem(str(i+1)+"."+re.sub(' title(.+?)>',"",match[i][3]).decode("gbk").encode("utf8")+"  ("+match[i][0].decode("gbk").encode("utf8")+"分)",match[i][5].replace(" ","%20"),match[i][5].replace(" ","%20"))
	        u=sys.argv[0]+"?mode=21&name="+urllib.quote_plus(name)+"&url="+urllib.quote_plus(match[i][2])
	        xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)

        matchp0=re.compile('href="(.+?)">(.+?)</a>').findall(matchp[0].replace(" ","").replace("&lt;&lt;","").replace("&gt;&gt;",""))
        for url1,name1 in matchp0:
                if name1.find(u"页".encode("gbk"))==-1: name1="第"+name1.decode("gbk").encode("utf8")+"页"
	        li=xbmcgui.ListItem(".."+name1)
	        u=sys.argv[0]+"?mode=20&name="+urllib.quote_plus(name)+"&url="+urllib.quote_plus(url1)
	        xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)

def BaikeList(name,url):
        url="http://bk.pps.tv"+url
        req = urllib2.Request(url)
        req.add_header("User-Agent", "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3")
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        link=re.sub("\r","",link)
        link=re.sub("\n","",link)
        link=re.sub("\t","",link)
        match=re.compile('<ul class="bs_new">(.+?)</ul>').findall(link)
        if len(match)>0:
                match0=re.compile('href="(.+?)"(.+?)>(.+?)</a>').findall(match[0])
                for i in range(0,len(match0)):
                        if match0[i][2].find("更多")==-1 and match0[i][2].find("视频")==-1:
	                        li=xbmcgui.ListItem("【在线观看】"+match0[i][2].decode("gbk").encode("utf8"))
	                        u=sys.argv[0]+"?mode=22&name="+urllib.quote_plus(match0[i][2].decode("gbk").encode("utf8"))+"&url="+urllib.quote_plus(match0[i][0])
	                        xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li)
        match=re.compile('<ul class="xg_new">(.+?)</ul>').findall(link)
        if len(match)>0:
                match0=re.compile('href="(.+?)"(.+?)>(.+?)</a>').findall(match[0])
                for i in range(0,len(match0)):
	                li=xbmcgui.ListItem("【相关播放】"+match0[i][2].decode("gbk").encode("utf8"))
	                u=sys.argv[0]+"?mode=22&name="+urllib.quote_plus(match0[i][2].decode("gbk").encode("utf8"))+"&url="+urllib.quote_plus(match0[i][0])
	                xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li)


def BaikePlay(name,url):
        req = urllib2.Request(url)
        req.add_header("User-Agent", "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3")
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile("ppspowerplayer.setsrc\('(.+?)'").findall(link)
        if len(match)>0:
		if (os.name == 'nt'):
                	xbmc.executebuiltin('System.ExecWait(\\"'+ os.getcwd()+'\\resources\\player\\pps4xbmc\\" '+match[0].decode("gbk").encode("utf8")+')')
		else:
                	xbmc.executebuiltin('System.ExecWait(\\"'+ os.getcwd()+'\\resources\\player\\pps4xbmc\\" '+match[0].decode("gbk").encode("utf8")+')')

def KankanPlay(url):
	if (os.name == 'nt'):
               	xbmc.executebuiltin('System.ExecWait(\\"'+ os.getcwd()+'\\resources\\player\\pps4xbmc\\" '+url.decode("gbk").encode("utf8")+')')
	else:
               	xbmc.executebuiltin('System.ExecWait(\\"'+ os.getcwd()+'\\resources\\player\\pps4xbmc\\" '+url.decode("gbk").encode("utf8")+')')

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



if mode==None:
	name=''
	Roots()
elif mode==1:
	Kankan(name)
elif mode==2:
	KankanA(name)
elif mode==3:
        KankanA0(name,url)
elif mode==4:
        KankanA1(name,url)
elif mode==5:
        KankanB(name)
elif mode==6:
	KankanB0(name)
elif mode==7:
	KankanB1(name,url)
elif mode==8:
	KankanC(name)
elif mode==9:
	KankanD(name)
elif mode==10:
	KankanD0(name,url)
elif mode==11:
	KankanE(name)
elif mode==12:
	KankanE0(name,url)
elif mode==13:
	KankanList0(name,url)
elif mode==14:
	KankanList1(name,url)
elif mode==15:
	KankanList2(name,url)
elif mode==16:
	Baike(name)
elif mode==17:
	BaikeA(name,url)
elif mode==18:
	BaikeB(name,url,type)
elif mode==19:
	BaikeC(name,url)
elif mode==20:
	BaikeD(name,url)
elif mode==21:
	BaikeList(name,url)
elif mode==22:
        BaikePlay(name,url)
elif mode==23:
        KankanPlay(url)

xbmcplugin.setPluginCategory(int(sys.argv[1]), name )
xbmcplugin.endOfDirectory(int(sys.argv[1]))

    
