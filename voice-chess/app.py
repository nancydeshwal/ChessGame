# Streamlit library import kar rahe hain (jisse web app UI banta hai),
# st naam se bulayenge
import streamlit as st
import chess
import chess.svg  #  scalable vector graphics  chess library ka ek extra part jo board ko image (SVG) format mein banane mein madad karta hai 
import base64 #  ye ek tarika hai images/files ko text format mein convert karne ka
from engine import get_best_move
from explain import explain_move
from voice import parse_voice_to_move
import io

# st.set_page_config() — Streamlit ko batate hain page ki basic settings kya honi chahiye:
# page_title="..." — browser tab mein jo title dikhega
# layout="wide" — page ko poori width use karne do (normal se zyada chaudi screen)
# initial_sidebar_state="expanded" — sidebar (left wala panel) shuru mein khula hua dikhe
st.set_page_config(page_title="Voice-Controlled XAI Chess", layout="wide", initial_sidebar_state="expanded")

def render_board(board):
    """Render the chess board as an SVG image."""
    # chess.svg.board(board=board, size=450) — ye chess.svg module (jo humne import kiya tha) ka function hai
    # Iska kaam hai: current board position ko dekh ke, ek SVG image bana do
    # ye ek image format hai jo text/code ke roop mein likha hota hai, lekin browser usko ek image ki tarah render kar sakta hai.
    # Jaise normal image (jpg/png) pixels ka hota hai, SVG shapes aur lines ke instructions se bana hota hai (isliye zoom karne pe bhi blur nahi hota)
    # Socho isko aise — chess.svg.board() function ek "artist" hai jo current board dekh ke ek drawing (as text/code) bana deta hai —
    # jaise "yahan pe White Knight banao, wahan Black Queen banao" jaisi instructions.
    boardsvg = chess.svg.board(board=board, size=450)
#    base 64 kyu chahiye 
   # Web browsers mein images dikhane ka normal tarika hai — ek file ka path/link dena, jaise <img src="chess_board.png">. Lekin humare paas koi actual file nahi hai save ki hui — humare paas sirf ek SVG text (code) hai jo abhi-abhi generate hua hai memory mein.
# Base64 encoding ek tarika hai kisi bhi data (image, text, kuch bhi) ko ek lambi string of characters mein convert karne ka, jisko hum seedha HTML ke andar directly embed kar sakte hain — bina koi alag file banaye.

# boardsvg.encode('utf-8') — pehle humara SVG text (jo abhi normal string hai) ko bytes mein convert kar rahe hain. Computers text ko "bytes" (0s aur 1s ka group) mein hi samajhte hain internally, utf-8 ek standard tarika hai text ko bytes mein convert karne ka.
# base64.b64encode(...) — un bytes ko Base64 format mein convert kar rahe hain — ye ek lambi string ban jaati hai jisme sirf letters, numbers, aur +, /, = jaise characters hote hain (koi bhi weird symbol nahi)
# .decode('utf-8') — jo result mila (wo bhi bytes format mein hota hai), usko wapas normal readable string mein convert kar rahe hain, taaki HTML mein use kar sakein
    b64 = base64.b64encode(boardsvg.encode('utf-8')).decode('utf-8')
# <img src="data:image/svg+xml;base64,{b64}"> — ye actual image tag hai

# Normally src="kuch_file.png" hota hai (file ka path)
# Lekin yahan src="data:image/svg+xml;base64,..." likha hai — ye ek special tarika hai HTML mein directly image data embed karne ka, bina koi separate file use kiye. Isko Data URI bolte hain.
# image/svg+xml batata hai ye SVG type ki image hai
# base64,{b64} — yahan humari wo lambi encoded string aa jaati hai jo humne upar banayi th
    html = f'<div style="display: flex; justify-content: center;"><img src="data:image/svg+xml;base64,{b64}"></div>'
