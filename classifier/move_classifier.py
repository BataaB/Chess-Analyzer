import chess.pgn
from collections import defaultdict
from engine.stockfish_wrapper import StockfishEvaluator

# Thresholds in centipawns
THRESHOLDS = {
    "Best": 20,
    "Inaccuracy": 50,
    "Mistake": 100
}

def classify_move(delta, thresholds=THRESHOLDS):
    abs_delta = abs(delta)
    if abs_delta < THRESHOLDS["Best"]:
        return "Best"
    elif abs_delta < THRESHOLDS["Inaccuracy"]:
        return "Inaccuracy"
    elif abs_delta < THRESHOLDS["Mistake"]:
        return "Mistake"
    else:
        return "Blunder"
    
def classify_phase(move_number, cutoffs):
    if move_number <= cutoffs["opening"]:
        return "opening"
    elif move_number <= cutoffs["middlegame"]:
        return "middlegame"
    else:
        return "endgame"

def analyze_accuracy(pgn_path, engine_path="stockfish", depth=15, cutoffs=None, thresholds=None):
    if cutoffs is None:
        cutoffs = {"opening": 12, "middlegame": 30}

    with open(pgn_path, "r") as pgn_file:
        game = chess.pgn.read_game(pgn_file)
        board = game.board()
        evaluator = StockfishEvaluator(engine_path=engine_path, depth=depth)

        accuracy_counts = {
            "white": defaultdict(int),
            "black": defaultdict(int)
        }

        phase_counts = {
            "white": defaultdict(lambda: defaultdict(int)),
            "black": defaultdict(lambda: defaultdict(int))
        }

        # Loop through each move
        for move in game.mainline_moves():
            # Calculate the delta of the move
            before_score = evaluator.evaluate(board)
            board.push(move)
            after_score = evaluator.evaluate(board)
            delta = after_score - before_score

            # Classify the move depening on the delta
            label = classify_move(delta, thresholds)

            # Update the accuracy count for that player
            player = "white" if board.turn == chess.BLACK else "black"
            accuracy_counts[player][label] += 1

            # Update the phase accuracy count for that player
            phase = classify_phase(board.fullmove_number, cutoffs)
            phase_counts[player][phase][label] += 1

        evaluator.close()

        return {
            "white": {
                "overall": dict(accuracy_counts["white"]),
                "phases": {phase: dict(counts) for phase, counts in phase_counts["white"].items()}
            },
            "black": {
                "overall": dict(accuracy_counts["black"]),
                "phases": {phase: dict(counts) for phase, counts in phase_counts["black"].items()}
            }
        }