from pathlib import Path
from datetime import datetime

from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

# Directory where your files like 2025-12-15_smetana.csv are stored
DATA_DIR = Path(__file__).parent / "data"

# shop["id"] must match the suffix in the filenames: YYYY-MM-DD_<id>.csv
SHOPS = [
    {"id": "antik", "name": "Antik Chiméra"},
    {"id": "smetana", "name": "Sběratelský antikvariát Smetana"},
    {"id": "empire", "name": "VINYL Empire"},
]


def get_two_latest_files_for_shop(shop_suffix: str):
    """
    For files named YYYY-MM-DD_<shop_suffix>.csv, return (older, newer) Path objects.
    If fewer than 2 files exist, return (None, None).
    """
    files = list(DATA_DIR.glob(f"*_{shop_suffix}.csv"))
    if len(files) < 2:
        return None, None

    def extract_date(path: Path):
        # "2025-12-15_smetana.csv" -> datetime(2025, 12, 15)
        date_str = path.name.split("_", 1)[0]
        return datetime.strptime(date_str, "%Y-%m-%d")

    files_sorted = sorted(files, key=extract_date)
    older = files_sorted[-2]
    newer = files_sorted[-1]
    return older, newer


def load_entries_from_file(path: Path):
    """
    Read a file where each non-empty line is one LP entry.
    Return a DataFrame with a single column 'LP', or None if no data.
    """
    if not path or not path.exists():
        return None

    lines = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                lines.append(line)

    if not lines:
        return None

    return pd.DataFrame({"LP": lines})


@app.route("/")
def index():
    shops_data = []

    for shop in SHOPS:
        older_path, newer_path = get_two_latest_files_for_shop(shop["id"])

        df_new = load_entries_from_file(newer_path)
        df_old = load_entries_from_file(older_path)

        new_entries = None
        gone_entries = None

        if df_new is not None and df_old is not None:
            set_new = set(df_new["LP"])
            set_old = set(df_old["LP"])

            only_new = sorted(set_new - set_old)
            only_gone = sorted(set_old - set_new)

            if only_new:
                new_entries = pd.DataFrame({"LP": only_new})
            if only_gone:
                gone_entries = pd.DataFrame({"LP": only_gone})
        elif df_new is not None:
            # Only a newer file exists: treat all as new
            new_entries = df_new

        shops_data.append(
            {
                "id": shop["id"],
                "name": shop["name"],
                "new_html": new_entries.to_html(
                    classes="table table-striped table-sm", index=False
                )
                if new_entries is not None
                else None,
                "gone_html": gone_entries.to_html(
                    classes="table table-striped table-sm", index=False
                )
                if gone_entries is not None
                else None,
            }
        )

    return render_template("index.html", shops=shops_data)


if __name__ == "__main__":
    # Development server: http://127.0.0.1:5002/
    app.run(host="0.0.0.0", port=5002, debug=False)
