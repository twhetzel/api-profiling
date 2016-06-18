from flask import Flask, render_template, request, redirect, jsonify, \
    url_for, flash
from flask_seasurf import SeaSurf
import random
import string
import logging
import json
import httplib2
import requests
from flask import make_response
from datetime import datetime

from scripts import profiling, miriam_datatype_identifiers, test_patterns
import re
import copy
import ast
from collections import deque
import collections


app = Flask(__name__)
# Use SeaSurf to prevent cross-site request forgery
csrf = SeaSurf(app)


# TEST Autocomplete-1
# From: http://ampersandacademy.com/tutorials/flask-framework-ajax-autocomplete/
NAMES=["abc","abcd","abcde","abcdef", "ab"]
@csrf.exempt
@app.route("/autocomplete")
def autocomplete():
    return render_template('autocomplete.html')

@csrf.exempt
@app.route('/ajaxautocomplete',methods=['POST', 'GET'])
def ajaxautocomplete():
	if request.method=='POST':
		# Build dictionary of MIRIAM datatypes
		miriam_datatype_obj = miriam_datatype_identifiers.get_miriam_datatypes()
		miriam_name_dict = miriam_datatype_identifiers.build_miriam_name_dictionary(miriam_datatype_obj)
		#result = [{"value": "USA", "data": "United States"}, {"value": "UK","data": "United Kingdom"}]
		result = [{'value': 'MIR:00000466', 'data': 'WormBase RNAi'}, {'value': 'MIR:00000031', 'data': 'Wormpep'}, {'value': 'MIR:00000186', 'data': 'Xenbase'}]
	return json.dumps({"suggestions":result})
# END TEST Autocomplete-1


# Autocomplete with categories of MIRIAM Datatypes
@csrf.exempt
@app.route('/catcomplete', methods=['POST'])
def catcomplete():
	# Get keypath passed from template
	keypath = request.json['variable']

	# Build dictionary of MIRIAM datatypes for Autocomplete
	miriam_datatype_obj = miriam_datatype_identifiers.get_miriam_datatypes()
	category_data = miriam_datatype_identifiers.build_miriam_autocomplete_data(miriam_datatype_obj)
	
	# Update category value by appending new deque item to left of category_data deque
	for key,value in demo_output.iteritems():
		# Use keypath passed from template to get pattern matches
		if keypath == key:
			if isinstance(value, list):
				autocomplete_data_deque = deque()
				for items in reversed(value):
					autocomplete_obj = {}
					for k,v in items.iteritems():
						autocomplete_obj['value'] = k
						autocomplete_obj['label'] = v
						autocomplete_obj['category'] = 'Pattern Matches'
						autocomplete_data_deque.append(autocomplete_obj)
				# Remove existing object with same value from category_data
				category_data = _remove_duplicate_items(category_data, value)
				# Add pattern match category item 
				category_data.extendleft(autocomplete_data_deque)
				# Convert to use jsonify
				category_data = list(collections.deque(category_data))
	return jsonify(category_data=category_data)


# Autocomplete using Select2
@csrf.exempt
@app.route('/select2ResourceAutocomplete', methods=['POST'])
def select2ResourceAutocomplete():
	# Get keypath passed from template
	keypath = request.json['variable']
	print keypath

	# Build dictionary of MIRIAM datatypes for Autocomplete
	miriam_datatype_obj = miriam_datatype_identifiers.get_miriam_datatypes()
	resource_list = miriam_datatype_identifiers.build_miriam_autocomplete_data(miriam_datatype_obj)

	if keypath == 'None':
		return jsonify(resource_list=resource_list)
	else:
		print "-- Add PM values"

	
	# Update category value by appending new deque item to left of category_data deque
	for key,value in demo_output.iteritems():
		# Use keypath passed from template to get pattern matches
		if keypath == key:
			if isinstance(value, list):
				autocomplete_data_deque = deque()
				for items in reversed(value):
					autocomplete_obj = {}
					for k,v in items.iteritems():
						autocomplete_obj['value'] = k
						autocomplete_obj['label'] = v
						autocomplete_obj['category'] = 'Pattern Matches'
						autocomplete_data_deque.append(autocomplete_obj)
				# Remove existing object with same value from category_data
				category_data = _remove_duplicate_items(category_data, value)
				# Add pattern match category item 
				category_data.extendleft(autocomplete_data_deque)
				# Convert to use jsonify
				category_data = list(collections.deque(category_data))
	return jsonify(resource_list=resource_list)


# Autocomplete using Select2
@csrf.exempt
@app.route('/select2Autocomplete', methods=['GET', 'POST'])
def select2Autocomplete():
	print "** DEBUG: select2Autocomplete() called"
	jsonData = request.json["variable"]
	print "VAR-KP: ",jsonData

	if request.method == 'POST':
		print "POST request"
		
		resource_list = [{'text': 'Pattern Match', 'children': [{'id': 'value one','text': 'Text one to display'}, \
	{'id': 'value two','text': 'Text two to display'}]}, {'text': 'All Resources', 'children': \
	[{'id': 'resource one','text': 'Resource one to display'}, \
	{'id': 'resource two','text': 'Resource two to display'}]}]
		return jsonify(resource_list=resource_list)
	
	else:
		print "GET request"

	resource_list = [{'text': 'All Resources', 'children': \
	[{'id': 'resource one','text': 'Resource one to display'}, \
	{'id': 'resource two','text': 'Resource two to display'}]}]

	# resource_list = [{'id': 'MIR:00000555', 'text': 'My WormBase RNAi'}, \
	# 	{'id': 'MIR:11100545', 'text': 'My Wormpep'}, {'id': 'MIR:11100777', 'text': 'A Test Resource'}]
	return jsonify(resource_list=resource_list)


# Remove object with same MIRIAM ID to prevent duplicates in autocomplete 
def _remove_duplicate_items(category_data, value):
	id_list = []
	# Iterate through list and get keys
	for value_dict_id in value:
		for k in value_dict_id.keys():
			id_list.append(k)
	
	for obj in list(category_data):
		for list_item in id_list:
			if list_item == obj['value']:
				category_data.remove(obj)
	return category_data


# Home page for smartAPI Web service annotation
@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def show_home():
	if request.method == 'POST':
		ws_input = request.form['ws_input']
		app.logger.info(ws_input)
		# api_calls_to_profile = getattr(profiling, 'get_calls')()
		# app.logger.info(api_calls_to_profile)
		# demo_output = getattr(profiling, 'build_api_profile')(api_calls_to_profile)
		# #app.logger.info(demo_output)
		global demo_output
		demo_output = profiling.main(ws_input)

		# Get master_identifier_dictionary for value display in result page
		api_calls = profiling.get_calls_from_form(ws_input)
		master_id_dictionary = profiling.build_api_profile(api_calls)

		# Build dictionary of MIRIAM datatypes
		miriam_datatype_obj = miriam_datatype_identifiers.get_miriam_datatypes()
		miriam_name_dict = miriam_datatype_identifiers.build_miriam_name_dictionary(miriam_datatype_obj)
		
		# Get regex pattern data
		all_pattern_data = test_patterns.get_all_pattern_data()
		all_pattern_dict = test_patterns.make_pattern_dictionary(all_pattern_data)


		return render_template('annotation_results.html', ws_input=ws_input, \
			demo_output=demo_output, master_id_dictionary=master_id_dictionary, \
			miriam_name_dict=miriam_name_dict, \
			all_pattern_dict=all_pattern_dict, re=re)
	else:
		app.logger.info('** Showing Home page **')
		return render_template('index.html')


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