# st.markdown(...) — Streamlit ka function hai jo Markdown ya HTML content ko screen pe display karta hai
# html — humara bana hua HTML code pass kar rahe hain
# unsafe_allow_html=True — ye zaroori hai! Normally Streamlit security ke liye raw HTML ko allow nahi karta (kyunki HTML se malicious code bhi aa sakta hai) — isliye default mein ye disabled hota hai. Lekin humein apna custom HTML (image wala) dikhana hai, isliye explicitly bolna padta hai "haan, HTML allow karo" — is parameter ko True karke.
    st.markdown(html, unsafe_allow_html=True)
    
# "Board ko SVG format mein generate karta hoon python-chess library se, fir usko Base64 encoding use karke ek Data URI mein convert karta hoon, taaki Streamlit ke andar bina kisi separate image file save kiye directly HTML mein embed karke dikha sakoon."
# Ye ek common technique hai web development mein jab tumhe dynamically generated images (jo runtime pe banti hain, disk pe save nahi hoti) ko browser mein dikhana ho.

# Streamlit ka sabse bada "quirk" (ajeeb cheez) ye hai: Jab bhi tum page pe kuch bhi karte ho — button click karo, koi text likho, koi bhi interaction karo — Streamlit poori Python file ko ek dam se upar se neeche phir se run kar deta hai!
# Socho ye jaise — tumne ek program likha hai jo har baar jab tum keyboard pe kuch bhi press karo, poora program restart ho jaata hai from line 1.
# Ab isme problem kya hai? Agar poora script baar baar restart hota hai, to normal Python variables har baar reset ho jaayenge. Jaise agar tumne likha:
# pythonboard = chess.Board()
# To har interaction pe ye line phir se chalegi, aur board hamesha naya (fresh) ban jaayega — matlab tumhara game kabhi progress hi nahi karega, har click pe wapas shuruaat mein chala jaayega!
# Iska solution hai st.session_state — ye ek special storage hai jo Streamlit deta hai, jisme rakha hua data script restart hone ke baad bhi bacha rehta hai (jab tak browser tab band na ho ya naya session start na ho).
# Socho isko jaise — tumhare ghar mein ek locker hai jo kabhi khali nahi hota, chahe ghar ke baaki saman rearrange ho jaaye. Session state waisa hi locker hai jahan important data safe rehta hai.

# Initialize Session State
# st.session_state — ye ek dictionary jaisi cheez hai (yaad hai humne engine.py mein dictionary dekhi thi — key-value pairs) jisme Streamlit data store karta hai
# 'board' not in st.session_state — check kar rahe hain: "kya 'board' naam ki koi cheez already is storage mein maujood hai?"
# not in — matlab agar 'board' maujood nahi hai (abhi tak store nahi hua), to condition True hogi
if 'board' not in st.session_state:
    st.session_state.board = chess.Board()
if 'logs' not in st.session_state:
    st.session_state.logs = []
# Bilkul same logic — check karo kya 'logs' (game ke moves ki history/list) already store hai
# Agar nahi, to ek khaali list [] bana ke store kar do — ye list aage move history aur AI ke reasoning entries store karegi
# "Streamlit ek reactive framework hai jo har user interaction pe poori script re-run karta hai.
# Agar main normal Python variables use karti, to game state (board position, move history) har interaction pe reset ho jaata. session_state Streamlit ka mechanism hai jisse data persist (bacha rahe) kar sakein multiple re-runs ke beech,
# jab tak session active hai."

# Sidebar for settings
with st.sidebar:
    st.title("⚙️ Settings")
    
    # st.markdown(...) — normal text/description dikhane ke liye (Markdown format support karta hai, jaise bold, italic waghera bhi likh sakte ho isme)
# Ye sirf ek helper text hai user ko batane ke liye ki sidebar mein kya hai
    st.markdown("Adjust AI configurations here.")
    depth = st.slider("AI Search Depth (Minimax)", min_value=1, max_value=4, value=3) # value means default value 
    
    # type="primary" — button ko ek highlighted/colored style deta hai (taaki important button dikhe alag se)
    if st.button("New Game", type="primary"):
        st.session_state.board = chess.Board()
        st.session_state.logs = []
        st.rerun()
        
    # "Sidebar mein main do controls hain — ek slider jo AI ki search depth control karta hai (jitni zyada depth, utna behtar lekin slow AI), aur ek button jo poore game ko reset kar deta hai. Dono session_state ko modify karte hain taaki changes persist ho sakein."
    
    
