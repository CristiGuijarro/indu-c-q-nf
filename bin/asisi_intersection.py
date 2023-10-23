#!/usr/bin/env python3
"""Python script to parse and extract intersection positions between the sample BED
file and the recorded AsiSI sites BED file"""
import argparse

class GenomicRegion:
    """Represents a genomic region defined by chromosome, start position, and end
    position.

    Attributes:
        chrom (str): The chromosome of the genomic region.
        start (int): The start position of the genomic region.
        end (int): The end position of the genomic region.
    """
    def __init__(self, chrom, start, end):
        self.chrom = chrom
        self.start = start
        self.end = end


def read_bed_file(bed_file: str) -> list:
    """Parse and extract the genomic regions from the given BED file

    Args:
        bed_file (str): relative path to BED file

    Returns:
        list: list of `GenomicRegion` objects
    """
    regions = []
    with open(bed_file, 'r', encoding="utf8") as file:
        regions = [GenomicRegion(*(line.strip().split('\t')[:3])) for line in file]
    return regions


def intersect_bed_files(sample_bed: str, asisi_bed: str, total_count: int) -> dict:
    """Find intersections between sample BED file and AsiSI break sites BED file
    and calculate the normalised count.

    Args:
        sample_bed (str): BED file from samples
        asisi_bed (str): BED file of AsiSI break sites
        total_count (int): Total count value

    Returns:
        dict: dictionary of intersecting `GenomicRegion` objects from asisi_bed as
            keys with their normalised counts as values
    """
    sample_regions = read_bed_file(sample_bed)
    asisi_breaks = read_bed_file(asisi_bed)

    intersecting_regions = {}

    for sample_region in sample_regions:
        for asisi_region in asisi_breaks:
            if asisi_region.start <= sample_region.start <= asisi_region.end and \
                    asisi_region.start <= sample_region.end <= asisi_region.end:
                if asisi_region not in intersecting_regions:
                    intersecting_regions[asisi_region] = 1
                else:
                    intersecting_regions[asisi_region] += 1
                break

    # Calculate normalised counts
    for region, count in intersecting_regions.items():
        intersecting_regions[region] = count / (total_count / 1000)

    return intersecting_regions


def main():
    """Main function to handle the command arguments"""
    parser = argparse.ArgumentParser(description="Filter BED file based on mapQ.")
    parser.add_argument(
        "-s", "--sample_bed",
        help="Input sample BED file",
        required=True
    )
    parser.add_argument(
        "-a", "--asisi_bed",
        help="Input AsiSI BED file",
        required=True
    )
    parser.add_argument(
        "-c", "--total_count",
        type=int,
        help="Total Break count in unfiltered BED file",
        required=True
    )
    parser.add_argument(
        "-o", "--output_file",
        help="Intersections output BED file",
        required=True
    )
    
    args = parser.parse_args()

    intersection = intersect_bed_files(args.sample_bed, args.asisi_bed, args.total_count)

    with open(args.output_file, "w", encoding="utf8") as file_out:
        for region, count in intersection.items():
            file_out.write(f"{region.chrom}\t{region.start}\t{region.end}\t{count}\n")


if __name__ == "__main__":
    main()
