# declare file encoding 
# -*- coding: utf-8 -*-

# htpcyh2@gmail.com 2012年7月创作,于2012年7月11号首发到XBMC中文插件库
# 未经允许,不得用于商业用途


import urllib,urllib2,re,xbmcplugin,xbmcgui,subprocess,sys,os,os.path,time,datetime
import xml.dom.minidom
import socket
import fcntl
import struct


from urllib2 import urlopen
from urlparse import urlparse
from posixpath import basename, dirname


ROOT_DIR = os.getcwd()
sys.path.append(ROOT_DIR +'/resources/lib') 
import ElementTree

addon_icon=os.path.join(ROOT_DIR,'icon.png')
reload(sys)
sys.setdefaultencoding('utf-8')



def parse_url(url):
    parse_object = urlparse(url)
    try:
        return basename(parse_object[2])
    except:
        return 'chlist.xml'


def Downloader(url,dest,description,heading):
    dp = xbmcgui.DialogProgress()
    dp.create(heading)
    dp.create(heading,description,url)
    urllib.urlretrieve(url,dest,lambda nb, bs, fs, url=url: _pbhook(nb,bs,fs,description,url,dp))

def _pbhook(numblocks, blocksize, filesize,description, url=None,dp=None):
    try:
        percent = min((numblocks*blocksize*100)/filesize, 100)
        print percent
        dp.update(percent,description,url)
    except:
        percent = 100
        dp.update(percent,description,url)
    if dp.iscanceled(): 
        print "DOWNLOAD CANCELLED" 
        dp.close()
        

def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s', ifname[:15]) )[20:24])


OS = os.environ.get("OS","xbox")
localIP=get_ip_address('eth0')
addon_resources_path= os.path.join(os.getcwd(),'resources')
CHAN_LIST_URL = 'http://channel.sopserv.com/chlist.xml'
CHAN_LIST = '/tmp'
CHAN_LIST = os.path.join(CHAN_LIST, parse_url(CHAN_LIST_URL))


spsc_binary = "sp-sc-auth"
SPSC = os.path.join(addon_resources_path, 'sop')
SPSC = os.path.join(SPSC,spsc_binary)
SPSC_LIB = os.path.join(addon_resources_path, 'lib')
SPSC_LIB_PY = os.path.join(SPSC_LIB,'libstd.py')
SPSC_LIB = os.path.join(SPSC_LIB,'libstdc++.so.5')

sopcast_pid = "/tmp/sopcast.pid"
spec_log = "/tmp/sopcast.log"
wait_time = 20
LOCAL_PORT = 9000
VIDEO_PORT = 9001
BUF_SIZE = 1024 * 4
list_expire = 10000
Platform = "Linux"
my_error = 0
string = xbmc.getLocalizedString
LANGUAGE = "cn" #'cn' or 'en'
if OS != Platform:
    dialog = xbmcgui.Dialog()
    ok = dialog.ok('系统报告', '对不起!你所使用系统不支持本插件','请使用openELEC或XBMC Live等linux系统' )
else:
    os.chmod(SPSC,0755)
    

