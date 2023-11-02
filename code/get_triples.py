import argparse
from json import load, dump
from utils import dbp_endpoint, send_query, remove_prefix
from tqdm import tqdm


def create_arg_parser():
	parser = argparse.ArgumentParser()
	parser.add_argument("-i", "--input_file", type=str, help="File containing dbr links")
	parser.add_argument("-o", "--output_file", type=str, help="Name of file where results are saved")
	return parser.parse_args()


def postprocess(triples):
	filtered_triples = []
	for triple in triples:
		# filter non-English languages 
		if lang := triple['value'].get('xml:lang'):
			if lang != 'en':
				continue
		# filter certain properties
		property = remove_prefix(triple['prop']['value'])
		if property in ['wikiPageUsesTemplate', 'sameAs']:
			continue
		filtered_triples.append(clean_triple(triple))
	return filtered_triples


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
	}
	""" % remove_prefix(dbr).replace('(', '\(').replace(')', '\)')
	result = send_query(query, dbp_endpoint)
	triples = postprocess(result)
	return triples


def main():
	args = create_arg_parser()
	items = load(open(args.input_file))
	for item in tqdm(items):
		item["triples"] = get_triples(item["dbr"])
	dump(items, open(args.output_file, "w"))


main()
