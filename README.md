# Nextflow Workflow

## Description

This Nextflow workflow is designed to process genomic data obtained from INDUCE-seq experiments. It performs the following tasks:

1. Filters out reads based on mapping quality.
2. Intersects sample break bed files with AsiSI site bed files.
3. Summarises and normalises the counts of AsiSI breaks.
4. Collects normalised AsiSI break counts into a single file.

## Installation of dependencies

### Dependencies

- Nextflow v23.04.3+
- Docker (optional)
- Python imports in [requirements.txt](requirements.txt)

To build the Docker image on macOS, run the following command:

```bash
docker buildx build --platform=linux/amd64 . -t quay.io/cristinag/indu-c-q:1.0.0
```

On linux:

```bash
docker build . -t quay.io/cristinag/indu-c-q:1.0.0
```

## Running the Workflow

To execute the workflow using Nextflow, run the following command:

### With dependencies installed locally

```bash
nextflow run main.nf -profile test_ci
```

### With Docker or singularity

```bash
nextflow run main.nf -profile test_ci -with-docker
nextflow run main.nf -profile test_ci -with-singularity
```

## Local Development

To install the Python dependencies locally, use the following command:

```bash
pip install -r requirements.txt
```

## Results/Output

Results are output in [results/results.html](results/results.html) - download file and open in browser to view.

## Future development

Add proper CI tests of course.
