import time

class ChatBot():

	def query(self, string):
		time.sleep(1.5)
		return string + ' out'

if __name__ == '__main__':
	cb = ChatBot()
	print(1)
	cb.query('Hello')
	print(2)
	