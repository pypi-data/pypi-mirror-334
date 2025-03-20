'''
data classes for codoniser
'''
from collections import Counter
from codoniser.utils.errors import BadCDSError

class CDS():
    '''
    CDS class for codoniser
    '''
    def __init__(self, source, name, sequence):
        '''
        initialise CDS class
        '''
        self.source = source
        self.name = name
        self.sequence = sequence

        self.check_sequence()

        self.codon_count = self.count_codons

    def check_sequence(self):
        '''
        check important info about the sequence and raise error if bad
        '''
        #first check divisible by 3
        if divmod(len(self.sequence),3)[1] != 0:
            raise BadCDSError(self.name, 'Sequence not divisible by three')
        #next check only nucleotide data
        nucleotides = ['a','t','g','c', 'u', 'A', 'T', 'G', 'C', 'U']
        if not all(character in nucleotides for character in self.sequence):
            raise BadCDSError(self.name, 'Sequence contains non-nucleotide characters')

    def count_codons(self):
        '''
        count coudons in sequence
        '''
        triplets = [self.sequence[i:i+3] for i in range(0, len(self.sequence), 3)]
        return Counter(triplets)
