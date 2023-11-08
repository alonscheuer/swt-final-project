import argparse
import json
import pandas as pd
from tqdm import tqdm
from nltk.tokenize import sent_tokenize
from statistics import mean, stdev

def create_arg_parser():
	parser = argparse.ArgumentParser()
	parser.add_argument("-i", "--input_file", type=str, help="File containing Wikipedia links")
	return parser.parse_args()


def main():
	args = create_arg_parser()
	hallucination_ratio = []
	with open(args.input_file) as file:
		for line in tqdm(file):
			sentences = sent_tokenize(line, language="swedish")
			n = len(sentences)
			h = sum([1 for s in sentences if "[H]" in s])
			hallucination_ratio.append(h / n)
	print(f"Hallucination ratio: {round(mean(hallucination_ratio) * 100, 1)}% ± {round(stdev(hallucination_ratio) * 100, 3)}%")

main()
