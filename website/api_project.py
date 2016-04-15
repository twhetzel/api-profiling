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

app = Flask(__name__)
# Use SeaSurf to prevent cross-site request forgery
csrf = SeaSurf(app)


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
		demo_output = profiling.main(ws_input)

		# Get master_identifier_dictionary for value display in result page
		api_calls = profiling.get_calls_from_form(ws_input)
		master_id_dictionary = profiling.build_api_profile(api_calls)

		# Build dictionary of MIRIAM datatypes
		miriam_datatype_obj = miriam_datatype_identifiers.get_miriam_datatypes()
		miriam_name_dict = miriam_datatype_identifiers.build_miriam_name_dictionary(miriam_datatype_obj)
		
		# Get regex pattern data
		pattern_data = test_patterns.get_pattern_data()
		pattern_dict = test_patterns.make_pattern_dictionary(pattern_data)
		print pattern_dict


		return render_template('annotation_results.html', ws_input=ws_input, \
			demo_output=demo_output, master_id_dictionary=master_id_dictionary, \
			miriam_name_dict=miriam_name_dict, \
			pattern_dict=pattern_dict, re=re)
	else:
		app.logger.info('** Showing Home page **')
		return render_template('index.html')


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
