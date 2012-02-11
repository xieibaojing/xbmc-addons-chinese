# -*- coding: utf-8 -*-
import os, sys, re
from traceback import print_exc

import xbmc, xbmcgui
from xbmcaddon import Addon

import urllib2, urllib, httplib, time

##############################################################################
# Chinese Keyboard Addon Module Change History
# See changelog.txt for earlier history
#
# Version 1.2.1 2012-02-11 (cmeng)
# a. Dynamic word selection per page based on word length
# b. Add scancode for Eden: < & > arrow buttons
##############################################################################

__settings__ = Addon( "script.module.keyboard.chinese" )
__addonDir__ = __settings__.getAddonInfo( "path" )
__language__ = __settings__.getLocalizedString

XBMC_SKIN  = xbmc.getSkinDir()
SKINS_PATH = os.path.join( __addonDir__, "resources", "skins" )
ADDON_SKIN = ( "default", XBMC_SKIN )[ os.path.exists( os.path.join( SKINS_PATH, XBMC_SKIN ) ) ]
MEDIA_PATH = os.path.join( SKINS_PATH, ADDON_SKIN, "media" )

ACTION_PARENT_DIR     = 9
ACTION_PREVIOUS_MENU  = (10, 92)
ACTION_CONTEXT_MENU   = 117
WORD_PER_PAGE = [9,7,5,4,3,3,3]

CTRL_ID_BACK = 8
CTRL_ID_SPACE = 32
CTRL_ID_RETN = 300
CTRL_ID_LANG = 302
CTRL_ID_CAPS = 303
CTRL_ID_SYMB = 304
CTRL_ID_LEFT = 305
CTRL_ID_RIGHT = 306
CTRL_ID_IP = 307
CTRL_ID_TEXT = 310
CTRL_ID_HEAD = 311
CTRL_ID_CODE = 401
CTRL_ID_HZLIST = 402

