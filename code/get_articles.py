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
	r = requests.get(wikilink)
	soup = bs4.BeautifulSoup(r.text,'html.parser').select('body')[0]
	text = []
	tags = ['p', 'a', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']
	for tag in soup.find(id="mw-content-text").descendants:
		if tag.name in tags:
			text.append(tag.text)
	print(text)
	return " ".join(text)


def main():
	args = create_arg_parser()
	items = load(open(args.input_file))
	items = items[0:5]
	for item in tqdm(items):
		item["en_text"] = get_wikipage(item["en"])
		item["sv_text"] = get_wikipage(item["sv"])
	dump(items, open(args.output_file, "w"))


main()
