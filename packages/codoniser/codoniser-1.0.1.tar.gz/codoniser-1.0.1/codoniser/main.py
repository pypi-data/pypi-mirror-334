'''
main routine for codoniser
    functions:
        !!!
'''
from typing import List, Union
from collections import Counter

import glob

from codoniser.utils import io, parser
from codoniser.utils.classes import CDS
from codoniser.utils.errors import BadCDSError, BadInputError, NoAnalysisError
from codoniser.plotting.barchart import plot_barchart
from codoniser.plotting.heatmap import rank

'''
consider adding sliding window one day...

def get_codon_distribution(codons, step_size, window_size):
    start_point = 0
    end_point = start_point + window_size
    while end_point < len(codons):
        window_codons = codons [start_point:end_point]
        mid_point = start_point + ((start_point - end_point)/2)
        codon_count = Counter(window_codons)
        #add midpoint and counts to data
        start_point += step_size
        end_point = start_point + window_size
    #return x
'''

def get_cdses_from_fasta(files: List[str], skip_malformed: bool) -> List[CDS]:
    '''
    generates cds objects for each cds in a fasta file
        arguments: 
            file:
                paths to fasta file
        returns:
            cdses:
                a list of cds objects
    '''
    cdses = []
    file_list = []
    for file in files:
        file_list.extend(glob.glob(file)) #allow for wildcards
    for file in file_list:
        sequence_names, sequences = io.read_cds_from_records(file, 'fasta')
        for sequence_name, sequence in zip(sequence_names, sequences):
            try:
                cds = CDS(source=file, name=sequence_name, sequence=sequence)
            except BadCDSError:
                if skip_malformed is True:
                    continue
            cdses.append(cds)
    if len(cdses) < 1:
        raise BadInputError(
            "No CDSs found in input. Check the correct file format was provided."
        )
    return cdses

def get_data(cdses) -> Union[List[str], List[Counter], List[str]]:
    '''
    takes a list of cds objects and extracts the 
    labels, counters and possible categories (i.e. codons)
        arguments:
            cdses: a list of codoniser cds objects
        returns:
            labels: 
                list of sources (e.g. organisms) from all CDSes
            counters:
                a list of all the codon Counters for each CDS
            categories:
                a list of all possible catgeories (i.e. codons)
    '''
    labels = list({cds.source for cds in cdses})
    counters = get_totals(cdses, labels)
    assert len(labels) == len(counters)
    categories = {key for counter in counters for key in counter.keys()}
    return labels, counters, categories

def get_totals(cdses: List[CDS], labels: List[str]) -> List[Counter]:
    '''
    Combines and extracts counters from cdses relative to the labels
        arguments:
            cdses:
                list of CDS objects
            labels:
                list of lables
        returns:
            counters:
                list of counters
    '''
    counters = []
    for label in labels:
        counter = Counter()
        for cds in cdses:
            if cds.source == label:
                counter += cds.codon_count()
        counters.append(counter)
    return counters


def main():
    '''
    main routine for codoniser
        args:
            None
        returns:
            None
    '''
    #io.print_to_system('Running codoniser!') ADD LOGGING
    args = parser.parse_args()
    cdses = get_cdses_from_fasta(args.files, args.skip_malformed_cds)
    #set a flag to ensure some analysis was done
    analysis_complete = False
    sources, counters, categories = get_data(cdses)
    #barcharts
    if args.barchart:
        plot_barchart(sources, counters, categories)
        analysis_complete = True
    #heatmaps
    if args.pearsons is True:
        rank(sources, counters, categories, 'pearsons')
        analysis_complete = True
    if args.spearmans is True:
        rank(sources, counters, categories, 'spearmans')
        analysis_complete = True
    #check if anaylsis run
    if analysis_complete is False:
        raise NoAnalysisError(
            'No analysis was requested. Use the paramaters to perform an analysis.'
            )
    print('Codoniser completed the analysis.')

    # TODO
    # sliding window <- requires positional info from gbk
    # add correlation scatter for 2 strains
    # identify outliers e.g. genes with wierd codon composition?
    # add logging
    # add output dir designation

if __name__ == '__main__':
    main()
