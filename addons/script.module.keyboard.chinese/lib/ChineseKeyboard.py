# -*- coding: utf-8 -*-

import os
import sys
from traceback import print_exc

import xbmc
import xbmcgui
from xbmcaddon import Addon


__settings__  = Addon( "script.module.keyboard.chinese" )
__addonDir__  = __settings__.getAddonInfo( "path" )

XBMC_SKIN  = xbmc.getSkinDir()
SKINS_PATH = os.path.join( __addonDir__, "resources", "skins" )
ADDON_SKIN = ( "default", XBMC_SKIN )[ os.path.exists( os.path.join( SKINS_PATH, XBMC_SKIN ) ) ]
MEDIA_PATH = os.path.join( SKINS_PATH, ADDON_SKIN, "media" )

ACTION_PARENT_DIR     = 9
ACTION_PREVIOUS_MENU  = 10
ACTION_CONTEXT_MENU   = 117

a = ['a','ai','an','ang','ao','ba','bai','ban','bang','bao','be','bei','ben','beng','bi','bia','bian','biao','bie','bin','bing','bo','bu','ca','cai','can','cang','cao','ce','cen','ceng','ceok','ceom','ceon','ceor','cha','chai','chan','chang','chao','che','chen','cheng','chi','chong','chou','chu','chua','chuai','chuan','chuang','chui','chun','chuo','ci','cis','cong','cou','cu','cuan','cui','cun','cuo','da','dai','dan','dang','dao','de','dei','dem','den','deng','di','dia','dian','diao','die','dim','ding','diu','dong','dou','du','duan','dui','dul','dun','duo','e','en','eng','eo','eol','eom','eos','er','fa','fan','fang','fei','fen','feng','fo','fou','fu','ga','gad','gai','gan','gang','gao','ge','gei','gen','geng','gib','go','gong','gou','gu','gua','guai','guan','guang','gui','gun','guo','ha','hai','hal','han','hang','hao','he','hei','hen','heng','ho','hol','hong','hou','hu','hua','huai','huan','huang','hui','hun','huo','hwa','i','ji','jia','jian','jiang','jiao','jie','jin','jing','jiong','jiu','jou','ju','juan','jue','jun','ka','kai','kal','kan','kang','kao','ke','kei','ken','keng','ki','kong','kos','kou','ku','kua','kuai','kuan','kuang','kui','kun','kuo','kweok','kwi','la','lai','lan','lang','lao','le','lei','li','lia','lian','liang','liao','lie','lin','ling','liu','lo','long','lou','lu','luan','lue','lun','luo','lv','m','ma','mai','man','mang','mao','me','mei','men','meng','meo','mi','mian','miao','mie','min','ming','miu','mo','mou','mu','myeo','myeon','myeong','n','na','nai','nan','nang','nao','ne','nei','nem','nen','neng','neus','ng','ngag','ngai','ngam','ni','nian','niao','nie','nin','ning','niu','nong','nou','nu','nuan','nue','nun','nung','nuo','nv','nve','o','oes','ol','on','ou','pa','pai','pak','pan','pang','pao','pei','pen','peng','peol','phas','phdeng','phoi','phos','pi','pian','piao','pie','pin','ping','po','pou','ppun','pu','q','qi','qia','qian','qiang','qiao','qie','qin','qing','qiong','qiu','qu','quan','que','qun','ra','ram','ran','rang','rao','re','ren','ri','rong','rou','ru','rua','ruan','rui','run','ruo','sa','saeng','sai','sal','san','sang','sao','se','sed','sei','sen','seng','seo','seon','sha','shai','shan','shang','shao','she','shen','sheng','shi','shou','shu','shua','shuai','shuan','shuang','shui','shun','shuo','shw','si','so','sol','song','sou','su','suan','sui','sun','suo','ta','tae','tai','tan','tang','tao','teng','ti','tian','tiao','tie','ting','tol','ton','tong','tou','tu','tuan','tui','tun','tuo','uu','wa','wai','wan','wang','wei','wen','weng','wie','wo','wu','xi','xia','xian','xiang','xiao','xie','xin','xing','xiong','xiu','xu','xuan','xue','xun','ya','yan','yang','yao','ye','yi','yin','ying','yo','yong','you','yu','yuan','yue','yun','za','zad','zai','zan','zang','zao','ze','zei','zen','zeng','zha','zhai','zhan','zhang','zhao','zhe','zhen','zheng','zhi','zhong','zhou','zhu','zhua','zhuai','zhuan','zhuang','zhui','zhun','zhuo','zi','zo','zong','zou','zu','zuan','zui','zun','zuo']
filename = os.path.join( __addonDir__, "lib", "pinyin.mb" )
fd = open( filename, 'r')
b = fd.read().split()
fd.close()

