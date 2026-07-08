
"""
train_nn.py -- Trains the chess Neural Network evaluator.

Run this once before playing:
    python train_nn.py
"""
import os
import chess
import numpy as np
import pandas as pd
from sklearn.neural_network import MLPRegressor # multiple layer perceptron regressor (MLP) — ek type ka neural network hai jo regression tasks ke liye use hota hai. 
# Hum isse chess board positions ko evaluate karne ke liye train karenge.

try:
    import joblib
except ImportError:
    raise SystemExit("joblib is not installed. Run: pip install joblib scikit-learn pandas")


from nn_eval import extract_features, MODEL_PATH


KAGGLE_CSV_PATH = "fen_analysis.csv"
MAX_ROWS_FROM_CSV = 20000  # keep training fast; raise this if  machine can handle more

MATE_SCORE = 3000  # centipawn value assigned to "mate in N" rows (a very large score)


def _parse_evaluation(raw_value): # raw_value csv se aayi hui direct value
    """
   Kaggle CSV mein evaluation column mein do tarah ki values ho sakti hain:

1. Normal number: "56", "-134" (centipawns — chess ka standard unit hai, 
        100 centipawns = 1 pawn ki value)
2. Mate notation: "#3" (matlab "White checkmate karega 3 moves mein"),
                    "#-2" (matlab "Black checkmate karega 2 moves mein")
    """
    # chahe input number ho ya text, isko forcefully string mein convert kar rahe hain (safety ke liye, taaki aage ke operations consistent rahein)
    value = str(raw_value).strip() # strip means space hata do starting and end se
    if value.startswith("#"):
        sign = -1 if value.startswith("#-") else 1
        return sign * MATE_SCORE
    try: # if any weird value aa jaye jo number mein convert na ho, to except block handle karega
        return float(value)
    except ValueError:
        return None


def load_kaggle_data(csv_path, max_rows=MAX_ROWS_FROM_CSV):
    """
    Loads and preprocesses the Kaggle chess-evaluations CSV.
    """
    print(f"Loading real chess data from '{csv_path}' ...")
    df = pd.read_csv(csv_path, nrows=max_rows)

    fen_col = "FEN" 
    score_col = "Analysis"
    
    # X have features (input to neural network), y have target scores (output of neural network)
    X, y = [], []
    for _, row in df.iterrows(): # df.iterrows() — pandas ka function hai jo DataFrame ki har row ko ek-ek karke deta hai (loop ke through) its returns two things row data and row index row index storing in _
        score = _parse_evaluation(row[score_col])
        if score is None:
            continue
        # chess.Board() ek FEN string bhi le sakta hai input mein, aur us exact position se ek board bana deta hai — matlab kisi bhi "beech game ki" position ko recreate kar sakta hai
        try:
            board = chess.Board(row[fen_col])
        except ValueError:
            continue  # skip any malformed FEN rows

# extract_features(board) — yaad hai nn_eval.py ka function, jo board ko 12 numbers mein convert karta hai — result X list mein add kar diya
        X.append(extract_features(board))
        y.append(score)
# Har valid row ke liye, hum do jodi cheeze bana rahe hain — "ye board hai (features)" aur "iska sahi score ye hai (label)" — ye jode hi actually training data banate hain.
    print(f"  -> Loaded {len(X)} usable positions from the Kaggle dataset.")
    return np.array(X), np.array(y)



def main():
    if not os.path.exists(KAGGLE_CSV_PATH):
        raise SystemExit(
            f"Could not find '{KAGGLE_CSV_PATH}' in this folder.\n"
            "Download a chess evaluations CSV from Kaggle, place it here, "
            "and update KAGGLE_CSV_PATH at the top of train_nn.py to match its filename."
        )
        
    print("Step 1/3: Preparing training data...")
    
   
    X, y = load_kaggle_data(KAGGLE_CSV_PATH)
  
    print(f"Step 2/3: Training the Neural Network on {len(X)} positions...")
    model = MLPRegressor(
        hidden_layer_sizes=(32, 16), #  NN ki do hidden layers hain: pehli mein 32 neurons, doosri mein 16 neurons
# Neurons/Layers
        activation="relu",
        max_iter=2000,
        random_state=42,
    )
    model.fit(X, y)

    print("Step 3/3: Saving trained model to disk...")
    joblib.dump(model, MODEL_PATH)
    print(f"Done! Model saved as: {MODEL_PATH}")
    print("You can now run the Streamlit app -- the AI will use the trained network.")


if __name__ == "__main__":
    main()