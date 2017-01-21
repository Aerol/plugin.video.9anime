# -*- coding: utf-8 -*-

import xbmc,xbmcplugin,xbmcgui,xbmcaddon,xbmcvfs
import re
import urllib,urllib2
import os
import net

from bs4 import BeautifulSoup
import simplejson
import urlparse

from t0mm0.common.addon import Addon
from metahandler import metahandlers

from config import *
from resources.lib.modules import control
from resources.lib import navigator

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

def get_genre(url, iconimage):
    get_anime_list(url, iconimage)

def get_newest(url, iconimage):
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
    # addDir('Most Watched', _domain_url+'filter?type[]=series&sort=views%3Adesc', 3, anime, fanart)
    # addDir('Search', _domain_url+'search?keyword=', 4, anime, fanart)
    # addDir('Newest', _domain_url+'newest', 2, anime, fanart)
    # addDir('Genre', _domain_url+'genre', 1, anime, fanart)
    navigator.addDirectoryItem('Most Watched', 'mostwatched', 'DefaultTvShows.png')

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
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&action="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&description="+urllib.quote_plus(description)+"&meta="+meta
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
    return link

if __name__ == '__main__':
    params = dict(urlparse.parse_qsl(sys.argv[2].replace('?','')))

    action = params.get('action')
    name = params.get('name')
    title = params.get('title')
    year = params.get('year')
    imdb = params.get('imdb')
    tvdb = params.get('tvdb')
    season = params.get('season')
    episode = params.get('episode')
    premiered = params.get('premiered')
    url = params.get('url')
    image = params.get('image')
    meta = params.get('meta')
    select = params.get('select')
    query = params.get('query')
    source = params.get('source')
    content = params.get('content')

    print params

    if action == None:
        navigator.navigator().root()
    elif action == 'movies':
        pass
    elif action == 'search':
        search(url)
    elif action == 'mostwatched':
        get_most_watched(url, image)
    elif action == 'genres':
        get_genre(url, image)

    xbmcplugin.endOfDirectory(int(sys.argv [1]))
