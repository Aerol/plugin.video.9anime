# -*- coding: utf-8 -*-

import xbmc,xbmcplugin,xbmcgui,xbmcaddon,xbmcvfs
import re
import urllib,urllib2
import os
import net

from bs4 import BeautifulSoup
import simplejson

from t0mm0.common.addon import Addon
from metahandler import metahandlers

from config import *
from resources.lib import control

net = net.Net()
addon_id = ps('_addon_id')
_domain_url = ps('_domain_url')
selfAddon = xbmcaddon.Addon(id=addon_id)
addonname = selfAddon.getAddonInfo('name')
datapath= xbmc.translatePath(selfAddon.getAddonInfo('profile'))
addon = Addon(addon_id, sys.argv)
fanart = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id , 'fanart.jpg'))
icon = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'icon.png'))
anime = xbmc.translatePath(os.path.join('special://home/addons/' + addon_id, 'anime.png'))
try:os.mkdir(datapath)
except:pass
file_var = open(xbmc.translatePath(os.path.join(datapath, 'cookie.lwp')), "a")
cookie_file = os.path.join(os.path.join(datapath,''), 'cookie.lwp')

def get_genres(url, iconimage):
        genres = {'action' : 'Action', 'adventure' : 'Adventure', 'cars' : 'Cars',
                  'comedy' : 'Comedy', 'dementia' : 'Dementia', 'demons' : 'Demons',
                  'drama' : 'Drama', 'ecchi' : 'Ecchi', 'fantasy' : 'Fantasy',
                  'game' : 'Game', 'harem' : 'Harem', 'historical' : 'Historical',
                  'horror' : 'Horror', 'josei' : 'Josei', 'kids' : 'Kids',
                  'magic' : 'Magic', 'martial-arts' : 'Martial Arts',
                  'mecha' : 'Mecha', 'military' : 'Military', 'music' : 'Music',
                  'mystery' : 'Mystery', 'parody' : 'Parody', 'police' : 'Police',
                  'psychological' : 'Psychological', 'romance' : 'Romance',
                  'samurai' : 'Samurai', 'school' : 'School', 'sci-fi' : 'Sci Fi',
                  'seinen' : 'Seinen', 'shoujo' : 'Shoujou', 'shoujo-ai' : 'Shoujo Ai',
                  'shounen' : 'Shounen', 'shounen-ai' : 'Shounen Ai',
                  'slice-of-life' : 'Slice of Life', 'space' : 'Space',
                  'sports' : 'Sports', 'super-power' : 'Super Power',
                  'supernatural' : 'Supernatural', 'thriller' : 'Thriller',
                  'vampire' : 'Vampire', 'yaoi' : 'Yaoi', 'yuri' : 'Yuri'}
        for i in genres:
                addDir(genres[i], _domain_url+'genre/'+i, i, iconimage, iconimage)

def get_genre(url, mode, iconimage):
    get_anime_list(url, iconimage)

def get_newest(url, mode, iconimage):
    get_anime_list(url, iconimage)

def get_most_watched(url, iconimage):
    get_anime_list(url, iconimage)

def get_anime_list(url, iconimage):
    metadata = metahandlers.MetaData(preparezip=False, tmdb_api_key='6cd18c483332380fd24ae41316af596f')
    html = open_url(url)
    soup = BeautifulSoup(html, 'html.parser')
    temp = soup.find_all('div')
    for i in temp:
        try:
            if 'item' in i.attrs['class']:
                title = i.a.img.get('alt').replace(' (Dub)', '').replace(':', '')
                info = metadata.get_meta('tvshow', name=title, imdb_id='')
                addDir(i.a.img.get('alt'), i.a.get('href'), 99, info['cover_url'], info['backdrop_url'], info['plot'])
        except:
            pass
    temp = soup.find_all('a')
    for i in temp:
        try:
            if 'btn' in i.attrs['class']:
                if 'Next' in i.get_text():
                    addDir(i.get_text(), _domain_url+i.attrs['href'], 3, iconimage, iconimage)
        except:
            pass

def get_episodes(url, title, iconimage):
    metadata = metahandlers.MetaData(preparezip=False, tmdb_api_key='6cd18c483332380fd24ae41316af596f')
    html = open_url(url)
    soup = BeautifulSoup(html, 'html.parser')
    temp = soup.find_all('div')
    for i in temp:
        try:
            if 'server' in i.attrs['class']:
                eps = i.find_all('a')
                break
        except:
            pass
    for i in eps:
        print(_domain_url+i.get('data-id'))
        print title
        info = metadata.get_episode_meta(title, '', 1, i.get('data-base'), episode_title=title)
        print(info)
        addDir(info['title'], i.get('data-id'), 98, info['poster'], info['cover_url'], info['plot'], info)
        #addDir("Episode "+i.get('data-base'), i.get('data-id'), 98, iconimage, iconimage)

def get_video_links(name, url, iconimage, meta):
    print(name)
    print(url)
    print(iconimage)
    vid_info = simplejson.loads(open_url('https://9anime.to/ajax/episode/info?id='+url+"&update=0"))
    print(vid_info)
    vid_id = vid_info['params']['id']
    token = vid_info['params']['token']
    options = vid_info['params']['options']
    base_grabber = 'https://9anime.to/grabber-api/?id='+vid_id+'&token='+token+'&options='+options
    video_links = simplejson.loads(open_url(base_grabber))
    print(video_links)
    links_list = {}
    for i in video_links['data']:
        links_list[i['label']] = i['file']
    #for i in video_links['data']:
        #addLink(i['label'], i['file'], 97, iconimage, iconimage)
        #choice = addDialog(i['label'], i['file'], 97, iconimage, iconimage)
    choice = addDialog(links_list, 'Description goes here', 97, meta)
    #PLAYLINK('test', choice, iconimage)

