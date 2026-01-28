from flask import Flask, jsonify, request
from ipl import (
    load_matches,
    teamAPI,
    team_vs_team,
    team_record,
    batting_record,
    bowling_record,
    get_match_level_df
)

app = Flask(__name__)

# ---------------- HOME ----------------
@app.route("/")
def home():
    """
    Basic home route
    Server running hai ya nahi check karne ke kaam aata hai
    """
    return "IPL API Service is Running 🚀"


# ---------------- ALL TEAMS ----------------
@app.route("/api/teams")
def teams():
    """
    IPL me jitni bhi teams rahi hain unki list deta hai
    """
    return jsonify(teamAPI())


# ---------------- MATCHES (MATCH LEVEL) ----------------
@app.route("/api/matches")
def matches():
    """
    Match-level data return karta hai
    Har match ek hi baar dikhega (ball-by-ball nahi)
    """
    df = get_match_level_df()

    return jsonify(
        df.head(10).to_dict(orient="records")
    )


# ---------------- TEAM VS TEAM ----------------
@app.route("/api/teamvteam")
def teamvteam():
    """
    Do teams ke beech head-to-head record
    Query Params:
    ?team1=CSK&team2=MI
    """
    team1 = request.args.get("team1")
    team2 = request.args.get("team2")

    if not team1 or not team2:
        return jsonify({
            "error": "team1 and team2 query parameters are required"
        }), 400

    return jsonify(team_vs_team(team1, team2))


# ---------------- TEAM RECORD ----------------
@app.route("/api/team-record")
def team_record_api():
    """
    Kisi ek team ka overall IPL record
    Query Param:
    ?team=CSK
    """
    team = request.args.get("team")

    if not team:
        return jsonify({
            "error": "team query parameter is required"
        }), 400

    return jsonify(team_record(team))


# ---------------- BATTING RECORD ----------------
@app.route("/api/batting-record")
def batting_record_api():
    """
    Team ka batting record (match outcome based)
    Query Param:
    ?team=CSK
    """
    team = request.args.get("team")

    if not team:
        return jsonify({
            "error": "team query parameter is required"
        }), 400

    return jsonify(batting_record(team))


# ---------------- BOWLING RECORD ----------------
@app.route("/api/bowling-record")
def bowling_record_api():
    """
    Team ka bowling record (match outcome based)
    Query Param:
    ?team=CSK
    """
    team = request.args.get("team")

    if not team:
        return jsonify({
            "error": "team query parameter is required"
        }), 400

    return jsonify(bowling_record(team))


# ---------------- RUN APP ----------------
if __name__ == "__main__":
    """
    debug=True:
    - Code change pe auto reload
    - Error trace clearly dikhega
    """
    app.run(debug=True)
