# -*- coding: utf-8 -*-
import xbmc,xbmcgui,xbmcplugin,urllib2,urllib,re,sys

#优酷视频- by robinttt 2010.

def Roots():
        li=xbmcgui.ListItem("视频")
        u=sys.argv[0]+"?mode=1&name="+urllib.quote_plus("视频")
        xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
        li=xbmcgui.ListItem("电影")
        u=sys.argv[0]+"?mode=10&name="+urllib.quote_plus("电影")+"&list="+urllib.quote_plus("c96")
        xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
        li=xbmcgui.ListItem("电视")
        u=sys.argv[0]+"?mode=10&name="+urllib.quote_plus("电视")+"&list="+urllib.quote_plus("c97")
        xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
        li=xbmcgui.ListItem("综艺")
        u=sys.argv[0]+"?mode=10&name="+urllib.quote_plus("综艺")+"&list="+urllib.quote_plus("c85")
        xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)

def Video(name):
        li=xbmcgui.ListItem(name+">全部")
        u=sys.argv[0]+"?mode=2&name="+urllib.quote_plus(name+">全部")+"&list="+urllib.quote_plus("c0")
        xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
        req = urllib2.Request("http://www.youku.com/v/")
        req.add_header("User-Agent", "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3")
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('<li><a href="/v_showlist/(.+?).html"(.+?)>(.+?)<').findall(link)
        for i in range(0,len(match)):
                li=xbmcgui.ListItem(name+">"+match[i][2])
                u=sys.argv[0]+"?mode=2&name="+urllib.quote_plus(name+">"+match[i][2])+"&list="+urllib.quote_plus(match[i][0])
                xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)

def Video0(name,list):
        li=xbmcgui.ListItem(name+">视频")
        u=sys.argv[0]+"?mode=3&name="+urllib.quote_plus(name+">视频")+"&list="+urllib.quote_plus(list)+"&type="+urllib.quote_plus("showlist")
        xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
        li=xbmcgui.ListItem(name+">专辑")
        u=sys.argv[0]+"?mode=5&name="+urllib.quote_plus(name+">专辑")+"&list="+urllib.quote_plus(list)+"&type="+urllib.quote_plus("plist")
        xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)

def Video1(name,list,type):
        li=xbmcgui.ListItem(name+">不限")
        u=sys.argv[0]+"?mode=4&name="+urllib.quote_plus(name+">不限")+"&list="+urllib.quote_plus(list)+"&type="+urllib.quote_plus(type)+"&kind="+urllib.quote_plus("0")
        xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
        req = urllib2.Request("http://www.youku.com/v_showlist/"+list+".html")
        req.add_header("User-Agent", "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3")
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('<span class="key"><a href="/v_showlist/t2d1'+list+'g(.+?).html"(.+?)>(.+?)<').findall(link)
        for i in range(0,len(match)):
                li=xbmcgui.ListItem(name+">"+match[i][2])
                u=sys.argv[0]+"?mode=4&name="+urllib.quote_plus(name+">"+match[i][2])+"&list="+urllib.quote_plus(list)+"&type="+urllib.quote_plus(type)+"&kind="+urllib.quote_plus(match[i][0])
                xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)

