# -*- coding: utf-8 -*-

# *  This Program is free software; you can redistribute it and/or modify
# *  it under the terms of the GNU General Public License as published by
# *  the Free Software Foundation; either version 2, or (at your option)
# *  any later version.
# *
# *  This Program is distributed in the hope that it will be useful,
# *  but WITHOUT ANY WARRANTY; without even the implied warranty of
# *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# *  GNU General Public License for more details.
# *
# *  You should have received a copy of the GNU General Public License
# *  along with XBMC; see the file COPYING. If not, write to
# *  the Free Software Foundation, 675 Mass Ave, Cambridge, MA 02139, USA.
# *  http://www.gnu.org/copyleft/gpl.html
# *

import os, sys, urllib2, socket, simplejson
import xbmcgui, xbmcaddon

__addon__      = xbmcaddon.Addon()
__provider__   = __addon__.getAddonInfo('name')
__cwd__        = __addon__.getAddonInfo('path')
__resource__   = xbmc.translatePath(os.path.join(__cwd__, 'resources', 'lib'))

sys.path.append (__resource__)

# Array for translate wind level and speed
WIND_SPEED = { "0" : "0",
               "1" : "3",
               "2" : "8.5",
               "3" : "15.5",
               "4" : "24",
               "5" : "33.5",
               "6" : "44",
               "7" : "55.5",
               "8" : "68",
               "9" : "81.5",
               "10" : "95.5",
               "11" : "110",
               "12" : "120"}

# Array for translate week to number
DAYS = { "星期一": 1,
         "星期二": 2,
         "星期三": 3,
         "星期四": 4,
         "星期五": 5,
         "星期六": 6,
         "星期日": 7}

# Array for translate OutlookIcon index
WEATHER_CODES = { '0' : '32',
                  '1' : '30',
                  '2' : '26',
                  '3' : '39',
                  '4' : '35',
                  '5' : '35',
                  '6' : '5',
                  '7' : '11',
                  '8' : '11',
                  '9' : '12',
                  '10' : '40',
                  '11' : '40',
                  '12' : '40',
                  '13' : '15',
                  '14' : '13',
                  '15' : '14',
                  '16' : '16',
                  '17' : '16',
                  '18' : '20',
                  '19' : '7',
                  '20' : '23',
                  '21' : '11',
                  '22' : '12',
                  '23' : '40',
                  '24' : '40',
                  '25' : '40',
                  '26' : '14',
                  '27' : '16',
                  '28' : '16',
                  '29' : '21',
                  '30' : '22',
                  '31' : '23',
                  '99' : 'na'}

LOCATION_URL    = 'http://m.weather.com.cn/data5/city%s.xml'
WEATHER_URL     = 'http://www.weather.com.cn/data/sk/%s.html'
WEATHER_DAY_URL = 'http://m.weather.com.cn/data/%s.html'
WEATHER_WINDOW  = xbmcgui.Window(12600)

socket.setdefaulttimeout(10)

def set_property(name, value):
    WEATHER_WINDOW.setProperty(name, value)

def refresh_locations():
    location_set1 = __addon__.getSetting('Location1')
    location_set2 = __addon__.getSetting('Location2')
    location_set3 = __addon__.getSetting('Location3')
    locations = 0
    if location_set1 != '':
        locations += 1
        set_property('Location1', location_set1)
    else:
        set_property('Location1', '')
    if location_set2 != '':
        locations += 1 
        set_property('Location2', location_set2)
    else:
        set_property('Location2', '')
    if location_set3 != '':
        locations += 1
        set_property('Location3', location_set3)
    else:
        set_property('Location3', '')
    set_property('Locations', str(locations))

def fetch(url):
    try:
        req = urllib2.urlopen(url)
        json_string = req.read()
        req.close()
    except:
        json_string = ''
    try:
        parsed_json = simplejson.loads(json_string)
    except:
        parsed_json = ''
    return parsed_json

def location(string):
    loc   = []
    locid = []
    url = LOCATION_URL % (urllib2.quote(string))
    try:
        req = urllib2.urlopen(url)
        ret_string = req.read()
        req.close()
    except:
        ret_string = ''
    values = ret_string.split(',')
    for item in values:
        location   = item.split('|')[1]
        locationid = item.split('|')[0]
        loc.append(location)
        locid.append(locationid)
    return loc, locid

