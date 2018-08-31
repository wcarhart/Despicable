import queue

class Drain(object):
	def __init__(self, queue):
		self.queue = queue
	def __iter__(self):
		while True:
			try:
				yield self.queue.get_nowait()
			except:
				break
				