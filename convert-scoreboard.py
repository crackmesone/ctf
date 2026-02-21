#!/usr/bin/env python3
"""
Convert CTFd scoreboard CSV to scoreboard.json
Usage: python3 convert-scoreboard.py <input.csv> [output.json]
"""

import csv
import json
import sys

def convert_csv_to_json(csv_path, json_path="scoreboard.json"):
    standings = []

    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            standings.append({
                "rank": int(row["place"]),
                "name": row["user name"],
                "score": int(row["score"])
            })

    # Sort by rank (should already be sorted, but just in case)
    standings.sort(key=lambda x: x["rank"])

    # Limit to top 100 players
    standings = standings[:100]

    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump({"standings": standings}, f, indent=2)

    print(f"Converted {len(standings)} players to {json_path}")
    print(f"Top 3:")
    for p in standings[:3]:
        print(f"  #{p['rank']} {p['name']}: {p['score']}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 convert-scoreboard.py <input.csv> [output.json]")
        print("Example: python3 convert-scoreboard.py 'Crackmesone CTF-scoreboard.csv'")
        sys.exit(1)

    csv_path = sys.argv[1]
    json_path = sys.argv[2] if len(sys.argv) > 2 else "scoreboard.json"
    convert_csv_to_json(csv_path, json_path)
