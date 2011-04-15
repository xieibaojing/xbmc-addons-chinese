# -*- coding: utf-8 -*-
import httplib,urllib,re,xbmcaddon,xbmcplugin,xbmcgui,xbmc,os

# CCTV Video - by Robinttt 2009.
# CNTV Video - Edit by Spy007 2010
# CNTV-live - Changed by taxigps 2011

# Plugin constants 
__addonname__ = "中国网络电视台直播"
__addonid__ = "plugin.video.cntv-live"
__addon__ = xbmcaddon.Addon(id=__addonid__)
__addonpath__ = xbmc.translatePath(__addon__.getAddonInfo('path'))

# 初次运行本插件时自动注册CNTV播放控件
if __addon__.getSetting('CCTVPlayerOcxReg') == "false":
         xbmc.executebuiltin('System.Exec(\\"'+ __addonpath__+'\\resources\\player\\CCTVPlayerOcxReg.exe\\")')
         __addon__.setSetting(id="CCTVPlayerOcxReg", value="true")

def CATEGORIES():
         addDir('央视直播','/index.shtml',6,__addonpath__+'\\resources\\media\\live-cctv.jpg',True)
         addDir('卫视直播','/live_h/index.shtml',6,__addonpath__+'\\resources\\media\\live-startv.png',True)

