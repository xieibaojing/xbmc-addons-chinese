import xbmc, xbmcgui, xbmcplugin, xbmcaddon, urllib2, urllib, re, sys, os, datetime, time, gzip, StringIO, random, ChineseKeyboard

#支持搜狐高清视频、优酷视频、天翼高清、新浪视频、奇艺、腾讯的影片搜索，若网站支持也可以查到演员、简介等相关视频
#使用前需保证上述视频插件已经安装，并且插件目录名未做修改。
#by visualcjy@21cn.com 20100725. 
#首发于http://bbs.htpc1.com
#20110129 修改适应google搜索的变化
#20110712 fxfboy@gmail.com 大幅修改，只保留了原来的插件id，使用百度输入法，需要安装基于百度输入法的中文输入法插件

# Plugin constants 
__addonname__ = "搜索电影"
__addonid__ = "plugin.video.somovie"
__addon__ = xbmcaddon.Addon(id=__addonid__)

CHANNEL_LIST = [['搜狐高清','11','plugin.video.sohuvideo'], ['优酷视频','12','plugin.video.youku'], ['奇艺视频','13','plugin.video.qiyi'], ['腾讯视频','14','plugin.video.tencent'], ['新浪视频','15','plugin.video.sina'], ['天翼高清','16','plugin.video.netitv'], ['土豆视频','17','plugin.video.tudou'], ['音悦台MV','18','plugin.video.yinyuetai']]

class SmartRedirectHandler(urllib2.HTTPRedirectHandler):
	def	http_error_301(self,req,fp,code,msg,headers):
		result=urllib2.HTTPRedirectHandler.http_error_301(self,req,fp,code,msg,headers)
		result.status=code
		return result
	def	http_error_302(self,req,fp,code,msg,headers):
		result=urllib2.HTTPRedirectHandler.http_error_302(self,req,fp,code,msg,headers)
		result.status=code
		return result
	
def	getPluginIcon(pluginId):
    plugin = xbmcaddon.Addon(id=pluginId)
    return os.path.join( plugin.getAddonInfo('path'), 'icon.png' )

