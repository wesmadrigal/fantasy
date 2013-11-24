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

<p><code><b>from fantasy import NFLData<br>
# instantiate an NFLData object<br>
nfl = NFLData()<br>
nfl._get_teams()<br>
nfl._get_players()<br>
nfl.get_player_stats()<br>
# we now have a fully accessible nfl object<br>
# the below will pop up a raw input with options for you to pick your team
stl_rams = nfl.get_team()</b></code>
</p>

<br>
<h1>License</h1>
Copyright (C) 2013 by Wes Madrigal

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
