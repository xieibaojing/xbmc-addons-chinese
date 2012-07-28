# -*- coding: utf-8 -*-
import xbmc, xbmcgui, xbmcplugin, xbmcaddon
import urllib2, urllib, re, sys, os
import zipfile
import ChineseKeyboard

########################################################################
# PPS网络电视(PPS客户端) by yxnr
# Version 1.0.1 2012-07-28 (cmeng)
# - change default.py text string to utf-8 for non-Chinese OS display
# - clean up python syntax error
# - clean up xbmc deprecated function call
# - add in chinese keyboard support
# - change search url querry string

# Version 1.0.0 2012-07-23 (yxnr)
# - initial release

# See changelog.txt for previous history
########################################################################

# Plugin constants 
__addonname__     = "PPS网络电视(PPS客户端)"
__addonid__       = "plugin.video.pps"
__settings__      = xbmcaddon.Addon(id=__addonid__)
__cwd__           = xbmc.translatePath( __settings__.getAddonInfo('path') )
__addon__ = xbmcaddon.Addon(id=__addonid__)
__addonicon__ = os.path.join( __addon__.getAddonInfo('path'), 'icon.png' )
UserAgent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'

RESOURCES_PATH = os.path.join(__cwd__ , "resources" )
sys.path.append( os.path.join( RESOURCES_PATH, "lib" ) )
import etree as etree
from etree import ElementTree

##################################################################################
# Routine to fetech url site data using Mozilla browser
# - deletc '\r|\n' for easy re.compile
# - do not delete '\t', xml uses tabe for string seperation
# - do not delete ' ' i.e. <space> as some url include spaces
# - unicode with 'replace' option to avoid exception on some url
# - translate to utf8 if possible
##################################################################################
def getHttpData(url):
    print "getHttpData: " + url
    
    req = urllib2.Request(url)
    req.add_header('User-Agent', UserAgent)
    req.add_header("Referer","www.soso.com")
    try:
        response = urllib2.urlopen(req)
    except urllib2.HTTPError, e:
        httpdata = e.read()
    except urllib2.URLError, e:
        httpdata = "IO Timeout Error"
    else:
        httpdata = response.read()
        response.close()

    httpdata = re.sub('\r|\n', '', httpdata)
    match = re.compile('<meta.+?charset=["]*(.+?)"').findall(httpdata)
    if len(match):
        charset = match[0].lower()
        if (charset != 'utf-8') and (charset != 'utf8'):
            httpdata = unicode(httpdata, charset,'replace').encode('utf8')
    return httpdata

