# -*- coding: utf-8 -*-

import re,urllib,urlparse,json

from bs4 import BeautifulSoup

from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import directstream
from resources.lib.modules import trakt
from resources.lib.modules import tvmaze

class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['9anime.to']
        self.base_link = 'https://9anime.to'
        self.search_link = '/search?keyword=%s'
        self.episode_link = '/watch/%s.%s/%s'

    def tvshow(self, imdb, tvdb, tvshowtitle, year):
        try:
            print('in tvshow({},\n {},\n {},\n {},\n {})'.format(self, imdb, tvdb, tvshowtitle, year))
            r = 'search/tvdb/{}?type=show&extended=full'.format(tvdb)
            r = json.loads(trakt.getTrakt(r))
            print(r)
            if not r:
                print('r was not?')
                return '0'

            print('doing this d thing?')
            d = r[0]['show']['genre']
            print(d)
            if not ('anime' in d or 'animation' in d): return '0'

            tv_maze = tvmaze.tvMaze()
            tvshowtitle = tv_maze.showLookup('thetvdb', tvdb)
            tvshowtitle = tvshowtitle['name']

            t = cleantitle.get(tvshowtitle)

            q = self.search_link % (urllib.quote_plus(tvshowtitle))
            q = urlparse.urljoin(self.base_link, q)

            r = client.request(q)
            r = r.decode('iso-8859-1').encode('utf-8')

            print(r)
        except:
            return

    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        pass

    def sources(self, url, hostDict, hostprDict):
        pass

    def resolve(self, url):
        pass


# def get_genres(url):
#         genres = {'action' : 'Action', 'adventure' : 'Adventure', 'cars' : 'Cars',
#                   'comedy' : 'Comedy', 'dementia' : 'Dementia', 'demons' : 'Demons',
#                   'drama' : 'Drama', 'ecchi' : 'Ecchi', 'fantasy' : 'Fantasy',
#                   'game' : 'Game', 'harem' : 'Harem', 'historical' : 'Historical',
#                   'horror' : 'Horror', 'josei' : 'Josei', 'kids' : 'Kids',
#                   'magic' : 'Magic', 'martial-arts' : 'Martial Arts',
#                   'mecha' : 'Mecha', 'military' : 'Military', 'music' : 'Music',
#                   'mystery' : 'Mystery', 'parody' : 'Parody', 'police' : 'Police',
#                   'psychological' : 'Psychological', 'romance' : 'Romance',
#                   'samurai' : 'Samurai', 'school' : 'School', 'sci-fi' : 'Sci Fi',
#                   'seinen' : 'Seinen', 'shoujo' : 'Shoujou', 'shoujo-ai' : 'Shoujo Ai',
#                   'shounen' : 'Shounen', 'shounen-ai' : 'Shounen Ai',
#                   'slice-of-life' : 'Slice of Life', 'space' : 'Space',
#                   'sports' : 'Sports', 'super-power' : 'Super Power',
#                   'supernatural' : 'Supernatural', 'thriller' : 'Thriller',
#                   'vampire' : 'Vampire', 'yaoi' : 'Yaoi', 'yuri' : 'Yuri'}

#         for i in genres:
#                 navigator.navigator().addDirectoryItem(genres[i], 'get_genre&url='+url+'&name='+i, 'genres.pg', 'DefaultTvShows.png')
#         navigator.navigator().endDirectory()

# def get_genre(url, name):
#     url = url+'genre/'+name
#     print(url)
#     get_anime_list(url)

# def get_newest(url):
#     get_anime_list(url, iconimage)

# def get_most_watched(url):
#     get_anime_list(url+'filter?type[]=series&sort=views%3Adesc')

# def get_movies(url):
#     get_anime_list(url+'filter?type[]=movie&sort=views%3Adesc')

# def get_anime_list(url):
#     print(url)
#     metadata = metahandlers.MetaData(preparezip=False, tmdb_api_key='6cd18c483332380fd24ae41316af596f')
#     html = open_url(url)
#     soup = BeautifulSoup(html, 'html.parser')
#     temp = soup.find_all('div')
#     show = []
#     for i in temp:
#         try:
#             if 'item' in i.attrs['class']:
#                 title = i.a.img.get('alt').replace(' (Dub)', '').replace(':', '')
#                 info = metadata.get_meta('tvshow', name=title, imdb_id='')
#                 show.append({'name' : i.a.img.get('alt'),
#                              'url' : 'get_episodes&url={}&title={}'.format(i.a.get('href'), info['title']),
#                              'image' : info['cover_url'],
#                              'fanart' : info['backdrop_url'],
#                              'banner' : info['banner_url'],
#                              'desc' : info['plot']})
#         except:
#             print('Caught exception: {}'.format(sys.exc_info()[0]))