st.title("🎙️ Voice-Controlled Explainable Chess AI")
st.markdown("Play hands-free chess! The AI uses Minimax optimization and explains the reasoning behind each move.")
col1, col2 = st.columns([1.2, 1])
with col1:
    st.subheader("Chess Board")
    render_board(st.session_state.board)
    
    #  ek red colored error box dikhata hai Streamlit mein (visually alert jaisa lagta hai)
    if st.session_state.board.is_game_over():
        st.error(f"Game Over! Result: {st.session_state.board.result()}")
with col2:
    st.subheader("Controls")
    
    tabs = st.tabs(["🗣️ Voice Command", "⌨️ Manual Entry"])
    
    with tabs[0]:
        st.markdown("**Speak your move (e.g., 'e2 to e4' or 'knight to f3')**")
        audio_val = st.audio_input("Record Move")
        if audio_val and st.session_state.board.turn == chess.WHITE and not st.session_state.board.is_game_over():
            with st.spinner("Processing voice command..."):
                # Pass file-like object to voice handler
                move, text = parse_voice_to_move(audio_val, st.session_state.board)
                if move:
                    # st.success(...) — ek green colored success message dikhao,
                    st.success(f"Recognized: '{text}' -> Interpreted as {move.uci()}")
                    explanation = explain_move(st.session_state.board, move)
                    st.session_state.board.push(move)
                    st.session_state.logs.append(f"👨‍🦱 **Human (Voice):** {move.uci()} \n\n*Reasoning:* {explanation}")
                    st.rerun()
                else:
                    st.warning(f"Could not interpret a valid move. Transcribed speech: '{text}'")
                    
    with tabs[1]:
        manual_move = st.text_input("Enter Move (e.g., e4, Nf3, or e2e4):")
        if st.button("Submit Manual Move") and st.session_state.board.turn == chess.WHITE and not st.session_state.board.is_game_over():
            parsed_move = None
            try:
                # Try parsing as standard algebraic notation (SAN) first, e.g. "e4", "Nf3"
                parsed_move = st.session_state.board.parse_san(manual_move)
            except ValueError:
                try:
                    # Fallback to pure coordinate notation / UCI e.g. "e2e4", "f2f4"
                    parsed_move = chess.Move.from_uci(manual_move)
                except ValueError:
                    pass
            
            if parsed_move and parsed_move in st.session_state.board.legal_moves:
                explanation = explain_move(st.session_state.board, parsed_move)
                st.session_state.board.push(parsed_move)
                st.session_state.logs.append(f"👨‍🦱 **Human:** {parsed_move.uci()} \n\n*Reasoning:* {explanation}")
                st.rerun()
            elif parsed_move:
                st.error("Illegal Move")
            else:
                st.error("Invalid Format. Please use standard chess notation (e.g., 'e4', 'Nf3') or UCI ('e2e4').")
    st.divider()  #ek horizontal line dikhata hai (visual separator)
    st.subheader("Explainable AI (XAI) Logs")
    
    # Render XAI logs in a scrollable container
    log_container = st.container(height=350)
    with log_container:
        for log in reversed(st.session_state.logs):
            st.info(log) #  har log entry ko ek blue colored info box mein dikhao
            
# AI Turn Execution
if st.session_state.board.turn == chess.BLACK and not st.session_state.board.is_game_over():
    with st.spinner("AI Engine is thinking..."):
        best_move = get_best_move(st.session_state.board, depth=depth)
        if best_move: 
            explanation = explain_move(st.session_state.board, best_move)
            st.session_state.board.push(best_move)
            st.session_state.logs.append(f"🤖 **AI Engine:** {best_move.uci()} \n\n*XAI Reasoning:* {explanation}")
            st.rerun()
