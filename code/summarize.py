import argparse
import json
import pandas as pd

def create_arg_parser():
	parser = argparse.ArgumentParser()
	parser.add_argument("-i", "--input_file", type=str, help="File containing evaluated data")
	return parser.parse_args()


def main():
	args = create_arg_parser()
	data = json.load(open(args.input_file))
	for item in data:
		item.pop("en_text")
		item.pop("sv_text")
		item.pop("triples")
	df = pd.DataFrame.from_dict(data)
	print(df.agg({"meteor_sv": ["mean", "std"], "bertscore_en": ["mean", "std"], "bertscore_sv": ["mean", "std"]}))


main()
