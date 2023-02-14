#!/usr/bin/env python3
# blast2taxonomy.py
# Author: Yannis Schöneberg <schoeneberg@gmx.de>
# This script takes in a blast result table and outputs the taxonomy data in a tsv file
# Version 1.2
import getopt
import sys
import logging
import pandas as pd
from multiprocessing import Pool
from ete3 import NCBITaxa
from itertools import repeat


def get_options(argv):
    version = 1.2
    try:
        opts, args = getopt.getopt(argv, "hsi:o:c:t:", ["ifile=", "ofile="])
    except getopt.GetoptError:
        print(f"Usage: blast2taxonomy_v{str(version)}.py -i <infile> -o <outfile> -c <column taxids> -t <num threads>\n"
              f"Type blast2taxonomy_v{str(version)}.py -h for help")
    global skip_update
    skip_update = False
    threads = 1
    for opt, arg in opts:
        if opt == '-h':
            print(f"\nUsage: blast2taxonomy_v{str(version)}.py [options]\n"
                  f"\n"
                  f"REQUIRED:\n"
                  f"\t-i\tTabular Blast results input file\n"
                  f"\t-o\tOutput file\n"
                  f"\t-c\tColumn number containing the staxids\n"
                  f"\n"
                  f"OPTIONAL:\n"
                  f"\t-t\tNumber of threads [1]\n"
                  f"\t-s\tSkip Taxonomy Database Update\n"
                  f"\t-h\tDisplay this help message\n"
                  f"\n"
                  f"Version: {str(version)}")
            exit()
        elif opt == '-i':
            global blast_infile
            blast_infile = arg
        elif opt == '-o':
            global outfile
            outfile = arg
        elif opt == "-c":
            global tax_column
            tax_column = int(arg)
        elif opt == "-t":
            global threads
            threads = int(arg)
        elif opt == "-s":
            skip_update = True


def update_taxdb():
    logger.info(f"### Updating Taxonomy Database")
    ncbi.update_taxonomy_database()
    logger.info(f"Finished Updating Database")


def get_taxonomy (parameters):
    blast_result = parameters[0]
    tax_column = int(parameters[1])
    taxids = blast_result[tax_column-1].split(";")
    if len(taxids) == 1:
        lineage = ncbi.get_lineage(taxids[0])
        taxonomy = ncbi.get_taxid_translator(lineage)
        return [blast_result[0]] + [taxonomy[taxid] for taxid in lineage]
    elif len(taxids) > 1:
        tax_annotations = []
        for id in taxids:
            lineage = ncbi.get_lineage(id)
            tax_dict = ncbi.get_taxid_translator(lineage)
            tax_inf = [taxonomy[taxid] for taxid in lineage]
            tax_annotations.append(tax_inf)
        transp_taxs = list(zip(*tax_annotations))
        lca_taxonomy = []
        for tax_level in transp_taxs:
            if tax_level.count(tax_level[0]) == len(tax_level):
                lca_taxonomy.append(tax_level[0])
            else:
                break
        return [blast_result[0]] + lca_taxonomy


if __name__ == '__main__':
    logger = logging.getLogger('my_logger')
    my_handler = logging.StreamHandler()
    my_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %("
                                     "message)s")
    my_handler.setFormatter(my_formatter)
    logger.addHandler(my_handler)
    logger.setLevel(logging.INFO)

    get_options(sys.argv[1:])

    logger.info(f"#### Extracting Taxonomy Information for Blast Results\n"
                f"{'Blast Results File:':<50} {blast_infile}\n"
                f"{'Column With TaxIDs:':<50} {tax_column}\n"
                f"{'Output file:':<50} {outfile}\n"
                f"{'Number of threads':<50} {threads}")
    blast_results = pd.read_csv(blast_infile, sep="\t")
    blast_results = blast_results.values.tolist()[:1]
    global ncbi
    ncbi = NCBITaxa()
    if skip_update is False:
        update_taxdb()
    else:
        logger.info("Skipping Taxonomy Database Update")

    logger.info(f"Searching TaxIDs vs Taxonomy DB")
    with Pool(threads) as pool:
        taxlist = pool.map(get_taxonomy, zip(blast_results, repeat(tax_column)))

    logger.info(f"Writing Taxonomy Information to: {outfile}")
    pd.DataFrame(taxlist).to_csv(outfile, sep="\t", index=False, header=False)
    logger.info(f"Done")
