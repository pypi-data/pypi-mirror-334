#!/usr/bin/env python3

import pytest
from etag_generator import generate_etag

def test_tuple_should_fail():
	with pytest.raises(TypeError) as type_error:
		generate_etag((1,2))

	assert type_error.value.args[0] == "Unsupported type"

def test_python_object_should_fail():
	class RandoClass (object):
		pass

	rando_class = RandoClass()

	with pytest.raises(TypeError) as type_error:
		generate_etag(rando_class)

	assert type_error.value.args[0] == "Unsupported type"

def test_none_should_fail():
	with pytest.raises(TypeError) as type_error:
		generate_etag({"a-key":None})

	assert type_error.value.args[0] == "Unsupported type"

def test_bool_should_fail():
	with pytest.raises(TypeError) as type_error:
		generate_etag({"a-key":False})

	assert type_error.value.args[0] == "Unsupported type"