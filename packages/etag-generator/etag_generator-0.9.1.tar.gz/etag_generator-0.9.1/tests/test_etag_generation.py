#!/usr/bin/env python3

import pytest
from etag_generator import generate_etag

def test_basic_string():
	string="asdffdsaasdffdsa"

	generated = generate_etag(string)
	assert generated==string

def test_long_string():
	standard = "fa349d4d023683fe08e2cd03e3cc88d9f122950ba1f4170d2dd44b19c4dadbd1"
	with open("long_string.txt","r") as input:
		string = input.read()

	generated = generate_etag(string)
	assert generated == standard

def test_simple_int():
	value=12345
	standard="12345"
	generated = generate_etag(value)
	assert generated == standard

def test_simple_array():
	array = [1,2,3,4,5]
	# should be sha256sum("1:2:3:4:5:")
	standard = "ba971ac389cf4b822be3ca47776d17a1296a7dd5ba248739f323f5a7336345c0"

	generated = generate_etag(array)
	assert generated == standard

def test_forbidden_chars():
	"""even a very short string should be hashed if it contains forbidden characters."""
	string = 'asdf " fdsa'
	standard = "318f39091c4ed71fe5c750424cd8a8b85951a26ac7eac7eb6022165053f9dadf"
	generated = generate_etag(string)
	assert generated == standard

def test_dictionary():
	value = {"foo":"bar"}
	# should be sha256sum("foo:bar|")
	standard = "042b0bf8d3ce2fbf44d5a58db7c70dde997711580dda994084ac9abd54f32321"
	generated = generate_etag(value)
	assert generated == standard

def test_utf():
	"""non-ascii values are not allowed in etags"""
	value="❤️🙏🙏🏿🎉🎁"
	standard = "c6da378d61b12a44df56a8e4c4270c0244a5ff98b672a1a1795599e1aa2d055b"
	generated = generate_etag(value)
	assert generated == standard

def test_equivilent_objects_hash_same():
	obj1 = {"foo":"asdffdsa", "bar":"fdsaasdf"}
	obj2 = {"bar":"fdsaasdf", "foo":"asdffdsa"}
	# both should be sha256sum("bar:fdsaasdf|foo:asdffdsa|")

	standard = "ef68ca7f80f36c878cf2165b20caabf266d5ca787d68aa9b4c863f6c81e27c71"

	generated1 = generate_etag(obj1)
	generated2 = generate_etag(obj2)

	assert generated1 == generated2
	assert generated1 == standard
	assert generated2 == standard

def test_complicated_object():
	obj = {"first":{"foo":"asdffdsa","bar":"fdsaasdf"}, "bing":"bogus"}
	# should be sha256sum(bing:bogus|first:sha256sum(bar:fdsaasdf|foo:asdffdsa)|)
	#         = sha256sum(bing:bogus|first:ef68ca7f80f36c878cf2165b20caabf266d5ca787d68aa9b4c863f6c81e27c71|)
	standard = "9f2be2b4eeedbf0f5ceb61a3515f39516e1c384cb17af5fe904dd14fee19d081"
	generated = generate_etag(obj)
	assert generated == standard