def	getHttpData(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = urllib2.urlopen(req)
    httpdata = response.read()
    if response.headers.get('content-encoding', None) == 'gzip':
            httpdata = gzip.GzipFile(fileobj=StringIO.StringIO(httpdata)).read()
            response.close()
    match = re.compile('<meta http-equiv=["]?[Cc]ontent-[Tt]ype["]? content="text/html;[\s]?charset=(.+?)"').findall(httpdata)
    if len(match)>0:
            charset = match[0].lower()
            if (charset != 'utf-8') and (charset != 'utf8'):
                    httpdata=httpdata.decode(charset, 'ignore').encode('utf-8')
    return httpdata

def	decodeHtml(htmlstr):
    CHAR_ENTITIES={'nbsp':' ','160':' ',
            'lt':'<','60':'<',
            'gt':'>','62':'>',
            'amp':'&','38':'&',
            'quot':'"','34':'"',}
    re_charEntity=re.compile(r'&#?(?P<name>\w+);')
    sz=re_charEntity.search(htmlstr)
    while sz:
        entity=sz.group()#entity全称，如&gt;
        key=sz.group('name')#去除&;后entity,如&gt;为gt
        try:
                htmlstr=re_charEntity.sub(CHAR_ENTITIES[key],htmlstr,1)
                sz=re_charEntity.search(htmlstr)
        except KeyError:
                #以空串代替
                htmlstr=re_charEntity.sub('',htmlstr,1)
                sz=re_charEntity.search(htmlstr)
    return htmlstr

def	stripHtml(htmlstr):
    #先过滤CDATA
    re_cdata=re.compile('//<!\[CDATA\[[^>]*//\]\]>',re.I) #匹配CDATA
    re_script=re.compile('<\s*script[^>]*>[^<]*<\s*/\s*script\s*>',re.I)#Script
    re_script_1=re.compile(r'<script type="text/javascript">.+</script>',re.I)
    re_script_2=re.compile(r'<script>.+</script>',re.I)
    re_style=re.compile('<\s*style[^>]*>[^<]*<\s*/\s*style\s*>',re.I)#style
    re_br=re.compile('<br\s*?/?>')#处理换行
    re_h=re.compile('</?\w+[^>]*>')#HTML标签
    re_comment=re.compile('<!--[^>]*-->')#HTML注释
    r_doctype = re.compile(r'(?m)(<!DOCTYPE[\t\n\r ]+\S+[^\[]+?(\[[^\]]+?\])?\s*>)')
    r_script=re.compile(r'<!--\[if IE]>.+<!\[endif]-->',re.S)
    s=re_cdata.sub('',htmlstr)#去掉CDATA
    s=re_script.sub('',s) #去掉SCRIPT
    s=re_script_1.sub('',s)#strip script 
    s=re_script_2.sub('',s)
    s=re_style.sub('',s)#去掉style
    s=re_br.sub('\n',s)#将br转换为换行
    s=re_br.sub('\n\n',s)
    s=re_br.sub('\r\n',s)
    s=re_h.sub('',s) #去掉HTML 标签
    s=re_comment.sub('',s)#去掉HTML注释
    s=r_doctype.sub('',s)
    s=r_script.sub('',s)
    #去掉多余的空行
    blank_line=re.compile('\n+')
    s=blank_line.sub('\n',s)
    return s
       
def createTempThumb(image_url):
	temp_dir = os.path.abspath(os.path.join(os.getcwd(), 'temp'))
	if not os.path.exists(temp_dir):
		os.mkdir(temp_dir)
	imagedata = urllib2.urlopen(image_url).read()
	f_name = str(random.randint(0,10000))
	f_name = os.path.join(temp_dir, f_name+'.jpg')
	f_image = open(f_name, 'wb')
	f_image.write(imagedata)
	f_image.flush()
	f_image.close()
	return f_name

def clearTempThumb():
	temp_dir = os.path.abspath(os.path.join(os.getcwd(), 'temp'))
	if os.path.isdir(temp_dir):
		for f in os.listdir(temp_dir):
			file = os.path.join(temp_dir, f)
			if os.path.exists(file):
				os.remove(file)

def	getTotalPages(items,count):
	if items > 0:
		totalpages = int(items / count)
		if (items % count) > 0:
			totalpages = totalpages + 1;
	else:
		totalpages = 0
	return totalpages

def getKeyword():
	keyword = None
	try:
		keyword = __addon__.getSetting("keyword")
	except:
		pass
	return keyword

def setKeyword(keyword):
	__addon__.setSetting(id="keyword", value=keyword)
	
def getHistoryCount():
	showHistory = int(__addon__.getSetting('history'))
	if showHistory == 0:
		histCount=0
	elif showHistory==1:
		histCount=20
	elif showHistory==2:
		histCount=10
	elif showHistory==3:
		histCount=5
	else:
		histCount=10
	return histCount
	
def loadHistory():
	histCount=getHistoryCount()
	if histCount==0:
		return []
	path = os.path.join(os.getcwd(), 'history.txt')
	if not os.path.exists(path):
		return []
	if not os.path.isfile(path):
		return []
	file = open(path, 'r')
	try:
		lines = file.readlines()
		result = []
		for line in lines:
			line = line.replace(os.linesep, '')
			result.append(line)
			if len(result)==histCount:
				break
		return result
	finally:
		file.close()
	return []

def saveHistory(keyword):
	showHistory = __addon__.getSetting('history')
	histCount=getHistoryCount()
	if histCount==0:
		return
	path = os.path.join(os.getcwd(), 'history.txt')
	if os.path.exists(path):
		if not os.path.isfile(path):
			return
	history = loadHistory()
#	for item in history:
#		print item
	pos = -1
	try:
		pos = history.index(keyword)
	except:
		pass
	if pos > -1:
		del history[pos]
	while len(history)>histCount-1:
		history.pop()
	history.insert(0, keyword)
#	for item in history:
#		print item
	file = open(path, 'w')
	try:
		for i in range(0, len(history)):
			line = history[i]
			if i < len(history)-1:
				line += os.linesep
			file.write(line)
	finally:
		file.close()

def	rootList():
	setKeyword('')
	u=sys.argv[0]+"?mode=0"
	addDir(u, "输入搜索内容", "")
	# Show history if history exist
	history = loadHistory()
	if len(history)>0:
		for keyword in history:
			u=sys.argv[0] + "/?mode=0&history=" + keyword
			addDir(u, '搜索"[COLOR FFFF0000]' + keyword + '[/COLOR]"', '')
		u=sys.argv[0] + "?mode=1"
		addItem(u, "清除历史记录", '')
	xbmcplugin.endOfDirectory(int(sys.argv[1]))

def searchSite(history):
	if history:
		setKeyword('')
		for name,id,pluginId in CHANNEL_LIST:
			u=sys.argv[0]+"?mode="+id+"&plugin="+pluginId+'&keyword='+history
			addDir(u, '从【[COLOR FF00FF00]' + name + '[/COLOR]】搜索"[COLOR FFFF0000]' + history + '[/COLOR]"', getPluginIcon(pluginId))
		xbmcplugin.endOfDirectory(int(sys.argv[1]))
	else:
		keyword = getKeyword()
		if len(keyword)>0:
			for name,id,pluginId in CHANNEL_LIST:
				u=sys.argv[0]+"?mode="+id+"&plugin="+pluginId+'&keyword='+keyword
				addDir(u, '从【[COLOR FF00FF00]' + name + '[/COLOR]】搜索"[COLOR FFFF0000]' + keyword + '[/COLOR]"', getPluginIcon(pluginId))
			xbmcplugin.endOfDirectory(int(sys.argv[1]))
		else:
			xbmcplugin.endOfDirectory(int(sys.argv[1]))
			setKeyword('')
			popupSearch()

def	clearHistory():
	setKeyword('')
	path = os.path.join(os.getcwd(), 'history.txt')
	try:
		os.remove(path)
	except:
		pass
	xbmc.executebuiltin('Container.Refresh')

def	popupSearch():
	keyboard = ChineseKeyboard.Keyboard('','请输入搜索内容')
	keyboard.doModal()
	if (keyboard.isConfirmed()):
		keyword = keyboard.getText()
		__addon__.setSetting(id="keyword", value=keyword)
		saveHistory(keyword)
		xbmc.executebuiltin('Container.Refresh')

def	searchSohu(keyword, page,plugin):
	print 'searchSohu('+keyword+')'
	if page:
		currpage = page
	else:
		currpage = 1
	if page:
		url = 'http://so.tv.sohu.com/mts?&wd='+urllib.quote_plus(keyword.decode('utf-8').encode('gb2312'))+'&chl=&fee=0&tvType=-2&whole=1&blog=1&p=' + str(page)
	else:
		url = 'http://so.tv.sohu.com/mts?wd=' + urllib.quote_plus(keyword.decode('utf-8').encode('gb2312'))
	print url
	html = getHttpData(url)
	html = re.sub("\r|\n|\t","",html)
	match = re.compile('<h1>.+?<span>(\d+?)</span>.+?</h1>').search(html)
	if match:
		totalItems = int(match.group(1))
	else:
		totalItems = 0;
	totalpages = getTotalPages(totalItems, 20)
	if totalItems == 0:
		addItem('', '抱歉，没有找到[COLOR FFFF0000]'+keyword+'[/COLOR]的相关视频', getPluginIcon(plugin))
	else:
		addItem('', '第'+str(currpage)+'/'+str(totalpages)+'页,【搜狐站内搜索"[COLOR FFFF0000]'+keyword+'[/COLOR]",共找到'+str(totalItems)+'个视频】', getPluginIcon(plugin))
		match=re.compile('<div class="list_pack">(.+?)</div></div>').findall(html)
		for item in match:
			v_link = re.compile('<a class="img" (.+?)></a>').findall(item)[0]
			p_url = re.compile('href="(.+?)"').findall(v_link)[0]
			match1 = re.compile('<img src="(.+?)" alt="(.+?)" width="120">').search(v_link)
			p_thumb = match1.group(1)
			p_name = decodeHtml(match1.group(2))
			match1 = re.compile('<span class="type">(.+?)</span>').search(item)
			p_type = ''
			p_ispay = ''
			isTeleplay = False
			if match1:
				p_type = match1.group(1)
			if p_type=='[电视剧]':
				isTeleplay = True
				p_type='【[COLOR FF00FF00]电视剧[/COLOR]】'
			elif p_type=='[电影]':
				p_type='【[COLOR FF00FF00]电影[/COLOR]】'
			if item.find('<em class="pay"></em>')>0:
				p_ispay = '【[COLOR FFFF0000]付费[/COLOR]】'
			if isTeleplay:
				u= 'plugin://'+plugin+'/?mode=2&url=http://so.tv.sohu.com'+urllib.quote_plus(p_url)+'&name='+urllib.quote_plus(p_name)+"&thumb="+urllib.quote_plus(p_thumb)
				addDir(u, p_type + p_name + p_ispay, p_thumb)
			else:
				u= 'plugin://'+plugin+'/?mode=3&url=http://so.tv.sohu.com'+urllib.quote_plus(p_url)+'&name='+urllib.quote_plus(p_name)+"&thumb="+urllib.quote_plus(p_thumb)
				addItem(u, p_type + p_name + p_ispay, p_thumb) 
		if currpage > 1:
			u = sys.argv[0]+'?mode=11&plugin='+plugin+'&page='+str(currpage-1)+'&keyword='+keyword
			addDir(u, '上一页', '')
		if currpage < totalpages:
			u = sys.argv[0]+'?mode=11&plugin='+plugin+'&page='+str(currpage+1)+'&keyword='+keyword
			addDir(u, '下一页', '')
	xbmcplugin.setContent(int(sys.argv[1]), 'movies')
	xbmcplugin.endOfDirectory(int(sys.argv[1]))

def	searchYouku(keyword, page,plugin):
	print 'SearchYouKu('+keyword+')'
	clearTempThumb()
	if page:
		currpage = page
	else:
		currpage = 1
	if page:
		url="http://www.soku.com/search_video/q_"+urllib.quote_plus(keyword)+'_orderby_1_page_'+str(page)
	else:
		url="http://www.soku.com/search_video/q_"+urllib.quote_plus(keyword)
	print url
	html = getHttpData(url)
	html = re.sub("\r|\n|\t","",html)
	match = re.compile('<div class="stat">共找到(.+?)个结果</div>').search(html)
	if match:
		totalItems = int(match.group(1))
	else:
		totalItems = 0;
	totalpages = getTotalPages(totalItems, 20)
	if totalItems == 0:
		addItem('', '抱歉，没有找到[COLOR FFFF0000]'+keyword+'[/COLOR]的相关视频', getPluginIcon(plugin))
	else:
		addItem('', '第'+str(currpage)+'/'+str(totalpages)+'页,【优酷站内搜索"[COLOR FFFF0000]'+keyword+'[/COLOR]",共找到'+str(totalItems)+'个视频】', getPluginIcon(plugin))
		# 2011/11/28 update start (Added the direct search result)
		match=re.compile('<div class="item">(.+?)</div><!--item end-->').findall(html)
		print str(len(match))
		for item in match:
			v_link = re.compile('<li class="base_name">(.+?)</li>').findall(item)[0]
			v_link = re.compile('href="([^"]*)"').findall(v_link)[0]
			print 'v_link=' + v_link
			if (v_link.find('http://www.youku.com') < 0):
				# Not in youku
				continue
			if (item.find('<div class="tv">') > -1):
				p_type = 'tv'
			elif (item.find('<div class="movie">') > -1):
				p_type = 'movie'
			else:
				p_type = 'other'
			print 'p_type=' + p_type
			p_name = stripHtml(re.compile('<h1>(.+?)</h1>').findall(item)[0])
			print 'p_name=' + p_name
			p_id = re.compile('http://www.youku.com/show_page/id_(.+?).html').findall(v_link)[0]
			p_url = v_link;
			print 'p_id=' + p_id
			p_thumb = re.compile('<li class="p_thumb">(.+?)</li>').search(item)
			if p_thumb:
				p_thumb = re.compile('src="(.+?)"').search(p_thumb.group(1))
				if p_thumb:
					p_thumb = p_thumb.group(1)
			if p_thumb and len(p_thumb) > 0:
				p_thumb = createTempThumb(p_thumb)
			p_ishd = re.compile('<li class="v_ishd"><span ([^>]*)></span>').findall(item)
			if len(p_ishd) > 0:
				if p_ishd[0].find('ico__SD') > 0:
					p_res = 2
					p_name += '[超清]'
				elif p_ishd[0].find('ico__HD') > 0:
					p_res = 1
					p_name += '[高清]'
				else:
					p_res = 0
			else:
				p_res = 0
			li=xbmcgui.ListItem(p_name,p_name,p_thumb,p_thumb)
			if p_type=='tv':
				u='plugin://'+plugin+'/?mode=3&name='+urllib.quote_plus(p_name)+'&id='+urllib.quote_plus(p_id)+'&thumb='+urllib.quote_plus(p_thumb)+'&page=1'
				addDir(u, '【[COLOR FF00FF00]电视剧】[/COLOR] ' + p_name, p_thumb)
			elif p_type=='movie':
				u='plugin://'+plugin+'/?mode=10&name='+urllib.quote_plus(p_name)+'&url='+urllib.quote_plus(p_url)+'&thumb='+urllib.quote_plus(p_thumb)+'&res=' + str(p_res)
				addItem(u, '【[COLOR FF00FF00]电影】[/COLOR] ' + p_name, p_thumb)
			else:
				u='plugin://'+plugin+'/?mode=10&name='+urllib.quote_plus(p_name)+'&url='+urllib.quote_plus(p_url)+'&thumb='+urllib.quote_plus(p_thumb)+'&res=' + str(p_res)
				addItem(u, p_name, p_thumb)
		# 2011/11/28 update end
		match=re.compile('<ul class="v">(.+?)</ul>').findall(html)
		for item in match:
			v_link = re.compile('<li class="v_link"><a([^>]*)></a></li>').findall(item)[0]
			p_name = decodeHtml(re.compile('title="([^"]*)"').findall(v_link)[0])
			p_url = re.compile('href="(.+?)"').findall(v_link)[0]
			p_thumb = re.compile('<li class="v_thumb">(.+?)</li>').search(item)
			if p_thumb:
				p_thumb = re.compile('src="(.+?)"').search(p_thumb.group(1))
				if p_thumb:
					p_thumb = p_thumb.group(1)
			if p_thumb and len(p_thumb) > 0:
				p_thumb = createTempThumb(p_thumb)
			p_ishd = re.compile('<li class="v_ishd"><span ([^>]*)></span>').findall(item)
			if len(p_ishd) > 0:
				if p_ishd[0].find('ico__SD') > 0:
					p_res = 2
					p_name += '[超清]'
				elif p_ishd[0].find('ico__HD') > 0:
					p_res = 1
					p_name += '[高清]'
				else:
					p_res = 0
			else:
				p_res = 0
			li=xbmcgui.ListItem(p_name,p_name,p_thumb,p_thumb)
			u='plugin://'+plugin+'/?mode=10&name='+urllib.quote_plus(p_name)+'&url='+urllib.quote_plus(p_url)+'&thumb='+urllib.quote_plus(p_thumb)+'&res=' + str(p_res)
			addItem(u, p_name, p_thumb)
		if currpage > 1:
			u = sys.argv[0]+'?mode=12&plugin='+plugin+'&page='+str(currpage-1)+'&keyword='+keyword
			addDir(u, '上一页', '')
		if currpage < totalpages:
			u = sys.argv[0]+'?mode=12&plugin='+plugin+'&page='+str(currpage+1)+'&keyword='+keyword
			addDir(u, '下一页', '')
	xbmcplugin.setContent(int(sys.argv[1]), 'movies')
	xbmcplugin.endOfDirectory(int(sys.argv[1]))

def	searchQiyi(keyword, page,plugin):
	print 'searchQiyi('+keyword+')'
	word = urllib.quote_plus(keyword).replace('%','_')
	if page:
		currpage = page
	else:
		currpage = 1

	if page:
		url='http://search.video.qiyi.com/search/' + word + '/' + str(currpage) + '/1/_20/10/www'
	else:
		url='http://search.video.qiyi.com/search/' + word + '/0/1/_20/10/www/'
	print url
	html = getHttpData(url)
	match = re.compile('<script type="text/javascript">frameElement.callback\((.+?)\);</script></head>').search(html)
	jsondata = match.group(1)
	match = re.compile('"sumCounts":(\d+),').search(jsondata)
	if match:
		totalItems = int(match.group(1))
	else:
		totalItems = 0;
	totalpages = getTotalPages(totalItems, 10)
	if totalItems == 0:
		addItem('', '抱歉，没有找到[COLOR FFFF0000]'+keyword+'[/COLOR]的相关视频', getPluginIcon(plugin))
	else:
		addItem('', '第'+str(currpage)+'/'+str(totalpages)+'页,【奇艺站内搜索"[COLOR FFFF0000]'+keyword+'[/COLOR]",共找到'+str(totalItems)+'个视频】', getPluginIcon(plugin))
		match = re.compile('"list":\[(.+?)\]').search(jsondata)
		items = re.compile('{(.+?)}').findall(match.group(1))
		for item in items:
			p_name = re.compile('"VrsVideoTv.tvName":"(.+?)",').findall(item)[0]
			p_name = p_name.replace('\/', '/')
			p_name = stripHtml(decodeHtml(p_name))
			p_url = re.compile('TvApplication.purl":"(.+?)",').findall(item)[0]
			p_thumb = re.compile('"vrsVideoTv.TvBigPic":"(.+?)",').findall(item)[0]
			p_type = re.compile('"category":"(.+?)",').findall(item)[0]
			li=xbmcgui.ListItem(p_name,p_name,p_thumb,p_thumb)
			if p_type=='电视剧':
				u='plugin://'+plugin+'/?mode=3&name='+urllib.quote_plus(p_name)+'&url='+urllib.quote_plus(p_url)+'&thumb='+urllib.quote_plus(p_thumb)
				addDir(u, '['+p_type+']'+p_name, p_thumb)
			else:
				u='plugin://'+plugin+'/?mode=2&name='+urllib.quote_plus(p_name)+'&url='+urllib.quote_plus(p_url)+'&thumb='+urllib.quote_plus(p_thumb)
				addItem(u, '['+p_type+']'+p_name, p_thumb)
		if currpage > 1:
			u = sys.argv[0]+'?mode=13&plugin='+plugin+'&page='+str(currpage-1)+'&keyword='+keyword
			addDir(u, '上一页', '')
		if currpage < totalpages:
			u = sys.argv[0]+'?mode=13&plugin='+plugin+'&page='+str(currpage+1)+'&keyword='+keyword
			addDir(u, '下一页', '')
	xbmcplugin.setContent(int(sys.argv[1]), 'movies')
	xbmcplugin.endOfDirectory(int(sys.argv[1]))

def	searchTencent(keyword, page,plugin,a1,a2,st):
	print 'searchTencent('+keyword+')'
	if page:
		currpage = page
	else:
		currpage = 1
	if not st:
		st = 1
	print 'st='+str(st)
	if page:
		url="http://sns.video.qq.com/fcgi-bin/search_c?pagetype=3&ms_key="+urllib.quote_plus(keyword)+'&ms_search_type='+str(st)+'&ms_sort=0&nds=1&uin=0&ms_type=&a1='+str(a1)+'&a2='+str(a2)+'&mi_pagenum='+str(currpage-1)
	else:
		url="http://sns.video.qq.com/fcgi-bin/search_c?pagetype=3&ms_key="+urllib.quote_plus(keyword)
	print url
	html = getHttpData(url)
	html = re.sub("\r|\n|\t","",html)
	match = re.compile('<strong class="c_txt3" id="s_a1">(\d+)</strong>.+?<strong class="c_txt3" id="s_a2">(\d+)</strong>').search(html)
	if match:
		a1 = int(match.group(1))
		a2 = int(match.group(2))
		if st == 1:
			totalItems = a1
		else:
			totalItems = a2
	else:
		totalItems = 0
	totalpages = getTotalPages(totalItems, 10)
	if totalItems == 0:
		addItem('', '抱歉，没有找到[COLOR FFFF0000]'+keyword+'[/COLOR]的相关视频', getPluginIcon(plugin))
	else:
		if st==1:
			st_str = '专辑'
		else:
			st_str = '视频'
		u = sys.argv[0]+'?mode=2&plugin='+plugin+'&page=1&a1='+str(a1)+'&a2='+str(a2)+'&st='+str(st)+'&keyword='+keyword
		addDir(u, '第'+str(currpage)+'/'+str(totalpages)+'页, 腾讯站内搜索"[COLOR FFFF0000]'+keyword+'[/COLOR]",【[COLOR FF00FF00]'+st_str+'[/COLOR]】有'+str(totalItems)+'项结果', getPluginIcon(plugin))
		match=re.compile('<li class="bbor">(.+?)</li>').findall(html)
		for item in match:
			v_link = re.compile('<dt>(.+?)</dt>').findall(item)[0]
			links = re.compile('<a[^>]*>(.+?)</a>').findall(v_link)
			p_name = stripHtml(decodeHtml(links[0]))
			if len(links)>1:
				p_type = links[1]
			else:
				p_type = ''
			p_id = re.compile('playid="(.)(.+?)"').search(v_link)
			if st==1:
				p_url = 'http://v.qq.com/cover/'+p_id.group(1)+'/'+p_id.group(1)+p_id.group(2)+'.html'
			else:
				p_url = p_id.group(1)+p_id.group(2)
			p_thumb = re.compile('<img src="(.+?)"').findall(item)[0]
			li=xbmcgui.ListItem(p_name,p_name,p_thumb,p_thumb)
			if p_type == '[电视剧]':
				u='plugin://'+plugin+'/?mode=2&name='+urllib.quote_plus(p_name)+'&url='+urllib.quote_plus(p_url)+'&thumb='+urllib.quote_plus(p_thumb)
				addDir(u, p_type+p_name, p_thumb)
			else:
				if st == 1:
					u='plugin://'+plugin+'/?mode=10&type=2&name='+urllib.quote_plus(p_name)+'&url='+urllib.quote_plus(p_url)+'&thumb='+urllib.quote_plus(p_thumb)
				else:
					u='plugin://'+plugin+'/?mode=3&name='+urllib.quote_plus(p_name)+'&url='+urllib.quote_plus(p_url)+'&thumb='+urllib.quote_plus(p_thumb)
				addItem(u, p_type+p_name, p_thumb)
		if currpage > 1:
			u = sys.argv[0]+'?mode=14&plugin='+plugin+'&page='+str(currpage-1)+'&a1='+str(a1)+'&a2='+str(a2)+'&st='+str(st)+'&keyword='+keyword
			addDir(u, '上一页', '')
		if currpage < totalpages:
			u = sys.argv[0]+'?mode=14&plugin='+plugin+'&page='+str(currpage+1)+'&a1='+str(a1)+'&a2='+str(a2)+'&st='+str(st)+'&keyword='+keyword
			addDir(u, '下一页', '')
	xbmcplugin.setContent(int(sys.argv[1]), 'movies')
	xbmcplugin.endOfDirectory(int(sys.argv[1]))

def	searchSina(keyword, page, plugin):
	print 'searchSina('+keyword+')'
	if page:
		currpage = page
	else:
		currpage = 1

	if page:
		url='http://video.sina.com.cn/search/index.php?k=' + urllib.quote_plus(keyword) + '&page=' + str(currpage)
	else:
		url='http://video.sina.com.cn/search/index.php?k=' + urllib.quote_plus(keyword)
	print url
	
	html = getHttpData(url)
	html = re.sub("\r|\n|\t","",html)
	match = re.compile('<div class="box_hd"><h3>.+?([\d,]+).+?</h3></div>').search(html)
	if match:
		totalItems = int(match.group(1).replace(',',''))
	else:
		totalItems=0
	totalpages = getTotalPages(totalItems, 20)
	if totalItems == 0:
		addItem('', '抱歉，没有找到[COLOR FFFF0000]'+keyword+'[/COLOR]的相关视频', getPluginIcon(plugin))
	else:
		addItem('', '第'+str(currpage)+'/'+str(totalpages)+'页,【新浪站内搜索"[COLOR FFFF0000]'+keyword+'[/COLOR]",共找到'+str(totalItems)+'个视频】', getPluginIcon(plugin))
		h_html = re.compile("<!-- 横版结果 start -->(.+?)<!-- 横版结果  end -->").search(html)
		if h_html:
			html = h_html.group(1)
		items = re.compile('(<div class="videoPic vp120">.+?</div></div>)').findall(html)
		for item in items:
			item = re.sub('<!--[^>]*-->','', item)
			item = re.sub('>[\s]*<', '><', item)
			p_link = re.compile('<a title="(.+?)" class="plicon" href="(.+?)" [^>]*></a>').search(item)
			if p_link:
				p_name = p_link.group(1)
				p_name = stripHtml(decodeHtml(p_name))
				p_url = p_link.group(2)
			else:
				print 'Fail Item : ' + item
				continue
			p_thumb = re.compile('<img class="pic" src="(.+?)" [^>]*>').search(item)
			if p_thumb:
				p_thumb = p_thumb.group(1)
			else:
				p_thumb = getPluginIcon(plugin)
			p_type = re.compile('<div class="name"><a [^>]*>(.+?)</a>').search(item)
			if p_type:
				p_type = p_type.group(1)
			else:
				p_type = ''
			li=xbmcgui.ListItem(p_name,p_name,p_thumb,p_thumb)
			if p_type=='[电视]':
				u='plugin://'+plugin+'/?mode=2&name='+urllib.quote_plus(p_name)+'&url='+urllib.quote_plus(p_url)+'&thumb='+urllib.quote_plus(p_thumb)
				addDir(u, p_type+p_name, p_thumb)
			else:
				u='plugin://'+plugin+'/?mode=10&name='+urllib.quote_plus(p_name)+'&url='+urllib.quote_plus(p_url)+'&thumb='+urllib.quote_plus(p_thumb)
				addItem(u, p_type+p_name, p_thumb)
		if currpage > 1:
			u = sys.argv[0]+'?mode=15&plugin='+plugin+'&page='+str(currpage-1)+'&keyword='+keyword
			addDir(u, '上一页', '')
		if currpage < totalpages:
			u = sys.argv[0]+'?mode=15&plugin='+plugin+'&page='+str(currpage+1)+'&keyword='+keyword
			addDir(u, '下一页', '')
	xbmcplugin.setContent(int(sys.argv[1]), 'movies')
	xbmcplugin.endOfDirectory(int(sys.argv[1]))

def searchYinyuetai(keyword, page, plugin):
	print 'searchYinyuetai('+keyword+')'
	clearTempThumb()
	if page:
		currpage = page
	else:
		currpage = 1

	if page:
		url='http://www.yinyuetai.com/search/mv?keyword=' + urllib.quote_plus(keyword) + '&page=' + str(currpage)
	else:
		url='http://www.yinyuetai.com/search/mv?keyword=' + urllib.quote_plus(keyword)
	print url
	
	html = getHttpData(url)
	html = re.sub("\r|\n|\t","",html)
	html = re.sub('>[\s]*<', '><', html)
	match = re.compile('<div id="search_result_category"><span><a [^>]*>MV</a><em>\((.+?)\)</em>').search(html)
	if match:
		totalItems = int(match.group(1))
	else:
		totalItems=0
	totalpages = getTotalPages(totalItems, 20)
	if totalItems == 0:
		addItem('', '抱歉，没有找到[COLOR FFFF0000]'+keyword+'[/COLOR]的相关视频', getPluginIcon(plugin))
	else:
		addItem('', '第'+str(currpage)+'/'+str(totalpages)+'页,【音悦台站内搜索"[COLOR FFFF0000]'+keyword+'[/COLOR]",共找到'+str(totalItems)+'个MV】', getPluginIcon(plugin))
		h_html = re.compile('<div id="search_result_list">(.+?)</div><div id="footer">').search(html)
		if h_html:
			html = h_html.group(1)
		items = re.compile('<li [^>]*>(.+?)</li>').findall(html)
		for item in items:
			p_link = re.compile('<div class="thumb thumb_mv"><a .+? href="(.+?)" [^>]*><img alt="(.+?)" src="(.+?)"/>.+?</a></div>').search(item)
			if p_link:
				p_url = 'http://www.yinyuetai.com' + p_link.group(1)
				p_name = p_link.group(2)
				p_name = stripHtml(decodeHtml(p_name))
				p_thumb = 'http://www.yinyuetai.com' + p_link.group(3)
				p_thumb = createTempThumb(p_thumb)
			else:
				print 'Fail Item : ' + item
				continue
			p_artist = re.compile('<div class="artist" title="(.+?)" [^>]*>.+?</div>').search(item)
			if p_artist:
				p_artist = p_artist.group(1)
				p_artist = stripHtml(decodeHtml(p_artist))
			else:
				p_artist = ''
			if len(p_artist)>0:
				p_name = p_name + ' - ' + p_artist 
			u='plugin://'+plugin+'/?mode=255&name='+urllib.quote_plus(p_name)+'&url='+urllib.quote_plus(p_url)+'&artist='+urllib.quote_plus(p_artist)
			print 'p_thumb='+p_thumb
			addItem(u, p_name, p_thumb)
		if currpage > 1:
			u = sys.argv[0]+'?mode=18&plugin='+plugin+'&page='+str(currpage-1)+'&keyword='+keyword
			addDir(u, '上一页', '')
		if currpage < totalpages:
			u = sys.argv[0]+'?mode=18&plugin='+plugin+'&page='+str(currpage+1)+'&keyword='+keyword
			addDir(u, '下一页', '')
	xbmcplugin.setContent(int(sys.argv[1]), 'movies')
	xbmcplugin.endOfDirectory(int(sys.argv[1]))
	
def	searchUndefined():
	addItem('', '抱歉，对此站点的搜索还未推出，敬请期待...', '')
	xbmcplugin.endOfDirectory(int(sys.argv[1]))

def	addDir(u,name,img):
	li=xbmcgui.ListItem(name, img, img)
	xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,li,True)

