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


app = Flask(__name__)
# Use SeaSurf to prevent cross-site request forgery
csrf = SeaSurf(app)


# Home page for smartAPI Web service annotation
@app.route('/')
@app.route('/home', methods=['GET', 'POST'])
def show_home():
	if request.method == 'POST':
		ws_input = request.form['ws_input']
		app.logger.info(ws_input)
		profiling.py
		#return redirect(url_for('show_annotations'))
		return render_template('annotation_results.html', ws_input=ws_input)
	else:
		app.logger.info('** Showing Home page')
		return render_template('index.html')


# Show results of automatic annotation
# @app.route('/results/', methods=['GET', 'POST'])
# def show_annotations():
# 	return render_template('annotation_results.html')


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
