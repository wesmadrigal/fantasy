#!/usr/bin/env python
import urllib
import urllib2
import mechanize
import cookielib
url = 'http://www.footballdb.com/teams/'


br = mechanize.Browser()
cj = cookielib.LWPCookieJar()
br.set_cookiejar(cj)
br.addheaders = [('User-Agent', 'Mozilla/5.0(X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
br.set_handle_equiv(True)
br.set_handle_robots(False)
br.set_handle_gzip(True)
br.set_debug_http(True)
br.set_debug_redirects(True)
br.open(url) abs_url = link.absolute_url
    start_team = abs_url.find('/', abs_url.find('/nfl/')+5)
    end_team = abs_url.find('/', start_team+1)
    team = abs_url[start_team+1:end_team]
links = [ i for i in br.links() ]
team_info = {}
team_links = [ i for i in links if '/teams/nfl/' in i.absolute_url ]
for link in team_links:
    team = link.text.lower()
    if team not in team_info.keys():
        team_info[team] = {}
    else:
        pass
    


def get_teams():
    links = [ i for i in br.links() ]
    team_info = {}
    team_links = [ i for i in links if '/teams/nfl/' in i.absolute_url ]
    for link in team_links:
        team = link.text.lower()
        team_url = link.absolute_url
        if team not in team_info.keys():
            team_info[team] = {'url': team_url}
        else:
            pass
