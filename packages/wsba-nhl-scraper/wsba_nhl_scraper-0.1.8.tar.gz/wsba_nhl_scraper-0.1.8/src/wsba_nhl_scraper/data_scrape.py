import re
from bs4 import BeautifulSoup, SoupStrainer
import hockey_scraper.utils.shared as shared
import numpy as np
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

# PREP FUNCTIONS
def get_pbp(game_id):
    """
    Given a game_id it returns the raw html
    Ex: http://www.nhl.com/scores/htmlreports/20162017/PL020475.HTM
    
    :param game_id: the game
    
    :return: raw html of game
    """
    game_id = str(game_id)
    url = 'http://www.nhl.com/scores/htmlreports/{}{}/PL{}.HTM'.format(game_id[:4], int(game_id[:4]) + 1, game_id[4:])

    page_info = {
        "url": url,
        "name": game_id,
        "type": "html_pbp",
        "season": game_id[:4],
    }

    return shared.get_file(page_info)


def get_contents(game_html):
    """
    Uses Beautiful soup to parses the html document.
    Some parsers work for some pages but don't work for others....I'm not sure why so I just try them all here in order
    
    :param game_html: html doc
    
    :return: "soupified" html 
    """
    parsers = ["html5lib", "lxml", "html.parser"]
    strainer = SoupStrainer('td', attrs={'class': re.compile(r'bborder')})

    for parser in parsers:
        # parse_only only works with lxml for some reason
        if parser == "lxml":
            soup = BeautifulSoup(game_html, parser, parse_only=strainer)
        else:
            soup = BeautifulSoup(game_html, parser)

        tds = soup.find_all("td", {"class": re.compile('.*bborder.*')})

        if len(tds) > 0:
            break

    return tds

def return_name_html(info):
    """
    In the PBP html the name is in a format like: 'Center - MIKE RICHARDS'
    Some also have a hyphen in their last name so can't just split by '-'
    
    :param info: position and name
    
    :return: name
    """
    s = info.index('-')  # Find first hyphen
    return info[s + 1:].strip(' ')  # The name should be after the first hyphen

def strip_html_pbp(td):
    """
    Strip html tags and such. (Note to Self: Don't touch this!!!) 
    
    :param td: pbp
    
    :return: list of plays (which contain a list of info) stripped of html
    """
    for y in range(len(td)):
        # Get the 'br' tag for the time column...this get's us time remaining instead of elapsed and remaining combined
        if y == 3:
            td[y] = td[y].get_text()   # This gets us elapsed and remaining combined-< 3:0017:00
            index = td[y].find(':')
            td[y] = td[y][:index+3]
        elif (y == 6 or y == 7) and td[0] != '#':
            # 6 & 7-> These are the player 1 ice one's
            # The second statement controls for when it's just a header
            baz = td[y].find_all('td')
            bar = [baz[z] for z in range(len(baz)) if z % 4 != 0]  # Because of previous step we get repeats...delete some

            # The setup in the list is now: Name/Number->Position->Blank...and repeat
            # Now strip all the html
            players = []
            for i in range(len(bar)):
                if i % 3 == 0:
                    try:
                        name = return_name_html(bar[i].find('font')['title'])
                        number = bar[i].get_text().strip('\n')  # Get number and strip leading/trailing newlines
                    except KeyError:
                        name = ''
                        number = ''
                elif i % 3 == 1:
                    if name != '':
                        position = bar[i].get_text()
                        players.append([name, number, position])

            td[y] = players
        else:
            td[y] = td[y].get_text()

    return td


def clean_html_pbp(html):
    """
    Get rid of html and format the data
    
    :param html: the requested url
    
    :return: a list with all the info
    """
    soup = get_contents(html)

    # Create a list of lists (each length 8)...corresponds to 8 columns in html pbp
    td = [soup[i:i + 8] for i in range(0, len(soup), 8)]

    cleaned_html = [strip_html_pbp(x) for x in td]

    return cleaned_html

