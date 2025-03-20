'''Constants and types.'''
from dataclasses import dataclass

@dataclass
class Mode:
    '''
    Class for choosing stat modes.
    '''

    per_game = "PerGame"
    per_100_poss = "Per100Poss"
    pace_adj = "PaceAdjusted"
    opp_adj = "OpponentAdjusted"
    opp_pace_adj = "OpponentAndPaceAdjusted"

    default = per_game

@dataclass
class SeasonType:
    '''
    Class for choosing season types.
    '''

    regular_season = "Regular Season"
    playoffs = "Playoffs"

    default = regular_season

@dataclass
class Site:
    '''
    Class for choosing site to collect data from.
    '''

    basketball_reference = "Basketball Reference"
    nba_stats = "NBA Stats"

    default = basketball_reference

def _teams() -> dict:
    return {"ATL":'37', "BOS":'38', "BKN":'51', "CHA":'66', "CHI":'41', "CLE":'39', "DAL":'42',
            "DEN":'43', "DET":'65', "GSW":'44', "HOU":'45', "IND":'54', "LAC":'46', "LAL":'47',
            "MEM":'63', "MIA":'48', "MIL":'49', "MIN":'50', "NOP":'40', "NYK":'52', "OKC":'60',
            "ORL":'53', "PHI":'55', "PHX":'56', "POR":'57', "SAC":'58', "SAS":'59', "TOR":'61',
            "UTA":'62', "WAS":'64', "NJN":"51", "CHO":"66", "VAN":"63", "NOH":"40", "SEA":"60",
            "NOK":'40'}

def _team_to_team_abbr() -> dict:
    return {
        'ATLANTA HAWKS': 'ATL',
        'BOSTON CELTICS': 'BOS',
        'BROOKLYN NETS': 'BKN',
        'NEW JERSEY NETS' : 'NJN',
        'CHICAGO BULLS': 'CHI',
        'CHARLOTTE HORNETS': 'CHO',
        'CHARLOTTE BOBCATS' : 'CHA',
        'CLEVELAND CAVALIERS': 'CLE',
        'DALLAS MAVERICKS': 'DAL',
        'DENVER NUGGETS': 'DEN',
        'DETROIT PISTONS': 'DET',
        'GOLDEN STATE WARRIORS': 'GSW',
        'HOUSTON ROCKETS': 'HOU',
        'INDIANA PACERS': 'IND',
        'LOS ANGELES CLIPPERS': 'LAC',
        'LA CLIPPERS': 'LAC',
        'LOS ANGELES LAKERS': 'LAL',
        'LA LAKERS': 'LAL',
        'KANSAS CITY KINGS': 'KCK',
        'MEMPHIS GRIZZLIES': 'MEM',
        'MIAMI HEAT': 'MIA',
        'MILWAUKEE BUCKS': 'MIL',
        'MINNESOTA TIMBERWOLVES': 'MIN',
        'NEW ORLEANS PELICANS' : 'NOP',
        'NEW ORLEANS HORNETS' : 'NOH',
        'NEW ORLEANS/OKLAHOMA CITY HORNETS': 'NOK',
        'NEW YORK KNICKS' : 'NYK',
        'OKLAHOMA CITY THUNDER' : 'OKC',
        'SEATTLE SUPERSONICS' : 'SEA',
        'ORLANDO MAGIC' : 'ORL',
        'PHILADELPHIA 76ERS' : 'PHI',
        'PHOENIX SUNS' : 'PHO',
        'PORTLAND TRAIL BLAZERS' : 'POR',
        'SACRAMENTO KINGS' : 'SAC',
        'SAN ANTONIO SPURS' : 'SAS',
        'TORONTO RAPTORS' : 'TOR',
        'UTAH JAZZ' : 'UTA',
        'NEW ORLEANS JAZZ' : 'NOJ',
        'VANCOUVER GRIZZLIES': 'VAN',
        'WASHINGTON BULLETS': 'WSB',
        'WASHINGTON WIZARDS' : 'WAS',
    }

def _desired_log_columns() -> list:
    return ['SEASON', 'DATE', 'NAME', 'TEAM', 'MATCHUP', 'MIN', 'FG', 'FGA', 'FG%', '3P', '3PA',
            '3P%', 'FT', 'FTA', 'FT%', 'ORB', 'DRB', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF',
            'PTS', 'GmSc', '+/-']
