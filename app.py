from flask import Flask, jsonify, request
from ipl import (
    load_matches,
    teamAPI,
    team_vs_team,
    team_record,
    batting_record,
    bowling_record
)

app = Flask(__name__)

# ---------------- HOME ----------------
@app.route("/")
def home():
    return "Hello World"

# ---------------- ALL TEAMS ----------------
@app.route("/api/teams")
def teams():
    return jsonify(teamAPI())

# ---------------- MATCHES ----------------
@app.route("/matches")
def matches():
    df = load_matches()
    return jsonify(df.head(10).to_dict(orient="records"))

# ---------------- TEAM VS TEAM ----------------
@app.route("/api/teamvteam")
def teamvteam():
    team1 = request.args.get("team1")
    team2 = request.args.get("team2")

    if not team1 or not team2:
        return jsonify({"error": "team1 and team2 required"}), 400

    return jsonify(team_vs_team(team1, team2))

# ---------------- TEAM RECORD ----------------
@app.route("/api/team-record")
def team_record_api():
    team = request.args.get("team")

    if not team:
        return jsonify({"error": "team parameter required"}), 400

    return jsonify(team_record(team))

# ---------------- BATTING RECORD ----------------
@app.route("/api/batting-record")
def batting_record_api():
    team = request.args.get("team")

    if not team:
        return jsonify({"error": "team parameter required"}), 400

    return jsonify(batting_record(team))

# ---------------- BOWLING RECORD ----------------
@app.route("/api/bowling-record")
def bowling_record_api():
    team = request.args.get("team")

    if not team:
        return jsonify({"error": "team parameter required"}), 400

    return jsonify(bowling_record(team))

# ---------------- RUN APP ----------------
if __name__ == "__main__":
    app.run(debug=True)
