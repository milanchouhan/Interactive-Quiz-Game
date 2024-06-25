import tkinter as tk
from tkinter import messagebox, ttk
import random  # Import the random module
from quiz_data import quiz_data

# Function to start the quiz
def start_quiz():
    start_frame.pack_forget()  # Hide the start frame
    show_question()  # Show the first question frame
    start_timer()  # Start the timer

# Function to show the current question
def show_question():
    question_frame.pack()  # Show the question frame
    question = questions[current_question]  # Use the selected questions list
    qs_label.config(text=question["question"])

    choices = question["choices"]
    for i in range(4):
        choice_btns[i].config(text=choices[i], state="normal", style="TButton")

    feedback_label.config(text="")
    next_btn.config(state="disabled", style="TButton")

# Function to check the selected answer
def check_answer(choice):
    question = questions[current_question]  # Use the selected questions list
    selected_choice = choice_btns[choice]
    
    for button in choice_btns:
        button.config(state="disabled")
        button.config(style="TButton")  # Reset other buttons

    selected_choice.config(style="Selected.TButton")  # Change style of selected button

    selected_text = selected_choice.cget("text")
    if selected_text == question["answer"]:
        global score
        score += 1
        score_label.config(text="Score: {}/{}".format(score, len(questions)))  # Use the selected questions list
        feedback_label.config(text="Correct!", foreground="green")
    else:
        feedback_label.config(text="Incorrect!", foreground="red")
    
    next_btn.config(state="normal", style="Selected.TButton")  # Change style of next button

# Function to move to the next question
def next_question():
    global current_question
    current_question += 1

    if current_question < len(questions):  # Use the selected questions list
        show_question()
    else:
        show_result()

# Function to show the result
def show_result():
    question_frame.pack_forget()  # Hide the question frame

    # Calculate score percentage
    percentage = (score / len(questions)) * 100  # Use the selected questions list
    
    # Set the result color based on pass/fail
    result_color = "#210440" if percentage >= 50 else "red"
    result_text = "passed" if percentage >= 50 else "failed"

    # Create the result frame
    result_frame = tk.Frame(root, bg="#E5958E")  # Set background color for the result frame
    result_frame.pack(fill=tk.BOTH, expand=True)

    # Create the result label
    result_label = ttk.Label(
        result_frame,
        text="Quiz Completed!\nYour score: {:.2f}%".format(percentage),
        anchor="center",
        font=("Helvetica", 24),
        padding=20,
        background="#E5958E",  # Set background color for the result frame
        foreground="#210440"  # Set font color
    )
    result_label.pack(pady=20)

    # Comment: The passing marks is 50%
    passing_marks_label = ttk.Label(
        result_frame,
        text="The passing marks is ",
        font=("Helvetica", 16, "bold"),  # Increase font size and make "50%" bold
        background="#E5958E"
    )
    passing_marks_label.pack()

    passing_marks_value_label = ttk.Label(
        result_frame,
        text="50%",
        font=("Helvetica", 16, "bold"),  # Increase font size and make "50%" bold
        foreground="#210440",  # Set font color to #210440
        background="#E5958E"
    )
    passing_marks_value_label.pack()

    # Create the result status label
    result_status_label = ttk.Label(
        result_frame,
        text=f"You have {result_text} the quiz.",
        anchor="center",
        font=("Helvetica", 16),
        padding=20,
        background="#E5958E",
        foreground=result_color
    )
    result_status_label.pack()

# Function to handle the timer expiration
def timer_expired():
    messagebox.showinfo("Time's Up!", "Quiz time expired! Proceeding to results.")
    show_result()

# Function to start the timer
def start_timer():
    global timer_id, remaining_time
    remaining_time = timer_value.get()  # Set remaining time to the initial timer value
    update_timer()  # Update the timer display
    timer_id = root.after(1000, update_timer)  # Start the timer update loop

# Function to update the timer display
def update_timer():
    global remaining_time
    if remaining_time <= 0:
        timer_expired()  # Timer expired, show result
        return
    timer_label.config(text="Time Remaining: {} seconds".format(remaining_time), foreground="#210440", font=("Helvetica", 12, "bold"))  # Update timer label
    remaining_time -= 1
    timer_id = root.after(1000, update_timer)  # Schedule the next update

