# Semntic Web Technlogoy - Final Project

## Dependencies

To install all the necessary dependencies, run the following command.

'''
pip install -r requirements.txt
'''

## How to run 

From the scripts directory, run the file 'pipeline.sh'. This will find the URLs of articles that fit all criteria as well as the corresponding text, DBpedia resource identifier, and set of triples - all of which are saved into the data directory.

This data was used to generate the prompts that can be found in the prompts directory. These prompts, in turn, were fed into ChatGPT; the output of which can be found in the data directory.

To evaluate the generated articles, run the file 'evaluate.sh' from the scripts directory (we used the Hábrók HPC cluster of the University of Groningen). 

