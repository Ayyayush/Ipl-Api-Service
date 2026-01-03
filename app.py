from flask import Flask, jsonify
from ipl import load_matches, teamAPI

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello World"

@app.route("/api/teams")
def teams():
    return jsonify(teamAPI())

@app.route("/matches")
def matches():
    df = load_matches()
    return jsonify(df.head(10).to_dict(orient="records"))

if __name__ == "__main__":
    app.run(debug=True)
