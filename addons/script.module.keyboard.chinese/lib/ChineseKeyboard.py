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

CTRL_ID_BACK = 8
CTRL_ID_SPACE = 32
CTRL_ID_RETN = 300
CTRL_ID_LANG = 302
CTRL_ID_CAPS = 303
CTRL_ID_SYMB = 304
CTRL_ID_LEFT = 305
CTRL_ID_RIGHT = 306
CTRL_ID_TEXT = 310
CTRL_ID_CODE = 401
CTRL_ID_HZLIST = 402

a = ['a','ai','an','ang','ao','ba','bai','ban','bang','bao','be','bei','ben','beng','bi','bia','bian','biao','bie','bin','bing','bo','bu','ca','cai','can','cang','cao','ce','cen','ceng','ceok','ceom','ceon','ceor','cha','chai','chan','chang','chao','che','chen','cheng','chi','chong','chou','chu','chua','chuai','chuan','chuang','chui','chun','chuo','ci','cis','cong','cou','cu','cuan','cui','cun','cuo','da','dai','dan','dang','dao','de','dei','dem','den','deng','di','dia','dian','diao','die','dim','ding','diu','dong','dou','du','duan','dui','dul','dun','duo','e','en','eng','eo','eol','eom','eos','er','fa','fan','fang','fei','fen','feng','fo','fou','fu','ga','gad','gai','gan','gang','gao','ge','gei','gen','geng','gib','go','gong','gou','gu','gua','guai','guan','guang','gui','gun','guo','ha','hai','hal','han','hang','hao','he','hei','hen','heng','ho','hol','hong','hou','hu','hua','huai','huan','huang','hui','hun','huo','hwa','i','ji','jia','jian','jiang','jiao','jie','jin','jing','jiong','jiu','jou','ju','juan','jue','jun','ka','kai','kal','kan','kang','kao','ke','kei','ken','keng','ki','kong','kos','kou','ku','kua','kuai','kuan','kuang','kui','kun','kuo','kweok','kwi','la','lai','lan','lang','lao','le','lei','li','lia','lian','liang','liao','lie','lin','ling','liu','lo','long','lou','lu','luan','lue','lun','luo','lv','m','ma','mai','man','mang','mao','me','mei','men','meng','meo','mi','mian','miao','mie','min','ming','miu','mo','mou','mu','myeo','myeon','myeong','n','na','nai','nan','nang','nao','ne','nei','nem','nen','neng','neus','ng','ngag','ngai','ngam','ni','nian','niao','nie','nin','ning','niu','nong','nou','nu','nuan','nue','nun','nung','nuo','nv','nve','o','oes','ol','on','ou','pa','pai','pak','pan','pang','pao','pei','pen','peng','peol','phas','phdeng','phoi','phos','pi','pian','piao','pie','pin','ping','po','pou','ppun','pu','q','qi','qia','qian','qiang','qiao','qie','qin','qing','qiong','qiu','qu','quan','que','qun','ra','ram','ran','rang','rao','re','ren','ri','rong','rou','ru','rua','ruan','rui','run','ruo','sa','saeng','sai','sal','san','sang','sao','se','sed','sei','sen','seng','seo','seon','sha','shai','shan','shang','shao','she','shen','sheng','shi','shou','shu','shua','shuai','shuan','shuang','shui','shun','shuo','shw','si','so','sol','song','sou','su','suan','sui','sun','suo','ta','tae','tai','tan','tang','tao','teng','ti','tian','tiao','tie','ting','tol','ton','tong','tou','tu','tuan','tui','tun','tuo','uu','wa','wai','wan','wang','wei','wen','weng','wie','wo','wu','xi','xia','xian','xiang','xiao','xie','xin','xing','xiong','xiu','xu','xuan','xue','xun','ya','yan','yang','yao','ye','yi','yin','ying','yo','yong','you','yu','yuan','yue','yun','za','zad','zai','zan','zang','zao','ze','zei','zen','zeng','zha','zhai','zhan','zhang','zhao','zhe','zhen','zheng','zhi','zhong','zhou','zhu','zhua','zhuai','zhuan','zhuang','zhui','zhun','zhuo','zi','zo','zong','zou','zu','zuan','zui','zun','zuo']
filename = os.path.join( __addonDir__, "lib", "pinyin.mb" )
fd = open( filename, 'r')
b = fd.read().split()
fd.close()

