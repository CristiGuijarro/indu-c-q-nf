#!/usr/bin/env nextflow

nextflow.enable.dsl = 2

def summary = [:]

if (workflow.revision) summary["Pipeline Release"] = workflow.revision

summary["Launch dir"]                                  = workflow.launchDir
summary["Working dir"]                                 = workflow.workDir
summary["Script dir"]                                  = workflow.projectDir
summary["User"]                                        = workflow.userName
summary["Output dir"]                                  = params.outdir
summary["Samples"]                                     = params.samples
summary["AsiSI File"]                                  = params.asisi_file
summary["mapQ Threshold"]                              = params.mapq_thresh

log.info summary.collect { k,v -> "${k.padRight(18)}: $v" }.join("\n")
log.info "-\033[2m--------------------------------------------------\033[0m-"

def helpMessage() {

    log.info """
    Usage:
    The typical command for running the pipeline is as follows:

    nextflow run main.nf --samples sample.breakends.bed --asisi_file chr21_AsiSI_sites.t2t.bed

    Mandatory:
    --samples           Input pre-processed sample bed file(s) containing only the breaksite
                        coordinates (default: $params.samples)
    --asisi_file        Input bed file that contains the positions of AsiSI sites (default: $params.asisi_file)
    --mapq_thresh       Threshold with which to filter the breaksite sample bed files as equal to or
                        greater than (default: $params.mapq_thresh)

    Resource Options:
    --max_cpus          Maximum number of CPUs (int)
                        (default: $params.max_cpus)  
    --max_memory        Maximum memory (memory unit)
                        (default: $params.max_memory)
    --max_time          Maximum time (time unit)
                        (default: $params.max_time)

    """.stripIndent()

}

include { filter_bed; find_asisi_intersections; plot_results } from "./modules/data_processing.nf"
include { results } from "./modules/results_processing.nf"


workflow {
    if (params.help) { helpMessage(); exit 0 }

    // User input
    samples = Channel.fromPath("${params.samples}")
    asisi_sites = Channel.fromPath("${params.asisi_file}")

    // Scripts as input
    quality_filter_exe = Channel.value("${workflow.projectDir}/bin/quality_filter.py")
    asisi_intersections_exe = Channel.value("${workflow.projectDir}/bin/asisi_intersection.py")
    results_exe = Channel.value("${workflow.projectDir}/bin/results.py")

    // step 1
    filtered_out = filter_bed(
        quality_filter_exe,
        samples
    )

    // step 2 & 3
    normalised_out = filtered_out.filtered 
        | combine(asisi_intersections_exe)
        | combine(asisi_sites)
        | find_asisi_intersections

    // step 4
    collected_counts = normalised_out.intersections
        | collect
        | plot_results

    results(
        results_exe,
        collected_counts
    )
}
