#!/usr/bin/env python3
"""Python script to parse and filter the sample bed files"""
import argparse

def filter_bed_file(input_file: str, mapq_thresh: int):
    """Generator function to yield lines from a BED file where the mapQ is greater
    than or equal to the specified `mapq_thresh` threshold.

    Args:
        input_file (str): The path to the input BED file.
        mapq_thresh (int): The threshold to filter mapQ in the input BED file.

    Yields:
        str: A line from the BED file that meets the mapQ filtering criteria.
    """
    with open(input_file, "r", encoding="utf8") as file_in:
        for line in file_in:
            if int(line.strip().split("\t")[4]) >= mapq_thresh:
                yield line


def main():
    """Main function to handle the command arguments"""
    parser = argparse.ArgumentParser(description="Filter BED file based on mapQ.")
    parser.add_argument(
        "-i", "--input_file",
        help="Input BED file",
        required=True
    )
    parser.add_argument(
        "-o", "--output_file",
        help="Output BED file",
        required=True
    )
    parser.add_argument(
        "-m", "--mapq_threshold",
        help="Threshold to filter >= mapQ",
        type=int,
        default=30,
        required=True
    )
    args = parser.parse_args()

    filtered_lines = filter_bed_file(args.input_file, args.mapq_threshold)

    with open(args.output_file, "w", encoding="utf8") as file_out:
        for line in filtered_lines:
            file_out.write(line)


if __name__ == "__main__":
    main()
