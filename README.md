# 🎉 Lucky Participant Guesser

A simple event-ready app that randomly selects participants from an Excel file **without repetition**.

---

# 🚀 Objective

- Upload Excel file with participant names  
- Pick random winner  
- Ensure **no duplicate selection**  
- Display winners list  

---

# 🧠 Common Data Contract (VERY IMPORTANT)

All modules must follow this structure:

```python
names = ["Rahul", "Sneha", "Aman"]     # list of participants
winner = "Rahul"                      # selected winner
winners = ["Rahul", "Sneha"]          # already selected winners

👉 This is the communication format between all files
👉 Do NOT change this structure

## 📁 Project Structure
lucky-participant-guesser/
│
├── app.py                # Main integration (ONLY HEAD edits)
├── logic.py              # Winner selection logic
├── data_handler.py       # Excel file handling
├── ui.py                 # UI layout (Streamlit)
├── effects.py            # Countdown / animation
│
├── requirements.txt
└── README.md


## 👥 Team Responsibilities
👑 Head (Prathamesh)
Handles app.py (integration)
Handles logic.py
Final testing


## 🧑‍💻 Data Handler

File: data_handler.py

Read Excel file
Extract names
Remove nulls & duplicates
Return clean list


## 🧑‍🎨 UI Developer

File: ui.py

Build UI layout
Buttons (Upload, Pick Winner, Reset)
Display sections


## 🧑‍🔧 Effects Developer

File: effects.py

Countdown (3…2…1…)
Loading / animation feel
Improve user experience


## ⚙️ Development Workflow (IMPORTANT)

# Step 1: Work Independently
Everyone works on their own file only
Do NOT edit other files
Do NOT touch app.py

#Step 2: Use Dummy Data First

# Example:

names = ["Rahul", "Sneha", "Aman"]

👉 Do NOT wait for Excel or backend
👉 Make your module work independently first

# Step 3: Completion

When your part is ready:

Test your file
Ensure no errors
Inform: "Done"
Step 4: Integration
Only Head will merge everything
Do NOT push directly to main logic
Do NOT modify others' code
⚠️ Rules (STRICT)
❌ Do NOT edit app.py
❌ Do NOT change function names
❌ Do NOT change data format
❌ Do NOT wait for others
✅ Work independently
✅ Keep code simple
✅ Inform when done
📊 Excel Format


Your Excel file must contain:

Name
Rahul
Sneha
Aman

👉 Column name must be exactly: Name

#▶️ How to Run
pip install -r requirements.txt
streamlit run app.py

#🧪 Testing Checklist

Before final submission:

 Excel uploads correctly
 Winner is selected randomly
 No duplicate winners ❗
 Winners list updates properly
 Reset button works
🚨 Common Mistakes (Avoid This)
Editing someone else’s file ❌
Changing data format ❌
Waiting for backend ❌
Pushing incomplete code ❌


#🔥 Goal

👉 Build a working, smooth, and event-ready app
👉 Not overdesign — focus on functionality

#💬 Communication

Use short updates:
"UI done"
"Logic ready"
"Data working"

#🏁 Final Note
Keep it simple.
Make it work.
Then make it smooth.🔥
