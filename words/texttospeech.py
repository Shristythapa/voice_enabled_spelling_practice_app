import os
import time
from gtts import gTTS
import pygame  
import pandas as pd

data = pd.read_excel("excles.xlsx")
data.head()
words = data.iloc[:, 0]
word_list = words.tolist()
language = 'en'
pygame.mixer.init()
for i, word in enumerate(word_list):
    try:
        mp3_file = f"{word}.mp3"
        if not os.path.exists(mp3_file):
            tts = gTTS(text=word, lang=language, slow=False)
            tts.save(mp3_file)
            print(f"Created audio file: {mp3_file}")
        else:
            print(f"Audio file already exists: {mp3_file}")

        print(f"Playing word: {word}")
        pygame.mixer.music.load(mp3_file)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():  
            time.sleep(1)

        time.sleep(10)

    except Exception as e:
        print(f"An error occurred while processing the word '{word}': {e}")
print("All words played!")
