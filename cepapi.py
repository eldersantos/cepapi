# -*- coding: utf-8 -*-

from flask import Flask
from flask import request, json, Response, jsonify
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import *
import os, re
import unicodedata


os.environ['DYLD_LIBRARY_PATH'] = '/Library/PostgreSQL/9.3/lib'

app = Flask(__name__)
app.config.from_object("config.DevelopmentConfig")
db = SQLAlchemy(app, use_native_unicode=True)

class cep_log_index(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	cep5 = db.Column(db.String(5))
	uf = db.Column(db.String(2))


	def __repr__(self):
		return "cep:" + self.cep5

class uf(db.Model):
	id = db.Column(db.String(2), primary_key = True)
	nome = db.Column(db.String(72))
	cep1 = db.Column(db.Integer)
	cep2 = db.Column(db.Integer)
	ibge = db.Column(db.Integer)


@app.route('/')
def hello():
    return "Hello World!!!"

@app.route('/api/cep/<cep>', methods = ['GET'])
def api(cep):
	#cep = request.args.get('cep')

	if cep:
		cepStr = str(cep)
		validCep = re.compile('^\d{5}-\d{3}$')

		if validCep.match(cep):
			intCep = int(cepStr[0:5])
			index = uf.query.filter(and_(intCep >= uf.cep1, intCep <= uf.cep2)).first()
			if index:
				sql = "SELECT * FROM " + index.id.lower() + " WHERE cep = '" + cepStr + "' limit 1"
				result = db.engine.execute(sql)
				if result.rowcount > 0:
					for row in result:
						data = {
								'tipo' : str(row.tp_logradouro).strip(),
								'logradouro' : row.logradouro,
								'bairro' : row.bairro,
								'cidade' : unicodedata.normalize('NFD', row.cidade).encode('ascii','ignore'),
								'uf' : index.id.lower(),
								'cep' : row.cep,
								'ibge' : ''
							}				
					resp = jsonify(data)
					resp.status_code = 200
					return resp
				else:
					return "CEP NotFound"
			else:
				data = {
					'NotFound'
				}
				resp = jsonify(data)
				resp.status_code = 404
				return resp
		else:
			data = {
				'Error' : 'Format invalid, should be a string like XXXXX-XXX where X is a number from 0 to 9'
			}
			resp = jsonify(data)
			resp.status_code = 400
			return resp
	else:
		return "CEP not found"

@app.route('/api/uf/<param>', methods = ['GET'])
def api_uf(param):
	#uf = request.args.get('uf')

	if param:
		ufStr = str(param)
		index = uf.query.filter_by(id=ufStr.upper()).first()
		if index:
			data = {
				'uf' : index.id,
				'ibge' : index.ibge,
				'start' : index.cep1,
				'finish' : index.cep2
			}
			resp = jsonify(data)
			resp.status_code = 200
			return resp
		else:
			data = {
				'Error' : ufStr + " is not a state"
			}
			resp = jsonify(data)
			resp.status_code = 400
			return resp
	else:
		return "UF not found"



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


if __name__ == '__main__':
    app.run()
    #print(os.environ['APP_SETTINGS'])
