import argparse
from nltk.tokenize import sent_tokenize
from statistics import mean, stdev
import numpy as np

def create_arg_parser():
	parser = argparse.ArgumentParser()
	parser.add_argument("-i", "--input_file", type=str, help="File containing Wikipedia links")
	return parser.parse_args()


def main():
	args = create_arg_parser()
	hallucination_ratio = []
	evaluated_ids = [1, 3, 7, 12, 13, 14, 20, 25, 27, 29, 40, 41, 43, 44, 45, 46, 47, 49, 55, 63, 64, 65, 68, 69, 71, 77, 79, 80, 83, 84, 86, 87, 88, 90, 100, 101, 102, 111, 118, 119, 121, 124, 125, 126, 130, 133, 135, 137, 138, 139, 140, 150, 155, 157, 159, 161, 166, 171, 173, 174, 176, 178, 179, 180, 181]
	with open(args.input_file) as file:
		for i, line in enumerate(file):
			if i in evaluated_ids:
				sentences = sent_tokenize(line, language="swedish")
				n = len(sentences)
				h = sum([1 for s in sentences if "[H]" in s])
				hallucination_ratio.append(h / n)
	print(f"Hallucination ratio: {round(mean(hallucination_ratio) * 100, 1)}% ± {round(stdev(hallucination_ratio) * 100, 3)}%")
	counts, bins = np.histogram(hallucination_ratio, bins=np.arange(0, 1, 0.05))
	for i, bin in enumerate(bins):
		if i == 0:
			print(f"# articles with 0 hallucinations: {sum(1 for x in hallucination_ratio if x == 0)}")
		else:
			print(f"# articles with less than {int(bin*100)}% hallucinations: {sum(counts[:i])}")

main()
