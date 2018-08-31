import threading
import sys
import queue

class Gru(threading.Thread):
	def __init__(self, result_queue, total, message):
		threading.Thread.__init__(self)
		self.result_queue = result_queue
		self.total = total
		self.message = message
	def run(self):
		thread_task(self.result_queue, self.total, self.message)

def thread_task(result_queue, total, message):
	return