#     temp = soup.find_all('a')
#     for i in temp:
#         try:
#             if 'btn' in i.attrs['class']:
#                 if 'Next' in i.get_text():
#                     show.append({'name' : 'Next',
#                                  'url' : 'next_page&url={}'.format(urllib.quote_plus(_domain_url+i.attrs.get('href'))),
#                                  'image' : '',
#                                  'fanart' : '',
#                                  'desc' : ''})
#         except:
#             print('Caught exception: {}'.format(sys.exc_info()[0]))
#     print(show)
#     addDirectory(show, 'tvshows')

# def get_episodes(url, title):
#     metadata = metahandlers.MetaData(preparezip=False, tmdb_api_key='6cd18c483332380fd24ae41316af596f')
#     html = open_url(url)
#     soup = BeautifulSoup(html, 'html.parser')
#     temp = soup.find_all('div')
#     for i in temp:
#         try:
#             if 'server' in i.attrs['class']:
#                 eps = i.find_all('a')
#                 break
#         except:
#             pass
#     episodes = []
#     for i in eps:
#         info = metadata.get_episode_meta(title, '', 1, i.get('data-base'), episode_title=title)
#         episodes.append({'name' : 'Episode {} - {}'.format(info['episode'], info['title'].encode('utf-8')),
#                          'url' : 'get_video_links&url='+i.get('data-id')+'&title='+info ['title']+'&season='+str(info ['season'])+'&episode='+str(info ['episode'])+'&show='+info['TVShowTitle'],
#                          'image' : info['cover_url'],
#                          'fanart' : info['backdrop_url'],
#                          'desc' : info['plot']})
#     addDirectory(episodes, 'episodes')

# def get_video_links(url, title, year, season, episode, show):
#     print(url)
#     metadata = metahandlers.MetaData(preparezip=False)
#     info = metadata.get_episode_meta(show, '', season, episode, episode_title=title)
#     vid_info = simplejson.loads(open_url('https://9anime.to/ajax/episode/info?id='+url+"&update=0"))
#     print(vid_info)
#     vid_id = vid_info['params']['id']
#     token = vid_info['params']['token']
#     options = vid_info['params']['options']
#     base_grabber = 'https://9anime.to/grabber-api/?id='+vid_id+'&token='+token+'&options='+options
#     video_links = simplejson.loads(open_url(base_grabber))
#     print(video_links)
#     #links_list = {}
#     links_list = []
#     items = []
#     #for i in video_links['data']:
#         #links_list[i['label']] = i['file']
#     for i in video_links['data']:
#         links_list.append(i['file'])
#         items.append({'name' : i['label'],
#                       'url' : 'playlink&url=%s&meta=%s' % (urllib.quote_plus(i['file']), urllib.quote_plus(str(info))),
#                       'image' : info['cover_url'],
#                       'fanart' : info['backdrop_url'],
#                       'desc' : info['plot']})
#         #addLink(i['label'], i['file'], 97, iconimage, iconimage)
#         #choice = addDialog(i['label'], i['file'], 97, iconimage, iconimage)
#     select = addLink(items)
#     return select
#     #choice = control.selectDialog(links_list)
#     #PLAYLINK('test', choice, iconimage)
#     #print(choice, title, season, episode)
#     #player.player().run(title, year, season, episode, '', '', links_list[choice], '')

# def search(url):
#     try:
#         control.idle()

#         url = url+'search?keyword='
#         k = control.keyboard('', 'Search')
#         k.doModal()
#         q = k.getText() if k.isConfirmed() else None

#         if (q == None or q == ''):
#             return

#         url = url + urllib.quote_plus(q)
#         url = "{}?action=do_search&url={}".format(sys.argv[0], urllib.quote_plus(url))
#         control.execute('Container.Update({})'.format(url))
#     except:
#         return

# def do_search(url):
#     get_anime_list(url)

# def addLink(items):
#     print(items)
#     if items == None or len(items) == 0:
#         control.idle()
#         sys.exit()
#     sysaddon = sys.argv[0]
#     syshandle = int(sys.argv[1])
#     addonFanart, addonThumb, artPath = control.addonFanart(), control.addonThumb(), control.artPath()