def Video2(name,list,type,kind):
        li=xbmcgui.ListItem(name+">最新发布")
        u=sys.argv[0]+"?mode=6&name="+urllib.quote_plus(name+">最新发布")+"&list="+urllib.quote_plus(list)+"&type="+urllib.quote_plus(type)+"&kind="+urllib.quote_plus(kind)+"&sort="+urllib.quote_plus("1")
        xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
        li=xbmcgui.ListItem(name+">最多播放")
        u=sys.argv[0]+"?mode=6&name="+urllib.quote_plus(name+">最多播放")+"&list="+urllib.quote_plus(list)+"&type="+urllib.quote_plus(type)+"&kind="+urllib.quote_plus(kind)+"&sort="+urllib.quote_plus("2")
        xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
        li=xbmcgui.ListItem(name+">最热话题")
        u=sys.argv[0]+"?mode=6&name="+urllib.quote_plus(name+">最热话题")+"&list="+urllib.quote_plus(list)+"&type="+urllib.quote_plus(type)+"&kind="+urllib.quote_plus(kind)+"&sort="+urllib.quote_plus("3")
        xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
        li=xbmcgui.ListItem(name+">最具争议")
        u=sys.argv[0]+"?mode=6&name="+urllib.quote_plus(name+">最具争议")+"&list="+urllib.quote_plus(list)+"&type="+urllib.quote_plus(type)+"&kind="+urllib.quote_plus(kind)+"&sort="+urllib.quote_plus("8")
        xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
        li=xbmcgui.ListItem(name+">最多收藏")
        u=sys.argv[0]+"?mode=6&name="+urllib.quote_plus(name+">最多收藏")+"&list="+urllib.quote_plus(list)+"&type="+urllib.quote_plus(type)+"&kind="+urllib.quote_plus(kind)+"&sort="+urllib.quote_plus("4")
        xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
        li=xbmcgui.ListItem(name+">最广传播")
        u=sys.argv[0]+"?mode=6&name="+urllib.quote_plus(name+">最广传播")+"&list="+urllib.quote_plus(list)+"&type="+urllib.quote_plus(type)+"&kind="+urllib.quote_plus(kind)+"&sort="+urllib.quote_plus("5")
        xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
        li=xbmcgui.ListItem(name+">用户推荐")
        u=sys.argv[0]+"?mode=6&name="+urllib.quote_plus(name+">用户推荐")+"&list="+urllib.quote_plus(list)+"&type="+urllib.quote_plus(type)+"&kind="+urllib.quote_plus(kind)+"&sort="+urllib.quote_plus("6")
        xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)

def Video3(name,list,type):
        li=xbmcgui.ListItem(name+">最新更新")
        u=sys.argv[0]+"?mode=6&name="+urllib.quote_plus(name+">最新更新")+"&list="+urllib.quote_plus(list)+"&type="+urllib.quote_plus(type)+"&kind="+urllib.quote_plus("")+"&sort="+urllib.quote_plus("1")
        xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
        li=xbmcgui.ListItem(name+">最多播放")
        u=sys.argv[0]+"?mode=6&name="+urllib.quote_plus(name+">最多播放")+"&list="+urllib.quote_plus(list)+"&type="+urllib.quote_plus(type)+"&kind="+urllib.quote_plus("")+"&sort="+urllib.quote_plus("2")
        xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
        li=xbmcgui.ListItem(name+">历史推荐")
        u=sys.argv[0]+"?mode=6&name="+urllib.quote_plus(name+">历史推荐")+"&list="+urllib.quote_plus(list)+"&type="+urllib.quote_plus(type)+"&kind="+urllib.quote_plus("")+"&sort="+urllib.quote_plus("4")
        xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)


def Video4(name,list,type,kind,sort):
        li=xbmcgui.ListItem(name+">历史")
        u=sys.argv[0]+"?mode=7&name="+urllib.quote_plus(name+">历史")+"&list="+urllib.quote_plus(list)+"&type="+urllib.quote_plus(type)+"&kind="+urllib.quote_plus(kind)+"&sort="+urllib.quote_plus(sort)+"&time="+urllib.quote_plus("4")+"&page="+urllib.quote_plus("1")
        xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
        li=xbmcgui.ListItem(name+">本月")
        u=sys.argv[0]+"?mode=7&name="+urllib.quote_plus(name+">本月")+"&list="+urllib.quote_plus(list)+"&type="+urllib.quote_plus(type)+"&kind="+urllib.quote_plus(kind)+"&sort="+urllib.quote_plus(sort)+"&time="+urllib.quote_plus("3")+"&page="+urllib.quote_plus("1")
        xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
        li=xbmcgui.ListItem(name+">本周")
        u=sys.argv[0]+"?mode=7&name="+urllib.quote_plus(name+">本周")+"&list="+urllib.quote_plus(list)+"&type="+urllib.quote_plus(type)+"&kind="+urllib.quote_plus(kind)+"&sort="+urllib.quote_plus(sort)+"&time="+urllib.quote_plus("2")+"&page="+urllib.quote_plus("1")
        xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
        li=xbmcgui.ListItem(name+">今日")
        u=sys.argv[0]+"?mode=7&name="+urllib.quote_plus(name+">今日")+"&list="+urllib.quote_plus(list)+"&type="+urllib.quote_plus(type)+"&kind="+urllib.quote_plus(kind)+"&sort="+urllib.quote_plus(sort)+"&time="+urllib.quote_plus("1")+"&page="+urllib.quote_plus("1")
        xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)

