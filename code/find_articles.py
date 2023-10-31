import argparse
from json import dump
from datetime import datetime
from utils import wd_endpoint, send_query

# USE 637 DAYS

def create_arg_parser():
	parser = argparse.ArgumentParser()
	parser.add_argument("-d", "--days", type=int, help="How far in the past to look for events (in days)")
	parser.add_argument("-l", "--limit", type=int, help="Maximum number of items to return")
	parser.add_argument("-o", "--output_file", type=str, help="Name of file where results are saved")
	return parser.parse_args()


def get_articles(days, limit):
	query = """
	PREFIX schema: <http://schema.org/>
	PREFIX wd: <http://www.wikidata.org/entity/>
	PREFIX wdt: <http://www.wikidata.org/prop/direct/>
	SELECT ?event ?eventlabel ?date ?url_en ?url_sv
	WITH {
		SELECT DISTINCT ?event ?date ?url_en ?url_sv
		WHERE {
			# find events
			?event wdt:P31/wdt:P279* wd:Q1190554.
			# with a point in time or start date
			OPTIONAL { ?event wdt:P585 ?date. }
			OPTIONAL { ?event wdt:P580 ?date. }
			# but at least one of those
			FILTER(BOUND(?date) && DATATYPE(?date) = xsd:dateTime).
			# not in the future, and not more than 31 days ago
			BIND(NOW() - ?date AS ?distance).
			FILTER(0 <= ?distance && ?distance < %i).
			?url_sv schema:about ?event .
			?url_sv schema:isPartOf <https://sv.wikipedia.org/> .
			?url_en schema:about ?event .
			?url_en schema:isPartOf <https://en.wikipedia.org/> .
		}
		ORDER BY uuid()
		LIMIT %i
	} AS %%i
	WHERE {
		INCLUDE %%i
		SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en" . }
	}
	# randomizer %s
	""" % (days, limit, datetime.now())
	result = send_query(query, wd_endpoint)
	formatted_result = [{"en": row["url_en"]["value"], "sv": row["url_sv"]["value"]} for row in result]
	return formatted_result


def main():
	args = create_arg_parser()
	result = get_articles(args.days, args.limit)
	dump(result, open(args.output_file, "w"))


main()