def getpid(name):
    """
        checks if a process with the given name exists
        returns the process' pid(s) or None
    """
    cmd = "ps -C %s -o pid=" % name
    pid = subprocess.Popen(cmd,shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    pid_out = pid.communicate()[0]

    list = []
    if len(pid_out) > 0:
        for item in pid_out.split():
            list.append(int(item))
        return list


def pid_exists(pid):
    try:
        os.kill(pid, 0)
        return 1
    except OSError, e:
        return 0



def PID_CHECK(OS,spsc_binary):
    print "OS",OS
    if OS == Platform:
        try:
            os.system('killall -9 %s' % (spsc_binary))        
            killed = 'YES'
            try:
                if killed == "YES":
                    return 1
            except:
                return
        except:
            return

def CHK_LIB():
    if not os.path.isfile(SPSC_LIB):
        os.rename(SPSC_LIB_PY, SPSC_LIB)


def FETCH_CHANNEL():
    if not os.path.isfile(CHAN_LIST):
        Downloader(CHAN_LIST_URL,CHAN_LIST,'请稍候','正在更新频道')
    else:
        for length in str(os.stat(CHAN_LIST)[6]).split('L'):
            if length == "0":
                Downloader(CHAN_LIST_URL,CHAN_LIST, '请稍候', '正在更新频道')
        now_time = time.mktime(datetime.datetime.now().timetuple())
        time_created = os.stat(CHAN_LIST)[8]
        if now_time - time_created > list_expire:
            Downloader(CHAN_LIST_URL,CHAN_LIST, '请稍候', '正在更新频道')
    GROUP(wait_time)



def GROUP(wait_time):
    result = CHAN_LIST
    try:
        response = ElementTree.parse(result)
        groups = response.findall('.//group')
        unname_group_index = 1
        for group in groups:
            if group.attrib[LANGUAGE] == "":
                group.attrib[LANGUAGE] = '未命名视频组'+str(unname_group_index)
                unname_group_index = unname_group_index + 1
                if re.sub('c','e',LANGUAGE) == LANGUAGE:
                    OTHER_LANG = re.sub('e','c',LANGUAGE)
                else:
                    OTHER_LANG = re.sub('c','e',LANGUAGE)
                if LANGUAGE == "cn":
                    try:
                        if len(group.attrib[OTHER_LANG]) > 0:
                            print group.attrib[OTHER_LANG]
                            group.attrib[LANGUAGE] = group.attrib[OTHER_LANG]
                            unname_group_index = unname_group_index - 1
                    except:
                        pass
            addDir(group.attrib[LANGUAGE],'',1,'',wait_time)
    except:
        dialog = xbmcgui.Dialog()
        dialog.ok(string(30000), string(30009), string(30010))
        f = open(CHAN_LIST,'w')
        f.write('')
        f.close()
        global my_error
        my_error = 1




def remove_line(contents):
    new_contents = []
    for line in contents:
        if not line.strip():
            continue
        else:
            new_contents.append(line)
    return "".join(new_contents)



def INDEX(name,wait_time):
    unname_group_index = 1
    dom = xml.dom.minidom.parse(CHAN_LIST)
    channel_list_root = dom.documentElement
    channel_groups = channel_list_root.getElementsByTagName('group')
    
    for channel_group in channel_groups:
        if channel_group.getAttribute(LANGUAGE) == "":
            channel_group.setAttribute(LANGUAGE, '未命名视频组'+str(unname_group_index))
            unname_group_index = unname_group_index + 1
            if LANGUAGE == "cn":
                try:
                    if len( channel_group.getAttribute('en') ) > 0:
                        channel_group.setAttribute(LANGUAGE, channel_group.getAttribute('en'))
                        unname_group_index = unname_group_index - 1
                except:
                    pass
        
        if name == channel_group.getAttribute(LANGUAGE):
            channel_chks = channel_group.getElementsByTagName('channel')
            for channel_chk in channel_chks:
                chan_id = channel_chk.getAttribute('id')
                chan_name='***'
                namelist = channel_chk.getElementsByTagName('name')
                channel_name = namelist[0]
                chan_cn_name = channel_name.getAttribute('cn')
                chan_en_name = channel_name.getAttribute('en')
                if LANGUAGE =='cn':
                    if chan_cn_name !='':
                        chan_name = chan_cn_name
                    else:
                        chan_name = chan_en_name
                else:
                    if chan_en_name !='':
                        chan_name = chan_en_name
                    else:
                        chan_name = chan_cn_name
                sop_item = channel_chk.getElementsByTagName('sop_address')[0]
                node = sop_item.getElementsByTagName('item')[0]
                rc = ""
                for node in node.childNodes:
                    if node.nodeType in ( node.TEXT_NODE, node.CDATA_SECTION_NODE):
                        rc = rc + node.data
                chan_url = rc
                node = channel_chk.getElementsByTagName('user_count')[0]
                rc = ""
                for node in node.childNodes:
                    if node.nodeType in ( node.TEXT_NODE, node.CDATA_SECTION_NODE):
                        rc = rc + node.data
                chan_users = rc
                node = channel_chk.getElementsByTagName('qc')[0]
                rc = ""
                for node in node.childNodes:
                    if node.nodeType in ( node.TEXT_NODE, node.CDATA_SECTION_NODE):
                        rc = rc + node.data
                chan_rcnetwork = rc
                i = 3 - len(rc)
                if i==1:
                    rc='0'+rc
                elif i==2:
                    rc='00'+rc
                
                i = 3 - len(chan_users)
                if i==1:
                    chan_users='0'+chan_users
                elif i==2:
                    chan_users='00'+chan_users
                network_q_str='[COLOR FF5555FF]网络质量:[/COLOR]'+'[COLOR FF00FFFF]'+rc+'[/COLOR] ' 
                users_str    ='[COLOR FF5555FF]人数:[/COLOR]' + '[COLOR FF00FFFF]' + chan_users + '[/COLOR]'
                chan_name_str='[COLOR FFFFFF00]'+chan_name+'[/COLOR]' 
                chan_name='[COLOR FF5555FF]【[/COLOR]' + network_q_str + users_str +'[COLOR FF5555FF]】[/COLOR]' + chan_name_str #FFFFFF00
                addLink(chan_name,chan_url,2,'',wait_time)



class streamplayer(xbmc.Player):
    def onplaybackended():
        print "killing sopcast process as playback ended"
        os.system('killall -9 %s' % (spsc_binary))
    def onPlayBackStopped(null):
        print null
        print "killing sopcast process as playback stopped"
        os.system('killall -9 %s' % (spsc_binary))



def wait(time,name):
    dp = xbmcgui.DialogProgress()
    mytime = 0
    dp.create('网络电视缓冲中' ,name , '请再等候'+str(time-mytime)+'秒')
    while mytime < time:
        try:
            percent = (mytime*100)/time
            dp.update(percent ,name,'请再等候'+str(time-mytime)+'秒')
        except:
            percent = 100
            dp.update(percent,'网路电视准备就绪')
        if dp.iscanceled():
            print "Streaming cancelled"
            dp.close()
            return 1
        if mytime >= 5:
            if spsc.poll() != None:
                dp.update(0,"网络电视下载失败","请稍后重试",'')
                xbmc.sleep(2000)
                dp.close()
                f = open(sopcast_pid, 'w')
                f.write('')
                f.close()
                mytime = time
                return 1
        mytime = mytime + 1
        xbmc.sleep(1000)
    if mytime == time:
        percent = 100
        dp.update(percent,"网路电视准备就绪")
    return 0






def STREAM(name,sop,wait_time):
    cmd = [SPSC, sop, str(LOCAL_PORT), str(VIDEO_PORT)]#,">", spec_log,"2>&1"]
    print "execute command", ' '.join(cmd)
    PID_CHECK(OS,spsc_binary)
    global spsc
    spsc = subprocess.Popen(cmd, shell=False, bufsize=BUF_SIZE ,stdin=None,stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    log = open(spec_log,'w')
    log.write('')
    log.close()
    subprocess.Popen("while read line; do echo $line >> "+spec_log+" ; done", shell=True,stdin=spsc.stdout,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    f = open(sopcast_pid, 'w')
    f.write(str(spsc.pid))
    f.close()
    if wait(wait_time,name) == 1:
        if PID_CHECK(OS,spsc_binary) == 1:
            rc = spsc.wait()
            f = open(sopcast_pid, 'w')
            f.write('')
            f.close()
        return
    url = "http://"+localIP+":"+str(VIDEO_PORT)+"/"
    listitem = xbmcgui.ListItem(name , thumbnailImage = addon_icon)
    listitem.setInfo('video', {'Title': name})
    player = streamplayer(xbmc.PLAYER_CORE_AUTO)
    player.play(url, listitem)



def addLink(name,url,mode,iconimage,wait_time):
    ok = True
    u=sys.argv[0]+"?"+"sop="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name.decode('utf8').encode('utf8'))+"&wait="+str(wait_time)
    liz = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name } )
    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz)
