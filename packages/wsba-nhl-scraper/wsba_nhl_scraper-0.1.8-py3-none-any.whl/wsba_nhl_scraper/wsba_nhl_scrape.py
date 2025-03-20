import requests as rs
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from wsba_nhl_scraper.data_scrape import combine_pbp_data, combine_shifts, combine_data, fix_shifts, fix_names, apply_wsba_xG

# MAIN FUNCTIONS
def wsba_scrape_game(game_ids):
    pbps = []
    shifts_data = []
    for game_id in game_ids:
        print("Scraping data from game " + str(game_id) + "...")

        game_id = str(game_id)
        season = str(game_id[:4])+str(int(game_id[:4])+1)

        api = "https://api-web.nhle.com/v1/gamecenter/"+game_id+"/play-by-play"
        report = "https://www.nhl.com/scores/htmlreports/"+season+"/PL"+str(game_id)[-6:]+".HTM"
        home_log = "https://www.nhl.com/scores/htmlreports/"+season+"/TH"+str(game_id)[-6:]+".HTM"
        away_log = "https://www.nhl.com/scores/htmlreports/"+season+"/TV"+str(game_id)[-6:]+".HTM"

        json = rs.get(api).json()
        html = rs.get(report).content
        home_shift = rs.get(home_log).content
        away_shift = rs.get(away_log).content

        pbp = combine_pbp_data(json,html)
        shifts = fix_names(fix_shifts(combine_shifts(home_shift,away_shift,json,game_id)),json)

        pbps.append(pbp)
        shifts_data.append(shifts)
    
    pbp_df = pd.concat(pbps)
    shifts_df = pd.concat(shifts_data)

    df = combine_data(pbp_df,shifts_df)
    
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
    shifts_col = ['season', 'season_type', 'game_id', 'game_date', 'away_team_abbr', 'home_team_abbr', 'period', 'seconds_elasped', 
                  'strength_state', 'situation_code', 'event_type', 'description', 'team_abbr', 'num_on', 'players_on', 'ids_on', 'num_off', 'players_off', 'ids_off', 'game_seconds_remaining',
                  'away_skaters', 'home_skaters', 
                  'away_on_1', 'away_on_2', 'away_on_3', 'away_on_4', 'away_on_5', 'away_on_6', 'away_goalie', 
                  'home_on_1', 'home_on_2', 'home_on_3', 'home_on_4', 'home_on_5', 'home_on_6', 'home_goalie'
                  ]
    
    remove = ['period-start','period-end','challenge','stoppage','change']
    return {"pbp":df.loc[~df['event_type'].isin(remove)][pbp_col],
            "shifts":df.loc[df['event_type']=='change'][shifts_col]
            }

                          

def wsba_scrape_schedule(season,start = "09-01", end = "08-01"):
    api = "https://api-web.nhle.com/v1/schedule/"

    new_year = ["01","02","03","04","05","06"]
    if start[:2] in new_year:
        start = str(int(season[:4])+1)+"-"+start
        end = str(season[:-4])+"-"+end
    else:
        start = str(season[:4])+"-"+start
        end = str(season[:-4])+"-"+end

    form = '%Y-%m-%d'

    start = datetime.strptime(start,form)
    end = datetime.strptime(end,form)

    game = []

    day = (end-start).days+1
    if day < 0:
        day = 365 + day
    for i in range(day):
        inc = start+timedelta(days=i)
        print("Scraping games on " + str(inc)[:10]+"...")
        
        get = rs.get(api+str(inc)[:10]).json()
        gameWeek = list(pd.json_normalize(get['gameWeek'])['games'])[0]

        for i in range(0,len(gameWeek)):
            game.append(pd.DataFrame({
                "id": [gameWeek[i]['id']],
                "season": [gameWeek[i]['season']],
                "season_type":[gameWeek[i]['gameType']],
                "game_center_link":[gameWeek[i]['gameCenterLink']]
                }))
    
    df = pd.concat(game)
    return df.loc[df['season_type']>1]

def wsba_scrape_season(season,start = "09-01", end = "08-01", local=False, local_path = ""):
    if local == True:
        load = pd.read_csv(local_path)
        load = load.loc[load['season'].astype(str)==season]
        game_ids = list(load['id'].astype(str))
    else:
        game_ids = list(wsba_scrape_schedule(season,start,end)['id'].astype(str))

    df = []
    df_s = []
    df_t = []
    errors = {}
    for game_id in game_ids: 
        try:
            data = wsba_scrape_game([game_id])
            df.append(data['pbp'])
            df_s.append(data['shifts'])

        except: 
            print("An error occurred...")
            errors.update({
                "id": game_id,
            })
    
    pbp = pd.concat(df)
    shifts = pd.concat(df_s)
    errors = pd.DataFrame([errors])

    return {"pbp":pbp,
            'shifts':shifts,
            "errors":errors}

