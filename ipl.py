import pandas as pd
from pathlib import Path
from typing import Union

DEFAULT_MATCHES = Path(
    r"C:\Users\Aayu0\Documents\MCA\Coding\Additional\Python\Projects\ipl-api-service\matches.csv"
)

def load_matches(path: Union[str, Path] = None) -> pd.DataFrame:
    if path is None:
        path = DEFAULT_MATCHES

    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(f"Matches file not found: {path}")

    return pd.read_csv(path)

def teamAPI():
    df = load_matches()

    teams = sorted(
        set(df["team1"]).union(set(df["team2"]))
    )

    return {
        "teams": teams,
        "total_teams": len(teams)
    }

if __name__ == "__main__":
    print(teamAPI())
