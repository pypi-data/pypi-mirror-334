# immundata-py

An efficient data framework for single-cell and bulk immune repertoire datasets of practically any scale.

Think AnnData, SingleCellExperiment or Seurat object, but for AIRR with the full support for out-of-memory datasets and easier access to additional receptor data such as gene expression from single-cell transcriptomics files, spatial data coordinates, or antigen specificity data, provided by user.
The goal of `immundata` is to standardize I/O and basic data manipulation, following the AIRR Community Data Standard for immune repertoire representation.
It's primary users are bioinformatics developers and data engineers who don't want to write from scratch an abstraction layer over the data.
Biologists and medical scientists could benefit as well, considering they learn the code syntaxis. However, the overall philosophy is to make sure that
immune repertoire data analysis tools such as `immunarch` cover more than 80% of use cases without explicitly using `immundata` by the end user.

## Installation

```bash
uv install
```

## Usage

See `notebooks/immundata-experiments.ipynb`.