##################################################################################
# Routine to fetch & build PPS 客户端 main menu
##################################################################################
def read_xml(fname,type=1):
#    dialog = xbmcgui.Dialog()
    if type :
        url= "http://list1.pps.tv/class/"+fname+".xml.zip" #目录    
    else :
        url= "http://list1.pps.tv/schs/"+fname+".xml.zip" #文件列表    
    print url
    dfile=urllib.urlretrieve(url)
    z = zipfile.ZipFile(dfile[0],'r')    
    text = z.read(fname+".xml")
    text = text.decode('GB18030').encode('UTF-8')
    text = text.replace('gb18030', 'utf-8')
    text = text.replace('GB18030', 'utf-8')
    
    root = ElementTree.fromstring(text)
    j = 0 
    #主目录
    lst_node = root.getiterator("Gen") 
    for node in lst_node:
        j+=1
        li=xbmcgui.ListItem('[COLOR FF00FF00]'+ str(j)+'. ['+node.attrib['name']+'][/COLOR]')
        u=sys.argv[0]+"?mode=gen&name="+urllib.quote_plus(node.attrib['name'].encode('gb18030'))+"&id="+node.attrib['id']
        xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
        
    #添加一个“欧美剧场”
    if lst_node:
        j+=1
        li=xbmcgui.ListItem('[COLOR FF00FF00]'+ str(j)+'. ['+'欧美剧场'+'][/COLOR]')
        u=sys.argv[0]+"?mode=gen&name="+urllib.quote_plus('欧美剧场')+"&id=192"
        xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)

    #次目录
    lst_node = root.getiterator("Sub")
    for node in lst_node:
        j+=1
        li=xbmcgui.ListItem('[COLOR FF00FF00]'+ str(j)+'. ['+node.attrib['name']+'][/COLOR]')
        try:
            li.setInfo( type="Video", infoLabels={"Title":node.attrib['name'], "count": int(get_params2(node.attrib['op'])["on"])})
        except:
            pass
        u=sys.argv[0]+"?mode=sub&name="+node.attrib['name']+"&id="+node.attrib['id']
        xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)

    #文件
    lst_node = root.getiterator("Ch")
    i=0
    for node in lst_node:
        try:     
            i+=1
            CHON=0
            CHBKID=""
            CHBKVM=1.0
            year=1990

            node_findall = node.find("ID")
            CHID=node_findall.attrib['ID']

            try:    CHON=int(node.attrib['ON'])               
            except: pass
            try:    CHBKID=node_findall.attrib['BKID']
            except: pass
            try:    CHBKVM=float(node_findall.attrib['VM'])
            except: pass
            try:
                cs=node_findall.attrib['search']
                yy=re.compile('(.+?):(.+?):(.+?):(.+?);').findall(cs)
                year=int(yy[0][3])
            except: pass

            node_findall = node.find("Name")
            CHName=node_findall.text

            node_findall = node.find("URL")
            CHURL=node_findall.text

           # ok=dialog.ok(CHName,CHName)
            li=xbmcgui.ListItem(CHName)
            try:     li.setInfo( type="Video", infoLabels={"Title":CHName, "count": CHON, "Rating":CHBKVM, "CODE":CHBKID,"Year":year})
            except:  li.setInfo( type="Video", infoLabels={"Title":CHName, "count": CHON, "Rating":CHBKVM, "CODE":CHBKID})
            u=sys.argv[0]+"?mode=ch&name="+CHName+"&id="+CHID+"&url="+urllib.quote_plus(CHURL.encode('gb18030'))
            xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,False)
        except:
            pass

    #添加一个“PPS搜索”
    li=xbmcgui.ListItem('  【[COLOR FFFF00FF]  PPS 搜索: [/COLOR] 点此进行】'+'[COLOR FF00FFFF]共计：[/COLOR][ '+str(i)+' ]')
    u=sys.argv[0]+"?mode=search&name="+urllib.quote_plus('PPS搜索')+"&id="
    xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)

##################################################################################
# Routine to search PPS based on user input string
##################################################################################
def Search(mname):
    if (mname == "PPS搜索"):
        #kb=xbmc.Keyboard('','输入所查影片中文信息-拼音或简拼(拼音首字母)',False)
        keyboard = ChineseKeyboard.Keyboard('','输入所查影片中文信息-拼音或简拼(拼音首字母)')
        xbmc.sleep( 1500 )
        keyboard.doModal()
        keyword=keyboard.getText()
        
        #url="http://www.soso.com/wh.q?w="+keyword
        url ='http://video.soso.com/smart.php?w='+keyword
        link = getHttpData(url)
        link = link.decode('GB18030').encode('UTF-8')

        #match=re.compile("    (.+?)    ").findall(link)
        match=re.compile("[0-9]+[,0-9]*[,0-9]*(.+?)0").findall(link)
        for i in range(0,len(match)):
            p_name = match[i].strip()
            p_list = str(i+1) + ': ' + p_name
            li=xbmcgui.ListItem(p_list)
            u=sys.argv[0]+"?mode=search&name="+urllib.quote_plus(p_name)+"&id="
            xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)        
    else:
        url="http://listso.ppstream.com/search.php?acp=936&w="+urllib.quote_plus(mname)
        text = getHttpData(url)
