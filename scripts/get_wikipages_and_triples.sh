python code/find_articles.py -l 3000 -o data/wikilinks.json
python code/get_articles.py -i data/wikilinks.json -o data/wikipages.json
python code/find_dbrs.py -i data/wikipages.json -o data/wikipages-dbrs.json
python code/get_triples.py -i data/wikipages-dbrs.json -o data/wikipages-triples.json