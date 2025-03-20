#!/usr/bin/env python3

"""
etag-generator.

A basic module for creating a stable ETag value from a JSON Object
(represented as a Python dict or array)
"""

import sys
import logging
from hashlib import sha256

# ensure trace is enabled...
TRACE=5
logging.addLevelName(TRACE,'TRACE')

logger = logging.getLogger(__name__)

__version__ = "0.9.1"
__author__  = 'Paul Williams'
__credits__ = 'EPAM Systems'

__all__     = ['generate_etag']

# List of types, and the generators that can do etags for each.
# Assume that if the type isn't in this list, that a call to str()
# can reduce it to a taggable item.
generators = {
	type({}): "do_generate_dict",
	type([]): "do_generate_list",
	type(""): "do_generate_str",
	type(1):  "do_generate_stringify",
	type(1.1): "do_generate_stringify"
}

# characters not allowed in a valid etag
disallowed_chars = '"'

# a sha256sum is 65 bytes -- no need to encode if the value is less than this!
min_sha_strlen = 65

# maximum size of a string before we use sha to shorten it.
max_sub_len = 100

def unsupported(something):
	raise TypeError("Unsupported type")


def do_generate_stringify(payload):
	return do_generate_str(str(payload))

def test_has_disallowed_chars(value):
	if any((c in disallowed_chars) for c in value):
		return True

	return any(ord(c) > 128 for c in value)

def do_generate_str(payload):
	if len(payload) >= max_sub_len or test_has_disallowed_chars(payload):
		return sha256(payload.encode('utf-8')).hexdigest()

	# no prohibited characters, short enough payload -- just use the string itself as etag.
	return payload


def do_generate_list(payload):
	m = sha256()
	for item in payload:
		m.update(str(generate_etag(item)).encode('utf-8'))
		m.update(":".encode('utf-8'))
	return m.hexdigest();


def do_generate_dict(payload):
	m = sha256()
	for item in sorted(payload.items()):
		gen_value = generate_etag(item[1])
		m.update(f"{item[0]}:{gen_value}|".encode('utf-8'))
		
	return m.hexdigest()


def generate_etag(payload):
	payload_type = type(payload)
	logger.log(TRACE,f"payload type {payload_type}")
	generator_name = generators.get(payload_type, "unsupported")
	generator = getattr(sys.modules[__name__], generator_name);
	return generator(payload)


if __name__ == "__main__":
	import json
	from colorlog import ColoredFormatter

	formatter = ColoredFormatter(
		"%(log_color)s%(levelname)-8s%(reset)s %(message)s",
		datefmt="%m-%d %H:%M:%S",
		reset=True,
		log_colors={
			'DEBUG':    'purple',
			'INFO':     'green',
			'WARNING':  'yellow',
			'ERROR':    'red',
			'CRITICAL': 'red,bg_white',
			'TRACE':	'yellow'
		}
	)

	handler = logging.StreamHandler()
	handler.setFormatter(formatter)
	logger = logging.getLogger(__name__)
	logger.addHandler(handler)
	logger.setLevel('TRACE')

	logger.info("==> Begin Run")

	for file in sys.argv[1:]:
		logger.info(f"evaluating {file}")
		with open(file,"r") as input:
			if file.endswith(".json"):
				logger.debug("json detected")
				data = json.load(input)
			else:
				logger.debug("text detected")
				data = input.read()
			etag = generate_etag(data)
			logger.info(f"final etag generated: {etag}")

	good=False
	logger.debug("trying tuple")
	try:
		generate_etag(("foo","bar"))
	except:
		good=True

	if not good:
		print("Didn't fail on tuple generation")

	logger.info("==> End Run")
