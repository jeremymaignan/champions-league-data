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
    clubs = {item['id']: item for item in sorted_list}
    return clubs

@app.route('/health', methods=['GET'])
def heathcheck():
    return jsonify({'hello': "world"})

@app.route('/clubs', methods=['GET'])
def get_clubs():
    c = fetch_clubs().values()
    return jsonify({'clubs': list(c)})

@app.route('/matches/<string:id>', methods=['GET'])
def get_matches(id):
    print("Getting matches for {}".format(id))

    # Query home team matches
    home_team_matches = db.query_items(
        'matches',
        'home_team_id = :id',
        {':id': id}
    )

    # Query away team matches using the secondary index
    away_team_matches = db.query_items(
        'matches',
        'away_team_id = :id',
        {':id': id},
        'AwayTeamIndex'
    )

    # Add locations to clubs
    clubs_data = fetch_clubs()
    results = {}
    for item in home_team_matches + away_team_matches:
        item["home_team"] = clubs_data.get(item["home_team_id"])
        item["away_team"] = clubs_data.get(item["away_team_id"])
        if id == item["home_team_id"]:
            opponent_id = item["away_team_id"]
        else:
            opponent_id = item["home_team_id"]
        if opponent_id not in results:
            results[opponent_id] = {
                "win": 0,
                "draw": 0,
                "loss": 0
            }
        if item["winner"] == id:
            results[opponent_id]["win"] += 1
        elif item["winner"] == "Draw":
            results[opponent_id]["draw"] += 1
        else:
            results[opponent_id]["loss"] += 1
    for item in home_team_matches + away_team_matches:
        if id == item["home_team_id"]:
            item["results"] = results[item["away_team_id"]]
        else:
            item["results"] = results[item["home_team_id"]]

    print("Found {} home matches and {} away matches".format(len(home_team_matches), len(away_team_matches)))
    return jsonify({'matches': home_team_matches + away_team_matches})

if __name__ == '__main__':
    app.run(port=5000, host="0.0.0.0", debug=True)