#PARSE FUNCTIONS
def parse_html(html_data):
    remove = ["PGSTR","PGEND","ANTHEM",'PSTR',"PEND","STOP","GSTR","GEND"]
    cols = ['event_num',"period",'strength','period_time_elasped','event_type','description',
            "away_on_1","away_on_2","away_on_3","away_on_4","away_on_5","away_on_6","away_goalie",
            "home_on_1","home_on_2","home_on_3","home_on_4","home_on_5","home_on_6","home_goalie"]
    rows = []
    for row in html_data:
            if row[0] == "#" or row[4] in remove:
                continue
            else:
                df = pd.DataFrame({
                    "event_num":[row[0]],
                    "period":[int(row[1])],
                    "strength":[row[2]],
                    "period_time_elasped":[row[3]],
                    "event_type":[row[4]],
                    "description":[row[5]]
                })

                if len(row[6])==0 or len(row[7])==0:
                    away_skaters = {}
                    for i in range(0,6):
                        away_skaters.update({
                            "away_on_"+str(i+1):[""]
                        })
                    home_skaters = {}
                    for i in range(0,6):
                        home_skaters.update({
                            "home_on_"+str(i+1):[""]
                        })
                    away_goalie = {
                        "away_goalie":[""]
                    }
                    home_goalie = {
                        "home_goalie":[""]
                    }
                else:
                    away_skaters = {}
                    for i in range(0,len(row[6])-1):
                        away_skaters.update({
                            "away_on_"+str(i+1):[row[6][i][0]]
                        })
                    home_skaters = {}
                    for i in range(0,len(row[7])-1):
                        home_skaters.update({
                            "home_on_"+str(i+1):[row[7][i][0]]
                        })
                    away_goalie = {}
                    if row[6][len(row[6])-1][2] == "G":
                        away_goalie.update({
                            "away_goalie":[row[6][len(row[6])-1][0]]
                        })
                    else:
                        away_skaters.update({
                            "away_on_"+str(len(row[6])):[row[6][len(row[6])-1][0]]
                        })
                    home_goalie = {}
                    if row[7][len(row[7])-1][2] == "G":
                        home_goalie.update({
                            "home_goalie":[row[7][len(row[7])-1][0]]
                        })
                    else:
                        home_skaters.update({
                            "home_on_"+str(len(row[7])):[row[7][len(row[7])-1][0]]
                        })

                dfp = pd.DataFrame(away_skaters | home_skaters)
                dfg = pd.DataFrame(away_goalie | home_goalie)

                rows.append(pd.concat([df,dfp,dfg],axis=1))
    html_pbp = pd.concat(rows).reset_index(drop=True)

    for col in cols:
        try: html_pbp[col]
        except:
            html_pbp[col] = ""
            
    html_pbp.replace({
        "PSTR":"period-start",
        "FAC":"faceoff",
        "GOAL":"goal",
        "SHOT":"shot-on-goal",
        "GIVE":"giveaway",
        "TAKE":"takeaway",
        "HIT":"hit",
        "MISS":"missed-shot",
        "STOP":"stoppage",
        "DELPEN":"delayed-penalty",
        "PENL":"penalty",
        "BLOCK":"blocked-shot",
        "PEND":"period-end",
        "CHL":"challenge",
        "GEND":"game-end"
    },inplace=True)

    html_pbp['event_num'] = html_pbp['event_num'].astype(int)
    html_pbp['period_time_simple'] = html_pbp['period_time_elasped'].str.replace(":","",regex=True)
    html_pbp['period_seconds_elasped'] = np.where(html_pbp['period_time_simple'].str.len()==3,
                                           ((html_pbp['period_time_simple'].str[0].astype(int)*60)+html_pbp['period_time_simple'].str[-2:].astype(int)),
                                           ((html_pbp['period_time_simple'].str[0:2].astype(int)*60)+html_pbp['period_time_simple'].str[-2:].astype(int)))
    html_pbp['period_seconds_remaining'] = 1200 - html_pbp['period_seconds_elasped']
    html_pbp['seconds_elasped'] = ((html_pbp['period']-1)*1200)+html_pbp['period_seconds_elasped']

    return html_pbp

