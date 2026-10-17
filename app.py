import os
from flask import Flask, render_template_string, request, jsonify, session
import random

app = Flask(__name__)
app.secret_key = "quiz_secret_key_100_questions_production"

# 100 Questions divided into 10 Sets (10 questions each) in English
QUIZ_SETS = {
    1: {
        "title": "Set 1: Basic Computer & Python",
        "questions": [
            {"id": 1, "q": "Who developed the Python programming language?", "options": ["Guido van Rossum", "Dennis Ritchie", "James Gosling", "Bjarne Stroustrup"], "ans": 0},
            {"id": 2, "q": "Which symbol is used for single-line comments in Python?", "options": ["//", "/*", "#", "--"], "ans": 2},
            {"id": 3, "q": "Which component is considered the 'Brain' of a computer?", "options": ["RAM", "Hard Disk", "CPU", "Motherboard"], "ans": 2},
            {"id": 4, "q": "Which of the following is an immutable data type in Python?", "options": ["List", "Dictionary", "Set", "Tuple"], "ans": 3},
            {"id": 5, "q": "What is the standard file extension for Python files?", "options": [".pt", ".py", ".pyt", ".pyc"], "ans": 1},
            {"id": 6, "q": "What is the full form of RAM?", "options": ["Read Access Memory", "Random Access Memory", "Run Access Memory", "Real Action Memory"], "ans": 1},
            {"id": 7, "q": "How is a block of code defined in Python?", "options": ["Curly Brackets {}", "Indentation (Spaces)", "Parentheses ()", "Semicolons ;"], "ans": 1},
            {"id": 8, "q": "What does WWW stand for?", "options": ["World Wide Web", "World Web Wide", "Wide World Web", "World Whole Web"], "ans": 0},
            {"id": 9, "q": "Which method is used to add an item to the end of a Python list?", "options": ["push()", "add()", "append()", "insert_end()"], "ans": 2},
            {"id": 10, "q": "How many bytes are there in 1 Kilobyte (KB)?", "options": ["1000", "1024", "1048", "512"], "ans": 1}
        ]
    },
    2: {
        "title": "Set 2: General Knowledge & India",
        "questions": [
            {"id": 1, "q": "What is the capital city of India?", "options": ["Mumbai", "Kolkata", "New Delhi", "Chennai"], "ans": 2},
            {"id": 2, "q": "Who is known as the 'Father of the Nation' in India?", "options": ["Jawaharlal Nehru", "Mahatma Gandhi", "Subhash Chandra Bose", "Bhagat Singh"], "ans": 1},
            {"id": 3, "q": "Which bird is the national bird of India?", "options": ["Parrot", "Pigeon", "Eagle", "Peacock"], "ans": 3},
            {"id": 4, "q": "On which date did the Constitution of India come into effect?", "options": ["15 August 1947", "26 January 1950", "26 November 1949", "2 October 1950"], "ans": 1},
            {"id": 5, "q": "Which is the longest river flowing entirely within India?", "options": ["Yamuna", "Godavari", "Ganga", "Brahmaputra"], "ans": 2},
            {"id": 6, "q": "Who is known as the 'Iron Man of India'?", "options": ["Sardar Vallabhbhai Patel", "B.R. Ambedkar", "Bal Gangadhar Tilak", "Lal Bahadur Shastri"], "ans": 0},
            {"id": 7, "q": "What is the national animal of India?", "options": ["Lion", "Royal Bengal Tiger", "Elephant", "Leopard"], "ans": 1},
            {"id": 8, "q": "What was the name of India's first satellite launched into space?", "options": ["Rohini", "Bhaskara", "Aryabhata", "Chandrayaan-1"], "ans": 2},
            {"id": 9, "q": "Who composed the Indian national song 'Vande Mataram'?", "options": ["Rabindranath Tagore", "Bankim Chandra Chattopadhyay", "Sarojini Naidu", "Munshi Premchand"], "ans": 1},
            {"id": 10, "q": "Where is the headquarters of ISRO located?", "options": ["New Delhi", "Bengaluru", "Hyderabad", "Mumbai"], "ans": 1}
        ]
    },
    3: {
        "title": "Set 3: Science & Technology",
        "questions": [
            {"id": 1, "q": "What is the chemical formula for water?", "options": ["CO2", "H2O", "NaCl", "O2"], "ans": 1},
            {"id": 2, "q": "Approximately how long does sunlight take to reach Earth?", "options": ["8 minutes", "5 minutes", "10 seconds", "1 hour"], "ans": 0},
            {"id": 3, "q": "How many bones are there in an adult human skeleton?", "options": ["200", "206", "210", "214"], "ans": 1},
            {"id": 4, "q": "Who formulated the law of universal gravitation?", "options": ["Albert Einstein", "Isaac Newton", "Galileo Galilei", "Thomas Edison"], "ans": 1},
            {"id": 5, "q": "Which planet is closest to the Sun?", "options": ["Venus", "Mars", "Mercury", "Jupiter"], "ans": 2},
            {"id": 6, "q": "Which planet is commonly referred to as the 'Red Planet'?", "options": ["Mars", "Venus", "Saturn", "Jupiter"], "ans": 0},
            {"id": 7, "q": "What is the SI unit of electric current?", "options": ["Volt", "Watt", "Ampere", "Ohm"], "ans": 2},
            {"id": 8, "q": "Which gas do plants absorb during the process of photosynthesis?", "options": ["Oxygen", "Carbon Dioxide", "Nitrogen", "Hydrogen"], "ans": 1},
            {"id": 9, "q": "Which gas is most abundant in the Earth's atmosphere?", "options": ["Oxygen", "Carbon Dioxide", "Nitrogen (78%)", "Argon"], "ans": 2},
            {"id": 10, "q": "What does the abbreviation DNA stand for?", "options": ["Deoxyribonucleic Acid", "Diribonucleic Acid", "Dual Nucleic Acid", "Data Nucleic Acid"], "ans": 0}
        ]
    },
    4: {
        "title": "Set 4: World Geography",
        "questions": [
            {"id": 1, "q": "Which is the highest mountain peak in the world above sea level?", "options": ["K2", "Kangchenjunga", "Mount Everest", "Lhotse"], "ans": 2},
            {"id": 2, "q": "Which is the largest and deepest ocean on Earth?", "options": ["Indian Ocean", "Atlantic Ocean", "Pacific Ocean", "Arctic Ocean"], "ans": 2},
            {"id": 3, "q": "Which country is the largest in the world by total land area?", "options": ["China", "Canada", "United States", "Russia"], "ans": 3},
            {"id": 4, "q": "Which is the largest hot desert in the world?", "options": ["Thar Desert", "Sahara Desert", "Gobi Desert", "Kalahari Desert"], "ans": 1},
            {"id": 5, "q": "What is the capital city of Japan?", "options": ["Seoul", "Beijing", "Tokyo", "Bangkok"], "ans": 2},
            {"id": 6, "q": "The kangaroo is the national symbol of which country?", "options": ["New Zealand", "Australia", "South Africa", "England"], "ans": 1},
            {"id": 7, "q": "Which is considered the longest river in the world?", "options": ["Amazon River", "Nile River", "Yangtze River", "Mississippi River"], "ans": 1},
            {"id": 8, "q": "Which viral disease is transmitted primarily through dog bites?", "options": ["Malaria", "Typhoid", "Rabies", "Cholera"], "ans": 2},
            {"id": 9, "q": "Which is the smallest independent state/country in the world?", "options": ["Monaco", "Vatican City", "Maldives", "San Marino"], "ans": 1},
            {"id": 10, "q": "In which city is the famous Statue of Liberty located?", "options": ["London", "Paris", "New York City", "Washington, D.C."], "ans": 2}
        ]
    },
    5: {
        "title": "Set 5: Sports & Athletics",
        "questions": [
            {"id": 1, "q": "India won the 2011 ICC Cricket World Cup final against which team?", "options": ["Pakistan", "Australia", "Sri Lanka", "England"], "ans": 2},
            {"id": 2, "q": "How often are the regular Olympic Games held?", "options": ["Every 2 years", "Every 3 years", "Every 4 years", "Every 5 years"], "ans": 2},
            {"id": 3, "q": "Who is known as the 'Wizard of Hockey'?", "options": ["Major Dhyan Chand", "Balbir Singh Sr.", "Dhanraj Pillay", "Manpreet Singh"], "ans": 0},
            {"id": 4, "q": "What is the official length of a standard cricket pitch?", "options": ["20 yards", "22 yards", "24 yards", "26 yards"], "ans": 1},
            {"id": 5, "q": "The FIFA World Cup is associated with which sport?", "options": ["Cricket", "Football (Soccer)", "Basketball", "Tennis"], "ans": 1},
            {"id": 6, "q": "With which Olympic sport is Neeraj Chopra associated?", "options": ["Shooting", "Wrestling", "Javelin Throw", "Boxing"], "ans": 2},
            {"id": 7, "q": "How many total squares are on a standard chess board?", "options": ["54", "64", "72", "81"], "ans": 1},
            {"id": 8, "q": "Which famous cricketer is fondly known as the 'Master Blaster'?", "options": ["Virat Kohli", "Sachin Tendulkar", "MS Dhoni", "Rohit Sharma"], "ans": 1},
            {"id": 9, "q": "PV Sindhu is an internationally acclaimed Indian player in which sport?", "options": ["Badminton", "Tennis", "Table Tennis", "Squash"], "ans": 0},
            {"id": 10, "q": "Which team won the inaugural ICC Men's T20 World Cup in 2007?", "options": ["Pakistan", "India", "West Indies", "Australia"], "ans": 1}
        ]
    },
    6: {
        "title": "Set 6: Web Development & Internet",
        "questions": [
            {"id": 1, "q": "What is the full form of HTML?", "options": ["HyperText Markup Language", "Hyperlink Text Machine", "Home Tool Markup Language", "HighText Machine Language"], "ans": 0},
            {"id": 2, "q": "Which technology is primarily used for styling and designing web pages?", "options": ["HTML", "CSS", "Python", "SQL"], "ans": 1},
            {"id": 3, "q": "Which language is primarily used to build client-side interactivity in browsers?", "options": ["C++", "Java", "JavaScript", "PHP"], "ans": 2},
            {"id": 4, "q": "What does HTTP stand for?", "options": ["HyperText Transfer Protocol", "HighText Transit Protocol", "Hyper Transfer Text Path", "Home Tool Transfer Protocol"], "ans": 0},
            {"id": 5, "q": "Which prefix indicates that a website URL uses an encrypted SSL/TLS connection?", "options": ["http://", "https://", "ftp://", "www://"], "ans": 1},
            {"id": 6, "q": "Which of the following is a popular lightweight Python backend web framework?", "options": ["Flask", "React", "Angular", "Vue"], "ans": 0},
            {"id": 7, "q": "What does 'IP' stand for in 'IP Address'?", "options": ["Internet Provider", "Internet Protocol", "Internal Path", "Instant Protocol"], "ans": 1},
            {"id": 8, "q": "Which standard query language is used to manage relational databases?", "options": ["HTML", "SQL", "CSS", "JSON"], "ans": 1},
            {"id": 9, "q": "Which HTML tag is used to display an image on a webpage?", "options": ["<image>", "<img>", "<pic>", "<src>"], "ans": 1},
            {"id": 10, "q": "What does URL stand for?", "options": ["Uniform Resource Locator", "Universal Resource Link", "United Resource Locator", "Uniform Remote Link"], "ans": 0}
        ]
    },
    7: {
        "title": "Set 7: World & Indian History",
        "questions": [
            {"id": 1, "q": "Which Mughal Emperor commissioned the building of the Taj Mahal?", "options": ["Akbar", "Shah Jahan", "Babur", "Humayun"], "ans": 1},
            {"id": 2, "q": "In which year did World War I begin?", "options": ["1912", "1914", "1918", "1939"], "ans": 1},
            {"id": 3, "q": "From which city did the Indian Revolt of 1857 officially begin?", "options": ["Meerut", "Delhi", "Jhansi", "Kanpur"], "ans": 0},
            {"id": 4, "q": "In which year did the tragic Jallianwala Bagh massacre take place?", "options": ["1915", "1919", "1921", "1925"], "ans": 1},
            {"id": 5, "q": "Who founded the Arya Samaj in 1875?", "options": ["Swami Dayanand Saraswati", "Swami Vivekananda", "Raja Ram Mohan Roy", "Ishwar Chandra Vidyasagar"], "ans": 0},
            {"id": 6, "q": "Along the basin of which river did the ancient Indus Valley Civilization flourish?", "options": ["Ganges", "Indus", "Yamuna", "Narmada"], "ans": 1},
            {"id": 7, "q": "Who was the founder of the ancient Mauryan Empire in India?", "options": ["Ashoka the Great", "Chandragupta Maurya", "Bindusara", "Brihadratha"], "ans": 1},
            {"id": 8, "q": "In which year did Mahatma Gandhi launch the 'Quit India Movement'?", "options": ["1930", "1935", "1942", "1945"], "ans": 2},
            {"id": 9, "q": "In which Indian state are the UNESCO World Heritage Ajanta & Ellora caves situated?", "options": ["Madhya Pradesh", "Maharashtra", "Gujarat", "Rajasthan"], "ans": 1},
            {"id": 10, "q": "Where did Gautama Buddha attain supreme spiritual enlightenment?", "options": ["Sarnath", "Bodh Gaya", "Kushinagar", "Lumbini"], "ans": 1}
        ]
    },
    8: {
        "title": "Set 8: Advanced Python Concepts",
        "questions": [
            {"id": 1, "q": "Which keyword is used to declare and define a function in Python?", "options": ["func", "function", "def", "define"], "ans": 2},
            {"id": 2, "q": "What are single-expression anonymous functions called in Python?", "options": ["Lambda functions", "Ghost functions", "Static functions", "Inline functions"], "ans": 0},
            {"id": 3, "q": "Which built-in function converts an appropriate string into an integer in Python?", "options": ["str()", "float()", "int()", "parse()"], "ans": 2},
            {"id": 4, "q": "What is the primary role of 'pip' in the Python ecosystem?", "options": ["Compiling bytecode", "Installing and managing third-party packages", "Running Python programs", "Code styling"], "ans": 1},
            {"id": 5, "q": "Which widely used Python library provides data structures like DataFrames?", "options": ["Pandas", "React", "Laravel", "Spring"], "ans": 0},
            {"id": 6, "q": "Which statement terminates the execution of the nearest enclosing loop immediately?", "options": ["continue", "stop", "break", "exit"], "ans": 2},
            {"id": 7, "q": "Which blocks are used to catch and handle exceptions in Python?", "options": ["try-catch", "try-except", "do-while", "if-else"], "ans": 1},
            {"id": 8, "q": "In what structural format does a Python dictionary store data?", "options": ["Key-Value pairs", "Index-Value pairs", "Pure array sequence", "Binary format"], "ans": 0},
            {"id": 9, "q": "What is the output of len([10, 20, 30]) in Python?", "options": ["2", "3", "30", "10"], "ans": 1},
            {"id": 10, "q": "How is Python primarily classified as a programming language?", "options": ["Purely Compiled", "Interpreted and High-Level", "Low-Level Assembly", "Hardware Description"], "ans": 1}
        ]
    },
    9: {
        "title": "Set 9: Logical Reasoning & Mind Teasers",
        "questions": [
            {"id": 1, "q": "Some months have 31 days, others have 30. How many months have 28 days?", "options": ["Only February (1 month)", "All 12 months", "4 months", "6 months"], "ans": 1},
            {"id": 2, "q": "Complete the geometric sequence: 2, 4, 8, 16, ___?", "options": ["24", "30", "32", "36"], "ans": 2},
            {"id": 3, "q": "What goes up constantly but never comes down?", "options": ["A Kite", "Your Age", "Rain", "The Sun"], "ans": 1},
            {"id": 4, "q": "There are 10 burning candles. The wind blows out 3. How many are left in the end?", "options": ["0", "3 (The 3 blown out don't melt away)", "7", "10"], "ans": 1},
            {"id": 5, "q": "Find the odd one out: Apple, Mango, Banana, Carrot", "options": ["Apple", "Mango", "Banana", "Carrot (It's a root vegetable)"], "ans": 3},
            {"id": 6, "q": "Find the next number in the arithmetic series: 5, 10, 15, 20, ___?", "options": ["22", "25", "30", "35"], "ans": 1},
            {"id": 7, "q": "If there are 3 apples on a table and you take away 2, how many apples do you have?", "options": ["1", "2 (Because you took 2)", "3", "0"], "ans": 1},
            {"id": 8, "q": "If A = 1, B = 2, C = 3... what is the letter value sum of 'CAT'? (3 + 1 + 20)", "options": ["22", "24", "26", "28"], "ans": 1},
            {"id": 9, "q": "I have keys but open no locks, space but no room, you can enter but can't go inside. What am I?", "options": ["A Keyring", "A Computer Keyboard", "A Door", "A Vault"], "ans": 1},
            {"id": 10, "q": "Identify the next perfect square: 1, 4, 9, 16, 25, ___?", "options": ["30", "36", "49", "40"], "ans": 1}
        ]
    },
    10: {
        "title": "Set 10: Mixed Grand Finale Quiz",
        "questions": [
            {"id": 1, "q": "On which date is World Environment Day observed globally?", "options": ["June 5", "August 15", "April 22", "December 1"], "ans": 0},
            {"id": 2, "q": "What does the abbreviation ATM stand for?", "options": ["Automated Teller Machine", "Any Time Money", "Auto Transaction Mode", "All Time Machine"], "ans": 0},
            {"id": 3, "q": "Which component in human blood is responsible for carrying oxygen?", "options": ["White Blood Cells", "Red Blood Cells (Hemoglobin)", "Blood Platelets", "Plasma"], "ans": 1},
            {"id": 4, "q": "Which was India's first sound/talkie feature motion picture?", "options": ["Raja Harishchandra", "Alam Ara (1931)", "Sholay", "Mother India"], "ans": 1},
            {"id": 5, "q": "Who was the first Indian citizen to win a Nobel Prize?", "options": ["C.V. Raman", "Rabindranath Tagore", "Mother Teresa", "Amartya Sen"], "ans": 1},
            {"id": 6, "q": "In cricket, what does an umpire signaling with both arms raised straight above indicate?", "options": ["Boundary Four", "Maximum Six Runs", "Batter is Out", "Wide Ball"], "ans": 1},
            {"id": 7, "q": "Which country is internationally known as the world's most populous democracy?", "options": ["United States", "India", "United Kingdom", "Canada"], "ans": 1},
            {"id": 8, "q": "The Android mobile operating system is developed primarily by which company?", "options": ["Apple", "Microsoft", "Google", "Samsung"], "ans": 2},
            {"id": 9, "q": "What is the only permanent natural satellite of Planet Earth?", "options": ["The Sun", "The Moon", "Venus", "Mars"], "ans": 1},
            {"id": 10, "q": "Who designed the official symbol of the Indian Rupee (₹)?", "options": ["Udaya Kumar Dharmalingam", "Raghuram Rajan", "Nandan Nilekani", "Homi Bhabha"], "ans": 0}
        ]
    }
}

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Mega Quiz Master - 100 Questions</title>
    <style>
        :root {
            --primary: #6366f1;
            --primary-dark: #4f46e5;
            --bg-color: #0b0f19;
            --card-bg: #1e293b;
            --card-border: #334155;
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --correct: #10b981;
            --wrong: #ef4444;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
            -webkit-tap-highlight-color: transparent;
        }

        body {
            background-color: var(--bg-color);
            color: var(--text-main);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 16px;
        }

        .app-card {
            width: 100%;
            max-width: 520px;
            background: var(--card-bg);
            border: 1px solid var(--card-border);
            border-radius: 20px;
            padding: 24px;
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.4);
        }

        .title-bar {
            text-align: center;
            margin-bottom: 20px;
        }

        .title-bar h1 {
            font-size: 22px;
            color: #e0e7ff;
            margin-bottom: 6px;
        }

        .title-bar p {
            font-size: 14px;
            color: var(--text-muted);
        }

        /* Set Selection Grid */
        .set-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 12px;
            margin-top: 15px;
        }

        .set-btn {
            background: #273549;
            color: var(--text-main);
            border: 1px solid #3b4d66;
            padding: 14px 10px;
            border-radius: 12px;
            font-size: 14px;
            font-weight: 600;
            cursor: pointer;
            text-align: center;
            transition: all 0.2s ease;
        }

        .set-btn:hover {
            background: var(--primary);
            border-color: var(--primary);
            transform: translateY(-2px);
        }

        /* Quiz Active Area */
        .quiz-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
        }

        .badge {
            background: #334155;
            color: #cbd5e1;
            padding: 5px 12px;
            border-radius: 15px;
            font-size: 13px;
            font-weight: 600;
        }

        .progress-track {
            width: 100%;
            height: 8px;
            background: #334155;
            border-radius: 5px;
            margin-bottom: 22px;
            overflow: hidden;
        }

        .progress-fill {
            height: 100%;
            width: 0%;
            background: linear-gradient(90deg, #6366f1, #a855f7);
            transition: width 0.3s ease;
        }

        .question-box {
            font-size: 18px;
            font-weight: 600;
            line-height: 1.45;
            margin-bottom: 20px;
            min-height: 52px;
        }

        .options-container {
            display: flex;
            flex-direction: column;
            gap: 10px;
            margin-bottom: 20px;
        }

        .option-button {
            background: #293548;
            border: 2px solid transparent;
            color: var(--text-main);
            padding: 14px 16px;
            border-radius: 12px;
            font-size: 15px;
            text-align: left;
            cursor: pointer;
            transition: all 0.15s ease;
        }

        .option-button:hover:not(:disabled) {
            background: #384860;
        }

        .option-button.correct {
            background: rgba(16, 185, 129, 0.2) !important;
            border-color: var(--correct) !important;
            color: #34d399 !important;
            font-weight: 700;
        }

        .option-button.wrong {
            background: rgba(239, 68, 68, 0.2) !important;
            border-color: var(--wrong) !important;
            color: #f87171 !important;
        }

        .action-button {
            width: 100%;
            background: var(--primary);
            color: white;
            padding: 14px;
            border-radius: 12px;
            border: none;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: background 0.2s;
        }

        .action-button:hover {
            background: var(--primary-dark);
        }

        /* Result View */
        .result-screen {
            text-align: center;
            padding: 15px 0;
            display: none;
        }

        .result-screen h2 {
            font-size: 26px;
            margin-bottom: 12px;
        }

        .score-circle {
            width: 120px;
            height: 120px;
            border-radius: 50%;
            border: 5px solid var(--primary);
            display: flex;
            justify-content: center;
            align-items: center;
            font-size: 32px;
            font-weight: 800;
            margin: 20px auto;
            color: #e0e7ff;
            background: rgba(99, 102, 241, 0.1);
        }

        .result-msg {
            color: var(--text-muted);
            margin-bottom: 25px;
            font-size: 16px;
        }

        .btn-group {
            display: flex;
            flex-direction: column;
            gap: 10px;
        }

        .secondary-button {
            background: #334155;
            color: white;
            padding: 13px;
            border-radius: 12px;
            border: none;
            font-size: 15px;
            font-weight: 600;
            cursor: pointer;
        }
    </style>
</head>
<body>

<div class="app-card">
    <!-- VIEW 1: Set Selection -->
    <div id="selection-view">
        <div class="title-bar">
            <h1>🎯 Mega Quiz (100 Questions)</h1>
            <p>10 Sets available. Choose a set to start:</p>
        </div>
        <div class="set-grid" id="sets-list">
            <!-- Populated dynamically -->
        </div>
    </div>

    <!-- VIEW 2: Active Quiz -->
    <div id="quiz-view" style="display: none;">
        <div class="quiz-header">
            <span class="badge" id="set-indicator">Set 1</span>
            <span class="badge" id="question-indicator">1 / 10</span>
        </div>
        <div class="progress-track">
            <div class="progress-fill" id="progress-bar"></div>
        </div>
        <div class="question-box" id="question-text">Loading question...</div>
        <div class="options-container" id="options-box"></div>
        <button class="action-button" id="next-btn" style="display: none;" onclick="loadNextQuestion()">Next Question →</button>
    </div>

    <!-- VIEW 3: Result Screen -->
    <div class="result-screen" id="result-view">
        <h2>🎉 Set Completed!</h2>
        <div class="score-circle" id="score-text">0 / 10</div>
        <p class="result-msg" id="score-message">Great effort!</p>
        <div class="btn-group">
            <button class="action-button" onclick="restartCurrentSet()">Play Again 🔄</button>
            <button class="secondary-button" onclick="goToSetSelection()">Choose Another Set 📋</button>
        </div>
    </div>
</div>

<script>
    let currentSetId = 1;
    let answered = false;

    // Load available sets on startup
    async function loadSetsMenu() {
        const res = await fetch('/api/get-sets');
        const sets = await res.json();
        const grid = document.getElementById('sets-list');
        grid.innerHTML = '';
        
        sets.forEach(s => {
            const btn = document.createElement('button');
            btn.className = 'set-btn';
            btn.innerHTML = `<strong>Set ${s.id}</strong><br><span style="font-size:11px; opacity:0.8;">${s.title.split(':')[1] || s.title}</span>`;
            btn.onclick = () => startSet(s.id);
            grid.appendChild(btn);
        });
    }

    async function startSet(setId) {
        currentSetId = setId;
        const res = await fetch('/api/start-set', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ set_id: setId })
        });
        
        if (res.ok) {
            document.getElementById('selection-view').style.display = 'none';
            document.getElementById('result-view').style.display = 'none';
            document.getElementById('quiz-view').style.display = 'block';
            fetchNextQuestion();
        }
    }

    async function fetchNextQuestion() {
        answered = false;
        document.getElementById('next-btn').style.display = 'none';

        const res = await fetch('/api/get-question');
        const data = await res.json();

        if (data.finished) {
            showResult(data.final_score, data.total);
            return;
        }

        document.getElementById('set-indicator').innerText = `Set ${currentSetId}`;
        document.getElementById('question-indicator').innerText = `${data.question_number} / ${data.total_questions}`;
        document.getElementById('progress-bar').style.width = `${(data.question_number / data.total_questions) * 100}%`;
        document.getElementById('question-text').innerText = data.question;

        const box = document.getElementById('options-box');
        box.innerHTML = '';
        data.options.forEach((opt, idx) => {
            const btn = document.createElement('button');
            btn.className = 'option-button';
            btn.innerText = opt;
            btn.onclick = () => checkAnswer(idx, btn);
            box.appendChild(btn);
        });
    }

    async function checkAnswer(choiceIdx, btnElement) {
        if (answered) return;
        answered = true;

        const res = await fetch('/api/submit-answer', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ choice: choiceIdx })
        });
        const result = await res.json();

        const allBtns = document.querySelectorAll('.option-button');
        allBtns.forEach((btn, idx) => {
            btn.disabled = true;
            if (idx === result.correct_answer_index) {
                btn.classList.add('correct');
            }
        });

        if (!result.correct) {
            btnElement.classList.add('wrong');
        }

        document.getElementById('next-btn').style.display = 'block';
    }

    function loadNextQuestion() {
        fetchNextQuestion();
    }

    function showResult(score, total) {
        document.getElementById('quiz-view').style.display = 'none';
        document.getElementById('result-view').style.display = 'block';
        document.getElementById('score-text').innerText = `${score} / ${total}`;

        const msg = document.getElementById('score-message');
        if (score === 10) {
            msg.innerText = "🏆 Outstanding! Perfect score 10 out of 10!";
        } else if (score >= 7) {
            msg.innerText = "👏 Great job! Excellent knowledge.";
        } else {
            msg.innerText = "💡 Good effort! Try again to improve your score.";
        }
    }

    function restartCurrentSet() {
        startSet(currentSetId);
    }

    function goToSetSelection() {
        document.getElementById('result-view').style.display = 'none';
        document.getElementById('quiz-view').style.display = 'none';
        document.getElementById('selection-view').style.display = 'block';
    }

    loadSetsMenu();
