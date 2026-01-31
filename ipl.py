import pandas as pd
from pathlib import Path     
from typing import Union
import matplotlib.pyplot as plt

# ======================================================
# BASE PATH
# ======================================================

BASE_DIR = Path(__file__).resolve().parent
DEFAULT_MATCHES = BASE_DIR / "data" / "ipl.csv"


# ======================================================
# TEAM ALIASES (FROM YOUR /api/teams OUTPUT)
# ======================================================

TEAM_ALIASES = {
    "RCB": [
        "Royal Challengers Bangalore",
        "Royal Challengers Bengaluru"
    ],
    "MI": ["Mumbai Indians"],
    "CSK": ["Chennai Super Kings"],
    "KKR": ["Kolkata Knight Riders"],
    "RR": ["Rajasthan Royals"],
    "SRH": ["Sunrisers Hyderabad"],
    "DC": ["Delhi Capitals", "Delhi Daredevils"],
    "PBKS": ["Punjab Kings", "Kings XI Punjab"],
    "GT": ["Gujarat Titans"],
    "GL": ["Gujarat Lions"],
    "LSG": ["Lucknow Super Giants"],
    "RPS": ["Rising Pune Supergiant", "Rising Pune Supergiants"],
    "KTK": ["Kochi Tuskers Kerala"],
    "PW": ["Pune Warriors"],
    "DCG": ["Deccan Chargers"]
}


# ======================================================
# LOAD DATA
# ======================================================

def load_matches(path: Union[str, Path] = None) -> pd.DataFrame:
    """
    IPL ball-by-ball CSV load karta hai
    """
    if path is None:
        path = DEFAULT_MATCHES
    return pd.read_csv(path)


# ======================================================
# NORMALIZE TEAM INPUT
# ======================================================

def normalize_team_names(team: str):
    """
    RCB / MI / CSK → dataset ke actual team names
    """
    team = team.strip().upper()
    return TEAM_ALIASES.get(team, [team])


# ======================================================
# TRUE MATCH-LEVEL DATA (CRITICAL FIX)
# ======================================================
def get_match_level_df():
    """
    Ball-by-ball data ko SAFE match-level data me convert karta hai
    - Har match me exactly 2 teams ensure karta hai
    - Incomplete / abandoned matches ko drop karta hai
    """
    df = load_matches()

    # Har match ke sab teams nikal lo (batting + bowling)
    teams_per_match = (
        df.groupby("match_id")
        .apply(
            lambda x: sorted(
                set(x["batting_team"].dropna())
                | set(x["bowling_team"].dropna())
            )
        )
        .reset_index(name="teams")
    )

    # Sirf valid matches rakho jisme exactly 2 teams ho
    teams_per_match = teams_per_match[
        teams_per_match["teams"].apply(len) == 2
    ]

    # team1 & team2 safely assign
    teams_per_match["team1"] = teams_per_match["teams"].apply(lambda x: x[0])
    teams_per_match["team2"] = teams_per_match["teams"].apply(lambda x: x[1])

    # Winner nikal lo
    winners = (
        df.groupby("match_id")["match_won_by"]
        .first()
        .reset_index()
    )
    
    match_df = teams_per_match.merge(
    winners,
    on="match_id",
    how="left"
    )

    match_df.rename(columns={"match_won_by": "winner"}, inplace=True)

    return match_df[["match_id", "team1", "team2", "winner"]]






# ======================================================
# PLOTTING
# ======================================================

def plot_total_matches_per_team():
    df = get_match_level_df()

    # Count matches per team (team1 + team2)
    team_counts = (
        pd.concat([df["team1"], df["team2"]])
        .value_counts()
        .sort_values(ascending=False)
    )

    # Plot
    plt.figure(figsize=(12, 6))
    team_counts.plot(kind="bar")
    plt.xlabel("Team")
    plt.ylabel("Matches Played")
    plt.title("Total Matches Played by Each Team (IPL)")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.show()
    


def plot_total_wins_per_team():
    df = get_match_level_df()

    # Count wins per team (ignore no-result matches)
    win_counts = (
        df["winner"]
        .dropna()
        .value_counts()
        .sort_values(ascending=False)
    )

    # Plot
    plt.figure(figsize=(12, 6))
    win_counts.plot(kind="bar")
    plt.xlabel("Team")
    plt.ylabel("Wins")
    plt.title("Total Wins by Each Team (IPL)")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.show()




