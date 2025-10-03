import os
import sys
import json
import time
import chess.pgn
from classifier.move_classifier import analyze_accuracy

with open("config/settings.json", "r") as config_file:
    config = json.load(config_file)
    cutoffs = config.get("phase_cutoffs", {"opening": 12, "middlegame": 30})
    thresholds = config.get("thresholds", {"Best": 20, "Inaccuracy": 50, "Mistake": 100})

def extract_game_info(pgn_path):
    with open(pgn_path, "r") as pgn_file:
        game = chess.pgn.read_game(pgn_file)
        result = game.headers.get("Result", "*")
        white_player = game.headers.get("White", "Unknown")
        black_player = game.headers.get("Black", "Unknown")

        # Interpret result
        if result == "1-0":
            white_result, black_result = "win", "lose"
        elif result == "0-1":
            white_result, black_result = "lose", "win"
        elif result == "1/2-1/2":
            white_result = black_result = "draw"
        else:
            white_result = black_result = "incomplete"

        return {
            "white": {"player": white_player, "result": white_result},
            "black": {"player": black_player, "result": black_result}
        }

def save_to_json(data, output_path="output/game_summary.json"):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w") as json_file:
        json.dump(data, json_file, indent=4)

def analyze_game(pgn_path):
    # Load basic info
    summary = extract_game_info(pgn_path)

    # Load configuration info
    engine_path = os.path.abspath(config["engine_path"])
    depth = config.get("engine_depth", 15)
    cutoffs = config.get("phase_cutoffs", {"opening": 12, "middlegame": 30})

    # Process accuracy of moves
    print(f"🔍 Starting analysis for: {os.path.basename(pgn_path)}")
    start_time = time.time()
    accuracy = analyze_accuracy(
        pgn_path,
        engine_path=engine_path,
        depth=depth,
        cutoffs=cutoffs,
        thresholds=thresholds
    )

    # Summarize the move accuracies
    for color in ["white", "black"]:
        overall = accuracy[color]["overall"]
        phases = accuracy[color]["phases"]

        total_moves = sum(overall.values())
        best_moves = overall.get("Best", 0)
        accuracy_percent = round((best_moves / total_moves) * 100, 2) if total_moves > 0 else 0.0

        phase_accuracy_percent = {}
        for phase_name, counts in phases.items():
            phase_total = sum(counts.values())
            phase_best = counts.get("Best", 0)
            if phase_total == 0:
                phase_accuracy_percent[phase_name] = "Not reached"
            else:
                phase_accuracy_percent[phase_name] = round((phase_best / phase_total) * 100, 2)

        summary[color]["accuracy"] = overall
        summary[color]["accuracy_percent"] = accuracy_percent
        summary[color]["phase_accuracy"] = phase_accuracy_percent

    # Save the result
    save_to_json(summary)

    # Let the user know that the analysis if finished
    end_time = time.time()
    print("✅ Analysis complete. Output saved to output/game_summary.json")
    print(f"⏱️ Analysis took {end_time - start_time:.2f} seconds")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python analyze_game.py path/to/game.pgn")
        sys.exit(1)

    analyze_game(sys.argv[1])