#     for i in items:
#         try:
#             name = i['name']
#             thumb = i['image']
#             url = '%s?action=%s' % (sysaddon, i['url'])
#             fanart = i['fanart']
#             desc = i['desc']

#             item = control.item(label=name)
#             item.setArt({'icon' : thumb, 'thumb' : thumb, 'fanart' : fanart})
#             item.setInfo(type='Video', infoLabels={"Title" : name, 'Plot' : desc, 'plotoutline' : desc})
#             item.setProperty('fanart_image', fanart)
#             control.addItem(handle=syshandle, url=url, listitem=item, isFolder=False)
#         except:
#             pass

# def addDirectory(items, content):
#     print(items)
#     if items == None or len(items) == 0:
#         control.idle()
#         sys.exit()
#     sysaddon = sys.argv[0]
#     syshandle = int(sys.argv[1])
#     addonThumb, artPath = control.addonThumb(), control.artPath()

#     for i in items:
#         try:
#             name = i['name']
#             thumb = i['image']
#             url = '%s?action=%s' % (sysaddon, i['url'])
#             fanart = i['fanart']
#             try:
#                 banner = i['banner']
#             except:
#                 banner = ''
#             desc = i['desc']

#             item = control.item(label=name)
#             item.setArt({'icon' : thumb, 'thumb' : thumb, 'fanart' : fanart, 'banner' : banner})
#             item.setInfo(type='Video', infoLabels={"Title" : name, 'Plot' : desc})
#             item.setProperty('fanart_image', fanart)
#             control.content(syshandle, content)

#             control.addItem(handle=syshandle, url=url, listitem=item, isFolder=True)
#         except:
#             pass


# def addDialog(items):
#     try:
#         print('in addDialog({})'.format(items))
#         labels = [i['name'] for i in items]

#         select = control.selectDialog(labels)
#         if select == -1:
#             select.close()
#             return 'close://'

#         url = items[select]['url']
#         url = '{}?action={}'.format(sys.argv[0], url)
#         print(url)
#         control.execute('Container.Update({})'.format(url))

#         return items[select]
#     except:
#         print('Caught exception in addDialog: {}'.format(sys.exc_info()[0]))


# def PLAYLINK(name,url,iconimage):
#     liz=xbmcgui.ListItem(name, iconimage)
#     xbmc.Player().play(url, liz, False)

# def playlink(url, meta):
#     print(meta)
#     meta = eval(meta)
#     title = meta['TVShowTitle']
#     #year = meta['year']
#     season = meta['season']
#     episode = meta['episode']
#     #tvdb = meta['tvdb_id']
#     #PLAYLINK(name, url, iconimage)
#     player.player().run(title, 2000, season, episode, 8937, 30765, url, meta)

# def open_url(url):
#     print("opening url "+url)
#     net.set_cookies(cookie_file)
#     link = net.http_GET(url).content
#     return link

# if __name__ == '__main__':
#     params = dict(urlparse.parse_qsl(sys.argv[2].replace('?','')))

#     action = params.get('action')
#     name = params.get('name')
#     title = params.get('title')
#     year = params.get('year')
#     imdb = params.get('imdb')
#     tvdb = params.get('tvdb')
#     season = params.get('season')
#     episode = params.get('episode')
#     premiered = params.get('premiered')
#     url = params.get('url')
#     image = params.get('image')
#     meta = params.get('meta')
#     select = params.get('select')
#     query = params.get('query')
#     source = params.get('source')
#     content = params.get('content')
#     show = params.get('show')
#     meta = params.get('meta')

#     print(params)

#     if action == None:
#         navigator.navigator().root()
#     elif action == 'movies':
#         get_movies(url)
#     elif action == 'search':
#         search(url)
#     elif action == 'mostwatched':
#         get_most_watched(url)
#     elif action == 'genres':
#         get_genres(url)
#     elif action == 'get_genre':
#         get_genre(url, name)
#     elif action == 'next_page':
#         get_anime_list(url)
#     elif action == 'get_episodes':
#         get_episodes(url, title)
#     elif action == 'get_video_links':
#         get_video_links(url, title, year, season, episode, show)
#     elif action == 'playlink':
#         playlink(url, meta)
#     elif action == 'do_search':
#         do_search(url)

#     xbmcplugin.endOfDirectory(int(sys.argv [1]))
