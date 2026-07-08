import chess

# Kyun "before" ka board chahiye? 
# Kyunki hume pata karna hai "move khelne se pehle wahan kya tha" —
# jaise agar capture ho raha hai, to hume pata karna hoga target square pe pehle kaunsa piece tha (jo ab capture ho jaayega).
def explain_move(board_before, move):
    """
    Generates a human-readable explanation for a given chess move.
    """
    
    """move.from_square — move ka ek property hai jo batata hai piece kahan se chal raha hai
    (jaise agar move "e2e4" hai, to from_square = e2)
board_before.piece_at(move.from_square) — us square pe (move khelne se pehle) kaunsa piece tha, 
wo nikaal rahe hain piece variable mein store ho gaya

    """
    piece = board_before.piece_at(move.from_square)
    if not piece:
        return "Unknown move reason."
        
    captured_piece = board_before.piece_at(move.to_square)
    is_castling = board_before.is_castling(move) # board_before.is_castling(move) — chess library ka function hai jo check karta hai "kya ye move castling hai?" 
    #(castling = King aur Rook ek special move mein position swap karte hain safety ke liye)
    """is_en_passant check kar raha hai kya ye move en passant hai — 
    ye chess ka ek special rule hai jab pawn diagonally capture karta hai ek special situation mein

 
    """
    is_en_passant = board_before.is_en_passant(move)
    
    explanation = []
    
    """
    .join() samjho: " ".join(list) ka matlab hai "list ke saare items ko jodo,
    beech mein ek space laga ke, aur ek single string bana do."
Jaise agar explanation = ["Hello", "World"], to " ".join(explanation) = "Hello World".
 
    """
    # 1. Castling
    if is_castling:
        explanation.append("The King castles to improve its safety and connect the Rooks.")
        return " ".join(explanation)
        
    # 2. Capture analysis
    if captured_piece:
        explanation.append(f"This move captures the opponent's {chess.piece_name(captured_piece.piece_type)}.")
    elif is_en_passant:
        explanation.append("This is an en passant capture, removing the opponent's pawn.")
        
    # 3. Check analysis
    board_after = board_before.copy()
    board_after.push(move)
    if board_after.is_checkmate():
        explanation.append("This is a checkmate move, winning the game!")
    elif board_after.is_check():
        explanation.append("The move puts the opponent's King in check, forcing a reaction.")
        
    # 4. Positional / Development
    if piece.piece_type in [chess.KNIGHT, chess.BISHOP] and chess.square_rank(move.from_square) in [0, 7]:
        explanation.append("It develops a minor piece from its starting square, increasing board influence.")
        
    # 5. Central control
    if move.to_square in [27, 28, 35, 36]: # e4, d4, e5, d5 squares
        explanation.append("The piece occupies the center, fighting for control of key squares.")
        
 # piece.piece_type evaluate hota hai
# Maan lo piece ek Knight hai
# Toh piece.piece_type = 2
        #Ye ek helper function hai jo chess library deti hai, jiska kaam hai: "Mujhe piece ka number do, main tumhe uska readable naam de dunga."
    if not explanation:
        explanation.append(f"The {chess.piece_name(piece.piece_type)} moves to a new square to improve its positional coordination.")
        #  piece have piece.color and piece.piece_type
    return " ".join(explanation)

    """
    Move aur board_before milta hai function ko
        ↓
Piece nikalo jo move kar raha hai (from_square se)
        ↓
Check karo: Castling hai kya? → Agar haan, turant explanation de do, ruk jao
        ↓
Check karo: Capture ho raha hai? Ya En Passant hai? → Sentence jodo
        ↓
Move khel ke dekho (copy pe) → Check/Checkmate hua kya? → Sentence jodo
        ↓
Check karo: Piece development ho raha hai? (Knight/Bishop starting row se) → Sentence jodo
        ↓
Check karo: Center square pe ja raha hai? → Sentence jodo
        ↓
Agar kuch bhi match nahi hua → Generic fallback sentence do
        ↓
Sare sentences ko jodo (space se) → Final explanation return karo
    """