class InputWindow(xbmcgui.WindowXMLDialog):
    def __init__( self, *args, **kwargs ):
        self.totalpage = 1
        self.nowpage = 0
        self.words = ''
        self.wordperpage = WORD_PER_PAGE[0]
        self.inputString = kwargs.get( "default" ) or ""
        self.heading = kwargs.get( "heading" ) or ""
        xbmcgui.WindowXMLDialog.__init__( self )

    def onInit(self):
        self.setKeyToChinese()
        self.getControl(CTRL_ID_HEAD).setLabel(self.heading)
        self.getControl(CTRL_ID_CODE).setLabel('')
        self.getControl(CTRL_ID_TEXT).setLabel(self.inputString)
        self.confirmed = False

    def onFocus( self, controlId ):
        self.controlId = controlId

    def onClick( self, controlID ):
        if controlID == CTRL_ID_CAPS:#big
            self.getControl(CTRL_ID_SYMB).setSelected(False)
            if self.getControl(CTRL_ID_CAPS).isSelected():
                self.getControl(CTRL_ID_LANG).setSelected(False)
            self.setKeyToChinese()
        elif controlID == CTRL_ID_IP:#ip
            dialog = xbmcgui.Dialog()
            value = dialog.numeric( 3, __language__(2), '' )
            self.getControl(CTRL_ID_TEXT).setLabel(self.getControl(CTRL_ID_TEXT).getLabel()+value)
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
                elif controlID>=48 and controlID<=57:#0-9
                    i = self.nowpage*self.wordperpage+(controlID-48)
                    hanzi = self.words[i]
                    self.getControl(CTRL_ID_TEXT).setLabel(self.getControl(CTRL_ID_TEXT).getLabel()+ hanzi)
                    self.getControl(CTRL_ID_CODE).setLabel('')
                    #Comment out to allow user to reselect the last hzlist
                    #self.getControl(CTRL_ID_HZLIST).setLabel('')
                    #self.words = []
            else:
                self.getControl(CTRL_ID_TEXT).setLabel(self.getControl(CTRL_ID_TEXT).getLabel()+self.getControl(controlID).getLabel().encode('utf-8'))

    def onAction(self,action):
        #s1 = str(action.getId())
        #s2 = str(action.getButtonCode())
        #print "======="+s1+"========="+s2+"=========="
        keycode = action.getButtonCode()
        #self.getControl(CTRL_ID_HEAD).setLabel(str(keycode))
        if keycode >= 61505 and keycode <= 61530: #a-z
            if self.getControl(CTRL_ID_LANG).isSelected():
                keychar = chr(keycode - 61505 + ord('a'))
                s = self.getControl(CTRL_ID_CODE).getLabel() + keychar
                self.getControl(CTRL_ID_CODE).setLabel(s)
                self.getChineseWord(s)
            else:
                if self.getControl(CTRL_ID_CAPS).isSelected():
                    keychar = chr(keycode - 61505 + ord('A')) #A-Z
                else:
                    keychar = chr(keycode - 61505 + ord('a'))
                self.getControl(CTRL_ID_TEXT).setLabel(self.getControl(CTRL_ID_TEXT).getLabel()+keychar)
        elif keycode >= 61488 and keycode <= 61497: #0-9 (Eden)-no overlapping code with Dharma
            self.onClick( keycode-61488+48 )
        elif keycode >= 61536 and keycode <= 61545: #0-9 (Dharma)-no overlapping code with Eden
            self.onClick( keycode-61536+48 )
        elif keycode == 61500 or keycode == 192700: #Eden & Dharma scancode difference
            self.onClick( CTRL_ID_LEFT ) # <
        elif keycode == 61502 or keycode == 192702: #Eden & Dharma scancode difference
            self.onClick( CTRL_ID_RIGHT ) # >
        elif keycode == 61472:
            self.onClick( CTRL_ID_SPACE )
        elif keycode == 61448:
            self.onClick( CTRL_ID_BACK )
        elif action.getId() in ACTION_PREVIOUS_MENU:
            self.close()

    def changepages (self):
        self.getControl(CTRL_ID_HZLIST).setLabel('')
        num=0
        if self.nowpage == 0:
            hzlist = ''
        else:
            hzlist = '< '
        for i in range(self.nowpage*self.wordperpage, len(self.words)):
            hzlist = hzlist+str(num)+'.'+self.words[i]+' '
            num+=1
            if num > self.wordperpage: break
        if self.nowpage < self.totalpage-1:
            hzlist = hzlist + '>'
        self.getControl(CTRL_ID_HZLIST).setLabel(hzlist)

    def getChineseWord (self,py):
        self.nowpage = 0
        self.totalpage = 1
        self.getControl(CTRL_ID_HZLIST).setLabel('')
        #if HANZI_MB.has_key(py):
        self.words=self.getwords(py)
        self.totalpage = int(len(self.words)/self.wordperpage)+1
        num=0
        hzlist = ''
        for i in range(0, len(self.words)):
            hzlist = hzlist+str(num)+'.'+self.words[i]+' '
            num+=1
            if num > self.wordperpage: break
        if self.totalpage>1:
            hzlist = hzlist + '>'
        self.getControl(CTRL_ID_HZLIST).setLabel(hzlist)

    def setKeyToChinese (self):
        self.getControl(CTRL_ID_CODE).setLabel('')
        if self.getControl(CTRL_ID_SYMB).isSelected():
            #if self.getControl(CTRL_ID_LANG).isSelected():
            #    pass
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
    
    def getwords(self, py):
        t = time.time()
        url = 'http://olime.baidu.com/py?py=' + py + '&rn=0&pn=20&ol=1&prd=shurufa.baidu.com&t=' + str(int(t))
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')      
        # need cookie to avoid bad gateway problem
        req.add_header('Cookie', 'BAIDUID=9056ED272CC1696BE2896EC96A43B806:FG=1')
        response = urllib2.urlopen(req)
        httpdata = response.read()
        response.close()
        words = []
        match = re.compile('\["(.+?)",\d+\]').findall(httpdata)
        wordcnt = len(match[0].split("\\"))-2
        self.wordperpage = WORD_PER_PAGE[wordcnt]
        for word in match:
            words.append(eval('u"'+word+'"').encode('utf-8'))
        return words
    


class Keyboard:
    def __init__( self, default='', heading='' ):
        self.confirmed = False
        self.inputString = default
        self.heading = heading

    def doModal (self):
        self.win = InputWindow("DialogKeyboardChinese.xml", __addonDir__, ADDON_SKIN, heading=self.heading, default=self.inputString )
        self.win.doModal()
        self.confirmed = self.win.isConfirmed()
        self.inputString = self.win.getText()
        del self.win

    def setHeading(self, heading):
        self.heading = heading

    def isConfirmed(self):
        return self.confirmed

    def getText(self):
        return self.inputString
