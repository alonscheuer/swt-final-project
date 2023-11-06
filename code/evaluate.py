import argparse
import json
from tqdm import tqdm
import nltk
from nltk.translate.meteor_score import single_meteor_score
from transformers import AutoTokenizer, AutoModel
import torch
import numpy as np

tokenizer = AutoTokenizer.from_pretrained("xlm-roberta-base")
model = AutoModel.from_pretrained("xlm-roberta-base")

nltk.download('wordnet')

def create_arg_parser():
	parser = argparse.ArgumentParser()
	parser.add_argument("-i", "--input_file", type=str, help="File containing Wikipedia links")
	parser.add_argument("-o", "--output_file", type=str, help="Name of file where results are saved")
	return parser.parse_args()


def get_embeddings(text):
	max_length = tokenizer.model_max_length
	tokens = tokenizer(text, return_tensors="pt", max_length=max_length, padding=True, truncation=True, return_overflowing_tokens=True)["input_ids"]
	embeddings = model.embeddings(tokens)[0]
	return embeddings


def bertscore(reference, candidate):
	emb_reference = get_embeddings(reference)
	emb_candidate = get_embeddings(candidate)
	cos = torch.nn.CosineSimilarity(dim=0)
	similarity = torch.tensor([[cos(x, y) for x in emb_reference] for y in emb_candidate])
	precision = sum([max(similarity[i, :]) for i in range(emb_candidate.shape[0])]) / emb_candidate.shape[0]
	recall = sum([max(similarity[:, i]) for i in range(emb_reference.shape[0])]) / emb_reference.shape[0]
	f1 = (precision * recall) / (precision + recall) * 2
	return f1.item()


def main():
	args = create_arg_parser()
	data = json.load(open(args.input_file))
	for item in tqdm(data, position=0, desc="main"):
		item["meteor_sv"] = single_meteor_score(item["sv_text"].split(" "), item["gpt"].split(" "))
		item["bertscore_en"] = bertscore(item["en_text"], item["gpt"])
		item["bertscore_sv"] = bertscore(item["sv_text"], item["gpt"])
	json.dump(data, open(args.output_file, 'w'))


main()
