#!/usr/bin/env nextflow

process results {
    label "process_small"
    label "python"
    publishDir "${params.outdir}/", mode: "copy"

    input:
    path "results.py"
    path results_file
    
    output:
    path "results.html"

    script:
    """
    python3 results.py -i $results_file
    """
}