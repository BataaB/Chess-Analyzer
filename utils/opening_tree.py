import json
import os
import requests
import chess.pgn

def load_tree(path="data/opening_tree.json"):
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return {}

def save_tree(tree, path="data/opening_tree.json"):
    with open(path, "w") as f:
        json.dump(tree, f, indent=2)

def retrieve_opening(tree, moves):
    node = tree
    for move in moves:
        if move in node:
            node = node[move]
        else:
            meta = query_opening_api(moves)
            if (meta != None):
                node[move] = {
                    "_meta": meta
                }
                node = node[move]
            else:
                return None
    return node.get("_meta")

def save_line(tree, moves, meta):
    node = tree
    for move in moves:
        node = node.setdefault(move, {})
    node["_meta"] = meta


def query_opening_api(moves):
    uci_line = ",".join(moves)
    url = f"https://explorer.lichess.ovh/masters?play={uci_line}"
    try:
        response = requests.get(url)
        if response.ok:
            data = response.json()
            opening = data.get("opening", {})
            return {
                "eco": opening.get("eco", "Unknown"),
                "name": opening.get("name", "Unknown"),
                "tags": []
            }
    except Exception:
        print("Problem with fetch.")
        print(f"URL: {url}")
        pass
    return None

def detect_opening(pgn_path, opening_capacity=8):
    if (not os.path.exists(pgn_path)):
        return None
    
    moves = []
    with open(pgn_path, "r") as pgn_file:
        game = chess.pgn.read_game(pgn_file)
        count = 0
        for move in game.mainline_moves():
            if (count < opening_capacity):
                moves.append(move.uci())
                count += 1
            else:
                break
    
    tree = load_tree()
    opening = retrieve_opening(tree, moves)
    save_tree(tree)
    return opening

if __name__ == "__main__":
    opening = detect_opening("last_blitz.pgn")
    print(opening if opening != None else "Unknown")