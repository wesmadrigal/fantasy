fantasy
=======

fantasy football data mining

<h1>A library for mining NFL data</h1>
<p>This is a WIP, but ideally the library will be able to mine all nfl team, player, and statistical data</p>

<ul>Accomplishments<br>
<li>NFLData class</li>
<li>Above gets nfl teams</li>
<li>Gets nfl players</li>
<li>Gets player statistics</li>
<li>Loads all into objects</li>
<li>Extensible</li>
</ul>
<br><br>
<ul>Todo<br>
<li>Add functionality to get holistic team data and not just player data</li>
<li>Build probability distrubutions around the stats</li>
<li>Build and API</li>
</ul>

<h1>Usage</h1>

<p><code>from fantasy import NFLData<br>
# instantiate an NFLData object<br>
nfl = NFLData()<br>
nfl._get_teams()<br>
nfl._get_players()<br>
nfl.get_player_stats()<br>
# we now have a fully accessible nfl object<br>
# the below will pop up a raw input with options for you to pick your team
stl_rams = nfl.get_team()</code>
</p>
