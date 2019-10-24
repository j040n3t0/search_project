# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, redirect, Response, jsonify
import requests, random, json
import sys
from datetime import datetime
from elasticsearch import Elasticsearch

app = Flask(__name__)
es = Elasticsearch('10.0.1.69')
######### Funções


def elastic_search(search):
	
	doc = {
	    'nome': search ,
	}

	nome = str(doc['nome'])
	
	res = es.search(index="usuarios", body={"query": {"match_phrase_prefix": { "nome": "%s" % (nome)}}})
	result_list = []
	for hit in res['hits']['hits']:
		result_list.append("%s" % (hit["_source"]["nome"]))
	return result_list

#####################################

@app.route('/')
def home():
	return render_template('index.html', name='It\'s Alive')

# Referencia - https://stackoverflow.com/questions/11774265/how-do-you-get-a-query-string-on-flask
@app.route('/search',methods= ['GET'])
def search():
	search = request.args.get("q")
	search_result = elastic_search(search)
	temp_var = ""
	if len(search_result) > 0:
		for i in range(len(search_result)):
			temp_var = temp_var + search_result[i] + "<p style='margin-block-start: 4px; margin-block-end: 4px;'>"
	else:
		temp_var = "nenhum valor encontrado! Tente a letra <b>J</b>" 
	
	return temp_var
	
	
if __name__ == "__main__":
	app.run("0.0.0.0", "80", debug=True)