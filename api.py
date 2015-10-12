from flask import Flask
from flask import request, json, Response, jsonify
import os, re

app = Flask(__name__)
#app.config.from_object(os.environ['APP_SETTINGS'])


@app.route('/')
def hello():
    return "Hello World!!!"

@app.route('/api', methods = ['GET'])
def api():
	cep = request.args.get('cep')

	if cep:
		cepStr = str(cep)
		validCep = re.compile('^\d{5}-\d{3}$')
		#return cep
		if validCep.match(cep):		
			return cepStr
		else:
			data = {
				'Error' : 'Format invalid, should be a string like XXXXX-XXX where X is a number from 0 to 9'
			}
			resp = jsonify(data)
			resp.status_code = 400
			return resp
	else:
		return "CEP not found"


@app.route('/api/echo', methods = ['GET', 'POST', 'PATCH', 'PUT', 'DELETE'])
def api_echo():
    if request.method == 'GET':
        return "ECHO: GET\n"

    elif request.method == 'POST':
        return "ECHO: POST\n"

    elif request.method == 'PATCH':
        return "ECHO: PACTH\n"

    elif request.method == 'PUT':
        return "ECHO: PUT\n"

    elif request.method == 'DELETE':
        return "ECHO: DELETE"

def app(environ, start_response):
    data = 'CEP API\n'
    status = '200 OK'
    response_headers = [
        ('Content-type','text/plain'),
        ('Content-Length', str(len(data)))
    ]
    start_response(status, response_headers)
    return iter([data])

'''
if __name__ == '__main__':
    app.run()
    #print(os.environ['APP_SETTINGS'])
'''