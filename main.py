import xbmc,xbmcplugin,xbmcgui,xbmcaddon,xbmcvfs
import re
import urllib,urllib2
import os
import net

from bs4 import BeautifulSoup
import simplejson

from t0mm0.common.addon import Addon

from config import *

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
        genres = ['action', 'adventure', 'cars', 'comedy', 'dementia', 'demons',
                          'drama', 'ecchi', 'fantasy', 'game', 'harem', 'historical',
                          'horror', 'horror', 'josei', 'kids', 'magic', 'martial-arts',
                          'mecha', 'military', 'music', 'mystery', 'parody', 'police',
                          'psychological', 'romance', 'samurai', 'schoo', 'sci-fi',
                          'seinen', 'shoujo', 'shoujo-ai', 'shounen', 'shounen-ai',
                          'slice-of-life', 'space', 'sports', 'super-power',
                          'supernatural', 'thriller', 'vampire', 'yaoi', 'yuri']
        for i in genres:
                addDir(i, _domain_url+'genre/'+i, i, iconimage, iconimage)

def get_genre(url, mode, iconimage):
    get_anime_list(url, iconimage)

def get_newest(url, mode, iconimage):
    get_anime_list(url, iconimage)

def get_most_watched(url, iconimage):
    get_anime_list(url, iconimage)

def get_anime_list(url, iconimage):
    html = open_url(url)
    soup = BeautifulSoup(html, 'html.parser')
    temp = soup.find_all('div')
    for i in temp:
        try:
            if 'item' in i.attrs['class']:
                s = BeautifulSoup(open_url(_domain_url+i.a.get('data-tip')))
                addDir(i.a.img.get('alt'), i.a.get('href'), 99, i.a.img.get('src'), iconimage, s.find_all('span')[7].get_text())
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

def get_episodes(url, iconimage):
    print "get_episodes called"
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
        print _domain_url+i.get('data-id')
        addDir("Episode "+i.get('data-base'), i.get('data-id'), 98, iconimage, iconimage)

def get_video_links(name, url, iconimage):
    print name
    print url
    print iconimage
    vid_info = simplejson.loads(open_url('https://9anime.to/ajax/episode/info?id='+url+"&update=0"))
    print vid_info
    vid_id = vid_info['params']['id']
    token = vid_info['params']['token']
    options = vid_info['params']['options']
    base_grabber = 'https://9anime.to/grabber-api/?id='+vid_id+'&token='+token+'&options='+options
    video_links = simplejson.loads(open_url(base_grabber))
    print video_links
    for i in video_links['data']:
        addLink(i['label'], i['file'], 97, iconimage, iconimage)

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
    addDir('Most Watched', _domain_url+'most-watched', 3, anime, fanart)
    addDir('Search', _domain_url+'search?keyword=', 4, anime, fanart)
    addDir('Newest', _domain_url+'newest', 2, anime, fanart)
    addDir('Genre', _domain_url+'genre', 1, anime, fanart)

def addDir(name,url,mode,iconimage,fanart,description=''):
    '''
    name, url, mode, iconimage, fanart, description=""
    '''
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&description="+urllib.quote_plus(description)
    ok=True
    liz=xbmcgui.ListItem(name.strip(), iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description} )
    liz.setProperty('fanart_image', fanart)
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
    return ok

def addLink(name,url,mode,iconimage,fanart,description=''):
    u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&description="+urllib.quote_plus(description)
    ok=True
    liz=xbmcgui.ListItem(name.strip(), iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description} )
    liz.setProperty('fanart_image', fanart)
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
    return ok

def PLAYLINK(name,url,iconimage):
    liz=xbmcgui.ListItem(name, iconimage)
    xbmc.Player().play(url, liz, False)

def get_playlink(name, url, iconimage):
    PLAYLINK(name, url, iconimage)

def open_url(url):
    print "opening url "+url
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

    print type(mode)

    if mode is None or url is None or len(url) < 1:
        main()
    elif mode is 1:
        print "entered mode 1"
        get_genres(url, iconimage)
    elif mode is 2:
        print "entered mode 2"
        get_newest(url, iconimage)
    elif mode is 3:
        print "entered mode 3, executing get_most_watched("+url+")"
        get_most_watched(url, iconimage)
    elif mode is 4:
        search(url)
    elif mode is 97:
        get_playlink(name, url, iconimage)
    elif mode is 98:
        print "entered mode 98, executing get_video_links("+url+")"
        get_video_links(name, url, iconimage)
    elif mode is 99:
        print "entered mode 99, executing get_episodes("+url+")"
        get_episodes(url, iconimage)
    elif mode is 100:
        print "entered mode 100"
        get_play_link(name, url, iconimage)
    elif 'str' in str(type(mode)):
        print 'assuming mode is genre'
        get_genre(url, mode, iconimage)

    xbmcplugin.endOfDirectory(int(sys.argv [1]))
