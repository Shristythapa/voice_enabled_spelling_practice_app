import os
import time
from gtts import gTTS
import pygame
import pandas as pd
from tkinter import *
import sqlite3
import datetime


# Load the word list and their meanings
data = pd.read_csv("D:/voice_enabled_spelling_pratice/spellings.csv", encoding='ISO-8859-1')
words = data.iloc[:, 0]
meanings = data['Meaning'] 
word_list = words.tolist()
results = pd.read_csv("D:/voice_enabled_spelling_pratice/results.csv", encoding='ISO-8859-1')


# Initialize pygame for audio playback
pygame.mixer.init()

# Variable to count correct answers
correct_count = 0

# Function to create and play the word audio
def play_word():
    global current_word_index
    word = word_list[current_word_index]
    meaning = meanings[current_word_index]  # Get the meaning of the current word
    
    # Display the meaning on the screen
    meaning_label.config(text=f"Meaning: {meaning}", fg="blue")
    
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
    global current_word_index, correct_count, results  # Make 'results' global here

    # Get the spelling entered by the user
    entered_spelling = spelling_entry.get()
    correct_spelling = word_list[current_word_index]
    
    current_date_str = datetime.datetime.now().strftime('%Y-%m-%d') 

    # Add the user-entered spelling to the current word index row
    data.at[current_word_index, current_date_str] = entered_spelling
    print(data.head())
    
    # Check if the entered spelling is correct
    if entered_spelling.lower() == correct_spelling.lower():
        result_label.config(text="Correct!", fg="green")
        correct_count += 1  # Increment correct answer count
    else:
        result_label.config(text=f"Incorrect! Correct spelling is '{correct_spelling}'", fg="red")
    
    # Move to the next word
    current_word_index += 1
    if current_word_index < len(word_list):
        spelling_entry.delete(0, 'end')  
        play_word()  
    else:
        result_label.config(text=f"All words played! You got {correct_count} out of {len(word_list)} correct.", fg="blue")
        play_button.config(state="disabled")
        next_button.config(state="disabled")

        new_row = {'Date': current_date_str, 'AttemptedWords': len(word_list), 'CorrectWords': correct_count}
        
        # Append the new row to the results DataFrame
        results = pd.concat([results, pd.DataFrame([new_row])], ignore_index=True)


        # Save the updated DataFrames back to the CSV files
        results.to_csv("D:/voice_enabled_spelling_pratice/results.csv", index=False)
        data.to_csv("D:/voice_enabled_spelling_pratice/spellings.csv", index=False)

      
        

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

# Label to show the meaning of the word
meaning_label = Label(root, text="Meaning: ", wraplength=400, justify="center")
meaning_label.pack(pady=10)

# Next Button to move to the next word
next_button = Button(root, text='Next', width=25, command=next_word)
next_button.pack(pady=10)

# Start by playing the first word
play_word()

# Run the Tkinter event loop
root.mainloop()
