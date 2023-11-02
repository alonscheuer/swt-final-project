import argparse
import requests
import bs4
from json import load, dump
from tqdm import tqdm
from utils import remove_prefix


def create_arg_parser():
	parser = argparse.ArgumentParser()
	parser.add_argument("-i", "--input_file", type=str, help="File containing Wikipedia links")
	parser.add_argument("-o", "--output_file", type=str, help="Name of file where results are saved")
	return parser.parse_args()


def get_wikipage(wikilink):
	req = requests.get(wikilink)
	soup = bs4.BeautifulSoup(req.text,'html.parser').select('body')[0]
	# Get article body
	main = soup.find(id="mw-content-text")
	# Get rid of citations in text
	references = main.find_all("sup", class_="reference")
	for r in references:
		r.extract()
	# Change links into text
	links = main.find_all("a")
	for l in links:
		l.unwrap()
	# Remove [edit] links from section titles
	edits = main.find_all(class_="mw-editsection")
	for e in edits:
		e.extract()
	# Remove utility divs
	divs = main.find_all("div")[1:]
	for d in divs:
		d.extract()
	# Remove unwanted sections
	discarded_sections = ["See_also", "References", "External_links", "Se_även", "Referenser", "Externa_länkar"]
	for section in discarded_sections:
		span = main.find(id=section)
		if span:
			h = span.find_parent()
			rest = h.find_next_siblings()
			for r in rest:
				r.extract()
			h.extract()
	return main.get_text().strip().replace("\n\n", "\n")


def main():
	args = create_arg_parser()
	items = load(open(args.input_file))
	for item in tqdm(items):
		item["en_text"] = get_wikipage(item["en"])
		item["sv_text"] = get_wikipage(item["sv"])
	dump(items, open(args.output_file, "w"))


main()
