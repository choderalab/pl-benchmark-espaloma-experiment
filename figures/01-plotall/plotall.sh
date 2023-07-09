#!/bin/bash

source ~/.bashrc
conda activate perses-espaloma-0.3.0

# openff-2.1.0
targets="tyk2 cdk2 mcl1 p38"
forcefield="openff-2.1.0"
python plotall.py --input_prefix "../../experiment" --targets "${targets}" --forcefield ${forcefield}

# espaloma-0.3.0
targets="tyk2 cdk2 mcl1 p38"
forcefield="espaloma-0.3.0rc6"
python plotall.py --input_prefix "../../experiment" --targets "${targets}" --forcefield ${forcefield}

# espaloma-0.3.0 complex
targets="tyk2 cdk2 mcl1 p38"
forcefield="espaloma-0.3.0rc6-complex"
python plotall.py --input_prefix "../../experiment" --targets "${targets}" --forcefield ${forcefield}