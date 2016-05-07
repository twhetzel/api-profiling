from flask import Flask, render_template, request, redirect, jsonify, \
    url_for, flash
from flask.ext.seasurf import SeaSurf
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
import yaml

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
@app.route('/catcomplete', methods=['GET'])
def catcomplete():
	search = request.args.get('q')

	keypath = request.args.get('data')
	print "** KP:", keypath

	# Build dictionary of MIRIAM datatypes for Autocomplete
	miriam_datatype_obj = miriam_datatype_identifiers.get_miriam_datatypes()
	category_data = miriam_datatype_identifiers.build_miriam_autocomplete_data(miriam_datatype_obj)
	
	# Use keypath to get pattern matches, values of type list
	for key,value in demo_output.iteritems():
		if keypath == key:
			if isinstance(value, list):
				autocomplete_data = []
				print "** K - TEST:", keypath, key,value, "\n"
				for items in value:
					autocomplete_obj = {}
					for k,v in items.iteritems():
						autocomplete_obj['value'] = k
						autocomplete_obj['label'] = v
						autocomplete_obj['category'] = 'Pattern Matches'
						autocomplete_data.append(autocomplete_obj)
				#print "** AC:",autocomplete_data
				category_data.extend(autocomplete_data)
				#print category_data
	
	print "** Cat-Data:", category_data, "\n"
 	return jsonify(category_data=category_data)


# Create Autocomplete data for Pattern Matches from individual keypath value
@app.route('/pattern_match_resources', methods=['GET', 'POST'])
def pattern_match_resources():
	#autocomplete_data = []
	data = request.args.get('id')
	print "** Keypath from annotation template:", id

	# Autocomplete data for each keypath pattern value match
	# my_list = ast.literal_eval(data)
	# for item in my_list:
	# 	autocomplete_obj = {}
	# 	for k,v in item.iteritems():
	# 		autocomplete_obj['value'] = k
	# 		autocomplete_obj['label'] = v
	# 		autocomplete_obj['category'] = 'Pattern Matches'
	# 		autocomplete_data.append(autocomplete_obj)
	
	#print "** Data:",autocomplete_data, "\n"
	#print type(autocomplete_data)
	#return "success"

	# All Miriam autocomplete data
	#miriam_datatype_obj = miriam_datatype_identifiers.get_miriam_datatypes()
	#category_data = miriam_datatype_identifiers.build_miriam_autocomplete_data(miriam_datatype_obj)
	
	# Combine two data sets
	#autocomplete_data.extend(category_data)

	# Encode to pass as parameter
	#formatted_data = json.dumps(data)
	#return jsonify(autocomplete_data=autocomplete_data)
	return redirect(url_for('catcomplete', data=data))


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