def Video5(name,list,type,kind,sort,page):
        if type=="showlist":
                if kind=="0":
                        url="http://www.youku.com/v_"+type+"/t"+sort+list+"d"+time+"p"+page+".html"
                else:
                        url="http://www.youku.com/v_"+type+"/t"+sort+list+"d"+time+"p"+page+"g"+kind+".html"
                req = urllib2.Request(url)
                req.add_header("User-Agent", "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3")
                response = urllib2.urlopen(req)
                link=response.read()
                response.close()
                link=re.sub("\r","",link)
                link=re.sub("\n","",link)
                link=re.sub("\t","",link)
                link=re.sub(" ","",link)
                li=xbmcgui.ListItem("当前位置："+name+" 第"+page+"页")
                u=sys.argv[0]+"?mode=40&name="+urllib.quote_plus(name)
                xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li)
                match=re.compile('<liclass="v_link"><ahref="(http://v.youku.com/v_show/id_.+?.html)"charset=(.+?)<imgsrc="(.+?)"alt="(.+?)"').findall(link)
                if len(match)>0:
                        for i in range(0,len(match)):
                                li=xbmcgui.ListItem(str(i+1)+"."+match[i][3],match[i][2],match[i][2])
                                u=sys.argv[0]+"?mode=18&name="+urllib.quote_plus(match[i][3])+"&url="+urllib.quote_plus(match[i][0])+"&director="+urllib.quote_plus("")+"&studio="+urllib.quote_plus("")+"&plot="+urllib.quote_plus("")
                                xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li)

                match=re.compile('<ulclass="pages">(.+?)</ul>').findall(link)
                if len(match)>0:
                        tmp="/v_"+type+"/t"+sort+list+"d"+time+"p"
                        if kind=="0":
                                match0=re.compile('href="'+tmp+'(.+?).html(.+?)>(.+?)</a>').findall(match[0])
                        else:
                                match0=re.compile('href="'+tmp+'(.+?)g'+kind+'.html(.+?)>(.+?)</a>').findall(match[0])

                        for i in range(0,len(match0)):
                                if match0[i][2].find("页")==-1:
                                        li=xbmcgui.ListItem("..第"+match0[i][2]+"页")
                                        u=sys.argv[0]+"?mode=7&name="+urllib.quote_plus(name)+"&list="+urllib.quote_plus(list)+"&type="+urllib.quote_plus(type)+"&kind="+urllib.quote_plus(kind)+"&sort="+urllib.quote_plus(sort)+"&time="+urllib.quote_plus(time)+"&page="+urllib.quote_plus(match0[i][0])
                                        xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
                                else:
                                        li=xbmcgui.ListItem(".."+match0[i][2])
                                        u=sys.argv[0]+"?mode=7&name="+urllib.quote_plus(name)+"&list="+urllib.quote_plus(list)+"&type="+urllib.quote_plus(type)+"&kind="+urllib.quote_plus(kind)+"&sort="+urllib.quote_plus(sort)+"&time="+urllib.quote_plus(time)+"&page="+urllib.quote_plus(match0[i][0])
                                        xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)

        else:
                url="http://www.youku.com/v_"+type+"/t"+sort+list+"d"+time+"p"+page+".html"
                req = urllib2.Request(url)
                req.add_header("User-Agent", "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3")
                response = urllib2.urlopen(req)
                link=response.read()
                response.close()
                link=re.sub("\r","",link)
                link=re.sub("\n","",link)
                link=re.sub("\t","",link)
                link=re.sub(" ","",link)
                li=xbmcgui.ListItem("当前位置："+name+" 第"+page+"页")
                u=sys.argv[0]+"?mode=40&name="+urllib.quote_plus(name)
                xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li)
                match=re.compile('<liclass="p_link"><ahref="/playlist_show/id_(.+?).html"charset=.+?<imgsrc="(.+?)"alt="(.+?)"').findall(link)
                if len(match)>0:
                        for i in range(0,len(match)):
                                li=xbmcgui.ListItem(str(i+1)+"."+match[i][2],match[i][1],match[i][1])
                                u=sys.argv[0]+"?mode=8&name="+urllib.quote_plus(name+">"+match[i][2])+"&url="+urllib.quote_plus(match[i][0])+"&upage="+urllib.quote_plus("1")
                                xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)

                match=re.compile('<ulclass="pages">(.+?)</ul>').findall(link)
                if len(match)>0:
                        tmp="/v_"+type+"/t"+sort+list+"d"+time+"p"
                        match0=re.compile('href="'+tmp+'(.+?).html.+?>(.+?)</a>').findall(match[0])
                        for i in range(0,len(match0)):
                                if match0[i][1].find("页")==-1:
                                        li=xbmcgui.ListItem("..第"+match0[i][1]+"页")
                                        u=sys.argv[0]+"?mode=7&name="+urllib.quote_plus(name)+"&list="+urllib.quote_plus(list)+"&type="+urllib.quote_plus(type)+"&kind="+urllib.quote_plus(kind)+"&sort="+urllib.quote_plus(sort)+"&time="+urllib.quote_plus(time)+"&page="+urllib.quote_plus(match0[i][0])
                                        xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
                                else:
                                        li=xbmcgui.ListItem(".."+match0[i][1])
                                        u=sys.argv[0]+"?mode=7&name="+urllib.quote_plus(name)+"&list="+urllib.quote_plus(list)+"&type="+urllib.quote_plus(type)+"&kind="+urllib.quote_plus(kind)+"&sort="+urllib.quote_plus(sort)+"&time="+urllib.quote_plus(time)+"&page="+urllib.quote_plus(match0[i][0])
                                        xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)


