# -*- coding: utf-8 -*-
import xbmc, xbmcgui, xbmcaddon,  xbmcplugin
import sys, urllib, urlparse

if sys.version_info < (2, 7):
	import simplejson
else:
	import json as simplejson

class BaiduFmPlayer(xbmc.Player):
	def __init__(self):
		xbmc.Player.__init__(self)
		self.songIds = []
		self.channelId = None
		self.channelName = None
		self.playing = False
	
	def genPluginUrl(self, params):
		utf8Params = {}
		for key, value in params.iteritems():
			utf8Params[key] = unicode(value).encode('utf-8')
		return self.pluginName + "?" + urllib.urlencode(utf8Params)
	
	def getParam(self, key):
		if self.params.has_key(key):
			return self.params[key]
		else:
			return None
		
	def parseArgv(self, argv):
		print argv
		self.pluginName = argv[0]
		self.windowId = int(argv[1])
		self.params = dict(urlparse.parse_qsl(argv[2][1:]))

		action = self.getParam("action")

		if action == None:
			self.loadChannelList()
		elif action == "playchannel":
			self.channelId = self.getParam("channel_id");
			self.channelName = self.getParam("channel_name");
			self.loadSongList(self.channelId)
			self.next()

	def pushSongId(self, id):
		self.songIds.append(id)

	def loadChannelList(self):
		html = urllib.urlopen("http://fm.baidu.com").read()
		start = html.find("{", html.find("rawChannelList"))
		end = html.find(";", start);
		json = simplejson.loads(html[start:end].strip())
		self.onChannelListLoaded(json["channel_list"])
	
	def onChannelListLoaded(self, channelList):
		for channel in channelList:
			channelId = channel["channel_id"]
			channelName = channel["channel_name"]
			item = xbmcgui.ListItem(channel["channel_name"])
			url = self.genPluginUrl({"action":"playchannel","channel_id":channelId,"channel_name":channelName})
			xbmcplugin.addDirectoryItem(self.windowId, url, item)
			#print url
		xbmcplugin.setContent(self.windowId, 'music')
		xbmcplugin.endOfDirectory(self.windowId)

	def loadSongList(self, channelId):
		html = urllib.urlopen("http://fm.baidu.com/dev/api/?tn=playlist&format=json&id="+urllib.quote(channelId)).read()
		json = simplejson.loads(html)
		for song in json["list"]:
			self.pushSongId(song["id"])

	def playId(self, id):
		id = str(id)
		html = urllib.urlopen("http://music.baidu.com/data/music/fmlink?type=mp3&rate=320&songIds="+urllib.quote(id)).read()
		json = simplejson.loads(html)
		xcode = json["data"]["xcode"]
		for song in json["data"]["songList"]:
			if song["queryId"] == id:
				listItem = xbmcgui.ListItem(song["songName"], thumbnailImage=song["songPicRadio"])
				listItem.setInfo(type="music", infoLabels={"Title":song["songName"],"Artist":song["artistName"],"Album":song["albumName"],"Genre":self.channelName})
				#print song
				self.playing = True
				self.play(song["songLink"] + "?xcode=" + xcode, listItem)
				return
		self.next()

	def next(self):
		if len(self.songIds) <= 0:
			self.loadSongList(self.channelId)

		id = self.songIds.pop(0)
		self.playId(id)
	
	def shouldClose(self):
		return not self.playing

	def onPlayBackEnded(self):
		self.next()

	def onPlayBackStopped(self):
		self.playing = False

player = BaiduFmPlayer()
player.parseArgv(sys.argv)

while(not player.shouldClose()):
	xbmc.sleep(1000)
