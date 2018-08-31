import sys
import os
from queue import *
from despicable import *
from spinner import Spinner
from exithooks import ExitHooks
import logging

def pwede_na(cmd_list, status, message):
	"""Minionese for 'can we start?'"""
	input_queue = Queue()
	output_queue = Queue()
	result_queue = Queue()

	total = len(cmd_list)
	for index, cmd in enumerate(cmd_list):
		cmd_tuple = (index, cmd)
		input_queue.put(cmd_tuple)
	threading_cap = total if total < THREAD_MAX else THREAD_MAX

	if thread_cap == 1:
		word = 'thread'
	else:
		word = 'threads'

	spawner = Nefario(input_queue, output_queue, result_queue, thread_cap)
	spawner.start()
	handler = Gru(result_queue, total, message)
	handler.start()
	spawner.join()
	handler.join()

	for thread_id, thread_message in Drain(output_queue):
		continue

def main():
	return

if __name__ == '__main__':
	main()