def parse_json(json):
    events = pd.json_normalize(json['plays']).reset_index(drop=True)
    info = pd.json_normalize(json)
    roster = pd.json_normalize(json['rosterSpots'])

    events['game_id'] = info['id'][0]
    events['season'] = info['season'][0]
    events['season_type'] = info['gameType'][0]
    events['game_date'] = info['gameDate'][0]
    events['away_team_id'] = info['awayTeam.id'][0]
    events['away_team_abbr'] = info['awayTeam.abbrev'][0]
    events['home_team_id'] = info['homeTeam.id'][0]
    events['home_team_abbr'] = info['homeTeam.abbrev'][0]

    teams = {
        info['awayTeam.id'][0]:info['awayTeam.abbrev'][0],
        info['homeTeam.id'][0]:info['homeTeam.abbrev'][0]
    }

    
    roster['playerName'] = roster['firstName.default']+" "+roster['lastName.default']
    players = {}
    players_pos = {}
    ids = {}
    for id, player in zip(list(roster['playerId']),list(roster['playerName'])):
        players.update({id:player.upper()})
    for id, pos in zip(list(roster['playerId']),list(roster['positionCode'])):
        players_pos.update({id:pos.upper()})
    for id, player in zip(list(roster['playerId']),list(roster['playerName'])):
        ids.update({player.upper():id})

    #Test columns
    cols = ['eventId', 'timeInPeriod', 'timeRemaining', 'situationCode', 'homeTeamDefendingSide', 'typeCode', 'typeDescKey', 'sortOrder', 'periodDescriptor.number', 'periodDescriptor.periodType', 'periodDescriptor.maxRegulationPeriods', 'details.eventOwnerTeamId', 'details.losingPlayerId', 'details.winningPlayerId', 'details.xCoord', 'details.yCoord', 'details.zoneCode', 'pptReplayUrl', 'details.shotType', 'details.scoringPlayerId', 'details.scoringPlayerTotal', 'details.assist1PlayerId', 'details.assist1PlayerTotal', 'details.assist2PlayerId', 'details.assist2PlayerTotal', 'details.goalieInNetId', 'details.awayScore', 'details.homeScore', 'details.highlightClipSharingUrl', 'details.highlightClipSharingUrlFr', 'details.highlightClip', 'details.highlightClipFr', 'details.discreteClip', 'details.discreteClipFr', 'details.shootingPlayerId', 'details.awaySOG', 'details.homeSOG', 'details.playerId', 'details.hittingPlayerId', 'details.hitteePlayerId', 'details.reason', 'details.typeCode', 'details.descKey', 'details.duration', 'details.servedByPlayerId', 'details.secondaryReason', 'details.blockingPlayerId', 'details.committedByPlayerId', 'details.drawnByPlayerId', 'game_id', 'season', 'season_type', 'game_date', 'away_team_id', 'away_team_abbr', 'home_team_id', 'home_team_abbr']

    for col in cols:
        try:events[col]
        except:
            events[col]=""

    events['event_player_1_id'] = events['details.winningPlayerId'].combine_first(events['details.scoringPlayerId'])\
                                                                   .combine_first(events['details.shootingPlayerId'])\
                                                                   .combine_first(events['details.playerId'])\
                                                                   .combine_first(events['details.hittingPlayerId'])\
                                                                   .combine_first(events['details.blockingPlayerId'])\
                                                                   .combine_first(events['details.committedByPlayerId'])
        
    events['event_player_2_id'] = events['details.losingPlayerId'].combine_first(events['details.assist1PlayerId'])\
                                                                    .combine_first(events['details.hitteePlayerId'])\
                                                                    .combine_first(events['details.drawnByPlayerId'])

    events['event_player_3_id'] = events['details.assist2PlayerId']

    events['event_team_status'] = np.where(events['home_team_id']==events['details.eventOwnerTeamId'],"home","away")

    events['x_fixed'] = abs(events['details.xCoord'])
    events['y_fixed'] = np.where(events['details.xCoord']<0,-events['details.yCoord'],events['details.yCoord'])
    events['x_adj'] = np.where(events['event_team_status']=="home",events['x_fixed'],-events['x_fixed'])
    events['y_adj'] = np.where(events['event_team_status']=="home",events['y_fixed'],-events['y_fixed'])
    events['event_distance'] = np.sqrt(((89 - events['x_fixed'])**2) + (events['y_fixed']**2))
    events['event_angle'] = np.degrees(np.arctan2(abs(events['y_fixed']), abs(89 - events['x_fixed'])))
    
    events['event_team_abbr'] = events['details.eventOwnerTeamId'].replace(teams)

    events['event_player_1_name'] = events['event_player_1_id'].replace(players)
    events['event_player_2_name'] = events['event_player_2_id'].replace(players)
    events['event_player_3_name'] = events['event_player_3_id'].replace(players)

    events['event_player_1_pos'] = events['event_player_1_id'].replace(players_pos)
    events['event_player_2_pos'] = events['event_player_2_id'].replace(players_pos)
    events['event_player_3_pos'] = events['event_player_3_id'].replace(players_pos)

    events['event_goalie_name'] = events['details.goalieInNetId'].replace(players)

    events['away_skaters'] = events['situationCode'].astype(str).str.slice(start=1,stop=2)
    events['home_skaters'] = events['situationCode'].astype(str).str.slice(start=2,stop=3)
    events['event_skaters'] = np.where(events['event_team_abbr']==events['home_team_abbr'],events['home_skaters'],events['away_skaters'])
    events['event_skaters_against'] = np.where(events['event_team_abbr']==events['home_team_abbr'],events['away_skaters'],events['home_skaters'])

    events['strength_state'] = events['event_skaters']+"v"+events['event_skaters_against']
    events = events.rename(columns={
        "eventId":"event_id",
        "periodDescriptor.number":"period",
        "periodDescriptor.periodType":"period_type",
        "timeInPeriod":"period_time_elasped",
        "timeRemaining":"period_time_remaining",
        "situationCode":"situation_code",
        "homeTeamDefendingSide":"home_team_defending_side",
        "typeCode":"event_type_code",
        "typeDescKey":"event_type",
        "details.shotType":"shot_type",
        "details.zoneCode":"zone_code",
        "details.xCoord":"x",
        "details.yCoord":"y",
        "details.goalieInNetId": "event_goalie_id",
        "details.awaySOG":"away_SOG",
        "details.homeSOG":"home_SOG"
    })

    events['period_time_simple'] = events['period_time_elasped'].str.replace(":","",regex=True)
    events['period_seconds_elasped'] = np.where(events['period_time_simple'].str.len()==3,
                                           ((events['period_time_simple'].str[0].astype(int)*60)+events['period_time_simple'].str[-2:].astype(int)),
                                           ((events['period_time_simple'].str[0:2].astype(int)*60)+events['period_time_simple'].str[-2:].astype(int)))
    events['period_seconds_remaining'] = 1200-events['period_seconds_elasped']
    events['seconds_elasped'] = ((events['period']-1)*1200)+events['period_seconds_elasped']
    
    fenwick_events = ['missed-shot','shot-on-goal','goal']
    ag = 0
    ags = []
    hg = 0
    hgs = []

    af = 0
    afs = []
    hf = 0
    hfs = []
    for event,team in zip(list(events['event_type']),list(events['event_team_status'])):
        if event in fenwick_events:
            if team == "home":
                hf = hf+1
                if event == 'goal':
                    hg = hg+1
            else:
                af = af+1
                if event == 'goal':
                    ag = ag+1
       
        ags.append(ag)
        hgs.append(hg)
        afs.append(af)
        hfs.append(hf)

    events['away_score'] = ags
    events['home_score'] = hgs
    events['away_fenwick'] = afs
    events['home_fenwick'] = hfs
    
    events = events.loc[(events['event_type']!="")&(events['event_type']!="game-end")]
    return events

#MISC FUNCTIONS
def retreive_players(json,result = "id"):
    roster = pd.json_normalize(json['rosterSpots'])
    info = pd.json_normalize(json)
    home = info['homeTeam.id'][0]
    away = info['awayTeam.id'][0]

    roster['playerName'] = roster['firstName.default']+" "+roster['lastName.default']
    try: roster['playerName_2'] = roster['firstName.cs']+" "+roster['lastName.default'] 
    except: roster['playerName_2'] = ""
    try: roster['playerName_3'] = roster['firstName.de']+" "+roster['lastName.default']
    except: roster['playerName_3'] = ""
    try: roster['playerName_4'] = roster['firstName.es']+" "+roster['lastName.default']
    except: roster['playerName_4'] = ""

    home_players = {}
    home_id = roster.loc[roster['teamId']==home]
    hid = list(home_id['playerId'])+list(home_id['playerId'])+list(home_id['playerId'])+list(home_id['playerId'])
    hpos = list(home_id['positionCode'])+list(home_id['positionCode'])+list(home_id['positionCode'])+list(home_id['positionCode'])
    hp = list(home_id['playerName'])+list(home_id['playerName_2'])+list(home_id['playerName_3'])+list(home_id['playerName_4'])
    
    for id, pos, player in zip(hid,hpos,hp):
        try: home_players.update({player.upper():
                        {result:id if result == 'id' else pos}})
        except:
            continue

    away_players = {}
    away_id = roster.loc[roster['teamId']==away]
    aid = list(away_id['playerId'])+list(away_id['playerId'])+list(away_id['playerId'])+list(away_id['playerId'])
    apos = list(away_id['positionCode'])+list(away_id['positionCode'])+list(away_id['positionCode'])+list(away_id['positionCode'])
    ap = list(away_id['playerName'])+list(away_id['playerName_2'])+list(away_id['playerName_3'])+list(away_id['playerName_4'])
    
    for id, pos, player in zip(aid,apos,ap):
        try: away_players.update({player.upper():
                        {result:id if result == 'id' else pos}})
        except:
            continue
        
    return {
        'home':home_players,
        'away':away_players
    }