def plot_wins_vs_losses_per_team():
    df = get_match_level_df()

    # Ignore no-result matches
    valid_matches = df.dropna(subset=["winner"])

    # Wins per team
    wins = valid_matches["winner"].value_counts()

    # Total matches per team (reuse earlier logic)
    total_matches = (
        pd.concat([df["team1"], df["team2"]])
        .value_counts()
    )

    # Losses = total matches - wins
    losses = total_matches.subtract(wins, fill_value=0)

    # Combine into a DataFrame
    stats_df = pd.DataFrame({
        "Wins": wins,
        "Losses": losses
    }).fillna(0)

    # Sort by wins
    stats_df = stats_df.sort_values(by="Wins", ascending=False)

    # Plot stacked bar chart
    plt.figure(figsize=(12, 6))
    stats_df.plot(
        kind="bar",
        stacked=True
    )

    plt.xlabel("Team")
    plt.ylabel("Matches")
    plt.title("Wins vs Losses by Each Team (IPL)")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.show()




def plot_team_vs_team(team1, team2):
    
    # Get head-to-head stats using existing logic
    stats = team_vs_team(team1, team2)

    # Extract values
    teams = [team1, team2]
    wins = [stats[team1], stats[team2]]

    # Plot
    plt.figure(figsize=(6, 5))
    plt.bar(teams, wins)

    plt.xlabel("Teams")
    plt.ylabel("Wins")
    plt.title(f"Head-to-Head: {team1} vs {team2}")
    plt.tight_layout()
    plt.show()






# ======================================================
# ALL TEAMS
# ======================================================

def teamAPI():
    df = load_matches()
    teams = sorted(set(df["batting_team"]).union(set(df["bowling_team"])))
    return {"teams": teams, "total_teams": len(teams)}


# ======================================================
# TEAM VS TEAM (FIXED)
# ======================================================

def team_vs_team(team1, team2):
    df = get_match_level_df()

    t1 = normalize_team_names(team1)
    t2 = normalize_team_names(team2)

    temp_df = df[
        (df["team1"].isin(t1) & df["team2"].isin(t2)) |
        (df["team1"].isin(t2) & df["team2"].isin(t1))
    ]

    wins = temp_df["winner"].value_counts()

    return {
        "total_matches": int(temp_df.shape[0]),
        team1: int(sum(wins.get(t, 0) for t in t1)),
        team2: int(sum(wins.get(t, 0) for t in t2)),
        "no_result": int(temp_df["winner"].isna().sum())
    }





# ======================================================
# TEAM RECORD
# ======================================================

def team_record(team):
    df = get_match_level_df()
    names = normalize_team_names(team)

    team_matches = df[df["team1"].isin(names) | df["team2"].isin(names)]

    total = int(team_matches.shape[0])
    wins = int(team_matches["winner"].isin(names).sum())
    no_result = int(team_matches["winner"].isna().sum())
    losses = total - wins - no_result

    against = {}

    for _, row in team_matches.iterrows():
        opponent = row["team2"] if row["team1"] in names else row["team1"]

        against.setdefault(opponent, {
            "matchesplayed": 0,
            "won": 0,
            "lost": 0,
            "noResult": 0
        })

        against[opponent]["matchesplayed"] += 1

        if pd.isna(row["winner"]):
            against[opponent]["noResult"] += 1
        elif row["winner"] in names:
            against[opponent]["won"] += 1
        else:
            against[opponent]["lost"] += 1

    return {
        "team": team,
        "matchesplayed": total,
        "won": wins,
        "lost": losses,
        "noResult": no_result,
        "against": against
    }



# ======================================================
# BATTING RECORD (TEAM LEVEL)
# ======================================================

def batting_record(team):
    df = get_match_level_df()
    names = normalize_team_names(team)

    team_matches = df[df["team1"].isin(names) | df["team2"].isin(names)]

    total = int(team_matches.shape[0])
    wins = int(team_matches["winner"].isin(names).sum())
    no_result = int(team_matches["winner"].isna().sum())
    losses = total - wins - no_result

    return {
        "team": team,
        "matchesplayed": total,
        "wins": wins,
        "losses": losses,
        "noResult": no_result,
        "note": "Derived from match outcomes, not pure batting stats"
    }




# ======================================================
# BOWLING RECORD (TEAM LEVEL)
# ======================================================

def bowling_record(team):
    df = get_match_level_df()
    names = normalize_team_names(team)

    team_matches = df[df["team1"].isin(names) | df["team2"].isin(names)]

    defended = failed = no_result = 0

    for _, row in team_matches.iterrows():
        if pd.isna(row["winner"]):
            no_result += 1
        elif row["winner"] in names:
            defended += 1
        else:
            failed += 1

    return {
        "team": team,
        "matchesplayed": int(team_matches.shape[0]),
        "successfully_defended": defended,
        "failed_defense": failed,
        "noResult": no_result,
        "note": "Derived from match outcomes"
    }



if __name__ == "__main__":
    plot_total_matches_per_team()
    plot_total_wins_per_team()
    plot_wins_vs_losses_per_team()
    plot_team_vs_team("RCB", "MI")
