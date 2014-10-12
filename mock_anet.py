#!/usr/bin/python

# This is a simple mock Authorize.net portal.
# Usage: direct your payment form to e.g. http://127.0.0.1:9000 instead of https://test.authorize.net/gateway/transact.dll
# Open django shell: "python manage.py shell"
#
# Then simply "import mock_anet" to start the server on port 9000
#
#
# The MIT License (MIT)
#
# Copyright (c) <2013> <Sergey Orshanskiy>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from os import curdir, sep
import cgi

from random import randrange, seed
seed(28399328)
import hashlib

PORT_NUMBER = 9000



# Set credentials for test Authorize.net
# MD5_HASH = ...
# LOGIN_ID = ...

# Actually, import from django.settings, as set for the merchant library
from django.conf import settings
merchant_settings = getattr(settings, "MERCHANT_SETTINGS")
assert merchant_settings and merchant_settings.get("authorize_net")
authorize_net_settings = merchant_settings["authorize_net"]
MD5_HASH = merchant_settings["authorize_net"]["MD5_HASH"]
LOGIN_ID = merchant_settings["authorize_net"]["LOGIN_ID"]

import requests

def compute_response_hash(trans_id, amount):
        hash_str = "%s%s%s%s" % (MD5_HASH, LOGIN_ID, trans_id, amount)
        return hashlib.md5(hash_str).hexdigest()

#This class will handles any incoming request from
#the browser 
class myHandler(BaseHTTPRequestHandler):


	#Handler for the POST requests
	def do_POST(self):
                print "do_POST"
		if self.path=="/":
			form = cgi.FieldStorage(
				fp=self.rfile, 
				headers=self.headers,
				environ={'REQUEST_METHOD':'POST',
		                 'CONTENT_TYPE':self.headers['Content-Type'],
			})
                        print form
                        # transaction amount, as submitted
                        amount = form['x_amount'].value
                        # generate transaction id
                        trans_id = str(randrange(1000000000))
                        md5_hash = compute_response_hash(trans_id, form['x_amount'].value)
                        response_reason_text = 'This transaction_has_been_approved'
                        response_code = 1

                        data = {'x_MD5_Hash': md5_hash, 'x_trans_id': trans_id, 'x_amount': amount, 'x_response_reason_text': response_reason_text, 'x_response_code': response_code }

                        if str(amount)=='13.13': # simulate failure
                            data['x_response_reason_text'] = 'This transaction_has_been_rejected'
                            data['x_response_code'] = 13
                            data['x_response_reason_code'] = 123

                        # pass the data
                        # todo: check x_fp_hash against x_fp_timestamp, x_fp_sequence
                        for key in form:
                                if not key in ['x_login',  'x_fp_timestamp', 'x_fp_hash', 'x_fp_sequence',  'x_relay_url', 'x_relay_response']:
                                        data[key] = form[key].value
                        assert form['x_relay_response'].value.upper() == "TRUE"
                        result = requests.post(form['x_relay_url'].value, data)


			
			self.send_response(200)
			self.end_headers()
			self.wfile.write(result.content)
			return			
			
			
try:
	#Create a web server and define the handler to manage the
	#incoming request
	server = HTTPServer(('', PORT_NUMBER), myHandler)
	print 'Started httpserver on port ' , PORT_NUMBER
	
	#Wait forever for incoming htto requests
	server.serve_forever()

except KeyboardInterrupt:
	print '^C received, shutting down the web server'
	server.socket.close()
