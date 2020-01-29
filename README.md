
# PANANSE

A python package to prepare enhancer file for ANANSE package from fastq files. 
1) p300 ChIP-seq; 
2) ATAC-seq and H3K27ac.

## Requirements

* Python >= 3.6
* ANANSE
* GimmeMotifs (development branch)

## Installation

You will need [conda](https://docs.continuum.io/anaconda/) using the [bioconda](https://bioconda.github.io/) channel.

Make sure you have conda installed. If you have not used bioconda before, first set up the necessary channels (in this order!). You only have to do this once.

```
$ conda config --add channels defaults
$ conda config --add channels bioconda
$ conda config --add channels conda-forge
```

Now you can create an environment for pananse:

``` 
conda create -n pananse python=3
conda activate pananse
```

Install the latest release of pananse:

```
pip install git+https://github.com/qxuchn/PANANSE.git
```

## Usage

Remember to activate the environment before using it
```
conda activate pananse
```

### Tutorial

