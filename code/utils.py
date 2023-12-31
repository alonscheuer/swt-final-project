from SPARQLWrapper import SPARQLWrapper, JSON
import re


wd_endpoint = SPARQLWrapper("https://query.wikidata.org/sparql")
wd_endpoint.setReturnFormat(JSON)

dbp_endpoint = SPARQLWrapper("https://dbpedia.org/sparql")
dbp_endpoint.setReturnFormat(JSON)


def send_query(query, endpoint):
	endpoint.setQuery(query)
	# endpoint.setTimeout(timeout=20)
	result = endpoint.queryAndConvert()
	formatted_result = result["results"]["bindings"]
	return formatted_result


def https_to_http(url):
	return url.replace('https', 'http')


def remove_prefix(url):
	"""
	Remove any prefix from a URL, leaving only the part which is followed by the last / or #
	"""
	m = re.search(r'([^/#]+)$', url)
	return m[1] if m else url


def fix_sv_encoding(text):
	mapping = {
		"%C3%84": "Ä",
		"%C3%85": "Å",
		"%C3%96": "Ö",
		"%C3%A4": "ä",
		"%C3%A5": "å",
		"%C3%B6": "ö"
	}
	for code, char in mapping.items():
		text = text.replace(code, char)
	return text.replace("_", " ")