#    print "link", u
    return ok

def addDir(name,url,mode,iconimage,wait_time):
    u=sys.argv[0]+"?"+"mode="+str(mode)+"&name="+urllib.quote_plus(name.decode('utf8').encode('utf8'))+"&wait="+str(wait_time)
    ok = True
    liz = xbmcgui.ListItem(name, iconImage="DefaultFolder.png",thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name })
    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
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
    sop=urllib.unquote_plus(params["sop"])
except:
    pass
try:
    name=urllib.unquote_plus(params["name"].decode('utf8').encode('utf8'))
except:
    pass
try:
    mode=int(params["mode"])
except:
    pass
try:
    wait_time=int(params["wait"])
except:
    pass

if mode==None or name==None or len(name)<1:
    if OS == Platform:
        CHK_LIB()
        FETCH_CHANNEL()
elif mode==1:
    INDEX(name,wait_time)
elif mode==2:
    if xbmc.Player(xbmc.PLAYER_CORE_AUTO).isPlaying("http://"+localIP+":"+str(VIDEO_PORT)+"/"):
        xbmc.Player(xbmc.PLAYER_CORE_AUTO).stop()
        PID_CHECK(OS,spsc_binary)
        STREAM(name,sop,wait_time)
    else:
        STREAM(name,sop,wait_time)

if (OS == Platform) and (my_error == 0):
    xbmcplugin.endOfDirectory(int(sys.argv[1]))


