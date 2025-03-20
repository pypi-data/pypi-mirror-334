'''Utils for basketball-reference scraping.'''
import sys
import time
import requests
import pandas as pd
from bs4 import BeautifulSoup
from tqdm import tqdm

try:
    from utils.util import _get_game_suffix, _request_get_wrapper
    from utils.constants import SeasonType
except ModuleNotFoundError:
    from opponent_adjusted_nba_scraper.utils.util import _get_game_suffix, _request_get_wrapper
    from opponent_adjusted_nba_scraper.utils.constants import SeasonType

def _get_dataframe(url: str, attrs_id: str) -> pd.DataFrame:
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"}

    response = _request_get_wrapper(requests.get, {
        "url": url,
        "headers": headers,
        "timeout": 10
    })
    if response.status_code != 200:
        sys.exit(f"{response.status_code} Error")
    soup = BeautifulSoup(response.text, features="lxml")
    table = soup.find("table", attrs={"id": attrs_id})
    header = []
    rows = []
    for i, row in enumerate(table.find_all('tr')):
        if i == 0:
            header = [el.text.strip() for el in row.find_all('th')]
        else:
            rows.append([el.text.strip() for el in row.find_all('td')])
    if attrs_id == "advanced-team":
        header = ["Rk", "Team", "Age", "W", "L", "PW", "PL", "MOV", "SOS", "SRS", "ORtg",
                "DRtg", "NRtg", "Pace", "FTr", "3PAr", "TS%", " ", "eFG%", "TOV%", "ORB%",
                "FT/FGA", " ", "eFG%", "TOV%", "DRB%", "FT/FGA", " ", "Arena", "Attend.",
                "Attend./G"]
        rows = rows[1:]
    return pd.DataFrame(rows, columns=header[1:])

def _add_possessions(logs: pd.DataFrame, _team_dict: dict, _season_type: SeasonType) -> int:
    total_poss = 0
    logs["DATE"] = pd.to_datetime(logs["DATE"])
    logs["GAME_SUFFIX"] = ""
    for i in tqdm(range(len(logs)), desc='Loading player possessions...', ncols=75):
        suffix = _get_game_suffix(logs.iloc[i]["DATE"], logs.iloc[i]["TEAM"],
                                                    logs.iloc[i]["MATCHUP"])
        url = f'https://www.basketball-reference.com{suffix}'
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36" + \
        " (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"}
        response = _request_get_wrapper(requests.get, {
            "url": url,
            "headers": headers,
            "timeout": 10
        })
        if response.status_code != 200:
            sys.exit(f"{response.status_code} Error")
        response = response.text.replace("<!--","").replace("-->","")
        soup = BeautifulSoup(response, features="lxml")
        pace = soup.find("td", attrs={"data-stat":"pace"}).text
        total_poss += (logs.iloc[i]["MIN"] / 48) * float(pace)
        time.sleep(21)
    logs = logs.drop(columns=["GAME_SUFFIX"])
    return total_poss
