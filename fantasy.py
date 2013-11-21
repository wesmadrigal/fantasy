#!/usr/bin/env python
import urllib
import urllib2
import mechanize
import cookielib
import re
url = 'http://www.footballdb.com/teams/'

class TestClass(object):
    def __init__(self):
        self._id = int()
        
    def __str__(self):
        return str(self._id)

class NFLData(object):
    def __init__(self):
        self._url = url
        self._br = get_browser()
       
    def _get_teams(self):
        self.teams = get_teams(url, self._br)
    
    def _get_players(self):
        get_players(self.teams, self._br)

    # must be called subsequent to the other two methods and will take some time to run
    def get_player_stats(self):
        for team in self.teams.keys():
            for player in self.teams[team]['players'].keys():
                cur_player_url = self.teams[team]['players'][player]['url']
                locations = find_locations(cur_player_url)
                response = urllib2.urlopen(cur_player_url).read()
                stats = build_stats(locations, response)
                # set the players statistics
                self.teams[team]['players'][player]['stats'] = stats
        



def get_browser():
    br = mechanize.Browser()
    cj = cookielib.LWPCookieJar()
    br.set_cookiejar(cj)
    br.addheaders = [('User-Agent', 'Mozilla/5.0(X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
    br.set_handle_equiv(True)
    br.set_handle_robots(False)
    br.set_handle_gzip(True)
    br.set_debug_http(True)
    br.set_debug_redirects(True)
    return br


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
def get_players(teams, br):
    for team in teams.keys():
        url = teams[team]['url']
        if 'buffalo-bills' in url:
            url = 'http://www.footballdb.com/teams/nfl/buffalo-bills'
        br.open(url + '/roster')
        players = [ i for i in br.links() if '/players/' in i.absolute_url ]
        players_object = { i.text : { 'url' : i.absolute_url } for i in players }
        # add the players to our team
        teams[team]['players'] = players_object
        print "%s players added" % team
    print "All teams players mined"


# finds all the statistics table locations on the parameterized player's page
def find_locations(url):
    # response = urllib2.urlopen(player['url']).read()
    response = urllib2.urlopen(url).read()
    to_find = '<div class="mdtext">'
    locations = [ response.find(to_find) ]
    while response.find(to_find, locations[len(locations)-1]+1) != -1:
        locations.append( response.find(to_find, locations[len(locations)-1]+1) )
    #stats_object = build_stats(locations, response)
    #return stats_object
    # find the college dividing line and don't take into the fucking college statistics
    college = response.find('College statistics')
    try:
        while locations[len(locations)-1] > college:
            locations.pop()
    except IndexError:
        pass
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
        # clean up the messy info with our function
        info = cleanup_info(info)
         
            # if our current table is rushing/receving
        if 'Receiving/Rushing Statistics' in info or 'Rushing/Receiving Statistics' in info:
            parse_receiving(stats_object, info)
        elif 'Passing Statistics' in info:
            parse_passing(stats_object, info)
        elif 'Scoring Statistics' in info:
            parse_scoring(stats_object, info)
        elif 'Defensive Statistics' in info:
            parse_defensive(stats_object, info)
        elif 'Kickoff Returns' in info:
            parse_return(stats_object, info)
        elif 'Kicking Statistics' in info:
            parse_kicking(stats_object, info) 
        elif 'Kickoff Statistics' in info:
            parse_kickoff(stats_object, info)
        elif 'Punting Statistics' in info:
            parse_punting(stats_object, info)

    return stats_object


def parse_receiving(stats_object, info):
    # Receiving/Rushing statistics
    titles = info[0:20]
    main_data = info[20: info.index('Career Totals')]
    career_totals = info[ info.index('Career Totals') : ]
    # update our stats_object
    category = titles[0]
    receiving = titles[2]
    rushing = titles[3]
    stats_object[category] = { receiving : [], rushing : [] }
    for i in range(0, len(main_data), 16):
        this = main_data[i : i+16]
        year, team, g, gs = this[0:4]
        rec_stuff = [year, team, g, gs] + this[4:10]
        rush_stuff = [year, team, g, gs] + this[10:] 
        # add these statistics to our stats_object
        stats_object[category][receiving].append( rec_stuff )
        stats_object[category][rushing].append( rush_stuff )
    total_g, total_gs = career_totals[1], career_totals[2]
    rec_totals = [total_g, total_gs] + career_totals[3:9]
    rush_totals = [total_g, total_gs] + career_totals[9:]
    # add our totals to our stats_object
    stats_object[category][receiving].append( rec_totals )
    stats_object[category][rushing].append( rush_totals )
    print "Receiving/Rushing updated" 


def parse_passing(stats_object, info):
    # Passing Statistics box
    # each row has the following columns which are combined together
    # year team G GS Att Cmp Pt Yds Avg TD TD% Int Int% Lg Sack Loss Rate
    titles = info[0:20]
    main_data = info[ 20 : info.index('Career Totals') ]
    career_totals = info[ info.index('Career Totals') : ]
    category = titles[0]
    # our sub_category here is just passing, unlike Rushing/Receiving which has 2 sub-categories
    sub_category = titles[2]
    # lets set up our stats object to populate this category and sub-category
    stats_object[category] = { sub_category : [] }
    # it would be handy to have a schema of this category
    stats_object[category]['schema'] = ['year', 'team', 'G', 'GS', 'Att', 'Cmp', 'Pt', 'Yds', 'Avg', 'TD', 'TD%', 'Int', 'Int%', 'Lg', 'Sack', 'Loss', 'Rate']
    # our columns are titles[3:], we don't really need or want them in our data structure
    # we have 17 columns, year, team, ...etc 
    for i in range(0, len(main_data), 17):
        this = main_data[i: i+17]
        stats_object[category][sub_category].append(this)
   
    # add our career totals to the end of our 2d array
    # NOTE this will have a length 2 less than all our other statistics columns
    stats_object[category][sub_category].append(career_totals[1:])
    print "Passing Statistics added"  


def parse_scoring(stats_object, info):
    # Scoring Statistics box
    # each row has sub-rows of touchdowns ( 9 items ), kicking (2 itmes), conv. (2 items), misc.(2 items)
    titles = info[0:25]
    main_data = info[25: info.index('Career Totals') ]
    career_totals = info[ info.index('Career Totals') : ]
    category = titles[0]
    touchdowns = titles[2]
    kicking = titles[3]
    conversions = titles[4]
    misc = titles[5]
    stats_object[category] = { touchdowns: [], kicking: [], conversions: [], misc: [] }
    # our schema looks something like this
    # touchdowns
    # [ year, team, g, gs, R, P, KR, PR, IR, FR, BK, BP, FGR ]
    # kicking
    # [ g, gs, PAT, FG ]
    # conv
    # [ R, P ]
    # misc
    # [ Saf Pts ]

    for i in range(0, len(main_data), 19):
        this = main_data[i: i+19]
        year, team, g, gs = this[0], this[1], this[2], this[3]
        touchdown_stuff = [ year, team, g, gs, this[4], this[5], this[6], this[7], this[8], this[9], this[10], this[11], this[12] ]
        kicking_stuff = [ year, team, g, gs, this[13], this[14] ]
        conversion_stuff = [ year, team, g, gs, this[15], this[16] ]
        misc_stuff = [ year, team, g, gs, this[17], this[18] ]
        # add it all to our stats_object in the correct places
        stats_object[category][touchdowns].append( touchdown_stuff )
        stats_object[category][kicking].append( kicking_stuff )
        stats_object[category][conversions].append( conversion_stuff )
        stats_object[category][misc].append( misc_stuff )
    # add our career totals
    total_g, total_gs = career_totals[1], career_totals[2]
    touchdown_totals = [total_g, total_gs] + career_totals[3:12]
    kicking_totals = [total_g, total_gs] + career_totals[12:14]
    conversion_totals = [total_g, total_gs] + career_totals[14:16]
    misc_totals = [total_g, total_gs] + career_totals[16:]
    print "Scoring Statistics built" 


def parse_defensive(stats_object, info):
    # defensive tables parsing algorithm
    titles = info[0:19]
    main_data = info[19: info.index('Career Totals')]
    career_totals = info[ info.index('Career Totals') : ]
    category = titles[0]
    tackles = titles[2]
    sacks = titles[3]
    interceptions = titles[4]
    # update our stats_object to get ready for more data, this data
    stats_object[category] = { tackles: [], sacks: [], interceptions: [] }
    # iterate by 14s 
    for i in range(0, len(main_data), 14):
        this = main_data[ i : i+14 ]
        year, team, g, gs = this[0], this[1], this[2], this[3]
        tackle_stuff = [year, team, g, gs] + this[4:7]
        sack_stuff = [year, team, g, gs] + this[7:9]
        int_stuff = [year, team, g, gs] + this[9:]
        # add it to our stats object
        stats_object[category][tackles].append( tackle_stuff )
        stats_object[category][sacks].append( sack_stuff )
        stats_object[category][interceptions].append( int_stuff )
        
    total_g, total_gs = career_totals[1], career_totals[2]
    tackle_totals = [total_g, total_gs ] + career_totals[3:6]
    sack_totals = [total_g, total_gs ] + career_totals[6:8]
    int_totals = [total_g, total_gs] + career_totals[8:]
    # add our totals and we're done
    stats_object[category][tackles].append( tackle_totals )
    stats_object[category][sacks].append( sack_totals )
    stats_object[category][interceptions].append( int_totals )
    print "Defensive Statistics built"


def parse_return(stats_object, info):
    # parse the return statistics objects
    # schema will look something like...
    # { kickoff_returns : [ g, gs, num, yds, avg, fc, lg, td],
    #   punt_returns : [ g, gs, num, yds, avg, fc, lg, td
    # }
    titles = info[0:20]
    category = titles[0]
    kr = titles[2]
    pr = titles[3]
    main_data = info[ 20 : info.index('Career Totals') ]
    career_totals = info[ info.index('Career Totals') : ]
    stats_object[category] = { kr : [], pr : [] }
    for i in range(0, len(main_data), 16):
        this = main_data[ i : i+16 ]
        year, team, g, gs = this[0:4]
        kr_stuff = [year, team, g, gs] + this[4:10]
        pr_stuff = [year, team, g, gs] + this[10:]
        # add this stuff to our stats_object
        stats_object[category][kr].append( kr_stuff )
        stats_object[category][pr].append( pr_stuff )
        
    # get our career_totals in order and add it to our object
    g, gs = career_totals[1], career_totals[2]
    kr_totals = [g, gs] + career_totals[3:9]
    pr_totals = [g, gs] + career_totals[9:]
    stats_object[category][kr].append( kr_totals )
    stats_object[category][pr].append( pr_totals )
    print "Return Statistics updated"


def parse_kicking(stats_object, info):
    # for kickers there is a table called Kicking Statistics with a schema like:
    # year, team, g, gs, pat, fg, 0-19, 20-29, 30-39, 40-49, 50+, Lg, Pts
    titles = info[0:16]
    category = titles[0]
    kicking = titles[2]
    main_data = info[16: info.index('Career Totals') ]
    career_totals = info[ info.index('Career Totals') : ]
    # update stats_object
    stats_object[category] = { kicking : [] }

    for i in range(0, len(main_data), 13):
        this = main_data[ i : i+13 ]
        stats_object[category][kicking].append( this )
    # add career totals
    stats_object[category][kicking].append( career_totals[1:] )
    print "Kicking Statistics updated"


def parse_kickoff(stats_object, info):
    # for kickers we also have the Kickoff Statistics table with a schema like:
    #           kickoffs                 opponent returns    onside kicks
    # G, GS  Num, Yds, Avg, Lg, TB, OB,  Ret, Yds, TDs,     OSK,    OSR
    titles = info[0:20]
    category = titles[0]
    kickoffs = titles[2]
    opp_returns = titles[3]
    onside_kicks = titles[4]
    main_data = info[20: info.index(' Totals') ]
    totals = info[ info.index(' Totals') : ]
    # update our stats object accordingly
    stats_object[category] = { kickoffs : [], opp_returns : [], onside_kicks : [] }
    for i in range(0, len(main_data), 15):
        this = main_data[ i : i+15 ]
        year, team, g, gs = this[0:4]
        kickoff_stuff = [year, team, g, gs] + this[4:10]
        opp_return_stuff = [year, team, g, gs] + this[10:13]
        onside_stuff = [year, team, g, gs] + this[13:]
        # update each sub-category accordingly
        stats_object[category][kickoffs].append( kickoff_stuff )
        stats_object[category][opp_returns].append( opp_return_stuff )
        stats_object[category][onside_kicks].append( onside_stuff )
    # now we need to iterate through and add our totals to each sub-category
    total_g, total_gs = totals[1], totals[2]
    kickoff_totals = [total_g, total_gs] + totals[3:9]
    opp_return_totals = [total_g, total_gs] + totals[9:12]
    onside_totals = [total_g, total_gs] + totals[12:]
    # add totals to our object
    stats_object[category][kickoffs].append( kickoff_totals )
    stats_object[category][opp_returns].append( opp_return_totals )
    stats_object[category][onside_kicks].append( onside_kicks )
    print "Kickoff Statistics updated"


def parse_punting(stats_object, info):
    # for kickers we also have Punting Statistics table with a schema like
    # G, GS, Punts, Yds, Avg, Lg, TB, In20, Blk, Ret, Yds, Net
    titles = info[0:17]
    category = titles[0]
    sub_category = titles[2] 
    main_data = info[17 : info.index(' Totals') ]
    totals = info[ info.index(' Totals') : ]
    # update our stats object
    stats_object[category] = { sub_category : [] }
    for i in range(0, len(main_data), 14):
        this = main_data[i : i+14]
        stats_object[category][sub_category].append( this )
    # now we need to update our totals
    totals = totals[1:]
    stats_object[category][sub_category].append( totals )
    print "Punting Statistics updated"
 
 
def build_stats_test(loc, response):
    stats_object = {}
    # our compile regular expression sequence for finding the info we give as shit about
    seq = re.compile(r'>.*?<')
 
    end = response.find('</table>', loc)
    current_string = response[ loc : end ]
    # parse the string with our regular expression and grab all of the data we need in between > <
    info = re.findall(seq, current_string)
    # get rid of the html characters
    for j in range(len(info)):
        info[j] = info[j].strip('>')
        info[j] = info[j].strip('<')
    [ info.remove(i) for i in info if i == '' ]
    # category and sub category information is here
    title_stuff = info[0:20]
    career_totals_location = info.index('Career Totals')
    main_data = info[20:career_totals_location]
    career_totals = info[career_totals_location:]
    category = title_stuff[0]
    # put the category in our stats_object
    sub_category1 = title_stuff[2]
    sub_category2 = title_stuff[3]
    stats_object[category] = { sub_category1 : [], sub_category2: [] }
    for i in range(0, len(main_data), 16):
        import pdb
        pdb.set_trace()
        this = main_data[i:i+16]
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



def cleanup_info(info):
    for j in range(len(info)):
        info[j] = info[j].strip('>')
        info[j] = info[j].strip('<')
    while len( [ info.remove(i) for i in info if i == '' ] ) > 0:
        [ info.remove(i) for i in info if i == '' ] 
    return info
