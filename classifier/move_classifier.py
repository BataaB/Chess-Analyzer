import chess.pgn
from collections import defaultdict
from engine.stockfish_wrapper import StockfishEvaluator

# Thresholds in centipawns
THRESHOLDS = {
    "Best": 20,
    "Inaccuracy": 50,
    "Mistake": 100
}

def classify_move(delta):
    abs_delta = abs(delta)
    if abs_delta < THRESHOLDS["Best"]:
        return "Best"
    elif abs_delta < THRESHOLDS["Inaccuracy"]:
        return "Inaccuracy"
    elif abs_delta < THRESHOLDS["Mistake"]:
        return "Mistake"
    else:
        return "Blunder"

def analyze_accuracy(pgn_path, engine_path="./engine/bin/stockfish.exe", depth=15):
    with open(pgn_path, "r") as pgn_file:
        game = chess.pgn.read_game(pgn_file)
        board = game.board()
        evaluator = StockfishEvaluator(engine_path=engine_path, depth=depth)

        accuracy_counts = {
            "white": defaultdict(int),
            "black": defaultdict(int)
        }

        for move in game.mainline_moves():
            before_score = evaluator.evaluate(board)
            board.push(move)
            after_score = evaluator.evaluate(board)
            delta = after_score - before_score

            player = "white" if board.turn == chess.BLACK else "black"
            label = classify_move(delta)
            accuracy_counts[player][label] += 1

        evaluator.close()

        # Convert defaultdicts to regular dicts
        return {
            "white": dict(accuracy_counts["white"]),
            "black": dict(accuracy_counts["black"])
        }