# Import to enable Python2/3 compatible code
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import
from future.utils import iteritems

from flask import Flask, render_template, request, redirect, jsonify, \
    url_for, flash, Response
import random
import string
import logging
import json
import httplib2
import requests
from flask import make_response
from datetime import datetime

from scripts import profiling, miriam_datatype_identifiers, test_patterns, data_registry_urls
import re
import copy
import ast
from collections import deque
import collections


app = Flask(__name__)


@app.route('/_annotated_data', methods=['GET'])
def _get_data():
    js = json.dumps(data)
    resp = Response(js, status=200, mimetype='application/json')
    resp.headers['Link'] = 'http://http://smart-api.info/profiler/'
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


# Home page for smartAPI Web service annotation
@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def show_home():
	if request.method == 'POST' and request.form['ws_input']:
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

		# Get dictionary of MIRIAM Ids and namespace URLs
		data_registry_id_url_dict = data_registry_urls.build_miriam_url_dictionary()

		return render_template('annotation_results.html', ws_input=ws_input, \
			demo_output=demo_output, master_id_dictionary=master_id_dictionary, \
			miriam_name_dict=miriam_name_dict, \
			all_pattern_dict=all_pattern_dict, re=re, iteritems=iteritems,
			data_registry_id_url_dict=data_registry_id_url_dict)
	else:
		app.logger.info('** Showing Home page **')
		return render_template('index.html')

# From Hello World Sample, https://github.com/GoogleCloudPlatform/python-docs-samples/blob/master/appengine/flexible/hello_world/main.py
@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500


if __name__ == '__main__':
    app.debug = True
    app.run(host='127.0.0.1', port=8081)
