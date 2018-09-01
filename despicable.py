import sys
import os
import argparse
import logging
import signal
import time
import datetime
import Queue
import traceback

from despicable import *
from spinner import Spinner

def pwede_na(cmd_list, message):
	"""Minionese for 'can we start?'"""
	input_queue = Queue.Queue()
	output_queue = Queue.Queue()
	result_queue = Queue.Queue()

	total = len(cmd_list)
	for index, cmd in enumerate(cmd_list):
		cmd_tuple = (index, cmd)
		input_queue.put(cmd_tuple)
	thread_cap = total if total < THREAD_MAX else THREAD_MAX

	if thread_cap == 1:
		word = 'thread'
	else:
		word = 'threads'

	print "\n"
	spinner.start()
	spawner = Nefario(input_queue, output_queue, result_queue, thread_cap)
	spawner.start()
	handler = Gru(result_queue, total, message)
	handler.start()
	spawner.join()
	handler.join()

	for thread_id, thread_message in Drain(output_queue):
		continue

	spinner.stop()

def parse_commands(commands, command_file):
	command_list = []
	if commands:
		for command in commands:
			command_list.append(command)

	if command_file:
		with open(command_file) as f:
			commands_from_file = f.read().splitlines()
			for command in commands_from_file:
				command_list.append(command)
		f.close()

	if len(command_list) == 0:
		logging.error("No valid commmands detected")
		sys.exit(1)
		
	pwede_na(command_list, "Testing")

def signal_handler():
	spinner.stop()
	print " Aborting despicable..."
	time.sleep(0.5)
	logging.debug("Exiting from keyboard interrupt")
	sys.exit(0)

def build_parser():
	parser = argparse.ArgumentParser(description=__doc__, formatter_class = argparse.ArgumentDefaultsHelpFormatter)
	parser.add_argument('-t', '--thread-max', type=int, default=8, required=False, help="maximum number of threads")
	parser.add_argument('-c', '--commands', type=str, nargs="+", required=False, help="a command to be parallelized (must be wrapped in double quotes)")
	parser.add_argument('-f', '--command-file', type=str, default=None, required=False, help="name of the file that contains commands to be parallelized")
	log_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
	parser.add_argument('--log-level', type=str, choices=log_levels, default="INFO", required=False, help="The level at which to log information during execution")
	parser.add_argument('--log-file', type=str, default="despicable_logs.txt", required=False, help="The file to log info to during execution")
	# TODO: finish omot-logs
	parser.add_argument('-o', '--omit-logs', action='store_true', default=False, help="if included, information will not be logged")
	return parser

def main():
	parser = build_parser()
	args = parser.parse_args()
	
	signal.signal(signal.SIGINT, signal_handler)

	global spinner
	spinner = Spinner()

	numeric_log_level = getattr(logging, args.log_level.upper(), None)

	frmt = '%(levelname)s %(asctime)s %(module)s (%(funcName)s): %(message)s'
	logging.basicConfig(
		filename="despicable_logs.txt",
		level=numeric_log_level,
		format=frmt,
		datefmt="%Y-%m-%d %H:%M:%S"
	)

	global THREAD_MAX
	THREAD_MAX = args.thread_max

	# TODO
	parse_commands(args.commands, args.command_file)


if __name__ == '__main__':
	main()