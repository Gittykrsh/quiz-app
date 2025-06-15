import tkinter as tk
from tkinter import messagebox
import json

def center_window(window, width=800, height=600):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    window.geometry(f"{width}x{height}+{x}+{y}")

# Define a class QuizApp
class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Quiz")
        self.root.geometry("800x600")
        self.root.resizable(False, False)
        self.root.minsize(800, 600)
        self.root.maxsize(800, 600)
        
        # Load questions from a JSON file
        self.questions = self.load_questions("questions.json")
        
        # Initialize variables
        self.current_question = 0
        self.score = 0
        self.selected_option = tk.StringVar(value="")
        self.wrong_answers = []
        self.review_later = []
        self.user_answers = [None] * len(self.questions)
        self.score_window = None
        self.timer = 60
        self.timer_id = None

        # Main frame
        self.frame = tk.Frame(root, width=750, height=500, bg="#f8a3a3")
        self.frame.pack_propagate(False)
        self.frame.pack(pady=20)

        self.question_label = tk.Label(
            self.frame,
            text="",
            font=("Helvetica", 16),
            wraplength=700,
            justify="left",
            bg="#64bef2",
            anchor="w"
        )
        self.question_label.place(x=20, y=10, width=710, height=80)

        # Create and pack the option buttons
        self.option_buttons = []
        option_y_positions = [100, 150, 200, 250]
        for i in range(4):
            btn = tk.Radiobutton(
                self.frame,
                text="",
                variable=self.selected_option,
                value=str(i + 1),
                font=("Arial", 12),
                bg="#f8a3a3",
                anchor="w",
                justify="left",
                wraplength=600,
                command=self.save_selected_option
            )
            btn.place(x=75, y=option_y_positions[i], width=600, height=30)
            self.option_buttons.append(btn)
        # Create and pack the "Previous" button
        self.previous_button = tk.Button(self.frame, text="Previous", width=12, command=self.go_to_previous)
        self.previous_button.place(x=80, y=310, width=120, height=30)

        # Create and pack the "Review Later" button
        self.review_button = tk.Button(self.frame, text="Review Later", width=15, command=self.mark_for_review)
        self.review_button.place(x=300, y=310, width=150, height=30)

        # Create and pack the "Next" button
        self.next_button = tk.Button(self.frame, text="Next", width=12, command=self.check_answer)
        self.next_button.place(x=550, y=310, width=120, height=30)

        # Create and pack the "Finish Test" button
        self.finish_button = tk.Button(self.frame, text="Finish Test", width=20, command=self.finish_test)
        self.finish_button.place(x=300, y=360, width=150, height=35)

        # Create and pack the score label
        self.score_label = tk.Label(root, text="")
        self.score_label.pack()

        # Create and pack the timer label
        self.timer_label = tk.Label(self.frame, text="", font=("Arial", 12), fg="black", bg="#f8f8f8")
        self.timer_label.place(x=275, y=410, width=200, height=25)

        # Load the first question and start the timer
        self.load_next_question()
        self.update_timer()

    # Function to load questions from a JSON file
    def load_questions(self, filename):
        try:
            with open(filename, 'r') as file:
                return json.load(file)
        except Exception as e:
            messagebox.showerror("Error", f"Could not load questions: {e}")
            self.root.destroy()

    # Function to load the next question
    def load_next_question(self):
        q = self.questions[self.current_question]
        self.correct_answer = q["correct_answer"]

        review_mark = " ⭐ (Marked for Review)" if self.current_question in self.review_later else ""
        self.question_label.config(text=f"Q{self.current_question+1}: {q['question']}{review_mark}")

        for i, opt in enumerate(q["options"]):
            self.option_buttons[i].config(text=opt)

        # Restore previously selected answer
        if self.user_answers[self.current_question] is not None:
            self.selected_option.set(str(self.user_answers[self.current_question]))
        else:
            self.selected_option.set("")
        
        self.previous_button.config(state="normal" if self.current_question > 0 else "disabled")

    # Function to check the selected answer
    def check_answer(self):
        if self.current_question >= len(self.questions):
            return
        selected = self.selected_option.get()
        if selected is None or selected == "":
           self.user_answers[self.current_question] = None
        else:
            try:
                selected_int = int(selected)
                self.user_answers[self.current_question] = selected_int
                if selected_int != self.correct_answer and self.current_question not in self.wrong_answers:
                    self.wrong_answers.append(self.current_question)
            except ValueError:
                self.user_answers[self.current_question] = None

        self.current_question += 1
        if self.current_question < len(self.questions):
            self.load_next_question()
        else:
            answer = messagebox.askyesno("Submit Quiz", "Are you sure you want to submit the quiz?")
            if answer:
                self.submit_quiz()
            else:
                self.current_question -= 1

    # Function to go to the previous question
    def go_to_previous(self):
        if self.current_question > 0:
            self.current_question -= 1
            self.load_next_question()

    # Function to review later
    def mark_for_review(self):
        selected = self.selected_option.get()

        # Save selected option if any
        if selected is not None and selected != "":
            try:
                selected_int = int(selected)
                self.user_answers[self.current_question] = selected_int
            except ValueError:
                self.user_answers[self.current_question] = None
        else:
            self.user_answers[self.current_question] = None

        # Toggle review status
        if self.current_question in self.review_later:
            self.review_later.remove(self.current_question)
        else:
            self.review_later.append(self.current_question)

        # Just refresh current question to show/hide ⭐
        self.load_next_question()

    # Function to save the current option
    def save_selected_option(self):
        selected = self.selected_option.get()
        if selected:
            try:
                selected_int = int(selected)
                self.user_answers[self.current_question] =  selected_int
                if selected_int != self.questions[self.current_question]["correct_answer"]:
                    if self.current_question not in self.wrong_answers:
                        self.wrong_answers.append(self.current_question)
                else:
                    if self.current_question in self.wrong_answers:
                        self.wrong_answers.remove(self.current_question)
            except ValueError:
                self.user_answers[self.current_question] = None

    # Function to finish the quiz
    def finish_test(self):
        answer = messagebox.askyesno("Submit Quiz", "Are you sure you want to submit the quiz?")
        if answer:
            self.submit_quiz()
        else:
            self.current_question -= 1

    # Function to submit the quiz and show results
    def submit_quiz(self):
        self.stop_timer()
        self.save_selected_option()

        # Disable all option buttons
        for btn in self.option_buttons:
            btn.config(state="disabled")

        # Clear previous content
        self.question_label.place_forget()
        for btn in self.option_buttons:
            btn.place_forget()
        self.previous_button.place_forget()
        self.next_button.place_forget()
        self.review_button.place_forget()
        self.finish_button.place_forget()
        self.timer_label.place_forget()

        correct_count = 0
        missed_questions = []
        wrong_answers = []

        # Score
        for i, ans in enumerate(self.user_answers):
            correct = self.questions[i]["correct_answer"]
            if ans is None:
                missed_questions.append(i)
            elif ans == correct:
                correct_count += 1
            else:
                wrong_answers.append(i)

        result_frame = tk.Frame(self.frame, bg="#efdede")
        result_frame.pack(fill="both", expand=True)

        canvas = tk.Canvas(result_frame, bg="#efdede")
        scrollbar = tk.Scrollbar(result_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#efdede")

        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")


        # 🎉 Centered Test Completed Label
        result_title = tk.Label(scrollable_frame, text="🎉 Test Completed 🎉", font=("Arial", 20, "bold"), fg="black", bg="#efdede")
        result_title.pack(pady=(20, 10))

        # Centered Score Label
        score_text = f"Your Score: {correct_count}/{len(self.questions)}"
        score_label = tk.Label(scrollable_frame, text=score_text, font=("Arial", 18, "bold"), fg="black", bg="#efdede")
        score_label.pack(pady=(0, 5))

        # 🎁 Compliment Message Based on Score
        total_questions = len(self.questions)
        if correct_count == total_questions:
            compliment = "🌟 Excellent! You nailed it! 🌟"
        elif correct_count >= total_questions * 0.7:
            compliment = "💪 Great job! You're almost there!"
        elif correct_count >= total_questions * 0.4:
            compliment = "🙂 Keep practicing, you're improving!"
        else:
            compliment = "😅 Better luck next time!"

        compliment_label = tk.Label(scrollable_frame, text=compliment, font=("Arial", 16, "italic"), fg="green", bg="#efdede")
        compliment_label.pack(pady=(0, 20))    

        # Wrong answers
        if self.wrong_answers:
            wrong_label = tk.Label(scrollable_frame, text="❌ Wrong Answers:", font=("Arial", 12, "bold"), bg="#efdede", fg="red")
            wrong_label.pack(anchor="w", padx=10)

            for idx in self.wrong_answers:
                q = self.questions[idx]
                correct_answer_text = q["options"][q["correct_answer"] - 1]
                user_answer_text = (q['options'][self.user_answers[idx] - 1] if self.user_answers[idx] is not None else "Not Attempted")
                wrong_text = f"Q{idx+1}: {q['question']}\nYour Answer: {user_answer_text}\nCorrect Answer: {correct_answer_text}\n"
                lbl = tk.Label(scrollable_frame, text=wrong_text, font=("Arial", 11), bg="#efdede", fg="red", justify="left", wraplength=700)
                lbl.pack(anchor="w", padx=20, pady=5)

        # Missed questions
        if missed_questions:
            miss_label = tk.Label(scrollable_frame, text="⚠️ Missed Questions (Not Attempted):", font=("Arial", 12, "bold"), bg="#efdede", fg="orange")
            miss_label.pack(anchor="w", padx=10, pady=(10, 0))

            for idx in missed_questions:
                q = self.questions[idx]
                correct_answer = q["options"][q["correct_answer"] - 1]
                user_answer = (q["options"][self.user_answers[idx] - 1] if self.user_answers[idx] is not None else "Not Attempted")
                miss_text = (f"Q{idx+1}: {q['question']}\nYour Answer: {user_answer}\nCorrect Answer: {correct_answer}\n")
                fg_color = "orange" if user_answer == "Not Attempted" else "red"
                lbl = tk.Label(scrollable_frame, text=miss_text, font=("Arial", 11), bg="#efdede", fg=fg_color, justify="left", wraplength=700)
                lbl.pack(anchor="w", padx=20, pady=5)

        # Review later questions
        if self.review_later:
            review_label = tk.Label(scrollable_frame, text="⭐ Marked for Review:", font=("Arial", 12, "bold"), bg="#efdede", fg="blue")
            review_label.pack(anchor="w", padx=10, pady=(10, 0))
        
            for idx in self.review_later:
                q = self.questions[idx]
                correct_answer = q["options"][q["correct_answer"] - 1]
                user_answer = (q["options"][self.user_answers[idx] - 1] if self.user_answers[idx] is not None else "Not Attempted")
                review_text = (f"Q{idx+1}: {q['question']}\nYour Answer: {user_answer}\nCorrect Answer: {correct_answer}\n")
                fg_color = "black" if user_answer == "Not Attempted" else "blue"
                lbl = tk.Label(scrollable_frame, text=review_text, font=("Arial", 11), bg="#efdede", fg=fg_color, justify="left", wraplength=700)
                lbl.pack(anchor="w", padx=20, pady=5)

        # Retake button
        retry_button = tk.Button(scrollable_frame, text="Retake Quiz", command=self.restart_quiz, font=("Arial", 12), bg="#ace7bd")
        retry_button.pack(pady=20)

    # Function to display the score and wrong answers
    def show_score_and_wrong_answers(self):
        score_text = f"Your score: {self.score}/{len(self.questions)}"
        wrong_answers_text = ""
        if self.wrong_answers:
            wrong_answers_text = "\nWrong Answers:\n"
            for question_number in self.wrong_answers:
                question_data = self.questions[question_number - 1]
                question_text = question_data["question"]
                correct_answer = question_data["options"][question_data["correct_answer"] - 1]
                wrong_answers_text += f"Q{question_number}: {question_text}\nCorrect Answer: {correct_answer}\n"

        # Create a new window to display the score
        self.score_window = tk.Toplevel(self.root)
        self.score_window.title("Quiz Score")
        score_label = tk.Label(self.score_window, text=score_text + wrong_answers_text, font=("Arial", 14))
        score_label.pack()

        # Create a button to retake the quiz
        retry_button = tk.Button(self.score_window, text="Retake Quiz", command=self.restart_quiz)
        retry_button.pack()

    # Function to restart the quiz
    def restart_quiz(self):
        self.stop_timer()
        self.timer_id = None
        self.timer = 60
        self.current_question = 0
        self.score = 0
        self.wrong_answers = []
        self.review_later = [] 
        self.next_button.config(state="active")
        self.finish_button.config(state="active")
        self.user_answers = [None] * len(self.questions)
        self.score_label.config(text="")

        # Enable options again
        for btn in self.option_buttons:
            btn.config(state="normal")
        
        self.load_next_question()
        self.question_label.place(x=20, y=10, width=710, height=80)

        option_y_positions = [100, 150, 200, 250]
        for i, btn in enumerate(self.option_buttons):
            btn.place(x=75, y=option_y_positions[i], width=600, height=30)

        self.previous_button.place(x=80, y=310, width=120, height=30)
        self.review_button.place(x=300, y=310, width=150, height=30)
        self.next_button.place(x=550, y=310, width=120, height=30)
        self.finish_button.place(x=300, y=360, width=150, height=35)
        self.timer_label.place(x=275, y=410, width=200, height=25)

        # Clear result screen
        for widget in self.frame.winfo_children():
            if isinstance(widget, tk.Frame) or isinstance(widget, tk.Canvas):
                widget.destroy()

        # Hide the score window (if it exists) without closing it
        if self.score_window and self.score_window.winfo_exists():
            self.score_window.withdraw()

        # Load first question again
        self.load_next_question()
        self.update_timer()   

    # Function to show result directly
    def show_result_direct(self):
        correct_count = sum(
            1 for i, ans in enumerate(self.user_answers)
            if ans == self.questions[i]["correct_answer"]
        )
        result_text = f"Your Score: {correct_count}/{len(self.questions)}\n"
        if self.wrong_answers:
            result_text += "\nWrong Answers:\n"
            for idx in self.wrong_answers:
                q = self.questions[idx]
                result_text += f"Q{idx+1}: {q['question']}\nCorrect: {q['options'][q['correct_answer'] - 1]}\n\n"

        if self.review_later:
            result_text += "\nMarked for Review:\n"
            for idx in self.review_later:
                q = self.questions[idx]
                result_text += f"Q{idx+1}: {q['question']}\n\n"
        
        self.question_label.config(text="Test Completed")
        for btn in self.option_buttons:
            btn.place_forget()
        self.previous_button.place_forget()
        self.next_button.place_forget()
        self.review_button.place_forget()
        self.finish_button.place_forget()
        self.timer_label.place_forget()

        result_label = tk.Label(self.frame, text=result_text, font=("Arial", 12), justify="left", bg="#f8a3a3")
        result_label.place(x=30, y=100, width=690, height=350)
        
    # Function to update the timer
    def update_timer(self):
        if self.timer == 0:
            self.stop_timer()
            self.submit_quiz()
            return

        # Change timer color to red when it's less than 10 seconds
        timer_color = "red" if self.timer < 10 else "black"
        self.timer_label.config(text=f"Time Left : {self.timer} sec", fg=timer_color)
            
        # Change next button and finish button colors
        next_button_color = "green" if self.timer > 10 else "black"
        finish_button_color = "red" if self.timer <= 10 else "black"
            
        self.next_button.config(fg=next_button_color)
        self.finish_button.config(fg=finish_button_color)

        self.timer -= 1
        self.timer_id = self.root.after(1000, self.update_timer)

    # Function to stop the timer
    def stop_timer(self):
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None

if __name__ == "__main__":
    # Create a Tkinter window and initialize the QuizApp
    root = tk.Tk()
    center_window(root)
    app = QuizApp(root)
    root.mainloop()