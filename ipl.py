import pandas as pd
from pathlib import Path
from typing import Union

# ---------------------- CSV PATH ----------------------

DEFAULT_MATCHES = Path(
    r"C:\Users\Aayu0\Documents\MCA\Coding\Additional\Python\Projects\ipl-api-service\matches.csv"
)

# ---------------------- LOAD MATCHES ----------------------

def load_matches(path: Union[str, Path] = None) -> pd.DataFrame:
    if path is None:
        path = DEFAULT_MATCHES
    return pd.read_csv(path)

# ---------------------- ALL TEAMS ----------------------

def teamAPI():
    df = load_matches()
    teams = sorted(set(df["team1"]).union(set(df["team2"])))
    return {
        "teams": teams,
        "total_teams": len(teams)
    }

# ---------------------- TEAM VS TEAM ----------------------

def team_vs_team(team1, team2):
    df = load_matches()

    temp_df = df[
        ((df["team1"] == team1) & (df["team2"] == team2)) |
        ((df["team1"] == team2) & (df["team2"] == team1))
    ]

    total_matches = int(temp_df.shape[0])
    draws = int(temp_df["winner"].isna().sum())
    wins = temp_df["winner"].dropna().value_counts()

    return {
        "total_matches": total_matches,
        team1: int(wins.get(team1, 0)),
        team2: int(wins.get(team2, 0)),
        "draws": draws
    }

# ---------------------- TEAM RECORD (DETAILED) ----------------------

def team_record(team):
    df = load_matches()
    team_matches = df[(df["team1"] == team) | (df["team2"] == team)]

    total_matches = int(team_matches.shape[0])
    wins = int((team_matches["winner"] == team).sum())
    no_result = int(team_matches["winner"].isna().sum())
    losses = total_matches - wins - no_result

    against = {}

    for _, row in team_matches.iterrows():
        opponent = row["team2"] if row["team1"] == team else row["team1"]

        if opponent not in against:
            against[opponent] = {
                "matchesplayed": 0,
                "won": 0,
                "lost": 0,
                "noResult": 0
            }

        against[opponent]["matchesplayed"] += 1

        if pd.isna(row["winner"]):
            against[opponent]["noResult"] += 1
        elif row["winner"] == team:
            against[opponent]["won"] += 1
        else:
            against[opponent]["lost"] += 1

    return {
        "team": team,
        "matchesplayed": total_matches,
        "won": wins,
        "lost": losses,
        "noResult": no_result,
        "against": against
    }

# ---------------------- BATTING RECORD (TEAM LEVEL) ----------------------

def batting_record(team):
    df = load_matches()
    team_matches = df[(df["team1"] == team) | (df["team2"] == team)]

    total_matches = int(team_matches.shape[0])
    wins = int((team_matches["winner"] == team).sum())
    no_result = int(team_matches["winner"].isna().sum())
    losses = total_matches - wins - no_result

    return {
        "team": team,
        "matchesplayed": total_matches,
        "wins": wins,
        "losses": losses,
        "noResult": no_result,
        "note": "Derived from match outcomes (no ball-by-ball data)"
    }

# ---------------------- BOWLING RECORD (TEAM LEVEL) ----------------------

def bowling_record(team):
    df = load_matches()
    team_matches = df[(df["team1"] == team) | (df["team2"] == team)]

    defended = 0
    failed_defense = 0
    no_result = 0

    for _, row in team_matches.iterrows():
        if pd.isna(row["winner"]):
            no_result += 1
        elif row["winner"] == team:
            defended += 1
        else:
            failed_defense += 1

    return {
        "team": team,
        "matchesplayed": int(team_matches.shape[0]),
        "successfully_defended": defended,
        "failed_defense": failed_defense,
        "noResult": no_result,
        "note": "Derived from match outcomes (no ball-by-ball data)"
    }
