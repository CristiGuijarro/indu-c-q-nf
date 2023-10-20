#!/usr/bin/env nextflow

process filter_bed {
    label "process_small"
    label "python"
    publishDir "${params.outdir}/filtered_beds/", mode: "copy"

    input:
    path "quality_filter.py"
    path sample
    
    output:
    path "${sample.baseName}.filtered.bed", emit: filtered
    tuple val("${sample.simpleName}"), env(TOTAL), emit: total_counts

    script:
    """
    python3 quality_filter.py \
        -i $sample \
        -o ${sample.baseName}.filtered.bed \
        -m ${params.mapq_thresh}

    TOTAL=\$(wc -l < $sample)
    """
}

process find_asisi_intersections {
    label "process_small"
    label "python"
    publishDir "${params.outdir}/intersections/", mode: "copy"

    input:
    path "asisi_intersection.py"
    each path(sample)
    path asisi_sites

    output:
    tuple val("${sample.simpleName}"), path("${sample.baseName}.intersection.bed"), env(COUNTS), emit: intersections

    script:
    """
    python3 asisi_intersection.py \
        -s $sample \
        -a $asisi_sites \
        -o ${sample.baseName}.intersection.bed

    COUNTS=\$(wc -l < $sample)
    """
}

process normalised_counts {
    label "process_small"
    label "python"
    publishDir "${params.outdir}/normalised/", mode: "copy"

    input:
    val normalised_counts

    output:
    path "normalized_results.tsv"

    script:
    """
    echo "sample\tnormalised_breaks" > normalized_results.tsv
    echo ${normalised_counts.join','} | sed 's/,/\\n/g' >> normalized_results.tsv
    """

}
