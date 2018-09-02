import argparse

def build_run_command(args):
	return

def build_parser():
	parser = argparse.ArgumentParser(description=__doc__, formatter_class = argparse.ArgumentDefaultsHelpFormatter)
	parser.add_argument('-t', '--thread-max', type=int, default=8, required=False, help="maximum number of threads")
	parser.add_argument('-c', '--commands', type=str, nargs="+", required=False, help="a command to be parallelized (must be wrapped in double quotes)")
	parser.add_argument('-f', '--command-file', type=str, default="Despicablefile", required=False, help="name of the file that contains commands to be parallelized")
	parser.add_argument('-m', '--message', type=str, nargs=1, default="Processing", help="The message to be displayed during concurrent execution")
	parser.add_argument('--log-level', type=str, choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'], default="INFO", required=False, help="The level at which to log information during execution")
	parser.add_argument('--log-file', type=str, default="despicable_logs.txt", required=False, help="The file to log info to during execution")
	parser.add_argument('-o', '--omit-logs', action='store_true', default=False, required=False, help="if included, information will not be logged")
	return parser

def main():
	parser = build_parser()
	args = parser.parse_args()

	build_run_command(args)

if __name__ == '__main__':
	main()