def combine_pbp_data(json,html):
        pbp_col = ['season','season_type','game_id','game_date',
        'away_team_abbr','home_team_abbr','event_num','event_id','period','period_type',
        "period_time_remaining",'seconds_elasped',"description",
        "situation_code","strength_state","home_team_defending_side","event_type_code","event_type",
        "shot_type","event_team_abbr","event_team_status","event_player_1_id","event_player_2_id","event_player_3_id",
        "event_player_1_name","event_player_2_name","event_player_3_name","event_player_1_pos","event_player_2_pos",
        "event_player_3_pos","event_goalie_id",
        "event_goalie_name","zone_code","x","y","x_fixed","y_fixed","x_adj","y_adj",
        "event_skaters","away_skaters","home_skaters",
        "event_distance","event_angle","away_score","home_score", "away_fenwick", "home_fenwick",
        "away_on_1","away_on_2","away_on_3","away_on_4","away_on_5","away_on_6","away_goalie",
        "home_on_1","home_on_2","home_on_3","home_on_4","home_on_5","home_on_6","home_goalie"]

        json_pbp = parse_json(json)
        html_pbp = parse_html(clean_html_pbp(html))

        merge_col = ['period','seconds_elasped',"event_type"]
        
        merged_df = pd.merge(json_pbp,html_pbp,how="outer",on=merge_col)[pbp_col].sort_values(by=['event_num'])

        return merged_df

#PREP FUNCTIONS (SHIFTS)
def get_shifts(game_id):
    """
    Given a game_id it returns a the shifts for both teams
    Ex: http://www.nhl.com/scores/htmlreports/20162017/TV020971.HTM
    
    :param game_id: the game
    
    :return: shifts or None
    """
    game_id = str(game_id)
    venue_pgs = tuple()

    for venue in ["home", "away"]:
        venue_tag = "H" if venue == "home" else "V"
        venue_url = 'http://www.nhl.com/scores/htmlreports/{}{}/T{}{}.HTM'.format(game_id[:4], int(game_id[:4])+1, venue_tag, game_id[4:])
  
        page_info = {
            "url": venue_url,
            "name": game_id,
            "type": "html_shifts_{}".format(venue),
            "season": game_id[:4],
        }

        venue_pgs += (shared.get_file(page_info), )

    return venue_pgs


def get_soup(shifts_html):
    """
    Uses Beautiful soup to parses the html document.
    Some parsers work for some pages but don't work for others....I'm not sure why so I just try them all here in order
    
    :param shifts_html: html doc
    
    :return: "soupified" html and player_shifts portion of html (it's a bunch of td tags)
    """
    parsers = ["lxml", "html.parser", "html5lib"]

    for parser in parsers:
        soup = BeautifulSoup(shifts_html, parser)
        td = soup.findAll(True, {'class': ['playerHeading + border', 'lborder + bborder']})

        if len(td) > 0:
            break

    return td, get_teams(soup)


def get_teams(soup):
    """
    Return the team for the TOI tables and the home team
    
    :param soup: souped up html
    
    :return: list with team and home team
    """
    team = soup.find('td', class_='teamHeading + border')  # Team for shifts
    team = team.get_text()

    # Get Home Team
    teams = soup.find_all('td', {'align': 'center', 'style': 'font-size: 10px;font-weight:bold'})
    regex = re.compile(r'>(.*)<br/?>')
    home_team = regex.findall(str(teams[7]))

    return [team, home_team[0]]

#PARSE FUNCTIONS
def analyze_shifts(shift, name, team, home_team, player_ids):
    """
    Analyze shifts for each player when using.
    Prior to this each player (in a dictionary) has a list with each entry being a shift.

    :param shift: info on shift
    :param name: player name
    :param team: given team
    :param home_team: home team for given game
    :param player_ids: dict with info on players
    
    :return: dict with info for shift
    """
    shifts = dict()

    shifts['player_name'] = name.upper()
    shifts['period'] = '4' if shift[1] == 'OT' else '5' if shift[1] == 'SO' else shift[1]
    shifts['team_abbr'] = shared.get_team(team.strip(' '))
    shifts['start'] = shared.convert_to_seconds(shift[2].split('/')[0])
    shifts['duration'] = shared.convert_to_seconds(shift[4].split('/')[0])

    # I've had problems with this one...if there are no digits the time is fucked up
    if re.compile(r'\d+').findall(shift[3].split('/')[0]):
        shifts['end'] = shared.convert_to_seconds(shift[3].split('/')[0])
    else:
        shifts['end'] = shifts['start'] + shifts['duration']

    try:
        if home_team == team:
            shifts['player_id'] = player_ids['home'][name.upper()]['id']
        else:
            shifts['player_id'] = player_ids['away'][name.upper()]['id']
    except KeyError:
        shifts['player_id'] = None

    return shifts

