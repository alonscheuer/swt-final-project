python code/process_output.py -i data/gpt-output.tsv -a data/wikipages-triples.json -o data/all-data.json 
python code/evaluate.py -i data/all-data.json -o data/evaluated.json
python code/summarize.py -i data/evaluated.json
python code/manual.py -i data/hallucinations.tsv