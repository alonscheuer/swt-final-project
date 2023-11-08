import argparse
import json
import re
from tqdm import tqdm

def create_arg_parser():
	parser = argparse.ArgumentParser()
	parser.add_argument("-i", "--input_file", type=str, help="File containing ChatGPT outputs")
	parser.add_argument("-o", "--output_file", type=str, help="Name of file where results are saved")
	parser.add_argument("-a", "--append_file", type=str, help="File containing existing dataset")
	return parser.parse_args()


def postprocess(text):
	# remove embedded images
	emb_link = r'!\[([^\]]+)\]\([^)]+\)'
	# remove link urls
	preprocessed = re.sub(emb_link, "", text)
	r_link = r'\[([^\]]+)\]\([^)]+\)'
	preprocessed = re.sub(r_link, lambda m : m[1], preprocessed)
	return preprocessed


def main():
	args = create_arg_parser()
	data = json.load(open(args.append_file))
	with open(args.input_file) as file:
		for i, line in enumerate(tqdm(file)):
			tokens = line.split("\t", maxsplit=1)
			output = postprocess(tokens[1])
			data[i]["gpt"] = output
	json.dump(data, open(args.output_file, 'w'))


main()
