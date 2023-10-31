import argparse
from json import load, dump
from utils import dbp_endpoint, send_query, https_to_http
from tqdm import tqdm


def create_arg_parser():
	parser = argparse.ArgumentParser()
	parser.add_argument("-i", "--input_file", type=str, help="File containing Wikipedia links")
	parser.add_argument("-o", "--output_file", type=str, help="Name of file where results are saved")
	return parser.parse_args()


def find_dbr(wikilink):
	"""
	Find the URL of a DBpedia resource based on a Wikipedia article URL
	"""
	query = """
	PREFIX foaf: <http://xmlns.com/foaf/0.1/>
	SELECT ?entity WHERE {
		?entity foaf:isPrimaryTopicOf <%s> .
	}
	LIMIT 1
	""" % https_to_http(wikilink)
	result = send_query(query, dbp_endpoint)
	return result[0]["entity"]["value"] if len(result) > 0 else ""


def find_dbrs(articles):
	article_values = [f"<{https_to_http(a)}>" for a in articles]
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


def main():
	args = create_arg_parser()
	items = load(open(args.input_file))
	en_links = [item["en"] for item in items]
	chunk_size = 50
	chunks = []
	for i in range(0, len(items), chunk_size):
		chunks.append(en_links[i:i+chunk_size])
	dbrs = []
	for chunk in tqdm(chunks):
		dbrs.append(find_dbrs(chunk))
	dbrs = sum(dbrs, [])
	for dbr in dbrs:
		item = [x for x in items if https_to_http(x["en"]) == dbr["wiki"]["value"]][0]
		item["dbr"] = dbr["entity"]["value"]
	linked_items = [x for x in items if "dbr" in x]
	dump(linked_items, open(args.output_file, "w"))


main()