def Video6(name,url0,upage):
        url="http://www.youku.com/playlist_show/id_"+url0+"_ascending_1_mode_pic_page_"+upage+".html"
        req = urllib2.Request(url)
        req.add_header("User-Agent", "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3")
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        link=re.sub("\r","",link)
        link=re.sub("\n","",link)
        link=re.sub("\t","",link)
        link=re.sub(" ","",link)
        li=xbmcgui.ListItem("当前位置："+name+" 第"+upage+"页")
        u=sys.argv[0]+"?mode=40&name="+urllib.quote_plus(name)
        xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li)
        match=re.compile('<liclass="v_link"><acharset=".+?"title="(.+?)"href="(http://v.youku.com/v_playlist/.+?.html)".+?<imgsrc="(.+?)"').findall(link)
        if len(match)>0:
                for i in range(0,len(match)):
                        li=xbmcgui.ListItem(str(i+1)+"."+match[i][0],match[i][2],match[i][2])
                        u=sys.argv[0]+"?mode=18&name="+urllib.quote_plus(match[i][0])+"&url="+urllib.quote_plus(match[i][1])+"&director="+urllib.quote_plus("")+"&studio="+urllib.quote_plus("")+"&plot="+urllib.quote_plus("")
                        xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li)
        match=re.compile('<divclass="pageBar">(.+?)</div>').findall(link)
        if len(match)>0:
                match0=re.compile('<ahref="http://www.youku.com/playlist_show/id_'+url0+'_ascending_1_mode_pic_page_(.+?).html"title=\'(.+?)\'>').findall(match[0])
                for i in range(0,len(match0)):
                        li=xbmcgui.ListItem(".."+match0[i][1])
                        u=sys.argv[0]+"?mode=8&name="+urllib.quote_plus(name)+"&url="+urllib.quote_plus(url0)+"&upage="+urllib.quote_plus(match0[i][0])
                        xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)

