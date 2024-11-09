The project directory is organized as follows:


├── data/                # Folder containing datasets  
├── Experiments/         # Folder containing experiment scripts and results  
├── Grouping/            # Folder for grouping algorithms and related code  
├── Community Detection/ # Folder for community detection algorithms and related code  
├── requirements.txt     # File listing project dependencies  

# Requirements

This project requires Python and the necessary dependencies listed in the requirements.txt file.

# Folder Descriptions

## data  
This folder contains all the datasets used in the project. The full datasets are for immediate use. The evaluation datasets are used for evaluation. Dataset_generation.py is used for the generation of data using user input. Graphs contains graphs as outcomes of experiments

## Community Detection  
    This folder contains the code for detecting communities within networks or graphs using the Louvain algorithm. It takes as input a csv file and outputs a JSON file with distinct communities

## Grouping
    Contains the implementation of grouping algorithms, taking as input a JSON file (output of using_Louvain_algorithm.ipynb) and outputs groups of communities. community_grouing.ipynb uses unique pairing, Temporal     NetSimile, and hierarchical clustering with average linkage to group communities together
    lsh_communities.ipynb does not need to be run and can be used for further research with Locality Sensitive Hashing
    
## Experiments/
    Contains the code and notebook used to run experiments. The notebook allows the user to not have to run the entire code for each experiment. Does not need to be run to create groups