def	addItem(u,name,img):
	l=xbmcgui.ListItem(name,img,img)
	xbmcplugin.addDirectoryItem(int(sys.argv[1]),u,l,False)

def	performChanges(keyword, page, plugin, a1, a2):
	change = False
	dialog = xbmcgui.Dialog()
	list = ['专辑', '视频'] 
	sel = dialog.select('类型', list)
	if sel != -1:
		change = True
	if change:
		searchTencent(keyword, page, plugin, a1, a2, sel + 1)


def	get_params():
	print sys.argv
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
page=None
plugin=None
keyword=None
a1=None
a2=None
st=None
history=None

try:
	mode=int(params["mode"])
except:
	pass

try:
	page=int(params["page"])
except:
	pass

try:
	plugin=params["plugin"]
except:
	pass

try:
	keyword=params["keyword"]
except:
	pass

try:
	a1=int(params["a1"])
except:
	pass

try:
	a2=int(params["a2"])
except:
	pass

try:
	st=int(params["st"])
except:
	pass

try:
	history=params["history"]
except:
	pass

if mode==None:
	rootList()
elif mode==0:
	searchSite(history)
elif mode==1:
	clearHistory()
elif mode==2:
	performChanges(keyword,page,plugin,a1,a2)
elif mode==11:
	saveHistory(keyword)
	searchSohu(keyword,page,plugin)
elif mode==12:
	saveHistory(keyword)
	searchYouku(keyword,page,plugin)
elif mode==13:
	saveHistory(keyword)
	searchQiyi(keyword,page,plugin)
elif mode==14:
	saveHistory(keyword)
	searchTencent(keyword,page,plugin,a1,a2,st)
elif mode==15:
	saveHistory(keyword)
	searchSina(keyword,page,plugin)
elif mode==18:
	saveHistory(keyword)
	searchYinyuetai(keyword,page,plugin)
else:
	searchUndefined()