# Create the main window
root = tk.Tk()
root.title("Quiz App")
root.geometry("600x500")
root.configure(bg="#E5958E")  # Set background color of the root window

# Create custom styles
style = ttk.Style()
style.configure("Selected.TButton", background="#FFBA00", foreground="#FFBA00")  # Style for selected option and next button
style.configure("TProgressbar", background="#210440")  # Style for the progress bar

# Select random 30 questions from the quiz_data
questions = random.sample(quiz_data, 30)

# Create the start frame
start_frame = tk.Frame(root, bg="#E5958E")  # Set background color for the start frame
start_frame.pack(fill=tk.BOTH, expand=True)

# Create the start label
start_label = ttk.Label(
    start_frame,
    text="Welcome to the Quiz App!",
    anchor="center",
    font=("Helvetica", 24),
    padding=20,
    background="#E5958E"
)
start_label.pack(pady=20)

# Create the timer label and entry
timer_label = ttk.Label(
    start_frame,
    text="Set Timer (seconds):",
    font=("Helvetica", 16),
    background="#E5958E"
)
timer_label.pack()

timer_value = tk.IntVar(value=300)  # Default timer value (300 seconds = 5 minutes)
timer_entry = ttk.Entry(
    start_frame,
    textvariable=timer_value,
    font=("Helvetica", 16)
)
timer_entry.pack(pady=10)

# Create the timer instruction label
timer_instruction_label = ttk.Label(
    start_frame,
    text="In this quiz, you can set the timer by yourself to solve the given 30 Questions.",
    font=("Helvetica", 12),
    background="#E5958E",
    foreground="#210440"  # Set font color to #210440
)
timer_instruction_label.pack(pady=5)

# Create the start button
start_btn = ttk.Button(
    start_frame,
    text="Start Quiz",
    command=start_quiz  # Start both quiz and timer
)
start_btn.pack(pady=10)

# Create the question frame
question_frame = tk.Frame(root, bg="#E5958E")  # Set background color for the question frame

# Create the timer label in the question frame
timer_label = ttk.Label(
    question_frame,
    text="Time Remaining: 300 seconds",
    font=("Helvetica", 12, "bold"),
    foreground="#210440",  # Set font color to #210440
    background="#E5958E"
)
timer_label.pack(pady=(10, 0))

# Create the question label
qs_label = ttk.Label(
    question_frame,
    anchor="center",
    wraplength=500,
    padding=10,
    background="#E5958E",  # Set the background color of the question label
    font=("Helvetica", 18, "bold"),  # Set font to bold and increase size
    foreground="#DFCEBF"  # Set the color of the question text
)
qs_label.pack(pady=(10, 0))  # Reduce the top padding to adjust spacing

# Create the choice buttons
choice_btns = []
for i in range(4):
    button = ttk.Button(
        question_frame,
        command=lambda i=i: check_answer(i),
        style="TButton",
        width=30,  # Adjust button width for better alignment
        padding=(5, 10)  # Adjust button padding for better appearance
    )
    button.pack(pady=(5, 0))  # Reduce the top padding to adjust spacing
    choice_btns.append(button)

# Create the feedback label
feedback_label = ttk.Label(
    question_frame,
    anchor="center",
    padding=10,
    background="#E5958E"  # Set background color for the feedback label
)
feedback_label.pack(pady=(10, 0))  # Reduce the top padding to adjust spacing

# Create the score label
score = 0
score_label = ttk.Label(
    question_frame,
    text="Score: 0/{}".format(len(questions)),
    anchor="center",
    padding=10,
    background="#E5958E",  # Set background color for the score label
    foreground="#210440",  # Set font color to #210440
    font=("Helvetica", 16)  # Set font size slightly smaller than the question label
)
score_label.pack(pady=(10, 0))  # Reduce the top padding to adjust spacing

# Create the next button
next_btn = ttk.Button(
    question_frame,
    text="Next",
    command=next_question,
    state="disabled",
    style="TButton"  # Set initial style for the next button
)
next_btn.pack(pady=(10, 0))  # Reduce the top padding to adjust spacing

# Initialize the current question index
current_question = 0

root.mainloop()
