import os, csv
from collections import defaultdict

CSV_FILE = "reaction_data.csv"

def get_next_session_index():
    if not os.path.isfile(CSV_FILE):
        return 1
    with open(CSV_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()
    if len(lines) <= 1:
        return 1
    last_session = int(lines[-1].split(",")[0])
    return last_session + 1

def save_reaction_data(limb_reaction_times: defaultdict):
    file_exists = os.path.isfile(CSV_FILE)
    with open(CSV_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["Session", "Limb", "ReactionTime"])
        session_idx = get_next_session_index()
        for limb, diffs in limb_reaction_times.items():
            for diff in diffs:
                writer.writerow([session_idx, limb, diff])