class InputWindow(xbmcgui.WindowXMLDialog):
	def __init__( self, *args, **kwargs ):
		self.action = None
		self.nowpage = 0
		xbmcgui.WindowXMLDialog.__init__( self, *args, **kwargs )

	def onInit(self):
		self.status = 0
		self.setKeyToChinese(0)
		self.getControl(101).setLabel('')
		self.getControl(2).setLabel('')
		self.confirmed = False
		self.inputString = ''

	def onFocus( self, controlId ):
		self.controlId = controlId

	def onClick( self, controlID ):
		if controlID == 332:#big
			self.status = 3
			self.setKeyToChinese(3)
		elif controlID == 333:#num
			self.status = 2
			self.setKeyToChinese(2)
		elif controlID == 335:#en
			self.status = 1
			self.setKeyToChinese(1)
		elif controlID == 336:#ch
			self.status = 0
			self.setKeyToChinese(0)
		elif controlID == 311:#back
			if self.status==0 and len(self.getControl(101).getLabel())>0:
				self.getControl(101).setLabel(self.getControl(101).getLabel()[0:-1])
				self.getChineseWord(self.getControl(101).getLabel())
			else:
				self.getControl(2).setLabel(self.getControl(2).getLabel().decode("utf-8")[0:-1])
		elif controlID == 321:#enter
			newText = self.getControl(2).getLabel()
			if not newText: return
			self.inputString = newText
			self.confirmed = True
			self.close()
			
		elif controlID == 601:#left
			if self.nowpage==0:
				self.nowpage =3
			else:
				self.nowpage -=1
			self.changepages()
		elif controlID == 602:#right
			if self.nowpage==3:
				self.nowpage =0
			else:
				self.nowpage +=1
			self.changepages()
		elif controlID == 334:#write
			self.getControl(2).setLabel(self.getControl(2).getLabel() + ' ')
		else:
			if self.status==0 and controlID!=329 and controlID!=330 and controlID!=331 and controlID<400:
				s = self.getControl(101).getLabel() + self.getControl(controlID).getLabel()
				self.getControl(101).setLabel(s)
				self.getChineseWord(s)
				#addfunction here
			else:
				self.getControl(2).setLabel(self.getControl(2).getLabel().decode("utf-8")+self.getControl(controlID).getLabel())
			
			if controlID>400 and controlID<500:
				self.setKeyToChinese(0)

	def onAction(self,action):
		#s1 = str(action.getId())
		#s2 = str(action.getButtonCode())
		#print "======="+s1+"========="+s2+"=========="
		keycode = action.getButtonCode()
		if keycode >= 61505 and keycode <= 61530:
			if self.status==0:
				keychar = chr(keycode - 61505 + ord('a'))
				s = self.getControl(101).getLabel() + keychar
				self.getControl(101).setLabel(s)
				self.getChineseWord(s)
			else:
				if self.status==3:
					keychar = chr(keycode - 61505 + ord('A'))
				else:
					keychar = chr(keycode - 61505 + ord('a'))
				self.getControl(2).setLabel(self.getControl(2).getLabel().decode("utf-8")+keychar)
				
		if action == ACTION_PARENT_DIR:
			self.onClick( 311 )
		elif action == ACTION_PREVIOUS_MENU:
			self.close()

	def changepages (self):
		tid = 151+self.nowpage
		self.getControl(151).setVisible(False)
		self.getControl(152).setVisible(False)
		self.getControl(153).setVisible(False)
		self.getControl(154).setVisible(False)
		self.getControl(tid).setVisible(True)
		
		self.getControl(601).controlRight(self.getControl(18*self.nowpage+401))
		self.getControl(602).controlLeft(self.getControl(18*self.nowpage+418))
		for i in range(301, 311):
			self.getControl(i).controlUp(self.getControl(18*self.nowpage+401))
		#print "R-->"+str(18*self.nowpage+401)

	def getChineseWord (self,py):
		self.nowpage = 0
		self.changepages()
		for i in range(401, 472):
			self.getControl(i).setLabel('')

		if py in a:
			words=b[a.index(py)]
			keyid=401
			for i in range(0, len(words), 2):
				self.getControl(keyid).setLabel(unicode(words[i:(2+i)],'gbk').encode('utf-8'))
				keyid+=1
				if keyid > 472: break

	def setKeyToChinese (self,t):
		#print "========="+str(t)
		if t==0 or t==1:		
			self.getControl(101).setLabel('')
			self.getControl(301).setLabel("q")
			self.getControl(302).setLabel("w")
			self.getControl(303).setLabel("e")
			self.getControl(304).setLabel("r")
			self.getControl(305).setLabel("t")
			self.getControl(306).setLabel("y")
			self.getControl(307).setLabel("u")
			self.getControl(308).setLabel("i")
			self.getControl(309).setLabel("o")
			self.getControl(310).setLabel("p")
			self.getControl(312).setLabel("a")
			self.getControl(313).setLabel("s")
			self.getControl(314).setLabel("d")
			self.getControl(315).setLabel("f")
			self.getControl(316).setLabel("g")
			self.getControl(317).setLabel("h")
			self.getControl(318).setLabel("j")
			self.getControl(319).setLabel("k")
			self.getControl(320).setLabel("l")
			self.getControl(322).setLabel("z")
			self.getControl(323).setLabel("x")
			self.getControl(324).setLabel("c")
			self.getControl(325).setLabel("v")
			self.getControl(326).setLabel("b")
			self.getControl(327).setLabel("n")
			self.getControl(328).setLabel("m")
		elif t==2:
			self.getControl(301).setLabel("1")
			self.getControl(302).setLabel("2")
			self.getControl(303).setLabel("3")
			self.getControl(304).setLabel("4")
			self.getControl(305).setLabel("5")
			self.getControl(306).setLabel("6")
			self.getControl(307).setLabel("7")
			self.getControl(308).setLabel("8")
			self.getControl(309).setLabel("9")
			self.getControl(310).setLabel("0")
			self.getControl(312).setLabel("!")
			self.getControl(313).setLabel("\\")
			self.getControl(314).setLabel("#")
			self.getControl(315).setLabel("$")
			self.getControl(316).setLabel("%")
			self.getControl(317).setLabel("^")
			self.getControl(318).setLabel("&")
			self.getControl(319).setLabel("*")
			self.getControl(320).setLabel("-")
			self.getControl(322).setLabel("(")
			self.getControl(323).setLabel(")")
			self.getControl(324).setLabel("=")
			self.getControl(325).setLabel("+")
			self.getControl(326).setLabel("/")
			self.getControl(327).setLabel("[")
			self.getControl(328).setLabel("]")
		else:
			self.getControl(301).setLabel("Q")
			self.getControl(302).setLabel("W")
			self.getControl(303).setLabel("E")
			self.getControl(304).setLabel("R")
			self.getControl(305).setLabel("T")
			self.getControl(306).setLabel("Y")
			self.getControl(307).setLabel("U")
			self.getControl(308).setLabel("I")
			self.getControl(309).setLabel("O")
			self.getControl(310).setLabel("P")
			self.getControl(312).setLabel("A")
			self.getControl(313).setLabel("S")
			self.getControl(314).setLabel("D")
			self.getControl(315).setLabel("F")
			self.getControl(316).setLabel("G")
			self.getControl(317).setLabel("H")
			self.getControl(318).setLabel("J")
			self.getControl(319).setLabel("K")
			self.getControl(320).setLabel("L")
			self.getControl(322).setLabel("Z")
			self.getControl(323).setLabel("X")
			self.getControl(324).setLabel("C")
			self.getControl(325).setLabel("V")
			self.getControl(326).setLabel("B")
			self.getControl(327).setLabel("N")
			self.getControl(328).setLabel("M")
		
		if t==0:
			self.getControl(100).setVisible(True)
			self.nowpage = 0
			self.changepages()
		else:
			self.getControl(100).setVisible(False)

	def isConfirmed(self):
		return self.confirmed

	def getText(self):
		return self.inputString
		
class Keyboard(object):
	def __init__( self, *args, **kwargs ):
		self.confirmed = False
		self.inputString = ''

	def doModal (self):
		self.win = InputWindow("script-input-windows.xml", __addonDir__, ADDON_SKIN )
		self.win.doModal()
		self.confirmed = self.win.isConfirmed()
		self.inputString = self.win.getText()
		del self.win

	def isConfirmed(self):
		return self.confirmed

	def getText(self):
		return self.inputString
