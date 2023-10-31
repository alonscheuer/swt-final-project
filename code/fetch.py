# Code for retrieving Wikipedia articles and DBpedia triples

from SPARQLWrapper import SPARQLWrapper, JSON
import re
import requests
import keys
import wikipedia
from datetime import datetime

dbp_endpoint = SPARQLWrapper("https://dbpedia.org/sparql")
dbp_endpoint.setReturnFormat(JSON)

wd_endpoint = SPARQLWrapper("https://query.wikidata.org/sparql")
wd_endpoint.setReturnFormat(JSON)

wp_token = keys.WP_TOKEN

def remove_prefix(url):
	"""
	Remove any prefix from a URL, leaving only the part which is followed by the last / or #
	"""
	m = re.search(r'([^/#]+)$', url)
	return m[1]


def send_query(query, endpoint):
	endpoint.setQuery(query)
	result = endpoint.queryAndConvert()
	formatted_result = result["results"]["bindings"]
	return formatted_result


def find_dbr(article):
	"""
	Find the URL of a DBpedia resource based on a Wikipedia article URL
	"""
	query = """
	PREFIX foaf: <http://xmlns.com/foaf/0.1/>
	SELECT ?entity WHERE {
		?entity foaf:isPrimaryTopicOf <%s> .
	}
	LIMIT 1
	""" % https_to_http(article)
	result = send_query(query, dbp_endpoint)
	return result[0]["entity"]["value"]


def find_dbrs(articles):
	article_values = [f"<{a}>" for a in articles]
	"""
	Find the URL of a DBpedia resource based on a Wikipedia article URL
	"""
	query = """
	PREFIX foaf: <http://xmlns.com/foaf/0.1/>
	SELECT ?entity, ?wiki WHERE {
		VALUES ?wiki { %s } .
		?entity foaf:isPrimaryTopicOf ?wiki .
	}
	""" % " ".join([https_to_http(url) for url in article_values])
	result = send_query(query, dbp_endpoint)
	return result

def clean_triple(triple):
	property = remove_prefix(triple['prop']['value'])
	value = triple['value']['value']
	return property, value

def get_triples(dbr):
	"""
	Get triples from DBpedia
	"""
	query = """
	PREFIX dbr: <http://dbpedia.org/resource/>
	SELECT ?prop, ?value WHERE {
		dbr:%s ?prop ?value .
		FILTER(lang(?value) = "en").
	}
	""" % remove_prefix(dbr)
	result = send_query(query, dbp_endpoint)
	triples = map(clean_triple, result)
	return triples
	