def parse_shifts(html, player_ids, game_id):
    """
    Parse the html
    
    Note: Don't fuck with this!!! I'm not exactly sure how or why but it works. 
    
    :param html: cleaned up html
    :param player_ids: dict of home and away players
    :param game_id: id for game
    
    :return: DataFrame with info
    """
    all_shifts = []
    columns = ['game_id', 'player_name', 'player_id', 'period', 'team_abbr', 'start', 'end', 'duration']

    td, teams = get_soup(html)

    team = teams[0]
    home_team = teams[1]
    players = dict()

    # The list 'td' is laid out with player name followed by every component of each shift. Each shift contains:
    # shift #, Period, begin, end, and duration. The shift event isn't included.
    for t in td:
        t = t.get_text()
        if ',' in t:     # If it has a comma in it we know it's a player's name...so add player to dict
            name = t
            # Just format the name normally...it's coded as: 'num last_name, first_name'
            name = name.split(',')
            name = ' '.join([name[1].strip(' '), name[0][2:].strip(' ')])
            name = shared.fix_name(name)
            players[name] = dict()
            players[name]['number'] = name[0][:2].strip()
            players[name]['shifts'] = []
        else:
            # Here we add all the shifts to whatever player we are up to
            players[name]['shifts'].extend([t])

    for key in players.keys():
        # Create a list of lists (each length 5)...corresponds to 5 columns in html shifts
        players[key]['shifts'] = [players[key]['shifts'][i:i + 5] for i in range(0, len(players[key]['shifts']), 5)]

        # Parse each shift
        shifts = [analyze_shifts(shift, key, team, home_team, player_ids) for shift in players[key]['shifts']]
        all_shifts.extend(shifts)

    df = pd.DataFrame(all_shifts)
    df['game_id'] = str(game_id)

    shifts_raw = df[columns]

    shifts_raw = shifts_raw[shifts_raw['duration'] > 0]

    # Process 'on' shifts
    shifts_on = shifts_raw.groupby(['team_abbr', 'period', 'start']).agg(
        num_on=('player_name', 'size'),
        players_on=('player_name', lambda x: ', '.join(x)),
        ids_on=('player_id', lambda x: ', '.join(map(str, x)))
    ).reset_index()

    shifts_on = shifts_on.rename(columns={
        'start':"seconds_elasped"
    })

    # Process 'off' shifts
    shifts_off = shifts_raw.groupby(['team_abbr', 'period', 'end']).agg(
        num_off=('player_name', 'size'),
        players_off=('player_name', lambda x: ', '.join(x)),
        ids_off=('player_id', lambda x: ', '.join(map(str, x)))
    ).reset_index()

    shifts_off = shifts_off.rename(columns={
        'end':"seconds_elasped"
    })

    # Merge the 'on' and 'off' shifts
    shifts = pd.merge(shifts_on, shifts_off, on=['team_abbr', 'period', 'seconds_elasped'], how='outer')
    
    shifts = shifts.sort_values('seconds_elasped')

    shifts['period'] = shifts['period'].astype(int)
    shifts['event_type'] = 'change'
    shifts['seconds_elasped'] = shifts['seconds_elasped'] + (1200 * (shifts['period']-1))
    shifts['game_seconds_remaining'] = 3600 - shifts['seconds_elasped']

    # Handle missing values (NA) at the start and end of periods
    shifts['players_on'] = shifts['players_on'].fillna('None')
    shifts['players_off'] = shifts['players_off'].fillna('None')
    shifts['ids_on'] = shifts['ids_on'].fillna('0')
    shifts['ids_off'] = shifts['ids_off'].fillna('0')
    shifts['num_on'] = shifts['num_on'].fillna(0).astype(int)
    shifts['num_off'] = shifts['num_off'].fillna(0).astype(int)

    #Manual Team Rename
    shifts['team_abbr'] = shifts['team_abbr'].replace({
        "L.A":"LAK",
        "N.J":"NJD",
        "S.J":"SJS",
        "T.B":"TBL"
    })

    return shifts.loc[shifts['period']<5]

def construct_skaters_matrix(rosters, shifts, team_abbr, home=True):
    skaters = pd.DataFrame()
    goalies = pd.DataFrame()
    if home:
        team = {key:value for key, value in rosters['home'].items() if value['pos'] != "G"}
    else:
        team = {key:value for key, value in rosters['away'].items() if value['pos'] != "G"}

    names = list(team.keys())
    try: names.remove("")
    except ValueError: ""

    for player in names:
        on_ice = (np.cumsum(
            shifts.loc[(shifts['team_abbr'] == team_abbr), 'players_on']
            .apply(str)
            .apply(lambda x: int(bool(re.search(player, x)))) -
            shifts.loc[(shifts['team_abbr'] == team_abbr), 'players_off']
            .apply(str)
            .apply(lambda x: int(bool(re.search(player, x))))
        ))
        skaters[player] = on_ice
    
    skaters = skaters.fillna(0).astype(int)
    
    on_skaters = (skaters == 1).stack().reset_index()
    on_skaters = on_skaters[on_skaters[0]].groupby("level_0")["level_1"].apply(list).reset_index()
    
    max_players = 6
    for i in range(max_players):
        on_skaters[f"{'home' if home else 'away'}_on_{i+1}"] = on_skaters["level_1"].apply(lambda x: x[i] if i < len(x) else " ")
    
    on_skaters = on_skaters.drop(columns=["level_1"]).rename(columns={"level_0": "row"})
    
    if home:
        team = {key:value for key, value in rosters['home'].items() if value['pos'] == "G"}
    else:
        team = {key:value for key, value in rosters['away'].items() if value['pos'] == "G"}
    
    names = list(team.keys())
    try: names.remove("")
    except ValueError: ""

    for player in names:
        on_ice = (np.cumsum(
            shifts.loc[(shifts['team_abbr'] == team_abbr), 'players_on']
            .apply(str)
            .apply(lambda x: int(bool(re.search(player, x)))) -
            shifts.loc[(shifts['team_abbr'] == team_abbr), 'players_off']
            .apply(str)
            .apply(lambda x: int(bool(re.search(player, x))))
        ))
        goalies[player] = on_ice
    
    goalies = goalies.fillna(0).astype(int)
    
    on_goalies = (goalies == 1).stack().reset_index()
    on_goalies = on_goalies[on_goalies[0]].groupby("level_0")["level_1"].apply(list).reset_index()
    
    max_players = 1
    for i in range(max_players):
        on_goalies[f"{'home' if home else 'away'}_goalie"] = on_goalies["level_1"].apply(lambda x: x[i] if i < len(x) else " ")
    
    on_goalies = on_goalies.drop(columns=["level_1"]).rename(columns={"level_0": "row"})
    on_players = pd.merge(on_skaters,on_goalies,how='outer',on=['row'])

    shifts['row'] = shifts.index
    
    return pd.merge(shifts,on_players,how="outer",on=['row'])

