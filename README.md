# Semantic Web Technology - Final Project

## Dependencies

To install all the necessary dependencies, run the following command:

```
pip install -r requirements.txt
```

## How to run

There are three pipelines provided in this repository:

`get_wikipages_and_triples.sh` gathers a dataset of topics along with their Wikipedia articles in English and Swedish, and the corresponding triples from DBpedia. Note that the first step of this process is a query to the WikiData endpoint and this query may take some time or even time-out some of the time. If it consistently times out, consider removing the randomization from this query (marked in the `find_articles.py` file).

`generate_prompts.sh` creates separate files with prompts based on each item in the dataset of wikipages and triples. Note that this will create a folder with many text files, one for each individual prompt.

`evaluate.sh` performs both automatic evaluation on the untouched output by ChatGPT, and a summarization of the manual annotation. Both require the existence of corresponding files containing the outputs by ChatGPT and the annotated outputs. Note that this pipeline envokes a resource-heavy evaluation for BERTscore relying on a large language model (XLM-RoBERTa) and many calculations of cosine similarity (we used the Hábrók HPC cluster of the University of Groningen to overcome this). 
