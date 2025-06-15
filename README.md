
# 🧠 Quiz App Using Python Tkinter

This is a GUI-based Quiz Application built using **Python's Tkinter** library. It presents multiple-choice questions from a JSON file and allows users to answer, review later, navigate between questions, track time, and finally view detailed results.

---

## 🚀 Features

- ✅ **Multiple Choice Questions** from a JSON file  
- ⏱️ **60-second timer** per quiz with auto-submit on timeout  
- 🔁 **Previous / Next Navigation**  
- ⭐ **Mark Questions for Review**  
- 📌 **Auto-save answers** on selection  
- ✅ **Displays Correct/Wrong/Missed/Review-Later questions** after submission  
- 🎯 **Score Summary + Performance Compliments**  
- 🔁 **Retake Quiz Button**  
- 🔒 Fixed window size for a stable layout  
- 📋 **Scrollable result** section for detailed analysis  

---

## 🖥️ GUI Preview

![Preview](https://github.com/user-attachments/assets/911fa308-3d7e-4d1b-9b0f-f9a9d973072b)

---

## 📝 How to Use

### 1. Clone or Download

```bash
git clone https://github.com/your-repo/quiz-tkinter.git
cd quiz-tkinter
```

### 2. Create `questions.json`

Sample format:

```json
[
    {
        "question": "What is the capital of France?",
        "options": ["Berlin", "London", "Paris", "Rome"],
        "correct_answer": 3
    },
    {
        "question": "Which language is used for web development?",
        "options": ["Python", "HTML", "C++", "Java"],
        "correct_answer": 2
    }
]
```

> `correct_answer` is 1-indexed (i.e., `1` = first option)

### 3. Run the App

```bash
python quiz.py
```

---

## 🔍 Key Functionalities

| Feature | Details |
|--------|---------|
| `save_selected_option()` | Saves the selected option immediately when clicked |
| `mark_for_review()` | Toggles review-later state for current question without resetting the option |
| `submit_quiz()` | Submits quiz and shows detailed report with categories |
| `restart_quiz()` | Clears previous state and restarts the quiz from question 1 |
| `update_timer()` | Updates countdown and auto-submits on time out |
| `show_result_direct()` | Displays a simple result when auto-submitted |

---

## 💡 Compliment Logic

After submission:

- `🌟 Excellent!` → Full score
- `💪 Great job!` → 70% or more
- `🙂 Keep practicing` → 40% or more
- `😅 Better luck next time!` → Otherwise

---

## 📂 Folder Structure

```
├── quiz.py              # Main app
├── questions.json       # MCQ question data
└── README.md            # This file
```

---

## 📌 Dependencies

- Python 3.x
- Tkinter (comes bundled with Python)

---

## 📜 License

This project is open-source and free to use for learning or demo purposes.

---

## Made with ❤️ by Shakyasimha Das.
