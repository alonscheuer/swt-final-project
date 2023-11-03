import argparse
import json
from tqdm import tqdm
from utils import remove_prefix, fix_sv_encoding

def create_arg_parser():
	parser = argparse.ArgumentParser()
	parser.add_argument("-i", "--input_file", type=str, help="File containing Wikipedia links")
	return parser.parse_args()


def prompt(title, triples):
	return """
	Du är en hjälpsam assistent vars uppgift är att skriva en Wikipedia-artikel om %s, skriv artikeln på svenska.
	Du får ENDAST använda nedanstående egenskapsvärdepar som din informationskälla.
	Du behöver inte förklara varför du inte kan skapa en fullständig wikipedia artikel eller om du inte vet så får du gissa så bra du kan. 
 	Jag vill ENDAST ha Wikipedia artikeln, jag behöver ingen information om hur du har skapat artikeln. 
  	Lägg inte till några nya källor. Skriv artikeln så likt Wikipedia som möjligt. Skriv artikeln så utförligt som möjligt.
	Svara på svenska.  

	%s
	""" % (title, triples)


def main():
	args = create_arg_parser()
	items = json.load(open(args.input_file))
	for i, item in enumerate(tqdm(items)):
		topic = fix_sv_encoding(remove_prefix(item["sv"]))
		triples = item["triples"]
		with open(f"prompts/{i}.txt", 'w') as file:
			file.write(prompt(topic, triples))

main()
