# Voice Controlled Chess Engine using Search Optimization and Neural Network

A chess application where you can play against an AI opponent using your voice or by typing moves. After every move the AI makes, it also explains in plain English why it chose that move. Built as our semester project.


## What This Project Does

We built a chess app where:
- You can speak your move out loud (like "e2 to e4") and it gets converted to an actual chess move
- You can also just type the move if voice doesn't work for some reason
- The AI opponent plays using Minimax with Alpha-Beta Pruning, which is a classic game-tree search algorithm
- On top of that, we trained a small Neural Network on real chess evaluation data (from Kaggle) so the AI's evaluation of a position isn't purely based on hand-coded rules
- After every move (yours and the AI's), the app explains the reasoning behind it - this is the "Explainable AI" part of the project

Basically the project tries to combine three things that are usually taught separately in our syllabus: search algorithms, a bit of machine learning, and explainability.

## Why We Built It This Way

Most basic chess engine projects online just use Minimax with a hardcoded evaluation function (Pawn = 1, Queen = 9, etc). We wanted to go a step further and see if we could make the evaluation function actually "learn" from data instead of us manually deciding piece values. That's where the Neural Network part came in.

We also didn't want the AI to be a black box, so the explanation module was added so that every move has a reason attached to it, not just a raw score.

## Tech Stack

| Part | What we used |
|---|---|
| UI | Streamlit |
| Chess rules/logic | python-chess |
| Voice input | SpeechRecognition (Google Speech API) |
| Search Algorithm | Minimax + Alpha-Beta Pruning (written from scratch) |
| Neural Network | scikit-learn MLPRegressor |
| Training Data | Kaggle chess evaluations dataset (FEN + Stockfish evaluation scores) |

## Project Structure

```
voice-chess-xai/
│
├── app.py              # Streamlit UI, session state, game loop
├── engine.py            # Minimax + Alpha-Beta search, hybrid evaluation
├── explain.py            # Generates human-readable reasoning for each move
├── voice.py             # Converts recorded speech into a chess move
├── nn_eval.py            # Loads the trained neural network, extracts board features
├── train_nn.py            # One-time script to train the neural network on Kaggle data
├── requirements.txt
└── chess_nn_model.pkl      # generated after running train_nn.py (not in repo)
```

## How the AI Actually Decides a Move

This part confused us a lot in the beginning so we're explaining it properly here (and this is basically what we'll tell the professor too):

1. When it's the AI's turn, `get_best_move()` in `engine.py` is called
2. It tries every legal move, and for each one, calls `minimax()` to simulate several moves ahead (how far ahead depends on the depth slider in the sidebar)
3. Alpha-Beta pruning is used so the algorithm doesn't waste time exploring branches that can't possibly affect the final decision - this is the "Search Optimization" in the title
4. When the search reaches its depth limit, the position needs to be scored somehow. Instead of using only our hand-written heuristic (based on standard piece values + center control), we average it with a prediction from our trained Neural Network - this is `evaluate_board_hybrid()` in engine.py
5. Whichever move leads to the best score for the AI is played

If the neural network model hasn't been trained yet (i.e `train_nn.py` wasn't run), the app doesn't crash - it just falls back to using only the hand-coded heuristic. We did this on purpose so the project still works even in a fresh setup.

## The Neural Network Part

We trained a small MLP (Multi-Layer Perceptron, 2 hidden layers) using scikit-learn. Instead of generating our own training data, we used a real dataset from Kaggle that has thousands of chess positions (in FEN notation) along with their Stockfish evaluation scores. 

For each position we extract 12 simple features - count of each piece type for White and Black, plus how many pieces are occupying the 4 center squares - and train the network to predict the evaluation score from these features. This model is saved as `chess_nn_model.pkl` and loaded during actual gameplay.

We kept the feature set small on purpose. We did try to keep this as simple as we reasonably could given the time we had, since the main focus of the project was still search + explainability, and the NN was more of an add-on to make the evaluation function smarter.

## The XAI (Explainable AI) Part

After every move, `explain.py` checks a few things about the move - was it a capture, does it put the opponent in check, is it developing a piece, is it moving into the center, etc - and generates a plain-English sentence explaining it. This is rule-based, not something the neural network is doing, so it's fully deterministic and easy to explain to anyone looking at the code.

## How to Run It

```bash
# clone/download the project, then inside the folder:
pip install -r requirements.txt

# (optional but recommended) train the neural network first
# 1. download a chess evaluations CSV from Kaggle, e.g:
#    https://www.kaggle.com/datasets/ffatty/350k-chess-positions-analyzed
# 2. put the CSV in this folder
# 3. update KAGGLE_CSV_PATH in train_nn.py to match the filename
python train_nn.py

# then run the app
streamlit run app.py
```

The app opens at `http://localhost:8501`. Allow microphone access if you want to use the voice input.

## Known Limitations

Being upfront about this since we know it'll probably come up in questions:

- The neural network's evaluation is only as good as the small feature set we extracted - it doesn't see the full board, just piece counts and center occupation
- Voice recognition depends on internet access since it uses Google's Speech API
- Search depth is capped at 4 in the UI because deeper search gets noticeably slow (Minimax complexity grows exponentially with depth even with pruning)
- We only tested this on a normal laptop, not on anything with a GPU, so training is deliberately kept lightweight

## What We'd Do With More Time

- Use a bigger/more complete feature set for the neural network (maybe encode the full board instead of just counts)
- Add an option to play as Black too, right now White is always the human player
- Store game history so you can review past games
- Try a slightly bigger Kaggle dataset once we're sure the pipeline works correctly on the smaller one

## Credits

- Chess evaluation training data: Kaggle (chess positions + Stockfish evaluations dataset)
- python-chess library for board representation and move generation
- SpeechRecognition + Google Speech API for voice-to-text
