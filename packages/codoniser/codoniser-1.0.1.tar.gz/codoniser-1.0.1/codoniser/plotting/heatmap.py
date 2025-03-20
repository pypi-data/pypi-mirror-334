'''
perform spearman's rank correlation analysis for codoniser
    functions:
        !!!
'''
from typing import List

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from scipy.stats import pearsonr, rankdata, spearmanr

from codoniser.utils.io import list_to_csv

def get_uniform_counters(counters):
    '''
    ensure all keys are in all counters and add 0 value if absent
    '''
    all_keys = set()
    for counter in counters:
        all_keys.update(counter.keys())
    for counter in counters:
        for key in all_keys:
            counter.setdefault(key, 0)
    return counters

def print_rank_data(filename: str, counters: List, labels: List) -> None:
    '''
    print rank data from counters
    '''
    #this is a terrible function rewrite
    rank_lines = []
    count_lines = []
    line = ["source"]
    line.extend(sorted(counters[0].keys()))
    count_lines.append(line)
    rank_lines.append(line)
    for label, counter in zip(labels, counters):
        line = []
        line.append(label)
        counts = [counter[key] for key in count_lines[0]][1:]
        ranks = rankdata(counts)
        line.extend(list(ranks))
        rank_lines.append(line)
        line = []
        line.append(label)
        line.extend(counts)
        count_lines.append(line)
    list_to_csv(filename + '_ranks.csv', rank_lines)
    list_to_csv(filename + '_counts.csv', count_lines)

def write_data(filename, data, labels):
    '''
    write data
    '''
    new_lines = []
    headers = [" "]
    headers.extend(labels)
    new_lines.append(headers)
    for line, label in zip (data, labels):
        new_line = []
        new_line.append(label)
        new_line.extend(list(line))
        new_lines.append(new_line)
    list_to_csv(filename, new_lines)

def write_dendro_heatmap(correlation_matrix, labels: List, filename: str) -> None:
    '''
    creates and writes a dendrogram heatmap from the provided matrix
        arguments:
            correlation_matrix: a numpy matrix for all vs all spearmans or pearsons correlations
            labels: list of labels for the rows of the matrix
            filename: string for the filename prefix
        returns:
            None
    '''
    # Plot heatmap with dendrogram
    plt.figure(figsize=(10, 8))
    sns.clustermap(
        correlation_matrix,
        cmap='Greens', metric="correlation", method="complete", annot=False, fmt='.2e',
        cbar_kws={'label': 'Correlation'},
        xticklabels=labels,
        yticklabels=labels
        )
    plt.savefig(filename)

def get_matracies(counters, categories, analysis_type):
    '''
    get the correlation and p-value matracies for Spearmans rank analysis
        arguments:
            !!!
        returns
    '''
    n_counters = len(counters)
    data = np.array([[counter.get(cat, 0) for cat in categories] for counter in counters])
    correlation_matrix = np.zeros((n_counters, n_counters))
    pvalue_matrix = np.zeros((n_counters, n_counters))
    for i in range(n_counters):
        for j in range(i, n_counters):
            if analysis_type == 'spearmans':
                correlation, pvalue = spearmanr(data[i], data[j])
            if analysis_type == 'pearsons':
                correlation, pvalue = pearsonr(data[i], data[j])
            correlation_matrix[i, j] = correlation
            correlation_matrix[j, i] = correlation
            pvalue_matrix[i, j] = pvalue
            pvalue_matrix[j, i] = pvalue
    return correlation_matrix, pvalue_matrix

def rank(labels, counters, categories, analysis_type: str):
    '''
    perform an all vs. all spearmans rank analysis on provided annotated proteomes
        arguments:
            !!!
        returns:
            None
    '''
    counters = get_uniform_counters(counters) #none equal counters will screw up ranking

    print_rank_data(analysis_type, counters, labels) # this is done twice if you do both

    correlation_matrix, pvalue_matrix = get_matracies(counters, categories, analysis_type)
    write_dendro_heatmap(correlation_matrix, labels, analysis_type + '.svg')

    write_data(analysis_type + '_correlations.csv', correlation_matrix, labels)
    write_data(analysis_type + '_pvalues.csv', pvalue_matrix, labels)
