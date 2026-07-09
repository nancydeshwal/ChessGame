# agar kisi ke system mein speech_recognition library install nahi hai,
# to poora app crash na ho jaaye turant — baad mein jab actually voice feature use hoga tabhi error aayega,
# wo bhi controlled tarike se.
try:
    import speech_recognition as sr
except Exception:
    sr = None


import chess
# re matlab regular expressions. Ye ek tarika hai
# text mein pattern dhundhne ka. Jaise agar tumhe kisi paragraph
# text mein pattern dhundhne ka. Jaise agar tumhe kisi paragraph
# Isme hum use karenge chess move jaisa pattern dhundhne ke
# liye (jaise "e2e4").
import re

# 

def parse_voice_to_move(audio_file_like, board):
    """
    Takes an audio file object, performs speech recognition,
    and returns a valid chess move and the transcribed text.
    """
    if sr is None:
        return None, "speech_recognition not available. Install via: pip install SpeechRecognition"

# speech_recognition library ka ek tool hai jo audio ko sunke text mein badalta hai.
# Isko hum recognizer naam ke variable mein store kar rahe hain, 
# taaki baar baar use kar sakein.

# Socho isko ek "translator machine" jaisa — jisko audio doge, wo text de dega.
    recognizer = sr.Recognizer()
    
    # Ab dubara try block shuru — kyunki audio process karte waqt bahut kuch galat ho sakta hai 
    # (mic kharab, internet nahi, awaaz samajh nahi aayi, etc).
    # Isliye sab kuch try ke andar likha hai.
    try:
        # reset file pointer just in case Streamlit gives it to us at the end of the buffer
    
        # — hasattr check karta hai "kya is object ke paas seek naam ka koi function/feature hai?"
#  File jaise objects mein seek hota hai jo file ke andar ek specific position pe jaane deta hai
# (jaise video mein aage-peeche jaana).
# audio_file_like.seek(0) — agar seek available hai, to file ke bilkul shuruaat (position 0) pe wapas le jao.
        if hasattr(audio_file_like, 'seek'):
            audio_file_like.seek(0)
    # Ye kyun zaroori hai? Kabhi kabhi jab Streamlit audio file deta hai, to uska "pointer" 
    # (reading position) already end mein hota hai — jaise kisi ne poori kitaab padh li ho
    # aur ab tum wahi se aage padhna chaho to kuch nahi milega.
    # Isliye pehle wapas shuru mein le jaate hain taaki poora audio padha ja sake.    #    
    
        with sr.AudioFile(audio_file_like) as source:
            # recognizer.record(source) — poora audio file padh ke ek "audio data" object bana raha hai jisko recognizer samajh sakta hai.
            # Ye audio_data variable mein store ho raha hai.
            # Socho: raw audio file ek unedited video jaisi hai, aur record() uska ek processed clip bana raha hai jisko aage bhejne layak bana diya.
            audio_data = recognizer.record(source)
            # Use Google Speech Recognition API (requires internet, but no key needed for basic usage)
            
            #  ye Google ke Speech Recognition API ko audio bhejta hai, aur wo audio ko sunke text return karta hai. Jaise tumne mic mein bola "e2 to e4",
            # to ye return karega "e2 to e4" (as text).
            # .lower() — text ko sab lowercase (chote letters) mein convert kar raha hai. 
            # Jaise agar text "E2 To E4" aaya, to ye "e2 to e4" bana dega. Isliye baad mein comparison karte waqt case ka issue nahi aayega.
            # use getattr to avoid static-analysis issues complaining about
            # unknown attribute on Recognizer while still calling the method.
            recognizer_recognize = getattr(recognizer, "recognize_google")
            text = recognizer_recognize(audio_data).lower()
            
            # Ab ye recognized text ko chess move mein convert karne ke liye ek doosra function call kar raha hai 
            # — match_move_to_board (jo neeche define hai). Usko text aur board dono de rahe hain, 
            # aur wo return karega actual chess move.
            move = match_move_to_board(text, board)
            return move, text
        
        # sr.UnknownValueError — ye specific error hai jab Google Speech API awaaz sunn hi nahi paaya ya samajh nahi paaya
        # (jaise khamoshi thi, ya bahut shor tha).
        # aur ek friendly message user ko batane ke liye.
    except sr.UnknownValueError:
        return None, "Silence or unclear audio detected. Please try speaking closer to the mic, like 'Move pawn to e4'."
    
        #  ye tab aata hai jab Google ke server tak connect hi nahi ho paaya (internet issue, ya API down hai).
    except sr.RequestError as e:
        return None, f"Google Speech API error (check your internet): {e}"
    
    #  ye generic Python error hai jab koi value expected format mein nahi hoti.
    # Yahan iska matlab hai audio file ka format kharab tha ya empty tha.
    except ValueError as e:
        return None, f"Audio format error (Browser might have sent an empty or unsupported format): {e}"
    except Exception as e:
        return None, f"Error: {e}"

# Naya function shuru — is baar text (jo bola gaya) aur board (current position) lekar, 
# actual valid chess move dhundhega.
def match_move_to_board(text, board):
    """
    Attempts to extract a valid chess move from transcribed text.
    Supports basic UCI formatted speech like 'e2 to e4' or 'knight to f3'.
    """
    # Clean padding words
    cleaned_text = text.replace(" to ", "").replace(" ", "").replace("-", "")
    
    # Check naive UCI match exactly
    for move in board.legal_moves:
        if move.uci() in cleaned_text:# har move ka UCI notation nikal rahe hain, 
            return move
            
    # Check naive SAN match
    for move in board.legal_moves:
        san = board.san(move).lower()
        if san in text:
            return move
            
    # Regex extraction for patterns like "e2e4"
    matches = re.findall(r'[a-h][1-8][a-h][1-8]', cleaned_text)
    if matches:
        proposed_uci = matches[0]
        for move in board.legal_moves:
            if move.uci() == proposed_uci:
                return move
                
    return None

# parse_voice_to_move — Audio leta hai → Google se text banata hai → us text ko match_move_to_board ko bhejta hai → move aur text dono return karta hai. 
# Errors ko gracefully handle karta hai.
# match_move_to_board — Text ko 3 tarike se try karta hai match karne ke:
# (1) UCI format check,
# (2) SAN format check,
# (3) Regex se pattern nikaal ke check. Jo bhi pehle match ho jaaye wahi return.

# Audio file aayi
    #   ↓
# Bookmark reset karo (seek 0)
#       ↓
# Audio ko AudioFile format mein convert karo
#       ↓
# Poora audio record/read karo
#       ↓
# Google API ko bhejo → text milta hai
#       ↓
# Text ko lowercase karo
#       ↓
# match_move_to_board() call karo → chess move milta hai (ya None)
#       ↓
# (move, text) return karo
      
#  ⚠️ Agar kahin bhi error aaya:
#  → specific error message ke saath (None, error_msg) return karo