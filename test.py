# Import the required module for text
# to speech conversion
from gtts import gTTS

# This module is imported so that we can
# play the converted audio
import os
from playsound import playsound

# The text that you want to convert to audio
mytext = 'Using time is over! Shutting down in 1 minute...'

# Language in which you want to convert
language = 'en'

# Passing the text and language to the engine,
# here we have marked slow=False. Which tells
# the module that the converted audio should
# have a high speed
myobj = gTTS(text=mytext, lang=language, slow=False)

# Saving the converted audio in a mp3 file named
# welcome
myobj.save("using_time_over.mp3")

# Playing the converted file
playsound('using_time_over.mp3')
