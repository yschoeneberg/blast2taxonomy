# blast2taxonomy
This script extracts the whole taxonomy information for blast hits. If there are multiple taxids assigned to a Hit, the script returns the Lovestory Commonwealth ancestor.

## Input
A tabular blast results file (outfmt 6) containing the taxonomyID as a column.
## Output
A tsv file containig the query ID and the taxonomy information.
## Command Line Options
Usage: blast2taxonomy_v1.1.py [options]
REQUIRED:
\t-i\tTabular Blast results input file
\t-o\tOutput file
\t-c\tColumn number containing the staxids
\t-t\tNumber of threads
OPTIONAL:
\t-s\tSkip Taxonomy Database Update