def wsba_scrape_seasons_info(seasons = []):
    import requests as rs
    import pandas as pd

    print("Scraping info for seasons: " + str(seasons))
    api = "https://api.nhle.com/stats/rest/en/season"
    info = "https://api-web.nhle.com/v1/standings-season"
    data = rs.get(api).json()['data']
    data_2 = rs.get(info).json()['seasons']

    df = pd.json_normalize(data)
    df_2 = pd.json_normalize(data_2)

    df = pd.merge(df,df_2,how='outer',on=['id'])
    
    if len(seasons) > 0:
        return df.loc[df['id'].astype(str).isin(seasons)].sort_values(by=['id'])
    else:
        return df.sort_values(by=['id'])

def wsba_scrape_standings(arg = "now"):
    import requests as rs
    import pandas as pd
    
    if arg == "now":
        print("Scraping standings as of now...")
    else:
        print("Scraping standings for season: "+arg)
    api = "https://api-web.nhle.com/v1/standings/"+arg
    
    data = rs.get(api).json()['standings']

    return pd.json_normalize(data)

def wsba_scrape_roster(team_abbr,season):
    print("Scrpaing rosters for " + team_abbr + " in season " + season + "...")

    api = "https://api-web.nhle.com/v1/roster/"+team_abbr+"/"+season
    
    data = rs.get(api).json()
    forwards = pd.json_normalize(data['forwards'])
    forwards['headingPosition'] = "F"
    dmen = pd.json_normalize(data['defensemen'])
    dmen['headingPosition'] = "D"
    goalies = pd.json_normalize(data['goalies'])
    goalies['headingPosition'] = "G"

    roster = pd.concat([forwards,dmen,goalies]).reset_index(drop=True)
    roster['fullName'] = (roster['firstName.default']+" "+roster['lastName.default']).str.upper()
    roster['season'] = str(season)
    roster['team_abbr'] = team_abbr

    return roster

def wsba_scrape_player_info(roster):
    data = roster

    print("Creating player info for provided roster data...")

    alt_name_col = ['firstName.cs',	'firstName.de',	'firstName.es',	'firstName.fi',	'firstName.sk',	'firstName.sv']
    for i in range(len(alt_name_col)):
        try: data['fullName.'+str(i+1)] = np.where(data[alt_name_col[i]].notna(),(data[alt_name_col[i]].astype(str)+" "+data['lastName.default'].astype(str)).str.upper(),np.nan)
        except: continue

    name_col = ['fullName',	'fullName.1',	'fullName.2',	'fullName.3',	'fullName.4',	'fullName.5', 'fullName.6']

    for name in name_col:
        try: data[name]
        except:
            data[name] = np.nan

    infos = []
    for name in name_col:
        infos.append(data[[name,"id","season","team_abbr","headshot",
                              "sweaterNumber","headingPosition",
                              "positionCode",'shootsCatches',
                              'heightInInches','weightInPounds',
                              'birthDate','birthCountry']].rename(columns={
                                                              name:'Player',
                                                              'id':"API",
                                                              "season":"Season",
                                                              "team_abbr":"Team",
                                                              'headshot':'Headshot',
                                                              'sweaterNumber':"Number",
                                                              'headingPosition':"Primary Position",
                                                              'positionCode':'Position',
                                                              'shootsCatches':'Handedness',
                                                              'heightInInches':'Height',
                                                              'weightInPounds':'Weight',
                                                              'birthDate':'Birthday',
                                                              'birthCountry':'Nationality'}))
    players = pd.concat(infos)
    players['Season'] = players['Season'].astype(str)
    players['Player'] = players['Player'].replace(r'^\s*$', np.nan, regex=True)

    return players.loc[players['Player'].notna()].sort_values(by=['Player','Season','Team'])