def combine_shifts(home_shift,away_shift,json,game_id):
    data = retreive_players(json,result="pos")
    data_id = retreive_players(json)

    away = parse_shifts(away_shift,data_id,game_id).sort_values(by=['period','seconds_elasped'])
    home = parse_shifts(home_shift,data_id,game_id).sort_values(by=['period','seconds_elasped'])
    away['row'] = away.index
    home['row'] = home.index
    
    away_shifts = construct_skaters_matrix(data,away,pd.json_normalize(json)['awayTeam.abbrev'][0],False).fillna("REMOVE")
    home_shifts = construct_skaters_matrix(data,home,pd.json_normalize(json)['homeTeam.abbrev'][0],True).fillna("REMOVE")

    shifts = pd.concat([away_shifts,home_shifts]).sort_values(by=['period','seconds_elasped'])
    info = pd.json_normalize(json)
    shifts['game_id'] = info['id'][0]
    shifts['season'] = info['season'][0]
    shifts['season_type'] = info['gameType'][0]
    shifts['game_date'] = info['gameDate'][0]
    shifts['away_team_id'] = info['awayTeam.id'][0]
    shifts['away_team_abbr'] = info['awayTeam.abbrev'][0]
    shifts['home_team_id'] = info['homeTeam.id'][0]
    shifts['home_team_abbr'] = info['homeTeam.abbrev'][0]

    away_on = ['away_on_1','away_on_2','away_on_3','away_on_4','away_on_5','away_on_6',"away_goalie"]
    home_on = ['home_on_1','home_on_2','home_on_3','home_on_4','home_on_5','home_on_6',"home_goalie"]
    
    shifts[away_on+home_on] = shifts[away_on+home_on].ffill()

    shifts['away_skaters'] = shifts[away_on[0:6]].replace(r'^\s*$', np.nan, regex=True).notna().sum(axis=1)
    shifts['home_skaters'] = shifts[home_on[0:6]].replace(r'^\s*$', np.nan, regex=True).notna().sum(axis=1)

    shifts['strength_state'] = np.where(shifts['team_abbr']==shifts['home_team_abbr'],shifts['home_skaters'].astype(str) + "v" + shifts['away_skaters'].astype(str),shifts['away_skaters'].astype(str) + "v" + shifts['home_skaters'].astype(str))

    return shifts.drop(columns=['row'])

def fix_names(shifts_df,json):
    data = pd.json_normalize(json['rosterSpots'])
    data['fullName'] = (data['firstName.default']+" "+data['lastName.default']).str.upper()

    alt_name_col = ['firstName.cs',	'firstName.de',	'firstName.es',	'firstName.fi',	'firstName.sk',	'firstName.sv']
    for i in range(len(alt_name_col)):
        try: data['fullName.'+str(i+1)] = np.where(data[alt_name_col[i]].notna(),(data[alt_name_col[i]].astype(str)+" "+data['lastName.default'].astype(str)).str.upper(),np.nan)
        except: continue

    name_col = ['fullName',	'fullName.1',	'fullName.2',	'fullName.3',	'fullName.4',	'fullName.5', 'fullName.6']

    for name in name_col:
        try: data[name]
        except:
            data[name] = np.nan

    names_dfs = []
    for name in name_col[1:len(name_col)]:
        names_dfs.append(data[[name,'fullName']].rename(columns={name:"alt",
                                            "fullName":'default'}))

    names_df = pd.concat(names_dfs)

    replace = {}
    for default, alt in zip(names_df['default'],names_df['alt']):
        if alt == np.nan or alt == "" or str(alt) == 'nan':
            continue
        else:
            replace.update({alt:default})
    
    return shifts_df.replace(replace,regex=True)

#MISC FUNCTIONS(SHIFTS)
def create_timeline(pbp):
    max_secs = int(pbp['seconds_elasped'].max())+1
    pbp = pbp.loc[pbp['event_type']=='change']
    pbp['away_goalie'].fillna("REMOVE",inplace=True)
    pbp['home_goalie'].fillna("REMOVE",inplace=True)

    timeline = pd.DataFrame()
    timeline['seconds_elasped'] = range(max_secs)
    on_ice_col = ['away_on_1','away_on_2','away_on_3','away_on_4','away_on_5','away_on_6',"away_goalie",
         'home_on_1','home_on_2','home_on_3','home_on_4','home_on_5','home_on_6',"home_goalie"]
    info_col = ['season','season_type','game_id','game_date',
        'away_team_abbr','home_team_abbr','period',
        "seconds_elasped","away_skaters","home_skaters","strength_state",]

    timeline = pd.merge(timeline,pbp[info_col+on_ice_col].drop_duplicates(subset=['seconds_elasped'],keep='last'),how="outer",on=['seconds_elasped'])
    
    timeline[info_col+on_ice_col] = timeline[info_col+on_ice_col].ffill()
    timeline = timeline.replace({
        "REMOVE":np.nan
    })
    timeline.to_csv("sample_timeline_pre.csv",index=False)
    away_on = ['away_on_1','away_on_2','away_on_3','away_on_4','away_on_5','away_on_6']
    home_on = ['home_on_1','home_on_2','home_on_3','home_on_4','home_on_5','home_on_6']
    
    timeline['away_skaters'] = timeline[away_on].replace(r'^\s*$', np.nan, regex=True).notna().sum(axis=1)
    timeline['home_skaters'] = timeline[home_on].replace(r'^\s*$', np.nan, regex=True).notna().sum(axis=1)
    
    timeline['strength_state'] = timeline['away_skaters'].astype(str) + "v" + timeline['home_skaters'].astype(str)

    return timeline[info_col+on_ice_col]

