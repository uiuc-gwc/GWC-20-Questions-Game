import tkinter as tk
from tkinter import messagebox, ttk
from ttkbootstrap import Style
from quiz_data import quiz_data
import numpy as np
'''Game Logic'''


def compute_entropy(arr):
  ratio = np.sum(arr) / len(arr)
  if ratio == 0 or ratio == 1:
    return 0
  return -np.log2(ratio) * ratio - np.log2(1 - ratio) * (1 - ratio)


num_of_q = 10
num_of_char = 10
randomTable = np.random.randint(2, size=(num_of_char, num_of_q))
appMe = np.arange(0, num_of_char, dtype='int')
randomTable = np.concatenate((appMe[:, None], randomTable), axis=1)
table = randomTable


def compute_entropy_table(table):
  entropies = []
  for j in range(1, table.shape[1]):
    entropies.append(compute_entropy(table[:, j]))
  return entropies


#Helper Functions
def get_max_index(arr):
  if np.max(arr) == 0:
    return None
  return np.argmax(arr) + 1


def subset(table, col_index, value):
  #subset the table by all rows where the col given by col_index, is equal to value
  return table[table[:, col_index] == value, :]


def give_next_question(table):
  entropies = compute_entropy_table(table)
  return get_max_index(entropies)


def compute_next_table(table, question_ind, answer):
  #subset the table by rows based on the question and answer
  new_table = subset(table, question_ind, answer)
  #get rid of the column where we asked the question to avoid asking it again
  new_table[:, question_ind] = 0
  return new_table


'''Game Logic'''

all_answers = []


def compute_character(all_answers):
  return "Harry Potter"


# Function to display the current question and choices
def show_question():
  # Get the current question from the quiz_data list
  question = quiz_data[current_question]
  qs_label.config(text=question["question"])

  # Display the choices on the buttons
  choices = question["choices"]
  for i in range(2):
    choice_btns[i].config(text=choices[i],
                          state="normal")  # Reset button state

  # Clear the feedback label and disable the next button
  feedback_label.config(text="")
  next_btn.config(state="disabled")


# Function to check the selected answer and provide feedback
def store_answer(choice):
  all_answers.append(choice)
  #print(all_answers)
  global table
  print(table)
  print(current_question)
  table = compute_next_table(table, current_question, all_answers[-1])
  # Get the current question from the quiz_data list
  # Check if the selected choice matches the correct answer
  #if selected_choice == question["answer"]:
  # Update the score and display it
  global score
  score += 1
  score_label.config(
      text="Questions Answered: {}/{}".format(score, len(quiz_data)))
  #feedback_label.config(text="Correct!", foreground="green")
  #else:
  #feedback_label.config(text="Incorrect!", foreground="red")
  # Disable all choice buttons and enable the next button
  for button in choice_btns:
    button.config(state="disabled")
  next_btn.config(state="normal")


# Function to move to the next question
def next_question():
  global current_question
  print(table)
  current_question = give_next_question(table)

  if current_question != None and table.shape[0] >= 2:
    # If there are more questions, show the next question
    show_question()
  else:
    # If all questions have been answered, display the final score and end the quiz
    messagebox.showinfo("Quiz Completed",
                        "Quiz Completed!, Final Guess " + str(table[0, 0]))
    root.destroy()


# Create the main window
root = tk.Tk()
root.title("Quiz App")
root.geometry("400x600")
style = Style(theme='flatly')

# Configure the font size for the question and choice buttons
style.configure("TLabel", font=("Helvetica", 15))
style.configure("TButton", font=("Helvetica", 10))

# Create the question label
qs_label = ttk.Label(root, anchor="center", wraplength=500, padding=10)
qs_label.pack(pady=10)

# Create the choice buttons
choice_btns = []
for i in range(2):
  button = ttk.Button(root, command=lambda i=i: store_answer(i))
  button.pack(pady=5)
  choice_btns.append(button)

# Create the feedback label
feedback_label = ttk.Label(root, anchor="center", padding=10)
feedback_label.pack(pady=10)

# Initialize the score
score = 0

# Create the score label
score_label = ttk.Label(root,
                        text="Score: 0/{}".format(len(quiz_data)),
                        anchor="center",
                        padding=10)
score_label.pack(pady=10)

# Create the next button
next_btn = ttk.Button(root,
                      text="Next",
                      command=next_question,
                      state="disabled")
next_btn.pack(pady=10)

# Initialize the current question index
current_question = 0

# Show the first question
next_question()

# Start the main event loop
root.mainloop()
