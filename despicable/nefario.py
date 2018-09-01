import threading
import Queue
from minion import Minion

class Nefario(threading.Thread):
	def __init__(self, input_queue, output_queue, result_queue, thread_max):
		threading.Thread.__init__(self)
		self.input_queue = input_queue
		self.output_queue = output_queue
		self.result_queue = result_queue
		self.thread_max = thread_max
	def run(self):
		thread_task(self.input_queue, self.output_queue, self.result_queue, self.thread_max)

def thread_task(input_queue, output_queue, result_queue, thread_max):
	for thread_id in range(thread_max):
		minion = Minion(thread_id, input_queue, output_queue, result_queue)
		minion.daemon = True
		minion.start()
	input_queue.join()