##        file=open('aa.txt','w')
##        file.write(mname)
##        file.close()
        text = text.decode('GB18030').encode('UTF-8')
        text = text.replace('gb18030', 'utf-8')
        text = text.replace('GB18030', 'utf-8')

        root = ElementTree.fromstring(text)
        #文件
        lst_node = root.getiterator("Ch")
        i=0
        for node in lst_node:
            try:     
                i+=1
                CHON=0
                CHBKID=""
                CHBKVM=0.0
                node_findall = node.find("ID")
                CHID=node_findall.attrib['ID']

                try:    CHON=int(node.attrib['ON'])               
                except: pass
                try:    CHBKID=node_findall.attrib['BKID']
                except: pass
                try:    CHBKVM=float(node_findall.attrib['VM'])
                except: pass
                try:
                    cs=node_findall.attrib['search']
                    yy=re.compile('(.+?):(.+?):(.+?):(.+?);').findall(cs)
                except: pass

                node_findall = node.find("Name")
                CHName=node_findall.text

                node_findall = node.find("URL")
                CHURL=node_findall.text

                # ok=dialog.ok(CHName,CHName)
                li=xbmcgui.ListItem(CHName)
                try:     li.setInfo( type="Video", infoLabels={"Title":CHName, "count": CHON, "Rating":CHBKVM, "CODE":CHBKID,"Year":int(yy[0][3])})
                except:  li.setInfo( type="Video", infoLabels={"Title":CHName, "count": CHON, "Rating":CHBKVM, "CODE":CHBKID})
                u=sys.argv[0]+"?mode=ch&name="+CHName+"&id="+CHID+"&url="+urllib.quote_plus(CHURL.encode('gb18030'))
                xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,False)
            except:
                pass
        
        #次目录
        lst_node = root.getiterator("Sub")
        for node in lst_node:
            li=xbmcgui.ListItem('[COLOR FF00FF00]['+node.attrib['name']+'][/COLOR]')
            try:
                li.setInfo( type="Video", infoLabels={"Title":node.attrib['name'], "count": int(get_params2(node.attrib['op'])["on"])})
            except:
                pass
            u=sys.argv[0]+"?mode=sub&name="+node.attrib['name']+"&id="+node.attrib['id']
            xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)
        
def KankanPlay(url):
#    if (os.name == 'nt'):
#        xbmc.executebuiltin('System.ExecWait(\\"'+ os.getcwd()+'\\resources\\player\\pps4xbmc\\" '+url.decode("gbk").encode("utf8")+')')
#    else:
#        xbmc.executebuiltin('System.ExecWait(\\"'+ os.getcwd()+'\\resources\\player\\pps4xbmc\\" '+url.decode("gbk").encode("utf8")+')')
     xbmc.executebuiltin('System.ExecWait(\\"' + __cwd__ + '\\resources\\player\\pps4xbmc\\" ' + url.decode("gbk").encode("utf8") + ')')

##################################################################################
# Routine to fetch system parameters
##################################################################################
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

def get_params2(dd):
        param=[]
        paramstring=dd
        if len(paramstring)>=2:
                params=dd
                cleanedparams=params.replace("'",'')
                pairsofparams=cleanedparams.split(';')
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
id=None

try:
    url=urllib.unquote_plus(params["url"])
except:
    pass
try:
    name=urllib.unquote_plus(params["name"])
except:
    pass
try:
    id=urllib.unquote_plus(params["id"])
except:
    pass
try:
    mode=urllib.unquote_plus(params["mode"])
except:
    pass

#print mode, name , id
if mode==None:
    name='pps'
    read_xml("generas")
elif mode=="gen":
    read_xml(id)
elif mode=="sub":
    read_xml(id,0)
elif mode=="ch":
    KankanPlay(url)
elif mode=="search":
    Search(name)

xbmcplugin.addSortMethod(int(sys.argv[1]), 1)  #1 名称
xbmcplugin.addSortMethod(int(sys.argv[1]), 18) #18 评价
xbmcplugin.addSortMethod(int(sys.argv[1]), 17) #16 年份
xbmcplugin.addSortMethod(int(sys.argv[1]), 20) #20 播放次数
xbmcplugin.setPluginCategory(int(sys.argv[1]), name )
xbmcplugin.endOfDirectory(int(sys.argv[1]))
    