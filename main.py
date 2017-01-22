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
from resources.lib.modules import player
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

def get_genres(url):
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
        print(url)
        for i in genres:
                #addDir(genres[i], 'get_genre&url='+_domain_url+'genre/'+i, i, 'DefaultTvShows.png', 'DefaultTvShows.png')
                navigator.navigator().addDirectoryItem(genres[i], 'get_genre&url='+url+'&name='+i, 'genres.pg', 'DefaultTvShows.png')
        navigator.navigator().endDirectory()

def get_genre(url, name):
    url = url+'genre/'+name
    print(url)
    get_anime_list(url)

def get_newest(url):
    get_anime_list(url, iconimage)

def get_most_watched(url):
    get_anime_list(url+'filter?type[]=series&sort=views%3Adesc')

def get_movies(url):
    get_anime_list(url+'filter?type[]=movie&sort=views%3Adesc')

def get_anime_list(url):
    metadata = metahandlers.MetaData(preparezip=False, tmdb_api_key='6cd18c483332380fd24ae41316af596f')
    html = open_url(url)
    soup = BeautifulSoup(html, 'html.parser')
    temp = soup.find_all('div')

    for i in temp:
        try:
            if 'item' in i.attrs['class']:
                title = i.a.img.get('alt').replace(' (Dub)', '').replace(':', '')
                info = metadata.get_meta('tvshow', name=title, imdb_id='')
                #addDir(i.a.img.get('alt'), i.a.get('href'), 99, info['cover_url'], info['backdrop_url'], info['plot'])
                navigator.navigator().addDirectoryItem(
                        i.a.img.get('alt'),
                        'get_episodes&url='+i.a.get('href')+'&title='+info['TVShowTitle'],
                        info['cover_url'],
                        info['backdrop_url'])
        except:
            pass

    temp = soup.find_all('a')
    for i in temp:
        try:
            if 'btn' in i.attrs['class']:
                if 'Next' in i.get_text():
                    navigator.navigator().addDirectoryItem(i.get_text(), 'next_page&url='+_domain_url+i.attrs['href'], 'tvshows.png', 'DefaultTVShows.png')
        except:
            pass
    navigator.navigator().endDirectory()

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
    episodes = []
    for i in eps:
        info = metadata.get_episode_meta(title, '', 1, i.get('data-base'), episode_title=title)
        #addDir(info['title'], i.get('data-id'), 98, info['poster'], info['cover_url'], info['plot'], info)
        episodes.append({'name' : 'Episode {} - {}'.format(info['episode'], info['title']),
                         'url' : 'get_video_links&url='+i.get('data-id')+'&title='+info ['title']+'&season='+str(info ['season'])+'&episode='+str(info ['episode'])+'&show='+info['TVShowTitle'],
                         'image' : info['cover_url'],
                         'fanart' : info['backdrop_url'],
                         'desc' : info['plot']})
    addDirectory(episodes)

def get_video_links(url, title, year, season, episode, show):
    print(url)
    metadata = metahandlers.MetaData(preparezip=False)
    info = metadata.get_episode_meta(show, '', season, episode, episode_title=title)
    vid_info = simplejson.loads(open_url('https://9anime.to/ajax/episode/info?id='+url+"&update=0"))
    print(vid_info)
    vid_id = vid_info['params']['id']
    token = vid_info['params']['token']
    options = vid_info['params']['options']
    base_grabber = 'https://9anime.to/grabber-api/?id='+vid_id+'&token='+token+'&options='+options
    video_links = simplejson.loads(open_url(base_grabber))
    print(video_links)
    #links_list = {}
    links_list = []
    items = []
    #for i in video_links['data']:
        #links_list[i['label']] = i['file']
    for i in video_links['data']:
        links_list.append(i['file'])
        items.append({'name' : i['label'],
                      'url' : 'playlink&url=%s&meta=%s' % (urllib.quote_plus(i['file']), urllib.quote_plus(str(info))),
                      'image' : info['cover_url'],
                      'fanart' : info['backdrop_url'],
                      'desc' : info['plot']})
        #addLink(i['label'], i['file'], 97, iconimage, iconimage)
        #choice = addDialog(i['label'], i['file'], 97, iconimage, iconimage)
    addLink(items)
    #choice = control.selectDialog(links_list)
    #PLAYLINK('test', choice, iconimage)
    #print(choice, title, season, episode)
    #player.player().run(title, year, season, episode, '', '', links_list[choice], '')

