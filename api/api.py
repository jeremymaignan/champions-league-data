from flask import Flask, jsonify
from flask_cors import CORS
from dynamodb import DynamoDB

app = Flask(__name__)
CORS(app)

clubs = {}

db = DynamoDB()

def fetch_clubs():
    global clubs
    if clubs:
        print("Use cache")
        return clubs

    print("Getting clubs")
    all_items = db.scan_table("clubs")
    sorted_list = sorted(all_items, key=lambda x: x['name'])
    clubs = {item['name']: item for item in sorted_list}
    return clubs

@app.route('/clubs', methods=['GET'])
def get_clubs():
    c = fetch_clubs().values()
    return jsonify({'clubs': list(c)})

@app.route('/games/<string:name>', methods=['GET'])
def get_games(name):
    print("Getting games for {}".format(name))

    # Query home team games
    home_team_games = db.query_items(
        'games',
        'home_team_name = :value',
        {':value': name}
    )

    # Query away team games using the secondary index
    away_team_games = db.query_items(
        'games',
        'away_team_name = :away_team_name',
        {':away_team_name': name},
        'AwayTeamDateIndex'
    )

    # Add locations to clubs
    clubs_data = fetch_clubs()
    for item in home_team_games + away_team_games:
        item["home_team"] = clubs_data.get(item["home_team_name"])
        item["away_team"] = clubs_data.get(item["away_team_name"])

    print("Found {} home games and {} away games".format(len(home_team_games), len(away_team_games)))
    return jsonify({'games': home_team_games + away_team_games})

if __name__ == '__main__':
    app.run(port=5000, debug=True)
