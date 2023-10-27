# Code for retrieving Wikipedia articles and DBpedia triples

from SPARQLWrapper import SPARQLWrapper, JSON
import re
import requests
import keys

dbp_endpoint = SPARQLWrapper("https://dbpedia.org/sparql")
dbp_endpoint.setReturnFormat(JSON)

wd_endpoint = SPARQLWrapper("https://query.wikidata.org/sparql")
wd_endpoint.setReturnFormat(JSON)


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
	""" % article
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
	""" % " ".join(article_values)
	result = send_query(query, dbp_endpoint)
	return result


def get_triples(dbr):
	"""
	Get triples from DBpedia
	"""
	query = """
	PREFIX dbr: <http://dbpedia.org/resource/>
	SELECT ?prop, ?value WHERE {
		%s ?prop ?value .
	}
	""" % dbr
	result = send_query(query, dbp_endpoint)
	return result


def get_articles():
	query = """
	SELECT ?event ?eventLabel ?date ?url_en ?url_sv
    WHERE {
    ?event wdt:P31/wdt:P279* wd:Q1190554.
    
    ?url_en schema:about ?event .
    ?url_en schema:isPartOf <https://en.wikipedia.org/> .
    ?url_sv schema:about ?event .
    ?url_sv schema:isPartOf <https://sv.wikipedia.org/> .
    
	}
	ORDER BY RAND()
	LIMIT 10
    """
	result = send_query(query, wd_endpoint)
	#formatted_result = [{"en": row["url_en"]["value"], "sv": row["url_sv"]["value"]} for row in result]
	formatted_result = [row["url_en"]["value"] for row in result]
	return formatted_result


print(get_articles())
print(find_dbrs(get_articles()))