import streamlit as st
import random
import time
import sqlite3
from threading import Thread
from playsound import playsound

# --------- DB SETUP ---------
conn = sqlite3.connect('typing_leaderboard.db', check_same_thread=False)
c = conn.cursor()
c.execute('''
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        streak INTEGER DEFAULT 0
    )
''')
c.execute('''
    CREATE TABLE IF NOT EXISTS scores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        wpm REAL,
        accuracy REAL,
        time_taken REAL,
        difficulty TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
''')
conn.commit()

# --------- Sound play in thread ---------
def play_sound_thread(sound_file):
    def play():
        playsound(sound_file)
    Thread(target=play, daemon=True).start()

# --------- Load CSS ---------
def load_css(theme):
    css_file = "style_light.css" if theme == "Light" else "style_dark.css"
    with open(css_file) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# --------- Load passages based on difficulty ---------
def load_passages(difficulty):
    filename = {
        "Easy": "easy.txt",
        "Medium": "medium.txt",
        "Hard": "hard.txt"
    }[difficulty]
    with open(filename, encoding="utf-8") as f:
        passages = [p.strip() for p in f.readlines() if p.strip()]
    return passages

# --------- Calculate speed, accuracy ---------
def calculate_speed(start_time, end_time, passage, user_input):
    elapsed_time = end_time - start_time
    words = len(user_input.split())
    speed_wpm = words / (elapsed_time / 60) if elapsed_time > 0 else 0
    correct_chars = sum(1 for a, b in zip(passage, user_input) if a == b)
    accuracy = (correct_chars / len(passage) * 100) if passage else 0
    return speed_wpm, accuracy, elapsed_time

# --------- Badges logic ---------
def get_badge(wpm, accuracy):
    if wpm > 80 and accuracy > 95:
        return "🚀 Speedster & Precision Master"
    if wpm > 80:
        return "🚀 Speedster"
    if accuracy > 95:
        return "🎯 Precision Master"
    if wpm > 50:
        return "🔥 Fast Typist"
    if accuracy > 80:
        return "✅ Accurate Typist"
    return "📝 Beginner"

# --------- Update leaderboard ---------
def save_score(username, wpm, accuracy, time_taken, difficulty):
    c.execute("INSERT INTO scores (username, wpm, accuracy, time_taken, difficulty) VALUES (?, ?, ?, ?, ?)",
              (username, wpm, accuracy, time_taken, difficulty))
    conn.commit()

def get_leaderboard(difficulty):
    c.execute("""
        SELECT username, MAX(wpm) as max_wpm, MAX(accuracy) as max_accuracy
        FROM scores WHERE difficulty = ? 
        GROUP BY username ORDER BY max_wpm DESC LIMIT 10
    """, (difficulty,))
    return c.fetchall()

# --------- Prevent copy paste JS ---------
NO_COPY_PASTE_JS = """
<script>
const textarea = window.parent.document.querySelector('textarea[aria-label="Your Text"]');
if(textarea){
    textarea.onpaste = (e) => e.preventDefault();
}
</script>
"""