class InputWindow(xbmcgui.WindowXMLDialog):
	def __init__( self, *args, **kwargs ):
		self.totalpage = 1
		self.nowpage = 0
		self.words = ''
		xbmcgui.WindowXMLDialog.__init__( self, *args, **kwargs )

	def onInit(self):
		self.status = 0
		self.setKeyToChinese()
		self.getControl(CTRL_ID_CODE).setLabel('')
		self.getControl(CTRL_ID_TEXT).setLabel('')
		self.confirmed = False
		self.inputString = ''

	def onFocus( self, controlId ):
		self.controlId = controlId

	def onClick( self, controlID ):
		if controlID == CTRL_ID_CAPS:#big
			self.getControl(CTRL_ID_SYMB).setSelected(False)
			if self.getControl(CTRL_ID_CAPS).isSelected():
				self.getControl(CTRL_ID_LANG).setSelected(False)
			self.setKeyToChinese()
		elif controlID == CTRL_ID_SYMB:#num
			self.setKeyToChinese()
		elif controlID == CTRL_ID_LANG:#en/ch
			if self.getControl(CTRL_ID_LANG).isSelected():
				self.getControl(CTRL_ID_CAPS).setSelected(False)
			self.setKeyToChinese()
		elif controlID == CTRL_ID_BACK:#back
			if self.getControl(CTRL_ID_LANG).isSelected() and len(self.getControl(CTRL_ID_CODE).getLabel())>0:
				self.getControl(CTRL_ID_CODE).setLabel(self.getControl(CTRL_ID_CODE).getLabel()[0:-1])
				self.getChineseWord(self.getControl(CTRL_ID_CODE).getLabel())
			else:
				self.getControl(CTRL_ID_TEXT).setLabel(self.getControl(CTRL_ID_TEXT).getLabel().decode("utf-8")[0:-1])
		elif controlID == CTRL_ID_RETN:#enter
			newText = self.getControl(CTRL_ID_TEXT).getLabel()
			if not newText: return
			self.inputString = newText
			self.confirmed = True
			self.close()
		elif controlID == CTRL_ID_LEFT:#left
			if self.nowpage>0:
				self.nowpage -=1
			self.changepages()
		elif controlID == CTRL_ID_RIGHT:#right
			if self.nowpage<self.totalpage-1:
				self.nowpage +=1
			self.changepages()
		elif controlID == CTRL_ID_SPACE:#space
			self.getControl(CTRL_ID_TEXT).setLabel(self.getControl(CTRL_ID_TEXT).getLabel() + ' ')
		else:
			if self.getControl(CTRL_ID_LANG).isSelected() and not self.getControl(CTRL_ID_SYMB).isSelected():
				if controlID>=65 and controlID<=90:
					s = self.getControl(CTRL_ID_CODE).getLabel() + self.getControl(controlID).getLabel().lower()
					self.getControl(CTRL_ID_CODE).setLabel(s)
					self.getChineseWord(s)
				elif controlID>=48 and controlID<=57:
					i = self.nowpage*10*2+(controlID-48)*2
					hanzi = unicode(self.words[i:(2+i)],'gbk').encode('utf-8')
					self.getControl(CTRL_ID_TEXT).setLabel(self.getControl(CTRL_ID_TEXT).getLabel()+hanzi)
					self.getControl(CTRL_ID_CODE).setLabel('')
			else:
				self.getControl(CTRL_ID_TEXT).setLabel(self.getControl(CTRL_ID_TEXT).getLabel()+self.getControl(controlID).getLabel().encode('utf-8'))

	def onAction(self,action):
		#s1 = str(action.getId())
		#s2 = str(action.getButtonCode())
		#print "======="+s1+"========="+s2+"=========="
		keycode = action.getButtonCode()
		if keycode >= 61505 and keycode <= 61530:
			if self.getControl(CTRL_ID_LANG).isSelected():
				keychar = chr(keycode - 61505 + ord('a'))
				s = self.getControl(CTRL_ID_CODE).getLabel() + keychar
				self.getControl(CTRL_ID_CODE).setLabel(s)
				self.getChineseWord(s)
			else:
				if self.getControl(CTRL_ID_CAPS).isSelected():
					keychar = chr(keycode - 61505 + ord('A'))
				else:
					keychar = chr(keycode - 61505 + ord('a'))
				self.getControl(CTRL_ID_TEXT).setLabel(self.getControl(CTRL_ID_TEXT).getLabel()+keychar)
				
		if action == ACTION_PARENT_DIR:
			self.onClick( CTRL_ID_BACK )
		elif action == ACTION_PREVIOUS_MENU:
			self.close()

	def changepages (self):
		self.getControl(CTRL_ID_HZLIST).setLabel('')
		num=0
		if self.nowpage == 0:
			hzlist = ''
		else:
			hzlist = '<  '
		for i in range(self.nowpage*10*2, len(self.words), 2):
			hzlist = hzlist+str(num)+'.'+unicode(self.words[i:(2+i)],'gbk').encode('utf-8')+'  '
			num+=1
			if num > 9: break
		if self.nowpage < self.totalpage-1:
			hzlist = hzlist + '>'
		self.getControl(CTRL_ID_HZLIST).setLabel(hzlist)

	def getChineseWord (self,py):
		self.nowpage = 0
		self.totalpage = 1
		self.getControl(CTRL_ID_HZLIST).setLabel('')
		if py in a:
			self.words=b[a.index(py)]
			self.totalpage = int(len(self.words)/2/10)+1
			num=0
			hzlist = ''
			for i in range(0, len(self.words), 2):
				hzlist = hzlist+str(num)+'.'+unicode(self.words[i:(2+i)],'gbk').encode('utf-8')+'  '
				num+=1
				if num > 9: break
			if self.totalpage>1:
				hzlist = hzlist + '>'
			self.getControl(CTRL_ID_HZLIST).setLabel(hzlist)

	def setKeyToChinese (self):
		self.getControl(CTRL_ID_CODE).setLabel('')
		if self.getControl(CTRL_ID_SYMB).isSelected():
			#if self.getControl(CTRL_ID_LANG).isSelected():
			#	pass
			#else:
				i = 48
				for c in ')!@#$%^&*(':
					self.getControl(i).setLabel(c)
					i+=1
					if i > 57: break
				i = 65
				for c in '[]{}-_=+;:\'",.<>/?\\|`~':
					self.getControl(i).setLabel(c)
					i+=1
					if i > 90: break
				for j in range(i,90+1):
					self.getControl(j).setLabel('')
		else:
			for i in range(48, 57+1):
				keychar = chr(i - 48 + ord('0'))
				self.getControl(i).setLabel(keychar)
			if self.getControl(CTRL_ID_CAPS).isSelected():
				for i in range(65, 90+1):
					keychar = chr(i - 65 + ord('A'))
					self.getControl(i).setLabel(keychar)
			else:
				for i in range(65, 90+1):
					keychar = chr(i - 65 + ord('a'))
					self.getControl(i).setLabel(keychar)
		if self.getControl(CTRL_ID_LANG).isSelected():
			self.getControl(400).setVisible(True)
			self.nowpage = 0
			self.changepages()
		else:
			self.getControl(400).setVisible(False)

	def isConfirmed(self):
		return self.confirmed

	def getText(self):
		return self.inputString
		
class Keyboard(object):
	def __init__( self, *args, **kwargs ):
		self.confirmed = False
		self.inputString = ''

	def doModal (self):
		self.win = InputWindow("DialogKeyboardChinese.xml", __addonDir__, ADDON_SKIN )
		self.win.doModal()
		self.confirmed = self.win.isConfirmed()
		self.inputString = self.win.getText()
		del self.win

	def isConfirmed(self):
		return self.confirmed

	def getText(self):
		return self.inputString
