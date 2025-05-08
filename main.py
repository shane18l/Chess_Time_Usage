import chess.pgn
import chess.engine
import pandas as pd
import re
import datetime
import matplotlib.pyplot as plt
import seaborn as sns
import glob
import os

engine_path = "Enter your engine path (stockfish.exe)"
pgn_folder = "match_histories"
pgn_files = glob.glob(os.path.join(pgn_folder, "*.pgn"))

moves = []

def parse_increment(tc_str):
    if '+' in tc_str:
        try:
            return int(tc_str.split('+')[1])
        except:
            return 0
    return 0

def parse_timestamp(ts):
    if pd.isna(ts):
        return None
    try:
        if ts.count(':') == 2:
            t = datetime.datetime.strptime(ts, "%H:%M:%S")
        else:
            t = datetime.datetime.strptime(ts, "%M:%S")
        return t.minute * 60 + t.second
    except Exception as e:
        print(f"Parse error for {ts}: {e}")
        return None



def get_material(board):
    material_count = {chess.WHITE: 0, chess.BLACK: 0}
    
    # Piece values
    piece_values = {
        chess.PAWN: 1,
        chess.KNIGHT: 3,
        chess.BISHOP: 3,
        chess.ROOK: 5,
        chess.QUEEN: 9,
        chess.KING: 0  
    }
    
    for square, piece in board.piece_map().items():
        material_count[piece.color] += piece_values.get(piece.piece_type, 0)
    
    return material_count[chess.WHITE], material_count[chess.BLACK]


def read_games_from_file(pgn):
    with chess.engine.SimpleEngine.popen_uci(engine_path) as engine:     
        while True:
            game = chess.pgn.read_game(pgn)
            
            if game is None:
                break
            headers = game.headers
            white = headers["White"]
            black = headers["Black"]
            result = headers["Result"]
            date = headers.get("Date", "Unknown")
            time_control = headers["TimeControl"]

            node = game
            move_number = 1
            board = game.board()

            info = engine.analyse(board, chess.engine.Limit(depth=15))
            score_before_move = info["score"]

            while node.variations:
                move_maker = board.turn
                next_node = node.variation(0)
                comment = next_node.comment
                move = next_node.move
                moved_piece = board.piece_at(move.from_square).piece_type
                moved_piece_name = chess.piece_name(moved_piece).capitalize()
                is_capture = board.is_capture(move)
                gives_check = board.gives_check(move)
                is_castle = board.is_castling(move)
                san_move = board.san(move)
                timestamp = None
                board.push(move)


                info = engine.analyse(board, chess.engine.Limit(depth=15))
                score_after_move = info["score"]
                move_quality = (
                    score_after_move.pov(move_maker).score(mate_score=10000) / 100 -
                    score_before_move.pov(move_maker).score(mate_score=10000) / 100)
                
                match = re.search(r"\[%clk\s*([^\]]+)\]", comment)
                if match:
                    timestamp = match.group(1).split('.')[0]
                    # Do something with timestamp
                else:
                    print(f"No timestamp found in comment: {comment}")

                white_material, black_material = get_material(board)    
                
                if move_number <= 20:
                    phase = "Opening"
                elif white_material + black_material < 20:
                    phase = "Endgame"
                else:
                    phase = "Middlegame"

                moves.append({
                    "Date": date,
                    "White": white,
                    "Black": black,
                    "White Material": white_material,
                    "Black Material": black_material,
                    "Result": result,
                    "Move Number": move_number,
                    "Move": san_move,
                    "Move By": "White" if move_maker else "Black",
                    "Timestamp": timestamp,
                    "Move Evaluation": move_quality,
                    "Phase": phase,
                    "Moved Piece": moved_piece_name,
                    "Is Capture": is_capture,
                    "Is Castle": is_castle,
                    "Gives Check": gives_check,
                    "Time Control": time_control,
                })

                node = next_node
                move_number += 1
                score_before_move = score_after_move

for file in pgn_files:
    pgn = open(file)
    read_games_from_file(pgn)

df = pd.DataFrame(moves)
df['Increment'] = df['Time Control'].apply(parse_increment)
df['Seconds Remaining'] = df['Timestamp'].apply(parse_timestamp)
df['Time Spent'] = -df.groupby(['Date', 'White', 'Black', 'Move By'])['Seconds Remaining'].diff() 
df['Time Spent'] = abs(df['Increment'] - abs(df['Time Spent']))
df.to_csv("chess_moves_with_time.csv", index=False)

