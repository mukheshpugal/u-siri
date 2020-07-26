import speech_recognition as sr

class Recognizer():

	def __init__(self, ):
		self.r = sr.Recognizer()
		self.m = sr.Microphone()

		with self.m as source: self.r.adjust_for_ambient_noise(source)

	def record(self):
		with self.m as source: self.audio = self.r.listen(source)

	def decode(self):
		try:
			text = self.r.recognize_google(self.audio)
		except sr.UnknownValueError:
			return('Could you repeat?', True)
		except sr.RequestError:
			return('Couldn\'t connect to the server', True)

		return(text, False)
