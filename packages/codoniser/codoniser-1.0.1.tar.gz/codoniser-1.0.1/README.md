# codoniser
visualise codon usage and codon usage correlation

## Description
`codoniser` calculates and visualises codon usage and correlation.
It produces tables of the raw data and (nearly) publication ready figures in SVG format.
Below you can find information for installing and using `codoniser`.

## Installation

You can install `codoniser` with `pip`.

Either use the PyPI installation: `pip install codoniser`.

Or, clone this repository and install manually. 

`codoniser` requires only Python dependencies, which should be installed automatically. 

## Usage

`codoniser` takes fasta nucleic acid files (`.fna`) as positional input. This file should contain the DNA sequences of all ORFs from the source genome.
Be careful to ensure that you have not included pseudogenes or other none-CDS sequences as this will interfer with the analysis (and probably cause an error!).
Example input can be found, [here](https://github.com/drboothtj/codoniser/tree/main/example_data/example_in).

`codoniser` currently offers three analyses:

-  `-b` will plot a bar chart of the codon usage. You can plot one, or many genomes.
-  `-p` will plot a heatmap of the codon usage correlation (Pearsons's Rank)between the genomes. You must plot at least three genomes.
-  `-s` will plot a heatmap of the codon usage correlation (Spearman's rank) between the genomes. You must plot at least three genomes.


Therefore, to run all three analysis you can run, for example:

`codoniser -b -p -s *.fna`

## Output
`codoniser` produces a number of tables and figures as output. 
The example outputs can be found, [here](https://github.com/drboothtj/codoniser/tree/main/example_data/example_out).

### Bar chart
`codoniser` can produce simple bar charts. It will produce an SVG for both the raw counts and the percantage usage. 
The below example is comparing the codon usage of  *Bacillus cereus* and *Caulobacter vibrioides*, using the command:

`codoniser -s Bacillus_cereus.fna Caulobacter_vibrioides.fna`
![example of codon usage bar chart](https://raw.githubusercontent.com/drboothtj/codoniser/main/example_data/example_out/barchart/barchart_percentages.svg).

### Spearman's and Pearson's Rank
`codoniser` can analyse the codon usage correlations and produce heatmaps to visualise there relationships. It will provide the correlation matrix, the correlation p-values, the codon counts, and the rank data separate `.csv` files. It will also provide a `.svg` image of the heatmap. Below is the SVG produced by using the example data from this repository. You can easily see the codon bias between the low-GC and the high-GC organisms. It was generated with the command:

`codoniser -s *.fna`

![example of spearman's rank heatmap](https://raw.githubusercontent.com/drboothtj/codoniser/main/example_data/example_out/spearmans/spearmans.svg)

## Citation
Coming soon...

## Version History
- 1.0.0
  - Initial release
- 1.0.1
  - Add skip-malformed-cds parameter for skipping pseudogenes etc.
