import chess
from typing import Optional
# Neural Network evaluation is optional -- if the nn_eval module isn't
# available (or the model hasn't been trained), fall back to a no-op
# implementation so the app doesn't crash.
try:
    from nn_eval import evaluate_board_nn
except ImportError:
    # If nn_eval isn't available, set to None and handle accordingly
    def evaluate_board_nn(board) -> Optional[float]:
        return None

# Simple evaluation function values
PIECE_VALUES = {
    chess.PAWN: 10,
    chess.KNIGHT: 30,
    chess.BISHOP: 30,
    chess.ROOK: 50,
    chess.QUEEN: 90,
    chess.KING: 900
}

def evaluate_board(board):
     # Yaad rakho: Poore code mein convention hai —
    # positive score = White ke liye acha, 
    # negative score = Black ke liye acha (White ke liye bura).
    
    #  chess library ka function hai jo check karta hai "kya abhi checkmate ho chuka hai?"
    # (True/False return karega)
# Agar checkmate ho chuka hai, to ek bahut extreme score return karte hain (9999 ya -9999) — 
# taaki AI ko pata chale ye position bahut important hai.
    if board.is_checkmate():
        return -9999 if board.turn == chess.WHITE else 9999
      # is_stalemate() — check karta hai kya stalemate hua hai (jab kisi player ki chaal hai but koi legal move nahi hai, 
    # aur check mein bhi nahi hai — ye draw hota hai)
    
    # is_insufficient_material() — check karta hai kya dono taraf itne kam pieces bache hain ki checkmate possible hi nahi 
    # (jaise sirf do Kings bache ho) — ye bhi draw
    
    # is_seventyfive_moves() — chess ka rule hai, agar 75 moves tak koi pawn move ya capture na ho, to automatic draw
    if board.is_stalemate() or board.is_insufficient_material() or board.is_seventyfive_moves():
        return 0 # Agar in teeno mein se koi bhi true hai, matlab game draw hai — isliye score 0 return karo (na White ke liye acha, na Black ke liye)

    
    score = 0
    for sq in chess.SQUARES: #chess.SQUARES — chess library ka ek built-in list hai jisme saare 64 squares hain board ke (a1, a2, ... h8)
          # piece.piece_type — us piece ka type nikal rahe hain (Pawn hai, Knight hai, etc)
# PIECE_VALUES.get(key, default) — dictionary se value nikaalne ka safe tarika hai. Agar piece.piece_type dictionary mein mil jaaye, to uski value de do. Agar na mile (jo yahan nahi hoga, but safety ke liye), to 0 de do (default value).
        piece = board.piece_at(sq)
        if piece:
            value = PIECE_VALUES.get(piece.piece_type, 0)
            # Center control premium
            # e4, d4, e5, d5 are sq numbers 28, 27, 36, 35
            if sq in [27, 28, 35, 36]:
                value += 1
    #  Yaad hai humne bola tha — positive score = White ke liye acha. Isliye White ke pieces score badhate hain,
# Black ke pieces score ghatate hain. Agar White ke paas zyada/bade pieces hain,
# to overall score positive (zyada) hoga.
            if piece.color == chess.WHITE:
                score += value
            else:
                score -= value
    return score

def evaluate_board_hybrid(board):
    
    if board.is_game_over():
        return evaluate_board(board)

    heuristic_score = evaluate_board(board)
    if evaluate_board_nn is None:
        return heuristic_score
    nn_score = evaluate_board_nn(board)

    if nn_score is None:
        return heuristic_score

    return 0.5 * heuristic_score + 0.5 * nn_score


def minimax(board, depth, alpha, beta, maximizing_player):
     # if depth == 0 — agar humne itne moves aage tak soch liya jitna bola gaya tha (depth khatam), to ab aur aage sochna band karo
# or board.is_game_over() — ya agar game hi khatam ho gaya hai (checkmate/draw), to bhi aage sochne ka koi matlab nahi
# In dono cases mein, hum evaluate_board(board) call kar rahe hain — matlab "is final position ko score do" — aur wahi score return kar rahe hain.
    if depth == 0 or board.is_game_over():
        return evaluate_board_hybrid(board)
        
    if maximizing_player:
        max_eval = -float('inf')
        for move in board.legal_moves:
            board.push(move)
            eval = minimax(board, depth - 1, alpha, beta, False)
            board.pop()
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for move in board.legal_moves:
            board.push(move)
            eval = minimax(board, depth - 1, alpha, beta, True)
            board.pop()
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval

def get_best_move(board, depth=3):
    best_move = None
    maximizing_player = board.turn == chess.WHITE
    best_value = -float('inf') if maximizing_player else float('inf')
    
    for move in board.legal_moves:
        board.push(move)
        board_value = minimax(board, depth - 1, -float('inf'), float('inf'), not maximizing_player)
        board.pop()
        
        if maximizing_player:
            if board_value > best_value:
                best_value = board_value
                best_move = move
        else:
            if board_value < best_value:
                best_value = board_value
                best_move = move
                
    if best_move is None and list(board.legal_moves):
        best_move = list(board.legal_moves)[0]
        
    return best_move