def Movie(name,list):
        #一次获取各类型参数，避免重复解析
        strtype=""
        req = urllib2.Request("http://www.youku.com/v_olist/c_"+list[1:]+".html")
        req.add_header("User-Agent", "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3")
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        #地区参数
        match=re.compile('href="/v_olist/c_'+list[1:]+'_a_(.+?)_s__g__r__d_1_fc__fe__fv_0_fl__o_7.html">(.+?)</a>').findall(link)
        for i in range(0,len(match)):
                strtype=strtype+"a_"+match[i][0]+","+match[i][1]+";"
        strtype=strtype+"|"
        #类型参数
        match=re.compile('href="/v_olist/c_'+list[1:]+'_a__fc__fe__s__g_(.+?)_r__d_1_fv_0_fl__o_7.html">(.+?)</a>').findall(link)
        for i in range(0,len(match)):
                strtype=strtype+"g_"+match[i][0]+","+match[i][1]+";"
        strtype=strtype+"|"
        #上映参数
        match=re.compile('href="/v_olist/c_'+list[1:]+'_a__s__g__r_(.+?)_d_1_fc__fe__fv_0_fl__o_7.html">(.+?)</a>').findall(link)
        for i in range(0,len(match)):
                strtype=strtype+"r_"+match[i][0]+","+match[i][1]+";"
        strtype=strtype+"|"

        if list=="c96":
                li=xbmcgui.ListItem(name+">影片")
                u=sys.argv[0]+"?mode=11&name="+urllib.quote_plus(name+">影片")+"&list="+urllib.quote_plus(list)+"&type="+urllib.quote_plus(strtype)
        elif list=="c97":
                li=xbmcgui.ListItem(name+">剧集")
                u=sys.argv[0]+"?mode=11&name="+urllib.quote_plus(name+">剧集")+"&list="+urllib.quote_plus(list)+"&type="+urllib.quote_plus(strtype)
        elif list=="c85":
                li=xbmcgui.ListItem(name+">节目")
                u=sys.argv[0]+"?mode=11&name="+urllib.quote_plus(name+">节目")+"&list="+urllib.quote_plus(list)+"&type="+urllib.quote_plus(strtype)
        if list=="c85":
                xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
                li=xbmcgui.ListItem(name+">视频")
                u=sys.argv[0]+"?mode=4&name="+urllib.quote_plus(name+">视频")+"&list="+urllib.quote_plus(list)+"&type="+urllib.quote_plus("showlist")+"&kind="+urllib.quote_plus("0")
                xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
        else:
                xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
                li=xbmcgui.ListItem(name+">视频")
                u=sys.argv[0]+"?mode=3&name="+urllib.quote_plus(name+">视频")+"&list="+urllib.quote_plus(list)+"&type="+urllib.quote_plus("showlist")
                xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
        if list!="c85":
                li=xbmcgui.ListItem(name+">专辑")
                u=sys.argv[0]+"?mode=5&name="+urllib.quote_plus(name+">专辑")+"&list="+urllib.quote_plus(list)+"&type="+urllib.quote_plus("plist")
                xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)

def Movie0(name,list,type):
        li=xbmcgui.ListItem(name+">所有")
        u=sys.argv[0]+"?mode=12&name="+urllib.quote_plus(name)+"&list="+urllib.quote_plus(list)+"&type="+urllib.quote_plus(type)+"&kind="+urllib.quote_plus("g_")
        xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
        keys=type.split("|")[1].split(";")
        for i in range(0,len(keys)-1):
                li=xbmcgui.ListItem(name+">"+keys[i].split(",")[1])
                u=sys.argv[0]+"?mode=12&name="+urllib.quote_plus(name+">"+keys[i].split(",")[1])+"&list="+urllib.quote_plus(list)+"&type="+urllib.quote_plus(type)+"&kind="+urllib.quote_plus(keys[i].split(",")[0])
                xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)

def Movie1(name,list,type,kind):
        li=xbmcgui.ListItem(name+">所有")
        u=sys.argv[0]+"?mode=13&name="+urllib.quote_plus(name)+"&list="+urllib.quote_plus(list)+"&type="+urllib.quote_plus(type)+"&kind="+urllib.quote_plus(kind)+"&area="+urllib.quote_plus("a_")
        xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
        keys=type.split("|")[0].split(";")
        for i in range(0,len(keys)-1):
                li=xbmcgui.ListItem(name+">"+keys[i].split(",")[1])
                u=sys.argv[0]+"?mode=13&name="+urllib.quote_plus(name+">"+keys[i].split(",")[1])+"&list="+urllib.quote_plus(list)+"&type="+urllib.quote_plus(type)+"&kind="+urllib.quote_plus(kind)+"&area="+urllib.quote_plus(keys[i].split(",")[0])
                xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)

