import threading
import sys
import Queue

class Gru(threading.Thread):
	def __init__(self, result_queue, total, message=""):
		threading.Thread.__init__(self)
		self.result_queue = result_queue
		self.total = total
		self.message = message
	def run(self):
		thread_task(self.result_queue, self.total, self.message)

def thread_task(result_queue, total, message):
	previous_thread_count = sys.maxint
	while result_queue.qsize() < total:
		thread_count = result_queue.qsize()
		if not thread_count == previous_thread_count:
			update(total, thread_count, message)
			previous_thread_count = thread_count
	update(total, total, "Done")

def update(total, progress, message):
	bar_length = 30
	index = progress

	if float(total) == 0:
		progress = 1.0
	else:
		progress = float(progress) / float(total)

	if progress >= 1.0:
		progress = 1.0

	if message == "":
		message = "Processing"

	block = int(round(bar_length * progress))
	progress_bar = "\r[{}] {:.0f}% ({})".format(">" * block + " " * (bar_length - block), round(progress * 100, 0), message)
	word = "task" if total - index == 1 else "tasks"
	progress_task = " {} {} remaining".format(total - index, word)

	print "\033[F\033[F\033[K" + progress_bar + "\n\033[K " + progress_task + "\r"
	