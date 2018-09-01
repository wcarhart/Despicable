import threading
import sys
import Queue

from subprocess import PIPE
from subprocess import Popen

class Minion(threading.Thread):
	def __init__(self, thread_id, input_queue, output_queue, result_queue):
		threading.Thread.__init__(self)
		self.thread_id = thread_id
		self.input_queue = input_queue
		self.output_queue = output_queue
		self.result_queue = result_queue
	def run(self):
		thread_task(self.thread_id, self.input_queue, self.output_queue, self.result_queue)

def thread_task(thread_id, input_queue, output_queue, result_queue):
	while True:
		cmd_id, cmd = input_queue.get()
		thread_tuple = (thread_id, "Starting thread for CID {}: {}".format(cmd_id, cmd))
		output_queue.put(thread_tuple)

		proc = Popen(cmd, stdout=PIPE, shell=True)
		out, err = proc.communicate()

		thread_tuple = (thread_id, "STDOUT from CID {}: ".format(cmd_id) + out)
		output_queue.put(thread_tuple)
		thread_tuple = (thread_id, "STDERR from CID {}: ".format(cmd_id) + str(err))
		output_queue.put(thread_tuple)
		input_queue.task_done()
		result_queue.put(cmd)