def Movie2(name,list,type,kind,area):
        li=xbmcgui.ListItem(name+">所有")
        u=sys.argv[0]+"?mode=14&name="+urllib.quote_plus(name)+"&list="+urllib.quote_plus(list)+"&type="+urllib.quote_plus(type)+"&kind="+urllib.quote_plus(kind)+"&area="+urllib.quote_plus(area)+"&time="+urllib.quote_plus("r_")
        xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
        keys=type.split("|")[2].split(";")
        for i in range(0,len(keys)-1):
                li=xbmcgui.ListItem(name+">"+keys[i].split(",")[1])
                u=sys.argv[0]+"?mode=14&name="+urllib.quote_plus(name+">"+keys[i].split(",")[1])+"&list="+urllib.quote_plus(list)+"&type="+urllib.quote_plus(type)+"&kind="+urllib.quote_plus(kind)+"&area="+urllib.quote_plus(area)+"&time="+urllib.quote_plus(keys[i].split(",")[0])
                xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)

def Movie3(name,list,type,kind,area,time):
        li=xbmcgui.ListItem(name+">所有热门")
        u=sys.argv[0]+"?mode=15&name="+urllib.quote_plus(name+">所有热门")+"&list="+urllib.quote_plus(list)+"&type="+urllib.quote_plus(type)+"&kind="+urllib.quote_plus(kind)+"&area="+urllib.quote_plus(area)+"&time="+urllib.quote_plus(time)+"&sort="+urllib.quote_plus("o_1")+"&page="+urllib.quote_plus("1")
        xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
        li=xbmcgui.ListItem(name+">本周热门")
        u=sys.argv[0]+"?mode=15&name="+urllib.quote_plus(name+">本周热门")+"&list="+urllib.quote_plus(list)+"&type="+urllib.quote_plus(type)+"&kind="+urllib.quote_plus(kind)+"&area="+urllib.quote_plus(area)+"&time="+urllib.quote_plus(time)+"&sort="+urllib.quote_plus("o_6")+"&page="+urllib.quote_plus("1")
        xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
        li=xbmcgui.ListItem(name+">今日热门")
        u=sys.argv[0]+"?mode=15&name="+urllib.quote_plus(name+">今日热门")+"&list="+urllib.quote_plus(list)+"&type="+urllib.quote_plus(type)+"&kind="+urllib.quote_plus(kind)+"&area="+urllib.quote_plus(area)+"&time="+urllib.quote_plus(time)+"&sort="+urllib.quote_plus("o_7")+"&page="+urllib.quote_plus("1")
        xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
        li=xbmcgui.ListItem(name+">最新上映")
        u=sys.argv[0]+"?mode=15&name="+urllib.quote_plus(name+">最新上映")+"&list="+urllib.quote_plus(list)+"&type="+urllib.quote_plus(type)+"&kind="+urllib.quote_plus(kind)+"&area="+urllib.quote_plus(area)+"&time="+urllib.quote_plus(time)+"&sort="+urllib.quote_plus("o_3")+"&page="+urllib.quote_plus("1")
        xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
        li=xbmcgui.ListItem(name+">最近上映")
        u=sys.argv[0]+"?mode=15&name="+urllib.quote_plus(name+">最近上映")+"&list="+urllib.quote_plus(list)+"&type="+urllib.quote_plus(type)+"&kind="+urllib.quote_plus(kind)+"&area="+urllib.quote_plus(area)+"&time="+urllib.quote_plus(time)+"&sort="+urllib.quote_plus("o_9")+"&page="+urllib.quote_plus("1")
        xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
        li=xbmcgui.ListItem(name+">评论最多")
        u=sys.argv[0]+"?mode=15&name="+urllib.quote_plus(name+">评论最多")+"&list="+urllib.quote_plus(list)+"&type="+urllib.quote_plus(type)+"&kind="+urllib.quote_plus(kind)+"&area="+urllib.quote_plus(area)+"&time="+urllib.quote_plus(time)+"&sort="+urllib.quote_plus("o_5")+"&page="+urllib.quote_plus("1")
        xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)

