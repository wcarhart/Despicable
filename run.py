import argparse
from subprocess import call

def build_run_command(args):
	cmd = 'docker run -it'
	mounts = ''

	if args.thread_max:
		thread_max = ' -e THREAD_MAX=\'-t {}\''.format(args.thread_max)
	else:
		thead_max = ' -e THREAD_MAX=\'\''
	cmd += thread_max

	if args.commands:
		docker_commands = []
		for command in args.commands:
			docker_commands.append('"'+command+'"')
		commands = ' -e COMMANDS=\'-c {}\''.format(docker_commands)
	else:
		commands = ' -e COMMANDS=\'\''
	cmd += commands

	if args.command_file:
		command_file = ' -e COMMAND_FILE=\'-f {}\''.format(args.command_file)
		mounts += ' --mount type=bind,source={0},target=/{0}'.format(args.command_file,)
	else:
		command_file = ' -e COMMAND_FILE=\'\''
	cmd += command_file

	if args.message:
		message = ' -e MESSAGE=\'-m {}\''.format(args.message)
	else:
		message = ' -e MESSAGE=\'\''
	cmd += message

	if args.log_level:
		log_level = ' -e LOG_LEVEL=\'--log-level {}\''.format(args.log_level)
	else:
		log_level = ' -e LOG_LEVEL=\'\''
	cmd += log_level

	if args.log_file:
		log_file = ' -e LOG_FILE=\'--log-file {}\''.format(args.log_file)
	else:
		log_file = ' -e LOG_FILE=\'\''
	cmd += log_file

	if args.omit_logs:
		omit_logs = ' -e OMIT_LOGS=\'-o\''
	else:
		omit_logs = ' -e OMIT_LOGS=\'\''
	cmd += omit_logs
	cmd += mounts

	suffix = ''.join(str(datetime.datetime.now()).replace(' ', '_').split('.')[:-1]).replace(':', '_')
	name = "despicable_" + str(suffix)
	cmd += ' --name {}'.format(name)

	cmd += ' despicable:latest'
	return cmd

def build_parser():
	parser = argparse.ArgumentParser(description=__doc__, formatter_class = argparse.ArgumentDefaultsHelpFormatter)
	parser.add_argument('-t', '--thread-max', type=int, default=8, required=False, help="maximum number of threads")
	parser.add_argument('-c', '--commands', type=str, nargs="+", required=False, help="a command to be parallelized (must be wrapped in double quotes)")
	parser.add_argument('-f', '--command-file', type=str, default="Despicablefile", required=False, help="name of the file that contains commands to be parallelized")
	parser.add_argument('-m', '--message', type=str, nargs=1, default="Processing", help="The message to be displayed during concurrent execution")
	parser.add_argument('--log-level', type=str, choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'], default="INFO", required=False, help="The level at which to log information during execution")
	parser.add_argument('--log-file', type=str, default="despicable_logs.txt", required=False, help="The file to log info to during execution")
	parser.add_argument('-o', '--omit-logs', action='store_true', default=False, required=False, help="if included, information will not be logged")
	# TODO: finish buffer dir
	parser.add_argument('-b', '--buffer-directory', type=str, default=None, required=False, help="if included, a buffer directory will be used (perhaps a common space where all users have access)")
	return parser

def main():
	parser = build_parser()
	args = parser.parse_args()

	build_command = 'docker build . -t despicable'
	call(build_command, shell=True)

	run_command = build_run_command(args)
	call(run_command, shell=True)

if __name__ == '__main__':
	main()