def combine_data(pbp_df,shifts_df):
    df = pd.concat([pbp_df,shifts_df]).sort_values(by=['period','seconds_elasped'])
    even_pri = ['takeaway','giveaway','missed_shot','hit','shot-on-goal','blocked-shot']
    df['priority'] = np.where(df['event_type'].isin(even_pri),1,
                              np.where(df['event_type']=='goal',2,
                              np.where(df['event_type']=='stoppage',3,
                              np.where(df['event_type']=='penalty',4,
                              np.where(df['event_type']=='change',5,
                              np.where(df['event_type']=='period-end',6,
                              np.where(df['event_type']=='game-end',7,
                              np.where(df['event_type']=='faceoff',8,8))))))))
    
    df.sort_values(by=['period','seconds_elasped','priority']).drop(columns=['priority'])
    df['event_type_last'] = df['event_type'].shift(1)
    df['event_type_next'] = df['event_type'].shift(-1)
    lag_events = ['stoppage','goal','period-end']
    lead_events = ['faceoff','period-end']
    period_end_secs = [0,1200,2400,3600,4800,6000,7200,8400,9600,10800]
    df['shift_type'] = np.where(np.logical_or(np.logical_or(df['event_type_last'].isin(lag_events),df['event_type_next'].isin(lead_events)),df['seconds_elasped'].isin(period_end_secs)),"Line Change","On The Fly")
    df['description'] = df['description'].combine_first(df['shift_type'])
    
    return df.replace(r'^\s*$', np.nan, regex=True)

def fix_shifts(shifts_df):
    shifts_df = shifts_df.replace("REMOVE",np.nan)
    away_on = ['away_on_1','away_on_2','away_on_3','away_on_4','away_on_5','away_on_6']
    home_on = ['home_on_1','home_on_2','home_on_3','home_on_4','home_on_5','home_on_6']
    
    shifts_df['away_skaters'] = shifts_df[away_on].replace(r'^\s*$', np.nan, regex=True).notna().sum(axis=1)
    shifts_df['home_skaters'] = shifts_df[home_on].replace(r'^\s*$', np.nan, regex=True).notna().sum(axis=1)
    shifts_df['away_goalie_in'] = np.where(shifts_df['away_goalie'].replace(r'^\s*$', np.nan, regex=True)!=np.nan,1,0)
    shifts_df['home_goalie_in'] = np.where(shifts_df['home_goalie'].replace(r'^\s*$', np.nan, regex=True)!=np.nan,1,0)

    shifts_df['strength_state'] = shifts_df['away_skaters'].astype(str) + "v" + shifts_df['home_skaters'].astype(str)
    shifts_df['situation_code'] = shifts_df['away_goalie_in'].astype(str) + shifts_df['away_skaters'].astype(str) + shifts_df['home_skaters'].astype(str) + shifts_df['home_goalie_in'].astype(str)

    return shifts_df