def LiveChannel(url,name):
         if name=='央视直播':
                 addDir(name+'>CCTV1综合频道',"pa://cctv_p2p_hdcctv1",7,__addonpath__+'\\resources\\media\\cctv1.png')
                 addDir(name+'>CCTV2财经频道',"pa://cctv_p2p_hdcctv2",7,__addonpath__+'\\resources\\media\\cctv2.png')
                 addDir(name+'>CCTV3文艺频道',"pl://cctv_p2p_hdcctv3",7,__addonpath__+'\\resources\\media\\cctv3.png')
                 addDir(name+'>CCTV4亚洲国际',"pl://cctv_p2p_hdcctv4",7,__addonpath__+'\\resources\\media\\cctv4.png')
                 addDir(name+'>CCTV4欧洲国际',"pl://cctv_p2p_hdcctv4euro",7,__addonpath__+'\\resources\\media\\cctv4o.png')
                 addDir(name+'>CCTV4美洲国际',"pl://cctv_p2p_hdcctv4america",7,__addonpath__+'\\resources\\media\\cctv4a.png')
                 addDir(name+'>CCTV5体育频道',"pa://cctv_p2p_hdcctv5",7,__addonpath__+'\\resources\\media\\cctv5.png')
                 addDir(name+'>CCTV6电影频道',"pl://cctv_p2p_hdcctv6",7,__addonpath__+'\\resources\\media\\cctv6.png')
                 addDir(name+'>CCTV7军事频道',"pa://cctv_p2p_hdcctv7",7,__addonpath__+'\\resources\\media\\cctv7.png')
                 addDir(name+'>CCTV8电视剧频道',"pl://cctv_p2p_hdcctv8",7,__addonpath__+'\\resources\\media\\cctv8.png')
                 addDir(name+'>CCTV9英语国际',"pl://cctv_p2p_hdcctv9",7,__addonpath__+'\\resources\\media\\cctv9.png')
                 addDir(name+'>CCTV10科教频道',"pl://cctv_p2p_hdcctv10",7,__addonpath__+'\\resources\\media\\cctv10.png')
                 addDir(name+'>CCTV11戏曲频道',"pl://cctv_p2p_hdcctv11",7,__addonpath__+'\\resources\\media\\cctv11.png')
                 addDir(name+'>CCTV12法制频道',"pl://cctv_p2p_hdcctv12",7,__addonpath__+'\\resources\\media\\cctv12.png')
                 addDir(name+'>CCTV少儿频道',"pl://cctv_p2p_hdcctvkids",7,__addonpath__+'\\resources\\media\\cctvshaoer.png')
                 addDir(name+'>CCTV新闻频道',"pa://cctv_p2p_hdcctvnews",7,__addonpath__+'\\resources\\media\\cctvnews.png')
                 addDir(name+'>CNTV24小时体育',"pa://cctv_p2p264_sports",7,__addonpath__+'\\resources\\media\\cctvsport.png')
                 addDir(name+'>CCTV音乐频道',"pl://cctv_p2p_hdcctvmusic",7,__addonpath__+'\\resources\\media\\cctvmusic.png')
                 addDir(name+'>CCTV高清频道',"pa://cctv_p2p_hdcctvgaoqing",7,__addonpath__+'\\resources\\media\\cctvhd.png')
                 addDir(name+'>CCTV法语频道',"pl://cctv_p2p_cctvfayu",7,__addonpath__+'\\resources\\media\\cctvf.png')
                 addDir(name+'>CCTV西班牙语频道',"pl://cctv_p2p_hdxiyu",7,__addonpath__+'\\resources\\media\\cctve.png')
                 addDir(name+'>CCTV俄语频道',"pl://cctv_p2p_hd700_cctvrussian",7,__addonpath__+'\\resources\\media\\cctveyu.png')
                 addDir(name+'>CCTV阿拉伯语频道',"pl://cctv_p2p_hd700_cctvarabic",7,__addonpath__+'\\resources\\media\\cctvayu.png')
                 addDir(name+'>CCTV中视购物频道',"pl://cctv_p2p_gouwu",7,__addonpath__+'\\resources\\media\\cctvgouwu.png')
                 addDir(name+'>CCTV风云足球频道',"pa://cctv_p2p_hdcctvfyzq",7,__addonpath__+'\\resources\\media\\cctvfootball.png')
                 addDir(name+'>CCTV高尔夫频道',"pa://cctv_p2p_hdcctvgaowang",7,__addonpath__+'\\resources\\media\\cctvgolf.png')
         elif name=="卫视直播":
                 addDir(name+'>安徽卫视',"pl://cctv_p2p_hdanhui",7,__addonpath__+'\\resources\\media\\anhui.png')
                 addDir(name+'>北京卫视',"pl://cctv_p2p_hdbeijing",7,__addonpath__+'\\resources\\media\\beijing.png')
                 addDir(name+'>东方卫视',"pl://cctv_p2p_hdshanghaikatong",7,__addonpath__+'\\resources\\media\\dongfang.png')
                 addDir(name+'>天津卫视',"pl://cctv_p2p_hdtianjin",7,__addonpath__+'\\resources\\media\\tianjin.png')
                 addDir(name+'>重庆卫视',"pl://cctv_p2p_hdchongqing",7,__addonpath__+'\\resources\\media\\chongqing.png')
                 addDir(name+'>东南卫视',"pl://cctv_p2p_hddongnan",7,__addonpath__+'\\resources\\media\\dongnan.png')
                 addDir(name+'>甘肃卫视',"pl://cctv_p2p_hdgansu",7,__addonpath__+'\\resources\\media\\gansu.png')
                 addDir(name+'>广东卫视',"pl://cctv_p2p_hdguangdong",7,__addonpath__+'\\resources\\media\\guangdong.png')
                 addDir(name+'>广西卫视',"pl://cctv_p2p_hdguangxi",7,__addonpath__+'\\resources\\media\\guangxi.png')
                 addDir(name+'>贵州卫视',"pl://cctv_p2p_hdguizhou",7,__addonpath__+'\\resources\\media\\guizhou.png')
                 addDir(name+'>河北卫视',"pl://cctv_p2p_hdhebei",7,__addonpath__+'\\resources\\media\\hebei.png')
                 addDir(name+'>黑龙江卫视',"pl://cctv_p2p_hdheilongjiang",7,__addonpath__+'\\resources\\media\\heilongjiang.png')
                 addDir(name+'>河南卫视',"pl://cctv_p2p_hdhenan",7,__addonpath__+'\\resources\\media\\henan.png')
                 addDir(name+'>湖北卫视',"pl://cctv_p2p_hdhubei",7,__addonpath__+'\\resources\\media\\hubei.png')
                 addDir(name+'>湖南卫视',"pl://cctv_p2p_hdhunan",7,__addonpath__+'\\resources\\media\\hunan.png')
                 addDir(name+'>江苏卫视',"pl://cctv_p2p_hdjiangsu",7,__addonpath__+'\\resources\\media\\jiangsu.png')
                 addDir(name+'>江西卫视',"pl://cctv_p2p_hdjiangxi",7,__addonpath__+'\\resources\\media\\jiangxi.png')
                 addDir(name+'>吉林卫视',"pl://cctv_p2p_hdjilin",7,__addonpath__+'\\resources\\media\\jilin.png')
                 addDir(name+'>辽宁卫视',"pl://cctv_p2p_hdliaoning",7,__addonpath__+'\\resources\\media\\liaoning.png')
                 addDir(name+'>旅游卫视',"pl://cctv_p2p_hdlvyou",7,__addonpath__+'\\resources\\media\\lvyou.png')
                 addDir(name+'>内蒙古卫视',"pl://cctv_p2p_hdneimeng",7,__addonpath__+'\\resources\\media\\neimenggu.png')
                 addDir(name+'>宁夏卫视',"pl://cctv_p2p_hdningxia",7,__addonpath__+'\\resources\\media\\ningxia.png')
                 addDir(name+'>青海卫视',"pl://cctv_p2p_hdqinghai",7,__addonpath__+'\\resources\\media\\qinghai.png')
                 addDir(name+'>山东卫视',"pl://cctv_p2p_hdshandong",7,__addonpath__+'\\resources\\media\\shandong.png')
                 addDir(name+'>山东教育',"pl://cctv_p2p_shandongjiaoyu",7,__addonpath__+'\\resources\\media\\shandong.png')
                 addDir(name+'>陕西卫视',"pl://cctv_p2p_hdshanxi",7,__addonpath__+'\\resources\\media\\shan_xi.png')
                 addDir(name+'>山西卫视',"pl://cctv_p2p_hdshan-xi",7,__addonpath__+'\\resources\\media\\shanxi.png')
                 addDir(name+'>四川卫视',"pl://cctv_p2p_hdsichuan",7,__addonpath__+'\\resources\\media\\sichuan.png')
                 addDir(name+'>新疆卫视',"pl://cctv_p2p_hdxinjiang",7,__addonpath__+'\\resources\\media\\xinjiang.png')
                 addDir(name+'>西藏卫视',"pl://cctv_p2p_hdxizang2",7,__addonpath__+'\\resources\\media\\xizang.png')
                 addDir(name+'>云南卫视',"pl://cctv_p2p_hdyunnan",7,__addonpath__+'\\resources\\media\\yunnan.png')
                 addDir(name+'>浙江卫视',"pl://cctv_p2p_hdzhejiang",7,__addonpath__+'\\resources\\media\\zhejiang.png')
                 addDir(name+'>厦门卫视',"pl://cctv_p2p_xiamenweishi",7,__addonpath__+'\\resources\\media\\xiamen.png')
                 addDir(name+'>成都新闻',"pa://cctv_p2p_cdtv1",7,__addonpath__+'\\resources\\media\\sichuan.png')
                 addDir(name+'>成都公共',"pa://cctv_p2p_cdtv5",7,__addonpath__+'\\resources\\media\\sichuan.png')
                 addDir(name+'>厦门一套',"pl://cctv_p2p_xiamen1",7,__addonpath__+'\\resources\\media\\xiamen.png')
                 addDir(name+'>厦门二套',"pl://cctv_p2p_xiamen2",7,__addonpath__+'\\resources\\media\\xiamen.png')

def LiveLink(url,name):
         xbmc.executebuiltin('System.ExecWait(\\"'+ __addonpath__+'\\resources\\player\\cctvlive.exe\\" '+url+')')

def addDir(name,url,mode,iconimage,folder=False):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=folder)
        return ok

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
url=None
name=None
mode=None

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

if mode==None:
        print ""
        CATEGORIES()
elif mode==6:
        print ""+url
        LiveChannel(url,name)
elif mode==7:
        print ""+url
        LiveLink(url,name)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
