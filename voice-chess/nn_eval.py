"""
Neural Network based board evaluation.

Instead of only using hand-coded piece values (like in engine.py's
evaluate_board), this module loads a small trained Neural Network
(a Multi-Layer Perceptron) that has LEARNED to score chess positions
from example data.

Run train_nn.py once before playing to create the trained model file
(chess_nn_model.pkl). If the model file is missing, evaluate_board_nn()
simply returns None, and engine.py will fall back to the pure heuristic
so the app never crashes.
"""
import os
import chess
import numpy as np
from typing import Optional
# joblib — ek library hai jo trained ML models ko save/load karne ke liye use hoti hai
# (jaise humne train_nn.py mein joblib.dump() se model save kiya tha)
try:
    import joblib
except ImportError:
    joblib = None

# __file__ — Python mein ye ek special built-in variable hai jo automatically batata hai current file ka path (matlab nn_eval.py khud kaha stored hai, disk pe)
# os.path.dirname(__file__) — dirname function file ke path se sirf folder ka path nikal leta hai (file ka naam hata ke). 
# Jaise agar __file__ = /home/nancy/voice-chess-xai/nn_eval.py, to os.path.dirname(__file__) = /home/nancy/voice-chess-xai
# os.path.join(folder_path, "chess_nn_model.pkl") — os.path.join() do parts ko sahi tarike se jodta hai ek valid file path banane ke liye
# (Windows aur Mac/Linux mein path likhne ka tarika thoda alag hota hai — \ vs / — ye function automatically sahi wala use karta hai)
MODEL_PATH = os.path.join(os.path.dirname(__file__), "chess_nn_model.pkl")

# Same 4 center squares used in engine.py and explain.py (d4, e4, d5, e5)
CENTER_SQUARES = [27, 28, 35, 36]

_model = None   # ya trained model store honga
_model_loaded = False  # kya humne mdel already load kr liya hai ???

# Caching kya hoti hai? Socho tumhe baar baar ek bhaari kitaab (trained model file, jo disk pe MBs ki ho sakti hai) padhni padti hai
# . Agar tum har baar jab bhi kisi cheez ki zaroorat ho, poori kitaab wapas se load karo (disk se padho), to bahut time waste hoga.
# Isliye ek smart tarika hai: "kitaab ko ek baar padho, memory mein rakh lo, aur agli baar jab zaroorat ho to seedha memory se le lo — dobara disk se mat padho." 
# Isi ko caching bolte hain.

def _load_model(): # underscore se suru mtlb y einternal use k liye hai 
    """Loads the trained model from disk only once, then reuses it (caching)."""
    #  global keyword bolta hai: "Nahi, main jis _model aur _model_loaded ki baat kar rahi hoon, wo file ke bahar wale (module-level) variables hain — unko hi update karna hai,
    # koi naya local variable nahi banana.
    global _model, _model_loaded
    if not _model_loaded:
        if joblib is not None and os.path.exists(MODEL_PATH):
            _model = joblib.load(MODEL_PATH)
        else:
            _model = None
        _model_loaded = True
    return _model


def extract_features(board):
    """
    Converts a chess board into a fixed-size list of numbers (a "feature vector")
    that the neural network can understand. Neural networks can't read a
    chess board directly -- they only understand numbers.

    Features used (12 total, kept simple on purpose):
      - Count of White's Pawns, Knights, Bishops, Rooks, Queens (5 numbers)
      - Count of Black's Pawns, Knights, Bishops, Rooks, Queens (5 numbers)
      - Number of White pieces occupying the center squares (1 number)
      - Number of Black pieces occupying the center squares (1 number)
    """
    piece_types = [chess.PAWN, chess.KNIGHT, chess.BISHOP, chess.ROOK, chess.QUEEN]
    features = []

    for color in [chess.WHITE, chess.BLACK]:
        for piece_type in piece_types:
            count = len(board.pieces(piece_type, color))
            features.append(count)

    white_center = sum(
        1 for sq in CENTER_SQUARES
        if board.piece_at(sq) and board.piece_at(sq).color == chess.WHITE
    )
    black_center = sum(
        1 for sq in CENTER_SQUARES
        if board.piece_at(sq) and board.piece_at(sq).color == chess.BLACK
    )
    features.append(white_center)
    features.append(black_center)

    return features


def evaluate_board_nn(board) -> Optional[float]:
    """
    Returns a board evaluation score predicted by the trained Neural Network.
    Returns None if no trained model is available yet (caller should then
    fall back to the classic heuristic in engine.py).
    """
    model = _load_model()
    if model is None:
        return None

    features = np.array(extract_features(board)).reshape(1, -1) # Doosra number -1 — ye sabse interesting part hai. -1 ka matlab hai: "Tum khud calculate kar lo kitne columns chahiye, mujhe manually count nahi karna."
    predicted_score = model.predict(features)[0]
    return float(predicted_score)

# Feature Engineering — hum poore 64-square board ko NN ko directly nahi de rahe,
# balki 12 meaningful numbers (features) nikaal rahe hain jo chess ki strategy ko represent karte hain (material count + center control). 
# Ye technique "Feature Engineering" kehlaati hai ML mein.

# Caching for Performance — model ko baar baar disk se load nahi kar rahe har move pe (jo slow hota),
# balki ek baar load karke memory mein rakh rahe hain — ye performance optimization hai.

# Graceful Degradation — agar NN available na ho (model train nahi hua, ya library missing hai), 
# poora app crash nahi hota, bas simple heuristic pe wapas chala jaata hai — ye robust software design ka example hai.