# --------- Main app ---------
def main():
    st.set_page_config(page_title="Typing Speed Tester", page_icon="⌨️", layout="wide")
    
    # Sidebar - Login
    st.sidebar.title("Login / User")
    if "username" not in st.session_state:
        username = st.sidebar.text_input("Enter your username")
        if st.sidebar.button("Login"):
            if username.strip():
                st.session_state.username = username.strip()
                # Create user in DB if not exist
                c.execute("INSERT OR IGNORE INTO users (username) VALUES (?)", (st.session_state.username,))
                conn.commit()
                st.sidebar.success(f"Logged in as {st.session_state.username}")
            else:
                st.sidebar.error("Username cannot be empty")
        st.stop()
    else:
        st.sidebar.write(f"Logged in as: **{st.session_state.username}**")
        if st.sidebar.button("Logout"):
            del st.session_state.username
            st.experimental_rerun()

    # Theme
    theme = st.sidebar.radio("🎨 Choose Theme:", ("Light", "Dark"))
    load_css(theme)

    # Difficulty level
    difficulty = st.sidebar.selectbox("Select Difficulty Level", ["Easy", "Medium", "Hard"])
    
    st.markdown("<h1 class='title'>AccuType</h1>", unsafe_allow_html=True)
    st.markdown("<h2 class='title'>⌨️ Typing Speed Tester</h2>", unsafe_allow_html=True)
    st.divider()
    
    passages = load_passages(difficulty)
    
    # Initialize session states
    if "passage" not in st.session_state or st.session_state.difficulty != difficulty:
        st.session_state.passage = random.choice(passages)
        st.session_state.start_time = None
        st.session_state.difficulty = difficulty
        st.session_state.user_input = ""
        st.session_state.submitted = False
        st.session_state.streak = st.session_state.get("streak", 0)
    
    st.subheader(f"Difficulty: {difficulty}")
    st.code(st.session_state.passage, language="")
    
    st.write("Start typing below (copy-paste disabled):")
    
    # Text area with no copy-paste
    user_input = st.text_area("Your Text", value=st.session_state.user_input, height=200)
    st.markdown(NO_COPY_PASTE_JS, unsafe_allow_html=True)
    
    # Start time tracking on first input
    if user_input and st.session_state.start_time is None:
        st.session_state.start_time = time.time()
    st.session_state.user_input = user_input
    
    # Submit button
    if st.button("✅ Submit") and not st.session_state.submitted:
        if not user_input.strip():
            st.warning("Please type the passage first!")
        else:
            end_time = time.time()
            speed_wpm, accuracy, elapsed_time = calculate_speed(st.session_state.start_time, end_time,
                                                               st.session_state.passage, user_input)
            st.session_state.submitted = True
            
            # Save score
            save_score(st.session_state.username, speed_wpm, accuracy, elapsed_time, difficulty)
            
            # Badge
            badge = get_badge(speed_wpm, accuracy)
            
            # Update streak if accuracy >= 90%, else reset streak
            if accuracy >= 90:
                st.session_state.streak = st.session_state.get("streak", 0) + 1
            else:
                st.session_state.streak = 0
            st.session_state['streak'] = st.session_state.streak
            
            # Results display
            st.markdown(f"""
            <div class='result-box'>
                <h3>🎯 Results:</h3>
                <ul>
                    <li>Typing Speed: <strong>{speed_wpm:.2f} WPM</strong></li>
                    <li>Accuracy: <strong>{accuracy:.2f}%</strong></li>
                    <li>Time Taken: <strong>{elapsed_time:.2f} seconds</strong></li>
                    <li>Badge Earned: <strong>{badge}</strong></li>
                    <li>Current Streak (accuracy ≥ 90%): <strong>{st.session_state.streak}</strong></li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
            # Play sound automatically
            if accuracy >= 90:
                play_sound_thread("success.mp3")
            else:
                play_sound_thread("fail.mp3")
    
    # Animated progress bar during typing (resets on submit)
    if not st.session_state.submitted and st.session_state.start_time is not None:
        elapsed = time.time() - st.session_state.start_time
        progress = min(elapsed / 60, 1.0)  # Max 1 minute progress bar
        st.progress(progress)
    
    # Show leaderboard for current difficulty
    st.markdown("---")
    st.subheader(f"🏆 Leaderboard - {difficulty}")
    leaderboard = get_leaderboard(difficulty)
    if leaderboard:
        for i, (user, wpm, acc) in enumerate(leaderboard, 1):
            st.write(f"{i}. **{user}** - WPM: {wpm:.2f}, Accuracy: {acc:.2f}%")
    else:
        st.write("No scores yet. Be the first!")
    
    # Button to reset & try new passage
    if st.button("🔄 Try New Passage"):
        st.session_state.passage = random.choice(passages)
        st.session_state.start_time = None
        st.session_state.user_input = ""
        st.session_state.submitted = False

if __name__ == "__main__":
    main()