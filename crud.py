# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, redirect, Response, jsonify
import requests, random, json
import sys
from datetime import datetime
from elasticsearch import Elasticsearch

app = Flask(__name__)
es = Elasticsearch("10.0.1.69")


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

def elastic_full_search(search):
	
	doc = {
	    'nome': search ,
	}

	nome = str(doc['nome'])
	res = es.search(index="usuarios", body={"query": {"match_phrase_prefix": { "nome": "%s" % (nome)}}})
	result_list = []
	for hit in res['hits']['hits']:
		result_list.append("Nome: %s|Cargo: %s|Telefone: %s|Email: %s" % (hit["_source"]["nome"],hit["_source"]["cargo"],hit["_source"]["contatos"]["telefone"],hit["_source"]["contatos"]["email"]))
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
			temp_var = temp_var + "<button style='background-color: transparent; border: none;' onclick='dosomething(\""+search_result[i]+"\")' >"+search_result[i]+"</button><p style='margin-block-start: 4px; margin-block-end: 4px;'>"
			#temp_var = temp_var + "<button style='background-color: transparent; border: none;' onclick=\"alert('"+search_result[i]+"')\">"+search_result[i]+"</button><p style='margin-block-start: 4px; margin-block-end: 4px;'>"
			#temp_var = temp_var + "<a href='http://localhost/search?q="+ search_result[i] +"' style='text-decoration:none'>" + search_result[i] + "</a><p style='margin-block-start: 4px; margin-block-end: 4px;'>"
			# Substituir A com HREF por uma DIV com Evento OnClick
			## 1 - Testar OnClick com uma funcao Alert contendo o texto.
			## 2 - Funcionando o passo 1, substituir a funcao Alert para a selecao de busca.
			# Passar LI
			# Validar a possibilidade de passar Json com os dados ao inves de enviar a TAG HTML completa.
	else:
		temp_var = "nenhum valor encontrado! Tente a letra <b>J</b>" 
	
	return temp_var
	
@app.route('/fullsearch',methods= ['GET'])
def fullsearch():
	search = request.args.get("qq")
	print search
	full_search_result = elastic_full_search(search)
	return full_search_result[0]
	
	#return full_search_result
	#return "ihuu"
	# search_result = elastic_search(search)
	# temp_var = ""
	# if len(search_result) > 0:
	# 	for i in range(len(search_result)):
	# 		temp_var = temp_var + "<button style='background-color: transparent; border: none;' onclick='dosomething(\""+search_result[i]+"\")' >"+search_result[i]+"</button><p style='margin-block-start: 4px; margin-block-end: 4px;'>"
	# 		#temp_var = temp_var + "<button style='background-color: transparent; border: none;' onclick=\"alert('"+search_result[i]+"')\">"+search_result[i]+"</button><p style='margin-block-start: 4px; margin-block-end: 4px;'>"
	# 		#temp_var = temp_var + "<a href='http://localhost/search?q="+ search_result[i] +"' style='text-decoration:none'>" + search_result[i] + "</a><p style='margin-block-start: 4px; margin-block-end: 4px;'>"
	# 		# Substituir A com HREF por uma DIV com Evento OnClick
	# 		## 1 - Testar OnClick com uma funcao Alert contendo o texto.
	# 		## 2 - Funcionando o passo 1, substituir a funcao Alert para a selecao de busca.
	# 		# Passar LI
	# 		# Validar a possibilidade de passar Json com os dados ao inves de enviar a TAG HTML completa.
	# else:
	# 	temp_var = "nenhum valor encontrado! Tente a letra <b>J</b>" 
	
	# return temp_var
	
if __name__ == "__main__":
	app.run("0.0.0.0", "80", debug=True)