</script>

</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/get-sets', methods=['GET'])
def get_sets():
    summary = []
    for s_id, s_data in QUIZ_SETS.items():
        summary.append({
            "id": s_id,
            "title": s_data["title"],
            "total_questions": len(s_data["questions"])
        })
    return jsonify(summary)

@app.route('/api/start-set', methods=['POST'])
def start_set():
    data = request.get_json()
    set_id = int(data.get('set_id', 1))
    if set_id not in QUIZ_SETS:
        return jsonify({"error": "Invalid set"}), 400
    
    session['current_set_id'] = set_id
    session['score'] = 0
    session['current_index'] = 0
    return jsonify({"status": "started", "set_id": set_id})

@app.route('/api/get-question', methods=['GET'])
def get_question():
    set_id = session.get('current_set_id', 1)
    index = session.get('current_index', 0)
    questions = QUIZ_SETS.get(set_id, {}).get("questions", [])

    if index >= len(questions):
        return jsonify({
            "finished": True,
            "final_score": session.get('score', 0),
            "total": len(questions)
        })

    q = questions[index]
    return jsonify({
        "finished": False,
        "question_number": index + 1,
        "total_questions": len(questions),
        "question": q["q"],
        "options": q["options"]
    })

@app.route('/api/submit-answer', methods=['POST'])
def submit_answer():
    data = request.get_json()
    user_choice = data.get('choice')
    
    set_id = session.get('current_set_id', 1)
    index = session.get('current_index', 0)
    questions = QUIZ_SETS.get(set_id, {}).get("questions", [])

    if index >= len(questions):
        return jsonify({"error": "Completed"}), 400

    correct_choice = questions[index]["ans"]
    is_correct = (user_choice == correct_choice)

    if is_correct:
        session['score'] = session.get('score', 0) + 1

    session['current_index'] = index + 1

    return jsonify({
        "correct": is_correct,
        "correct_answer_index": correct_choice,
        "current_score": session.get('score', 0)
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)