def search(url):
    url = url+'search?keyword='
    search_entered = ''
    keyboard = xbmc.Keyboard(search_entered, 'Search')
    keyboard.doModal()
    if keyboard.isConfirmed():
        search_entered = keyboard.getText().replace(' ','+')
    if len(search_entered) > 1:
        url = url + search_entered
        do_search(url)

def do_search(url):
    get_anime_list(url)

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

def addLink(items):
    print(items)
    if items == None or len(items) == 0:
        control.idle()
        sys.exit()
    sysaddon = sys.argv[0]
    syshandle = int(sys.argv[1])
    addonFanart, addonThumb, artPath = control.addonFanart(), control.addonThumb(), control.artPath()

    for i in items:
        try:
            name = i['name']
            thumb = i['image']
            url = '%s?action=%s' % (sysaddon, i['url'])
            fanart = i['fanart']
            desc = i['desc']

            item = control.item(label=name)
            item.setArt({'icon' : thumb, 'thumb' : thumb, 'fanart' : fanart})
            item.setInfo(type='Video', infoLabels={"Title" : name, 'Plot' : desc})
            item.setProperty('fanart_image', fanart)
            control.addItem(handle=syshandle, url=url, listitem=item, isFolder=False)
        except:
            pass

def addDirectory(items):
    print(items)
    if items == None or len(items) == 0:
        control.idle()
        sys.exit()
    sysaddon = sys.argv[0]
    syshandle = int(sys.argv[1])
    addonFanart, addonThumb, artPath = control.addonFanart(), control.addonThumb(), control.artPath()

    for i in items:
        try:
            name = i['name']
            thumb = i['image']
            url = '%s?action=%s' % (sysaddon, i['url'])
            print(url)
            fanart = i['fanart']
            desc = i['desc']

            item = control.item(label=name)
            item.setArt({'icon' : thumb, 'thumb' : thumb, 'fanart' : fanart})
            item.setInfo(type='Video', infoLabels={"Title" : name, 'Plot' : desc})
            item.setProperty('fanart_image', fanart)

            control.addItem(handle=syshandle, url=url, listitem=item, isFolder=True)
        except:
            pass


def addDialog(dct):
    lst = []
    url = []
    for i in dct:
        name = i
        url.append(dct[i])
        lst.append(i)
    dlg = control.selectDialog(lst)
    url = url[dlg]
    print url
    #u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&description="+urllib.quote_plus(desc)
    return url

def PLAYLINK(name,url,iconimage):
    liz=xbmcgui.ListItem(name, iconimage)
    xbmc.Player().play(url, liz, False)

def playlink(url, meta):
    print(meta)
    meta = eval(meta)
    title = meta['TVShowTitle']
    #year = meta['year']
    season = meta['season']
    episode = meta['episode']
    #tvdb = meta['tvdb_id']
    #PLAYLINK(name, url, iconimage)
    player.player().run(title, 2000, season, episode, 8937, 30765, url, meta)

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
    show = params.get('show')
    meta = params.get('meta')

    print(params)

    if action == None:
        navigator.navigator().root()
    elif action == 'movies':
        get_movies(url)
    elif action == 'search':
        search(url)
    elif action == 'mostwatched':
        get_most_watched(url)
    elif action == 'genres':
        get_genres(url)
    elif action == 'get_genre':
        get_genre(url, name)
    elif action == 'next_page':
        get_anime_list(url)
    elif action == 'get_episodes':
        get_episodes(url, title, image)
    elif action == 'get_video_links':
        get_video_links(url, title, year, season, episode, show)
    elif action == 'playlink':
        playlink(url, meta)

    xbmcplugin.endOfDirectory(int(sys.argv [1]))
