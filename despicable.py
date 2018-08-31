import sys
import os
import argparse
import logging
import signal
import atexit
import time
import datetime

from queue import *
from despicable import *

from spinner import Spinner
from exithooks import ExitHooks

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

def signal_handler():
	spinner.stop()
	print " Aborting despicable..."
	time.sleep(0.5)
	logging.debug("Exiting from keyboard interrupt")
	sys.exit(0)

def exit_handler():
	spinner.stop()
	if hooks.exit_code is not None and not hooks.exit_code == 0:
		logging.error("Exiting with error code {}".format(hooks.exit_code))
	elif hooks.exception is not None:
		logging.error("Exiting due to uncaught exception: \n{}".format(hooks.exception))
		traceback.print_exc()
	else:
		logging.debug("Clean exit")
	return

def build_parser():
	parser = argparse.ArgumentParser(description=__doc__, formatter_class = argparse.ArgumentDefaultsHelpFormatter)
	parser.add_argument('-t', '--thread-max', type=int, default=8, help="maximum number of threads")
	parser.add_argument('-c', '--command', type=string, help="a command to be parallelized (must be wrapped in double quotes)")
	parser.add_argument('-f', '--command-file', type=string, help="name of the file that contains commands to be parallelized")
	return parser

def main():
	parser = build_parser()
	args = parser.parse_args()
	
	signal.signal(signal.SIGINT, signal_handler)
	global hooks
	hooks = ExitHooks()
	hooks.hook()
	atexit.register(exit_handler)

	global spinner
	spinner = Spinner()

	frmt = '%(levelname)s %(asctime)s %(module)s (%(funcName)s): %(message)s'
	logging.basicConfig(
		filename="despicable_logs.txt",
		level=numeric_logging_level,
		format=frmt,
		datefmt="%Y-%m-%d %H:%M:%S"
	)

	

if __name__ == '__main__':
	main()