def Movie4(name,list,type,kind,area,time,sort,page):
        url="http://www.youku.com/v_olist/c_"+list[1:]+"_"+area+"_"+kind+"_"+time+"_d_1_fv_0_fl__"+sort+"_p_"+page+".html"
        req = urllib2.Request(url)
        req.add_header("User-Agent", "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3")
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        link=re.sub("\r","",link)
        link=re.sub("\n","",link)
        link=re.sub("\t","",link)
        link=re.sub(" ","",link)
        li=xbmcgui.ListItem("当前位置："+name+" 第"+page+"页")
        u=sys.argv[0]+"?mode=40&name="+urllib.quote_plus(name)
        xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li)
        match=re.compile('<liclass="p_link"><ahref="http://www.youku.com/show_page/id_(.+?).html"title="(.+?)"target=.+?<imgsrc="(.+?)".+?<emclass="num">(.+?)</em>').findall(link)
        if len(match)>0:
                for i in range(0,len(match)):
                        li=xbmcgui.ListItem(str(i+1)+"."+match[i][1]+" 【"+match[i][3]+"】",match[i][2],match[i][2])
                        if list=="c96":
                                u=sys.argv[0]+"?mode=16&name="+urllib.quote_plus(match[i][1])+"&url="+urllib.quote_plus(match[i][0])
                                xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li)
                        else:
                                u=sys.argv[0]+"?mode=17&name="+urllib.quote_plus(match[i][1])+"&url="+urllib.quote_plus(match[i][0])+"&upage="+urllib.quote_plus("1")
                                xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
        match=re.compile('<ulclass="pages">(.+?)</ul>').findall(link)
        if len(match)>0:
                match0=re.compile('p_(.+?).html".+?>(.+?)</a>').findall(match[0])
                for i in range(0,len(match0)):
                        if match0[i][1].find("页")==-1:
                                li=xbmcgui.ListItem("..第"+match0[i][1]+"页")
                        else:
                                li=xbmcgui.ListItem(".."+match0[i][1])
                        u=sys.argv[0]+"?mode=15&name="+urllib.quote_plus(name)+"&list="+urllib.quote_plus(list)+"&type="+urllib.quote_plus(type)+"&kind="+urllib.quote_plus(kind)+"&area="+urllib.quote_plus(area)+"&time="+urllib.quote_plus(time)+"&sort="+urllib.quote_plus(sort)+"&page="+urllib.quote_plus(match0[i][0])
                        xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)

def Movie5(name,url):
        req = urllib2.Request("http://www.youku.com/show_page/id_"+url+".html")
        req.add_header("User-Agent", "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3")
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        link=re.sub("\r","",link)
        link=re.sub("\n","",link)
        link=re.sub("\t","",link)
        link=re.sub(" ","",link)
        match=re.compile('<spanclass="time"><spanclass="num">(.+?)</span>').findall(link)
        if len(match)>0:duration=match[0]
        else:duration=""
        match=re.compile('<spanclass="label">导演:</span>.+?target="_blank">(.+?)</a>').findall(link)
        if len(match)>0:director=match[0]
        else:director=""
        match=re.compile('<spanclass="label">演员:</span>.+?target="_blank">(.+?)</a>').findall(link)
        if len(match)>0:studio=match[0]
        else:studio=""
        match=re.compile('<spanid="infoLong".+?>(.+?)</span>').findall(link)
        if len(match)>0:plot=match[0]
        else:plot=""
        #match=re.compile('<spanclass="action">(.+?)href="(http://v.youku.com/v_show/id_.+?.html)"').findall(link)
        match=re.compile('<divid="showBanner".+?href="(http://v.youku.com/v_show/id_.+?.html)"><spanclass="status">(.+?)</span>').findall(link)
        if len(match)>0:
                PlayVideo(match[0][1]+'：'+name,match[0][0],director,studio,plot)

