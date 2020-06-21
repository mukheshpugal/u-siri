import speech_recognition as sr
import pyaudio as pa

r = sr.Recognizer()

with sr.Microphone() as source:
	r.adjust_for_ambient_noise(source)
	print("Speak now")
	audio = r.listen(source)
	text = r.recognize_google(audio)
	print(text)
