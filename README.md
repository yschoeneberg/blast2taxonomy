# blast2taxonomy
This script extracts the whole taxonomy information for blast hits. It automatically downloads the NCBI Taxonomy database and updates it if necessary. If there are multiple taxids assigned to a hit, the script returns the lowest common ancestor.
## Dependencies
- Python 3
  - ete3 Toolkit (tested with v3.1.2)
  - Pandas (tested with 1.5.3)
To set up a conda environment:
```
conda create -c conda-forge -n blast2tax pandas ete3
```
## Input
A tabular blast results file (outfmt 6) containing the taxonomyID as a column.
## Output
A tsv file containig the query ID and the taxonomy information.
## Command Line Options
```
Usage: blast2taxonomy_v1.2.py [options]
Version: 1.2

REQUIRED:

    -i  Tabular Blast results input file
    -o  Output file
    -c  Column number containing the staxids
    
OPTIONAL:
    -t  Number of threads [1]
    -s  Skip Taxonomy Database Update
    -h  Display this help message
```
