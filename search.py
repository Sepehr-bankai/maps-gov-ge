import argparse
import glob
import json
import unicodedata


def normalize(text):
    return " ".join(unicodedata.normalize("NFC", text).casefold().split())


def find_name(name, pattern="responses_*.json"):
    query = normalize(name)
    matches = []
    for filename in sorted(glob.glob(pattern)):
        with open(filename, encoding="utf-8") as file:
            rows = json.load(file)
        if any(
            query in normalize(owner)
            for row in rows
            for result in row.get("response", {}).get("result", [])
            for owner in result.get("owners", [])
        ):
            matches.append(filename)
    return matches


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Find an owner name in response JSON files")
    parser.add_argument("name", nargs="?", help="Full or partial owner name")
    parser.add_argument("--pattern", default="responses_*.json")
    args = parser.parse_args()

    matches = find_name(args.name or input("Owner name: "), args.pattern)
    print("\n".join(matches) if matches else "No matches found.")
