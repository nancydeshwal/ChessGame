import chess

print(chess.piece_name
      (chess.PAWN))  # Output: pawn
print(chess.PieceType(chess.KNIGHT))  # Output: 2

piece = chess.Piece(chess.KNIGHT, chess.WHITE)
print(piece.piece_type)  # Output: 2