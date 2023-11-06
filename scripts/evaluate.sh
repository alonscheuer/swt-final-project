#!/bin/bash
#SBATCH --time=08:00:00
#SBATCH --gpus-per-node=v100:1
#SBATCH --mem=16000

module purge
module load PyTorch

source $HOME/venvs/swt_final/bin/activate

pip install transformers tqdm numpy nltk torch

python3 --version
which python3

python3 code/evaluate.py -i data/all-data.json -o data/evaluated.json

deactivate