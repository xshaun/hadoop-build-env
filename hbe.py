#!/usr/bin/env python3 -B

import os
import yaml


class Log(object):
	"""
	@TODO
	to support log mechnism
	"""

	@staticmethod
	def info(msg):
		print('INFO: ' + msg)
		pass

	@staticmethod
	def warning(msg):
		print('WARNING: ' + msg)
		pass

	@staticmethod
	def error(msg):
		print('ERROR:' + msg)
		pass


def parse_settings(abspath_filename):
	if not os.path.isfile(abspath_filename):
		Log.error('not found yamlfile.')
		return None

	try:
		file = open(abspath_filename)
		ys = yaml.load(file)

		# check necessary fields within settings.yaml
		for item in ('mode', 'codepath', 'roles', 'steps'):
			if item not in ys:
				Log.error('not found \'' + item + '\' in yamlfile')

		return ys

	except Exception as e:
		Log.error('catched exceptions while loading yamlfile.')
	
	return None


def main():	
	ys = parse_settings(os.path.abspath('./settings.yaml'))
	
	for step in ys['steps']:
		a = ("scripts.%s" % (step))
		import a
		scripts.pre_compile_env.pre_compile_env(ys)
		globals()[step](ys)

if __name__ == '__main__':
	main()













