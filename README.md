📘 Expression Grammar Validator

A simple web-based tool to validate context-free grammars.
It analyzes grammar rules and detects structural issues like unreachable symbols, non-generating symbols, missing productions, and left recursion.

🚀 Features
Grammar parsing and validation
Detects:
Invalid syntax
Missing productions
Unreachable non-terminals
Non-generating symbols
Left recursion
Clean frontend UI for input and results
REST API backend using Flask
🧠 How It Works
Backend (app.py)

The backend processes grammar rules and performs multiple checks:

Parsing → Converts input text into production rules
Generating Symbols → Checks if a symbol can derive terminal strings
Reachability → Ensures all symbols are accessible from start symbol
Left Recursion Detection → Identifies immediate left recursion
Validation Output → Returns structured JSON with:
Status (VALID / INVALID)
Errors
Warnings
Per-symbol analysis
Frontend (index.html)
Simple UI to input grammar
Sends request to backend (/validate)
Displays:
Start symbol
Validation status
Errors & warnings
Symbol-wise breakdown
📂 Project Structure
project/
│── app.py          # Flask backend
│── index.html      # Frontend UI
⚙️ Installation & Setup
1. Clone the repository
git clone <your-repo-url>
cd project
2. Install dependencies
pip install flask flask-cors
3. Run backend
python app.py

Backend will run at:

http://127.0.0.1:5000
4. Open frontend

Just open:

index.html

No server needed for frontend.

🧪 Example Input
E -> E + T | T
T -> T * F | F
F -> ( E ) | id
📊 Sample Output
✔ VALID or ✖ INVALID
Start Symbol: E
Per non-terminal:
✓ if correct
Issues like:
Unreachable
Non-generating
Left recursion
⚠️ Limitations (Don’t Ignore This)
Only detects immediate left recursion, not indirect recursion
Grammar format is strict:
Must use ->
Non-terminals must be uppercase
No FIRST/FOLLOW or parsing table generation
No ambiguity detection
💡 Improvements You Should Actually Consider

If you're serious about making this project strong (especially for placements), add:

FIRST & FOLLOW computation
LL(1) parsing table
Left recursion elimination
Left factoring
Parse tree visualization
Better error messages (current ones are basic)

Right now, this is a good academic demo, not a production-grade compiler tool.

🛠 Tech Stack
Backend: Python (Flask)
Frontend: HTML, CSS, JavaScript
API: REST