def search(url):
    search_entered = ''
    keyboard = xbmc.Keyboard(search_entered, 'Search')
    keyboard.doModal()
    if keyboard.isConfirmed():
        search_entered = keyboard.getText().replace(' ','+')
    if len(search_entered) > 1:
        url = url + search_entered
        do_search(url)

def do_search(url):
    get_anime_list(url, anime)

def main():
    addDir('Most Watched', _domain_url+'filter?type[]=series&sort=views%3Adesc', 3, anime, fanart)
    addDir('Search', _domain_url+'search?keyword=', 4, anime, fanart)
    addDir('Newest', _domain_url+'newest', 2, anime, fanart)
    addDir('Genre', _domain_url+'genre', 1, anime, fanart)

def addDir(name,url,mode,iconimage,fanart,description='', meta=''):
    '''
    Add directory item to GUI

    Args:
        name (str): Entry label
        url (str): url/path for entry to link to
        iconimage (str): url/path of poster image
        fanart (str): url/path of fanart image for background

    Kwargs:
        description (str): Description of entry (eg episode plot or show description)
        meta = (dct): metahandler dictionary
    '''
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&description="+urllib.quote_plus(description)+"&meta="+meta
    ok=True
    liz=xbmcgui.ListItem(name.strip(), iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description} )
    liz.setProperty('fanart_image', fanart)
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
    return ok

def addLink(name,url,mode,iconimage,fanart,description='', meta=''):
    '''
    Add link item to GUI

    Args:
        name (str): Entry label
        url (str): url/path for entry to link to
        iconimage (str): url/path of poster image
        fanart (str): url/path of fanart image for background

    Kwargs:
        description (str): Description of entry (eg episode plot or show description)
        meta = (dct): metahandler dictionary
    '''
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&description="+urllib.quote_plus(description)
    ok=True
    liz=xbmcgui.ListItem(name.strip(), iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description} )
    liz.setProperty('fanart_image', fanart)
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
    return ok


def addDialog(dct, desc, mode, meta=''):
    lst = []
    url = []
    for i in dct:
        name = i
        url.append(dct[i])
        liz = xbmcgui.ListItem(name.strip(), iconImage="DefaultFolder.png")
        liz.setInfo(type="video", infoLabels={"title" : name, 'plot' : desc, 'path' : url})
        lst.append(liz)
    dialog = xbmcgui.Dialog()
    ok = dialog.select('Choose', lst)
    url = url[ok]
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&description="+urllib.quote_plus(desc)
    return url

def PLAYLINK(name,url,iconimage):
    liz=xbmcgui.ListItem(name, iconimage)
    xbmc.Player().play(url, liz, False)

def get_playlink(url, meta):
    title = meta['TVShowtitle']
    year = meta['year']
    season = meta['season']
    episode = meta['episode']
    tvdb = meta['tvdb_id']
    #PLAYLINK(name, url, iconimage)
    player().run(title, year, season, episode, tvdb, url, meta)

def open_url(url):
    print("opening url "+url)
    net.set_cookies(cookie_file)
    link = net.http_GET(url).content
    #link = cleanHex(link)
    return link

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

def cleanHex(text):
    def fixup(m):
        text = m.group(0)
        if text[:3] == "&#x": return unichr(int(text[3:-1], 16)).encode('utf-8')
        else: return unichr(int(text[2:-1])).encode('utf-8')
        try :return re.sub("(?i)&#\w+;", fixup, text.decode('ISO-8859-1').encode('utf-8'))
        except:return re.sub("(?i)&#\w+;", fixup, text.encode("ascii", "ignore").encode('utf-8'))

if __name__ == '__main__':
    params=get_params()
    url=None; name=None; mode=None; site=None; iconimage=None
    try:
        site = urllib.unquote_plus(params["site"])
    except:
        pass
    try:
        url = urllib.unquote_plus(params["url"])
    except:
        pass
    try:
        name = urllib.unquote_plus(params["name"])
        if params["mode"].isdigit():
            mode=int(params["mode"])
        else:
            mode = params["mode"]
    except:
        pass
    try:
        iconimage = urllib.unquote_plus(params["iconimage"])
    except:
        pass

    if mode is None or url is None or len(url) < 1:
        main()
    elif mode is 1:
        get_genres(url, iconimage)
    elif mode is 2:
        get_newest(url, mode, iconimage)
    elif mode is 3:
        get_most_watched(url, iconimage)
    elif mode is 4:
        search(url)
    elif mode is 97:
        get_playlink(url, meta)
    elif mode is 98:
        get_video_links(name, url, iconimage)
    elif mode is 99:
        get_episodes(url, name, iconimage)
    elif mode is 100:
        get_play_link(name, url, iconimage)
    elif 'str' in str(type(mode)):
        get_genre(url, mode, iconimage)

    xbmcplugin.endOfDirectory(int(sys.argv [1]))
