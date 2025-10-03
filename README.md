# ♟️ Chess Analyzer

A simple Python tool to analyze a single chess game from a PGN file and output structured insights for both players.

## Features (Phase 1)

- Extract player names from PGN
- Output JSON summary with "white" and "black" keys

## Setup

```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

## Usage

```bash
python analyze_game.py path/to/game.pgn
```

## Output

Creates `output/game_summary.json` with player info and analysis.
