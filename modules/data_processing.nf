#!/usr/bin/env nextflow

process filter_bed {
    label "process_small"
    label "python"
    publishDir "${params.outdir}/filtered_beds/", mode: "copy"

    input:
    path "quality_filter.py"
    path sample
    
    output:
    tuple val("${sample.simpleName}"), path("${sample.baseName}.filtered.bed"), env(TOTAL), emit: filtered

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
    tuple val(sample_id), path(sample), val(total_count), path("asisi_intersection.py"), path(asisi_sites)

    output:
    path("${sample.baseName}.normalised_counts.bed"), emit: intersections

    script:
    """
    python3 asisi_intersection.py \
        -s $sample \
        -a $asisi_sites \
        -c $total_count \
        -o ${sample.baseName}.normalised_counts.bed
    """
}

process plot_results {
    label "process_small"
    label "python"
    publishDir "${params.outdir}/normalised_results/", mode: "copy"

    input:
    path normalised_counts

    output:
    path "normalised_results.tsv" 

    script:
    """
    echo "sample_id\tchrom\tstart\tend\tcount" > normalised_results.tsv
    for file in ${normalised_counts.join(' ')}; do
        sample_id=\$(basename -- "\${file}" .breakends.filtered.normalised_counts.bed)
        while IFS= read -r line; do
            echo -e "\${sample_id}\t\${line}" >> normalised_results.tsv
        done < "\$file"
    done
    """
}