def wsba_calculate_stats(pbp,shifts,season,season_types,game_strength):
    print("Calculating stats for play-by-play and shifts data provided in the frame: " + season + "...")
    pbp = apply_wsba_xG(pbp)

    # Individual Stats
    pbp = pbp.loc[(pbp['season_type'].isin(season_types)) & (pbp['period'] < 5)]
    
    # Filter by game strength if not "all"
    if game_strength != "all":
        pbp = pbp.loc[pbp['strength_state'].isin(game_strength)]
    

    indv = (
        pbp.loc[pbp['event_type'].isin(["goal", "shot-on-goal", "missed-shot"])].groupby(['event_player_1_name', 'event_team_abbr']).agg(
        G=('event_type', lambda x: (x == "goal").sum()),
        iFF=('event_type', lambda x: (x != "blocked-shot").sum()),
        ixG=('xG', 'sum'),
        Rush=('rush_mod',lambda x: (x > 0).sum()),
        Rush_POW=('rush_mod','sum')
    ).reset_index().rename(columns={'event_player_1_name': 'Player', 'event_team_abbr': 'Team'})
    )

    a1 = (
        pbp.loc[pbp['event_type'].isin(["goal"])].groupby(['event_player_2_name', 'event_team_abbr']).agg(
        A1=('event_type','count')
    ).reset_index().rename(columns={'event_player_2_name': 'Player', 'event_team_abbr': 'Team'})
    )

    a2 = (
        pbp.loc[pbp['event_type'].isin(["goal"])].groupby(['event_player_3_name', 'event_team_abbr']).agg(
        A2=('event_type','count')
    ).reset_index().rename(columns={'event_player_3_name': 'Player', 'event_team_abbr': 'Team'})
    )

    indv = pd.merge(indv,a1,how='outer',on=['Player','Team'])
    indv = pd.merge(indv,a2,how='outer',on=['Player','Team'])

    indv['ixG/iFF'] = indv['ixG']/indv['iFF']
    indv['G/ixG'] = indv['G']/indv['ixG']
    indv['iFsh%'] = indv['G']/indv['iFF']

    indv_stats = indv

    # Filter for specific event types
    pbp_new = pbp.loc[pbp['event_type'].isin(["goal", "shot-on-goal", "missed-shot"])]
    
    # Convert player on-ice columns to vectors
    pbp_new['home_on_ice'] = pbp_new['home_on_1'].astype(str) + ";" + pbp_new['home_on_2'].astype(str) + ";" + pbp_new['home_on_3'].astype(str) + ";" + pbp_new['home_on_4'].astype(str) + ";" + pbp_new['home_on_5'].astype(str) + ";" + pbp_new['home_on_6'].astype(str)
    pbp_new['away_on_ice'] = pbp_new['away_on_1'].astype(str) + ";" + pbp_new['away_on_2'].astype(str) + ";" + pbp_new['away_on_3'].astype(str) + ";" + pbp_new['away_on_4'].astype(str) + ";" + pbp_new['away_on_5'].astype(str) + ";" + pbp_new['away_on_6'].astype(str)
    
    # Remove NA players
    pbp_new['home_on_ice'] = pbp_new['home_on_ice'].str.replace(';nan', '', regex=True)
    pbp_new['away_on_ice'] = pbp_new['away_on_ice'].str.replace(';nan', '', regex=True)
    
    def process_team_stats(df, on_ice_col, team_col, opp_col):
        df = df[['game_id', 'event_num', team_col, opp_col, 'event_type', 'xG', 'event_team_abbr', on_ice_col]].copy()
        df[on_ice_col] = df[on_ice_col].str.split(';')
        df = df.explode(on_ice_col)
        df = df.rename(columns={on_ice_col: 'Player'})
        df['xGF'] = np.where(df['event_team_abbr'] == df[team_col], df['xG'], 0)
        df['xGA'] = np.where(df['event_team_abbr'] == df[opp_col], df['xG'], 0)
        df['GF'] = np.where((df['event_type'] == "goal") & (df['event_team_abbr'] == df[team_col]), 1, 0)
        df['GA'] = np.where((df['event_type'] == "goal") & (df['event_team_abbr'] == df[opp_col]), 1, 0)
        df['FF'] = np.where((df['event_type'] != "blocked-shot") & (df['event_team_abbr'] == df[team_col]), 1, 0)
        df['FA'] = np.where((df['event_type'] != "blocked-shot") & (df['event_team_abbr'] == df[opp_col]), 1, 0)

        stats = df.groupby(['Player',team_col]).agg(
            FF=('FF', 'sum'),
            FA=('FA', 'sum'),
            GF=('GF', 'sum'),
            GA=('GA', 'sum'),
            xGF=('xGF', 'sum'),
            xGA=('xGA', 'sum')
        ).reset_index()
        
        return stats.rename(columns={team_col:"Team"})
    
    home_stats = process_team_stats(pbp_new, 'home_on_ice', 'home_team_abbr', 'away_team_abbr')
    away_stats = process_team_stats(pbp_new, 'away_on_ice', 'away_team_abbr', 'home_team_abbr')

    onice_stats = pd.concat([home_stats, away_stats]).groupby(['Player','Team']).agg(
            FF=('FF', 'sum'),
            FA=('FA', 'sum'),
            GF=('GF', 'sum'),
            GA=('GA', 'sum'),
            xGF=('xGF', 'sum'),
            xGA=('xGA', 'sum')
    ).reset_index()

    onice_stats['xGF/FF'] = onice_stats['xGF']/onice_stats['FF']
    onice_stats['GF/xGF'] = onice_stats['GF']/onice_stats['xGF']
    onice_stats['FshF%'] = onice_stats['GF']/onice_stats['FF']
    onice_stats['xGA/FA'] = onice_stats['xGA']/onice_stats['FA']
    onice_stats['GA/xGA'] = onice_stats['GA']/onice_stats['xGA']
    onice_stats['FshA%'] = onice_stats['GA']/onice_stats['FA']
    
    def calculate_toi(shifts,team,season_types,game_strength):
        shifts['seconds_elasped'] = shifts['seconds_elasped'].astype(int)
        shifts = shifts.loc[(shifts['season_type'].isin(season_types)) & (shifts['strength_state'].isin(game_strength)) & (shifts['period'] < 5)]
        
        if team == 'home':
            shifts = shifts.drop(['away_on_1','away_on_2','away_on_3','away_on_4','away_on_5','away_on_6','away_goalie'],axis=1)
        else:
            shifts = shifts.drop(['home_on_1','home_on_2','home_on_3','home_on_4','home_on_5','home_on_6','home_goalie'],axis=1)

        # Convert player on-ice columns to vectors
        shifts['on_ice'] = shifts[team+'_on_1'].astype(str) + ";" + shifts[team+'_on_2'].astype(str) + ";" + shifts[team+'_on_3'].astype(str) + ";" + shifts[team+'_on_4'].astype(str) + ";" + shifts[team+'_on_5'].astype(str) + ";" + shifts[team+'_on_6'].astype(str) + ";" + shifts[team+'_goalie']

        # Remove NA players
        shifts['on_ice'] = shifts['on_ice'].str.replace(';nan', '', regex=True)

        # Remove duplicate timestamps per game
        shifts = shifts.sort_values(by=['game_id', 'seconds_elasped']).drop_duplicates(subset=['game_id', 'seconds_elasped'], keep='last')
        
        # Fill missing game seconds (padding)
        all_seconds = shifts.groupby('game_id').apply(lambda df: df.set_index('seconds_elasped').reindex(range(1, df['seconds_elasped'].max() + 1))).ffill().reset_index(drop=True)
        all_seconds['seconds_elasped'] = all_seconds.index
        shifts = all_seconds[['game_id', 'seconds_elasped','on_ice',team+"_team_abbr"]]
        
        # Expand on_ice into individual player records
        full_shifts = shifts.assign(
            on_ice=shifts['on_ice'].str.split(';'),
        ).explode('on_ice')
        
        full_shifts = full_shifts.loc[full_shifts.index > 0]

        # Calculate Time on Ice (TOI)
        toi_df = full_shifts.groupby(['on_ice',team+"_team_abbr"]).agg(
            GP=('game_id', lambda x: x.nunique()),
            TOI=('seconds_elasped', 'count')
        ).reset_index()
        
        toi_df['TOI'] = toi_df['TOI'] / 60
        toi_df['on_ice'] = toi_df['on_ice'].replace(r'^\s*$', np.nan, regex=True)

        return toi_df.loc[toi_df['on_ice'].notna()].rename(columns={"on_ice": "Player",team+"_team_abbr":"Team"})

    home = calculate_toi(shifts,'home',season_types,game_strength)
    away = calculate_toi(shifts,'away',season_types,game_strength)

    info = pd.concat([home,away]).groupby(['Player','Team'], as_index=False).agg(
        GP = ('GP','sum'),
        TOI = ("TOI",'sum')
    )

    complete = pd.merge(indv_stats,onice_stats,how="outer",on=['Player','Team'])
    complete = pd.merge(complete,info,how="outer",on=['Player','Team'])
    complete['Season'] = season
    complete['GC%'] = complete['G']/complete['GF']
    complete['AC%'] = (complete['A1']+complete['A2'])/complete['GF']
    complete['GI%'] = (complete['G']+complete['A1']+complete['A2'])/complete['GF']
    complete['FC%'] = complete['iFF']/complete['FF']
    complete['xGC%'] = complete['ixG']/complete['xGF']
    complete['RC%'] = complete['Rush']/complete['iFF']
    complete['AVG_Rush_POW'] = complete['Rush_POW']/complete['Rush']

    return complete[[
        'Player',"Season","Team","GP","TOI",
        "G","A1","A2","iFF","ixG",'ixG/iFF',"G/ixG","iFsh%",
        "GF","FF","xGF","xGF/FF","GF/xGF","FshF%",
        "GA","FA","xGA","xGA/FA","GA/xGA","FshA%",
        "GC%","AC%","GI%","FC%","xGC%","Rush","Rush_POW","AVG_Rush_POW","RC%"
    ]].fillna(0)