import os
import time
from gtts import gTTS
import pygame
import pandas as pd
from tkinter import *

# Load the word list
data = pd.read_excel("D:/text-to-speach/excles.xlsx")
words = data.iloc[:, 0]
word_list = words.tolist()

# Add a new column for correctness (1 for correct, 0 for incorrect)
data['Correctness'] = [None] * len(data)  # Initialize the column with None

# Initialize pygame for audio playback
pygame.mixer.init()

# Dictionary to store correct word as key and user-entered spelling as value
spelling_attempts = {}

# Variable to count correct answers
correct_count = 0

# Function to create and play the word audio
def play_word():
    global current_word_index
    word = word_list[current_word_index]
    
    try:
        mp3_file = f"words/{word}.mp3"
        if not os.path.exists(mp3_file):
            tts = gTTS(text=word, lang='en', slow=False)
            tts.save(mp3_file)
            print(f"Created audio file: {mp3_file}")
        else:
            print(f"Audio file already exists: {mp3_file}")

        print(f"Playing word: {word}")
        pygame.mixer.music.load(mp3_file)
        pygame.mixer.music.play()

    except Exception as e:
        print(f"An error occurred while processing the word '{word}': {e}")

# Function to handle the "Next" button
def next_word():
    global current_word_index, correct_count
    
    # Get the spelling entered by the user
    entered_spelling = spelling_entry.get()
    correct_spelling = word_list[current_word_index]
    
    # Add the word and the entered spelling to the dictionary
    spelling_attempts[correct_spelling] = entered_spelling
    
    # Check if the entered spelling is correct
    if entered_spelling.lower() == correct_spelling.lower():
        result_label.config(text="Correct!", fg="green")
        correct_count += 1  # Increment correct answer count
        data.at[current_word_index, 'Correctness'] = 1  # Mark as correct (1)
    else:
        result_label.config(text=f"Incorrect! Correct spelling is '{correct_spelling}'", fg="red")
        data.at[current_word_index, 'Correctness'] = 0  # Mark as incorrect (0)
    
    # Move to the next word
    current_word_index += 1
    if current_word_index < len(word_list):
        spelling_entry.delete(0, 'end')  # Clear the entry field
        play_word()  # Automatically play the next word
    else:
        result_label.config(text=f"All words played! You got {correct_count} out of {len(word_list)} correct.", fg="blue")
        play_button.config(state="disabled")
        next_button.config(state="disabled")
        
        # Print the spelling attempts dictionary
        print("Spelling attempts:")
        print(spelling_attempts)
        
        # Save the updated DataFrame with the new "Correctness" column to the Excel file
        data.to_excel("../updated_excels.xlsx", index=False)  # Save to a new Excel file

# Initialize the current word index
current_word_index = 0

# Create the GUI using tkinter
root = Tk()
root.title("Spelling Practice")

# Play Button to play the current word
play_button = Button(root, text='Play', width=10, command=play_word)
play_button.pack(pady=10)

# Label for spelling instruction
spelling_label = Label(root, text='Enter spelling:')
spelling_label.pack(pady=5)

# Text entry for the user to input spelling
spelling_entry = Entry(root, width=30)
spelling_entry.pack(pady=5)

# Label to show the result of spelling
result_label = Label(root, text="")
result_label.pack(pady=5)

# Next Button to move to the next word
next_button = Button(root, text='Next', width=25, command=next_word)
next_button.pack(pady=10)

# Start by playing the first word
play_word()

# Run the Tkinter event loop
root.mainloop()