#!/usr/bin/env python
import urllib
import urllib2
import mechanize
import cookielib
import re
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
    

def get_teams(url, br):
    br.open(url)
    links = [ i for i in br.links() ]
    team_info = {}
    team_links = [ i for i in links if '/teams/nfl/' in i.absolute_url and '/stats' not in i.absolute_url and '/roster' not in i.absolute_url ]
    for link in team_links:
        team = link.text.lower()
        team_url = link.absolute_url
        if team not in team_info.keys():
            team_info[team] = {'url': team_url}
        else:
            pass
    return team_info


# for each team in the nfl, get all their players and information about those players
# remember we care about the roster, first and foremost
# add '/roster' to the url
def get_players(team, br):
    url = team['url']
    if 'buffalo-bills' in url:
        url = 'http://www.footballdb.com/teams/nfl/buffalo-bills'
    br.open(url + '/roster')
    players = [ i for i in br.links() if '/players/' in i.absolute_url ]
    players_object = { i.text : { 'url' : i.absolute_url } for i in players }
    return players_object

def find_stats(player):
    response = urllib2.urlopen(player['url']).read()
    to_find = '<div class="mdtext">'
    locations = [ response.find(to_find) ]
    while response.find(to_find, locations[len(locations)-1]+1) != -1:
        locations.append( response.find(to_find, locations[len(locations)-1]+1) )
    #stats_object = build_stats(locations, response)
    #return stats_object
    return locations



# takes as input a location iterable with the string locations of all the statistics tables for a given player and a response text
# of the html
# the re module is a dependency and must be imported prior to this function's execution
def build_stats(locs, response):
    stats_object = {}
    # our compile regular expression sequence for finding the info we give as shit about
    seq = re.compile(r'>.*?<')
    # for each table on the players page
    for table_location in locs:
        end = response.find('</table>', table_location)
        current_string = response[ table_location : end ]
        # parse the string with our regular expression and grab all of the data we need in between > <
        info = re.findall(seq, current_string)
        # get rid of the html characters
        for j in range(len(info)):
            if info[j] == '':
                info.remove(info[j])
            else:
                info[j] = info[j].strip('>')
                info[j] = info[j].strip('<')
        return info          
        # category and sub category information is here
        title_stuff = info[0:20]
        career_totals_location = info.index('Career Totals')
        main_data = info[20:career_totals_location]
        career_totals = info[career_totals_location:]
        category = title_stuff[0]
        # put the category in our stats_object
        return title_stuff, main_data
        sub_category1 = title_stuff[2]
        sub_category2 = title_stuff[3]
        stats_object[category] = { sub_category1 : [], sub_category2: [] }
        for i in range(0, len(main_data), 14):
            this = main_data[i:i+14]
            year = this[0]
            team = this[1]
            g = this[2]
            gs = this[3]
            att1 = this[4]
            yds1 = this[5]
            avg1 = this[6]
            lg1 = this[7]
            td1 = this[8]
            fd1 = this[9]
            att2 = this[10]
            yds2 = this[11]
            avg2 = this[12]
            lg2 = this[13]
            td2 = this[14]
            fd2 = this[15]
            cat1 = [year, team, g, gs, att1, yds1, avg1, lg1, td1, fd1]
            cat2 = [year, team, g, gs, att2, yds2, avg2, lg2, td2, fd2]
            stats_object[category][sub_category1].append(cat1)
            stats_object[category][sub_category2].append(cat2)
        
    return stats_object
