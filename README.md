# ⌨️AccuType
A fully-featured typing speed test app built with Streamlit. It tracks your typing speed, accuracy, and time taken across various difficulty levels, supports login and streaks, awards badges, and includes sound feedback for success/failure. It also saves scores in a SQLite leaderboard for real-time ranking!

## Overview
A **typing speed test app** built using **Streamlit** with real-time WPM, accuracy tracking, user login, difficulty levels, streaks, badges, sound effects, and a leaderboard saved via SQLite. Fast, fun, and fully local!

## 🚀Features
- 🎮 Difficulty Levels: `Easy`, `Medium`, `Hard`
- ⏱️ Real-time **WPM**, **Accuracy**, and **Time Taken**
- 🧑‍💻 User Login with persistent streak tracking
- 🏅 Badge System for performance rewards
- 🔊 Sound Effects: success and fail tones
- 🏆 Leaderboard with top scores by difficulty
- 🎨 Light/Dark Theme toggle
- 🧼 Copy-Paste disabled for fair testing
- 🔄 New Passage button to retry instantly

## ⚙️Installation
Install the required packages:
```sh
pip install streamlit playsound
```

Run this command in the terminal:
```sh
streamlit run app.py
```

## 🛠️How It Works
1️⃣Login with Your username

2️⃣Select a difficulty level that you want

3️⃣Type the randomly selected passage that is displayed on the screen

4️⃣On submission:
-You will Get your WPM, Accuracy, Time Taken
-Can View your streak and earn a badge
-You will Hear a success/fail sound
-At last Score is saved to the leaderboard

## 💡Why Use This Typing Speed Tester?
✅Improves typing skills with real passages tailored by difficulty level.
✅Tracks your typing speed (WPM), accuracy, and time taken for detailed feedback.
✅Gamifies practice using badges and streaks to keep you motivated.

## 🛠️Tech Stack Used
Frontend - Streamlit – for interactive UI
Backend	- Python
Database - SQLite – for storing users and scores
Audio	- playsound – to play success/failure sounds
Styling	- Custom CSS (light & dark themes)
Data Files	- Text files (easy.txt, medium.txt, hard.txt) for typing passages
