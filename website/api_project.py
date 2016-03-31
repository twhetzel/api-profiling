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

from scripts import profiling


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
		return render_template('annotation_results.html', ws_input=ws_input, \
			demo_output=demo_output)
	else:
		app.logger.info('** Showing Home page **')
		return render_template('index.html')


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
