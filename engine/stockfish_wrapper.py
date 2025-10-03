import chess
import chess.engine

class StockfishEvaluator:
    def __init__(self, engine_path="./engine/bin/stockfish.exe", depth=15):
        self.engine_path = engine_path
        self.depth = depth
        self.engine = chess.engine.SimpleEngine.popen_uci(self.engine_path)

    def evaluate(self, board):
        info = self.engine.analyse(board, chess.engine.Limit(depth=self.depth))
        score = info["score"].white()
        return score.score() if score.is_mate() == False else 1000  # Treat mate as large score

    def close(self):
        self.engine.quit()


if __name__ == "__main__":
    import chess

    # Create a starting position
    board = chess.Board()

    # Initialize evaluator
    evaluator = StockfishEvaluator()

    # Evaluate the starting position
    score = evaluator.evaluate(board)
    print(f"Evaluation of starting position: {score} centipawns")

    # Make a move and re-evaluate
    board.push_san("e4")
    score_after_e4 = evaluator.evaluate(board)
    print(f"Evaluation after 1.e4: {score_after_e4} centipawns")

    # Clean up
    evaluator.close()