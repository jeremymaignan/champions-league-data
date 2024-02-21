import requests
from utils import get_conf

headers = {
    'Accept': 'application/json, text/plain, */*',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    'x-api-key': 'ceeee1a5bb209502c6c438abd8f30aef179ce669bb9288f2d1cf2fa276de03f4',
}

params = {
    'competitionId': '',
    'limit': '200',
    'offset': '0',
    'order': 'DESC',
    'phase': 'TOURNAMENT',
    'seasonYear': '',
}
clubs = {} 
def build_match_item(match):
    try:
        competition =  match["competition"]["metaData"]["name"]
        round = match["round"]["metaData"]["type"]
        try:
            if match["homeTeam"]["internationalName"] not in clubs and round != "FINAL":
                clubs[match["homeTeam"]["internationalName"]] = {
                    "id": match["homeTeam"]["id"],
                    "name": match["homeTeam"]["internationalName"],
                    "country": match["homeTeam"]["translations"]["countryName"]["EN"],
                    "logo": match["homeTeam"]["bigLogoUrl"],
                    "geolocation": {
                        "lat": str(match["stadium"]["geolocation"]["latitude"]),
                        "long": str(match["stadium"]["geolocation"]["longitude"])
                    }
                }
        except:
            pass
        try:
            winner = match["winner"]["match"]["team"]["internationalName"]
        except:
            winner = "Draw"
        return {
            "date": match["kickOffTime"]["date"],
            "competition": competition,
            "match_type": match["matchday"]["type"],
            "round": round,
            "winner": winner,
            "home_team_name": match["homeTeam"]["internationalName"],
            "home_team_id": match["homeTeam"]["id"],
            "home_team_score": match["score"]["regular"]["home"],
            "away_team_name": match["awayTeam"]["internationalName"],
            "away_team_id": match["awayTeam"]["id"],
            "away_team_score": match["score"]["regular"]["away"],
        }
    except Exception as err:
        print("Error {}".format(err))

def scrapper(competition_name):
    games = []
    competition = get_conf("competitions")[competition_name]

    #for year in range(competition["from"], 2023):
    for year in range(2021, 2023):
        params["seasonYear"] = year
        params["competitionId"] = competition["id"]
        response = requests.get('https://match.uefa.com/v5/matches', params=params, headers=headers, timeout=10)
        if response.status_code != 200:
            print(response.status_code)
            continue
        for match in response.json():
            d = build_match_item(match)
            if d:
               games.append(d)
        print("Year {} has {} games for competition {}".format(year, len(games), competition_name))
    print("Total clubs {}".format(len(clubs)))
    return games, clubs.values()