#XG MODEL FUNCTIONS
def prep_data(pbp):
    import pandas as pd
    import numpy as np

    fenwick_events = ['missed-shot','shot-on-goal','goal']

    prep = (pbp
    .sort_values(['season', 'game_id', 'seconds_elasped','event_num'])
    .query("event_type in ['faceoff', 'goal', 'blocked-shot', 'shot-on-goal', 'missed-shot', 'hit', 'takeaway', 'giveaway'] and period < 5")
    .loc[(pbp['strength_state']!="6v3")&(pbp['strength_state']!="3v6")]
    .loc[pbp['x_fixed'].notna() & pbp['y_fixed'].notna()]
    .loc[~pbp['description'].str.contains("penalty shot", case=False, na=False)]
    )

    prep['seconds_since_last'] = prep['seconds_elasped'] - prep['seconds_elasped'].shift(1)
    prep['event_type_last'] = prep['event_type'].shift(1)
    prep['event_team_last'] = prep['event_team_abbr'].shift(1)
    prep['event_strength_last'] = prep['strength_state'].shift(1)
    prep['coords_x_last'] = prep['x_fixed'].shift(1)
    prep['coords_y_last'] = prep['y_fixed'].shift(1)

    prep['same_team_last'] = (prep['event_team_abbr'] == prep['event_team_last']).astype(int)
    prep['is_home'] = (prep['event_team_abbr'] == prep['home_team_abbr']).astype(int)
    prep['score_state'] = np.where(prep['is_home'] == 1, 
                                        prep['home_score'] - prep['away_score'], 
                                        prep['away_score'] - prep['home_score'])
    prep['shot_type'] = prep['shot_type'].fillna("wrist")
    prep['distance_from_last'] = np.sqrt((prep['x_fixed'] - prep['coords_x_last'])**2 + 
                                                (prep['y_fixed'] - prep['coords_y_last'])**2)
    
    non_off = ['N','D']
    prep['rush_mod'] = np.where(np.logical_and(np.logical_and(np.logical_or(prep['coords_x_last']<=25,prep['zone_code'].isin(non_off)),prep['seconds_since_last']<=5),prep['event_type'].isin(fenwick_events)),1+(5-prep['seconds_since_last']),0)
    prep['rebound_mod'] = np.where(np.logical_and(np.logical_and(prep['event_type_last'].isin(fenwick_events),prep['seconds_since_last']<=2),prep['event_type'].isin(fenwick_events)),1+(2-prep['seconds_since_last']),0)

    data = prep

    model_prep = (data
        .assign(is_goal = (data['event_type'] == "goal").astype(int),

                state_5v5 = (data['strength_state'] == "5v5").astype(int),
                state_4v4 = (data['strength_state'] == "4v4").astype(int),
                state_3v3 = (data['strength_state'] == "3v3").astype(int),
                state_5v4 = (data['strength_state'] == "5v4").astype(int),
                state_4v3 = (data['strength_state'] == "4v3").astype(int),
                state_5v3 = (data['strength_state'] == "5v3").astype(int),
                state_6v5 = (data['strength_state'] == "6v5").astype(int),
                state_5v6 = (data['strength_state'] == "5v6").astype(int),
                state_6v4 = (data['strength_state'] == "6v4").astype(int),
                state_4v6 = (data['strength_state'] == "4v6").astype(int),
                state_4v5 = (data['strength_state'] == "4v5").astype(int),
                state_3v4 = (data['strength_state'] == "3v4").astype(int),
                state_3v5 = (data['strength_state'] == "3v5").astype(int),

                regular = (data['season_type'] == 2).astype(int),
                playoff = (data['season_type'] == 3).astype(int),

                wrist_shot = (data['shot_type'] == "wrist").astype(int),
                deflected_shot = (data['shot_type'] == "deflected").astype(int),
                tip_shot = (data['shot_type'] == "tip-in").astype(int),
                slap_shot = (data['shot_type'] == "slap").astype(int),
                backhand_shot = (data['shot_type'] == "backhand").astype(int),
                snap_shot = (data['shot_type'] == "snap").astype(int),
                wrap_shot = (data['shot_type'] == "wrap-around").astype(int),
                poke_shot = (data['shot_type'] == "poke").astype(int),
                bat_shot = (data['shot_type'] == "bat").astype(int),
                cradle_shot = (data['shot_type'] == "cradle").astype(int),
                between_legs_shot = (data['shot_type'] == "between-legs").astype(int),

                prior_shot_same = ((data['event_type_last'] == "shot_on_goal") & (data['same_team_last'] == 1)).astype(int),
                prior_miss_same = ((data['event_type_last'] == "missed-shot") & (data['same_team_last'] == 1)).astype(int),
                prior_block_same = ((data['event_type_last'] == "blocked-shot") & (data['same_team_last'] == 1)).astype(int),

                prior_shot_opp=((data["event_type_last"] == "shot_on_goal") & (data["same_team_last"] == 0)).astype(int),
                prior_miss_opp=((data["event_type_last"] == "missed-shot") & (data["same_team_last"] == 0)).astype(int),
                prior_block_opp=((data["event_type_last"] == "blocked-shot") & (data["same_team_last"] == 0)).astype(int),
                
                prior_give_opp=((data["event_type_last"] == "giveaway") & (data["same_team_last"] == 0)).astype(int),
                prior_give_same=((data["event_type_last"] == "giveaway") & (data["same_team_last"] == 1)).astype(int),
                prior_take_opp=((data["event_type_last"] == "takeaway") & (data["same_team_last"] == 0)).astype(int),
                prior_take_same=((data["event_type_last"] == "takeaway") & (data["same_team_last"] == 1)).astype(int),
                
                prior_hit_opp=((data["event_type_last"] == "hit") & (data["same_team_last"] == 0)).astype(int),
                prior_hit_same=((data["event_type_last"] == "hit") & (data["same_team_last"] == 1)).astype(int),
                
                prior_face=(data["event_type_last"] == "faceoff").astype(int)
        )
    )

    return model_prep


def apply_wsba_xG(pbp = pd.DataFrame(), load_model = "xg_model/wsba_xg.joblib"):
    import xgboost as xgb
    import scipy.sparse as sp
    import joblib

    fenwick_events = ['missed-shot','shot-on-goal','goal']

    data = prep_data(pbp)

    cols = list(data.columns)
    booleans = cols[-37:]

    model_prep = data[['is_goal',
                'event_distance', 'event_angle',
                'seconds_since_last', 'distance_from_last', 
                'coords_x_last', 'coords_y_last',
                'x_fixed',"y_fixed",
                'period','seconds_elasped','score_state','rush_mod','rebound_mod']+booleans]

    # Make sparse
    model_data_sparse = sp.csr_matrix(model_prep)

    # Separate into target / predictors
    is_goal_vect = model_data_sparse[:, 0].A
    predictors_matrix = model_data_sparse[:, 1:]

    # Full XGB data model 
    full_xgb = xgb.DMatrix(data=predictors_matrix, label=is_goal_vect)

    model = joblib.load(load_model)
    data['xG'] = np.where(np.logical_and(data['event_type'].isin(fenwick_events),np.logical_and(data['x_fixed'] != np.nan,data['y_fixed'] != np.nan)),model.predict(full_xgb),np.nan)
    return data[['season','season_type','game_id','game_date',
    'away_team_abbr','home_team_abbr','event_num','event_id','period','period_type',
    "period_time_remaining",'seconds_elasped',"description",
    "situation_code","strength_state","home_team_defending_side","event_type_code","event_type",
    "shot_type","event_team_abbr","event_team_status","event_player_1_id","event_player_2_id","event_player_3_id",
    "event_player_1_name","event_player_2_name","event_player_3_name","event_player_1_pos","event_player_2_pos",
    "event_player_3_pos","event_goalie_id",
    "event_goalie_name","zone_code","x","y","x_fixed","y_fixed","x_adj","y_adj",
    "event_skaters","away_skaters","home_skaters",
    "event_distance","event_angle","away_score","home_score", "away_fenwick", "home_fenwick",
    "away_on_1","away_on_2","away_on_3","away_on_4","away_on_5","away_on_6","away_goalie",
    "home_on_1","home_on_2","home_on_3","home_on_4","home_on_5","home_on_6","home_goalie",
    'rush_mod','rebound_mod','xG']]