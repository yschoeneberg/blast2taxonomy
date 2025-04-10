# blast2taxonomy
[![DOI](https://zenodo.org/badge/597052423.svg)](https://zenodo.org/doi/10.5281/zenodo.10009721)

This script extracts human readable NCBI taxonomy information for blast hits. It automatically downloads the NCBI Taxonomy database and updates it if necessary. If there are multiple taxids assigned to a hit, the script returns the lowest common ancestor.
## Installation
The easiest way to get blast2taxonomy is to download the script by simply cloning the github repository, downloading the latest release.
### Dependencies
- Python 3
  - ete3 Toolkit (tested with v3.1.2)
  - Pandas (tested with v1.5.3)
 
To install all dependencies into a conda environment, run:
```
conda create -c conda-forge -n blast2tax pandas ete3=3.1.2
```
## Input
A tabular blast results file (outfmt 6) containing the taxonomyID as a column.
## Output
A tsv file containig the query ID, percent identity, subject length and the taxonomy information.
## Command Line Options
```
Usage: blast2taxonomy.py [options]
Version: 1.4.4

REQUIRED:
        -i      Tabular Blast results input file
        -o      Output file

OPTIONAL:
        -r      Comma seperated list of taxonomic ranks to extract
        -c      Column number containing the staxids [13]
        -p      Column number containing the percent identity [3]
        -l      Column number containing the length of the subject [4]
        -t      Number of threads [1]
        -s      Skip Taxonomy Database Update
        -f      Skip failed taxIDs and write those to 'failed_taxids.tsv'
        -h      Display this help message
```

## Citation
You can reference this script by citing the Github Repository:

Yannis Schöneberg (2023) „yschoeneberg/blast2taxonomy: v1.3.4“. Zenodo. doi: 10.5281/zenodo.10009721.
