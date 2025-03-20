'''
custom errors for codoniser
    classes:
'''

class CodoniserError(Exception):
    '''
    top level error for codoniser
    '''
    pass

class NoAnalysisError(CodoniserError):
    '''
    error raised when no analysis was completed. 
    '''
    pass

class BadInputError(CodoniserError):
    '''
    error raised when no cdses are found in the input data
    '''
    pass

class BadCDSError(CodoniserError):
    '''
    error when catching bad cds input
        examples: 
            length not divisble by 3
            non-nucleotide letters
            etc...
    '''
    def __init__(self, cds, reason):
        '''
        init for bad cds error to explain a custom reason
        '''
        self.reason = reason
        super().__init__(f"{cds} is malformed! {self.reason}.")