def forecast(city):
    data = fetch(WEATHER_URL % (city))
    if data != '':
        properties(data)
    data = fetch(WEATHER_DAY_URL % (city))
    if data != '':
        properties2(data)

def properties(query):
    set_property('Current.Temperature'   , query['weatherinfo']['temp'].encode('utf-8'))
    set_property('Current.Wind'          , WIND_SPEED[query['weatherinfo']['WSE'].encode('utf-8')])
    set_property('Current.WindDirection' , query['weatherinfo']['WD'].encode('utf-8'))
    set_property('Current.Humidity'      , query['weatherinfo']['SD'].rstrip('%'))
    set_property('Current.FeelsLike'     , query['weatherinfo']['temp'].encode('utf-8'))

def properties2(query):
    weathercode = WEATHER_CODES[query['weatherinfo']['img1'].encode('utf-8')]
    set_property('Current.Condition'     , query['weatherinfo']['weather1'].encode('utf-8'))
    set_property('Current.UVIndex'       , query['weatherinfo']['index_uv'].encode('utf-8'))
    # No DewPoint data from site www.weather.com.cn
    #set_property('Current.DewPoint'      , str(query['weatherinfo']['dewpoint_c']))
    set_property('Current.OutlookIcon'   , '%s.png' % weathercode)
    set_property('Current.FanartCode'    , weathercode)
    week = DAYS[query['weatherinfo']['week'].encode('utf-8')]
    for count in [0, 1, 2, 3]:
        img = query['weatherinfo']['img%i' % (count + 1)].encode('utf-8')
        if count in [1, 3] and img == '99':
            img = query['weatherinfo']['img%i' % count].encode('utf-8')
        weathercode = WEATHER_CODES[img]
        day = week + count
        if day > 7: day -= 7
        temp = query['weatherinfo']['temp%i' % (count + 1)].encode('utf-8').replace('℃', '').split('~')
        set_property('Day%i.Title'       % count, xbmc.getLocalizedString( 10 + day ))
        if int(temp[0]) > int(temp[1]):
            set_property('Day%i.HighTemp'    % count, temp[0])
            set_property('Day%i.LowTemp'     % count, temp[1])
        else:
            set_property('Day%i.HighTemp'    % count, temp[1])
            set_property('Day%i.LowTemp'     % count, temp[0])
        set_property('Day%i.Outlook'     % count, query['weatherinfo']['weather%i' % (count + 1)].encode('utf-8'))
        set_property('Day%i.OutlookIcon' % count, '%s.png' % weathercode)
        set_property('Day%i.FanartCode'  % count, weathercode)

if sys.argv[1].startswith('Location'):
    dialog = xbmcgui.Dialog()
    # select Province
    locations, locationids = location('')
    if locations != []:
        selected = dialog.select('选择省/自治区/直辖市', locations)
        if selected != -1:
            name = locations[selected]
            code = locationids[selected]
            # select City
            locations, locationids = location(code)
            if locations != []:
                selected = dialog.select('选择'+name+'的市', locations)
                if selected != -1:
                    name = locations[selected]
                    code = locationids[selected]
                    # select County
                    locations, locationids = location(code)
                    if locations != []:
                        selected = dialog.select('选择'+name+'的区县', locations)
                        if selected != -1:
                            name = locations[selected]
                            code = locationids[selected]
                            locations, locationids = location(code)
                            if locations != []:
                                __addon__.setSetting(sys.argv[1], name)
                                __addon__.setSetting(sys.argv[1] + 'id', locations[0])
                            else:
                                dialog.ok(__provider__, xbmc.getLocalizedString(284))
                    else:
                        dialog.ok(__provider__, xbmc.getLocalizedString(284))
            else:
                dialog.ok(__provider__, xbmc.getLocalizedString(284))
    else:
        dialog.ok(__provider__, xbmc.getLocalizedString(284))

else:
    location = __addon__.getSetting('Location%sid' % sys.argv[1])
    forecast(location)

refresh_locations()
set_property('WeatherProvider', '中国天气网')