def Movie6(name,url,upage):
        li=xbmcgui.ListItem("当前节目："+name+" 第"+upage+"页")
        u=sys.argv[0]+"?mode=40&name="+urllib.quote_plus(name)
        xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li)
        req = urllib2.Request("http://www.youku.com/show_eplist/showid_"+url+"_type_pic_from_ajax_page_"+upage+".html")
        req.add_header("User-Agent", "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3")
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        link=re.sub("\r","",link)
        link=re.sub("\n","",link)
        link=re.sub("\t","",link)
        link=re.sub(" ","",link)
        match=re.compile('<liclass="v_link"><acharset=".+?"href="(http://v.youku.com/v_show/id_.+?.html)"target=.+?<imgsrc="(.+?)"alt="(.+?)"').findall(link)
        if len(match)>0:
                for i in range(0,len(match)):
                        li=xbmcgui.ListItem(str(i+1)+"."+match[i][2],match[i][1],match[i][1])
                        u=sys.argv[0]+"?mode=18&name="+urllib.quote_plus(match[i][2])+"&url="+urllib.quote_plus(match[i][0])+"&director="+urllib.quote_plus("")+"&studio="+urllib.quote_plus("")+"&plot="+urllib.quote_plus("")
                        xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li)
        match=re.compile('<ulclass="pages">(.+?)</ul>').findall(link)
        if len(match)>0:
                match0=re.compile('show_eplist/showid_'+url+'_type_pic_from_ajax_page_(.+?).html').findall(match[0])
                for i in range(0,len(match0)):
                        if match0[i]!=upage:
                                li=xbmcgui.ListItem("..第"+match0[i]+"页")
                                u=sys.argv[0]+"?mode=17&name="+urllib.quote_plus(name)+"&url="+urllib.quote_plus(url)+"&upage="+urllib.quote_plus(match0[i])
                                xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)

def PlayVideo(name,url,director,studio,plot):
        req = urllib2.Request("http://www.flvcd.com/parse.php?kw="+url)
        req.add_header("User-Agent", "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3")
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        link=re.sub("\r","",link)
        link=re.sub("\n","",link)
        link=re.sub("\t","",link)
        link=re.sub(" ","",link)
        match=re.compile('href="http://f.youku.com/player/getFlvPath/(.+?)"target="_blank"').findall(link)
        if len(match)>0:
                playlist=xbmc.PlayList(1)
                playlist.clear()
                for i in range(0,len(match)):
                        listitem=xbmcgui.ListItem(name)
                        listitem.setInfo(type="Video",infoLabels={"Title":name,"Director":director,"Studio":studio,"Plot":plot})
                        playlist.add("http://f.youku.com/player/getFlvPath/"+match[i], listitem)
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
list=None
type=None
sort=None
time=None
kind=None
page=None
upage=None
area=None
cate=None
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
        list=urllib.unquote_plus(params["list"])
except:
        pass
try:
        type=urllib.unquote_plus(params["type"])
except:
        pass
try:
        kind=urllib.unquote_plus(params["kind"])
except:
        pass
try:
        sort=urllib.unquote_plus(params["sort"])
except:
        pass
try:
        time=urllib.unquote_plus(params["time"])
except:
        pass
try:
        page=urllib.unquote_plus(params["page"])
except:
        pass
try:
        upage=urllib.unquote_plus(params["upage"])
except:
        pass
try:
        area=urllib.unquote_plus(params["area"])
except:
        pass
try:
        cate=urllib.unquote_plus(params["cate"])
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
        mode=int(params["mode"])
except:
        pass

if mode==None:
        name=''
        Roots()
elif mode==1:
        Video(name)
elif mode==2:
        Video0(name,list)
elif mode==3:
        Video1(name,list,type)
elif mode==4:
        Video2(name,list,type,kind)
elif mode==5:
        Video3(name,list,type)
elif mode==6:
        Video4(name,list,type,kind,sort)
elif mode==7:
        Video5(name,list,type,kind,sort,page)
elif mode==8:
        Video6(name,url,upage)
elif mode==9:
        Video7(name,url)
elif mode==10:
        Movie(name,list)
elif mode==11:
        Movie0(name,list,type)
elif mode==12:
        Movie1(name,list,type,kind)
elif mode==13:
        Movie2(name,list,type,kind,area)
elif mode==14:
        Movie3(name,list,type,kind,area,time)
elif mode==15:
        Movie4(name,list,type,kind,area,time,sort,page)
elif mode==16:
        Movie5(name,url)
elif mode==17:
        Movie6(name,url,upage)
elif mode==18:
        PlayVideo(name,url,director,studio,plot)


xbmcplugin.setPluginCategory(int(sys.argv[1]),name)
xbmcplugin.endOfDirectory(int(sys.argv[1]))

