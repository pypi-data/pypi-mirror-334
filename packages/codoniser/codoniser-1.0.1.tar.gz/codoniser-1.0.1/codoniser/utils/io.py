'''
io utilities for codoniser
    functions:
        list_to_csv(filename: str, write_lines: List[]): -> None
        read_cds_from_records(filename: str, file_type: str) -> None
'''
from typing import List
import csv
from Bio import SeqIO

def list_to_csv(filename: str, write_lines: List) -> None:
    '''
    write a list of lines to a .csv
        arguments: 
            filename: path to write file
            write_lines: lines to write
        returns:
            None
    '''
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file,delimiter=',')
        writer.writerows(write_lines)

def read_cds_from_records(filename: str, file_type: str) -> None:
    '''
    read cdses from file using biopython
        arguments:
            filename: path to file
            filetype: string to define 'fasta' or 'genbank'
        returns:
            record_names: list of sequence names
            record_sequnences: list of sequences
    '''
    record_names = []
    record_sequences = []
    for seq_record in SeqIO.parse(filename, file_type):
        record_names.append(seq_record.id)
        record_sequences.append(str((seq_record.seq)).strip())
    return record_names, record_sequences
