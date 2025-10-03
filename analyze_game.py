import chess.pgn
import json
import sys
import os

def extract_player_names(pgn_path):
    with open(pgn_path, "r") as pgn_file:
        game = chess.pgn.read_game(pgn_file)
        white_player = game.headers.get("White", "Unknown")
        black_player = game.headers.get("Black", "Unknown")
        return {
            "white": {"player": white_player},
            "black": {"player": black_player}
        }

def save_to_json(data, output_path="output/game_summary.json"):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w") as json_file:
        json.dump(data, json_file, indent=4)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python analyze_game.py path/to/game.pgn")
        sys.exit(1)

    pgn_path = sys.argv[1]
    summary = extract_player_names(pgn_path)
    save_to_json(summary)
    print("✅ Analysis complete. Output saved to output/game_summary.json")
