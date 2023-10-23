#!/usr/bin/env python3
"""Python script to parse and extract intersection results from the
normalised AsiSI sites intersections with samples"""
import argparse

import pandas as pd
import plotly.express as px


def analyse_data(dframe: pd.DataFrame) -> list:
    """Analyses the dataframe of normalised AsiSI counts to infer
    the samples that are cases or controls, uncertain and the maximum
    percentage of AsiSI site that is observed in a single sample

    Args:
        dframe (pd.DataFrame): Takes a Pandas DataFrame object with normalised
            AsiSI counts per site per sample

    Returns:
        list: Containing cases, controls, uncertain_samples, max_percentage
    """
    max_percentage = dframe["count"].max()
    mean_normalised = dframe["count"].mean()
    cases = set(dframe[dframe["count"] > mean_normalised]["sample_id"])
    controls = set(dframe[dframe["count"] <= mean_normalised]["sample_id"])

    uncertain_samples = None
    if len(cases) != 0 and len(controls) != 0:
        if len(cases) > len(controls):
            uncertain_samples = set(controls) - set(cases)
        else:
            uncertain_samples = set(cases) - set(controls)

    return cases, controls, uncertain_samples, max_percentage

def main():
    """Main function to handle the command arguments"""
    parser = argparse.ArgumentParser(description="Filter BED file based on mapQ.")
    parser.add_argument(
        "-i", "--input_file",
        help="Input BED file",
        required=True
    )

    args = parser.parse_args()

    dframe = pd.read_csv(args.input_file, sep="\t")

    cases, controls, uncertain_samples, max_percentage = analyse_data(dframe)

    title="Box Plot of Normalised Counts per AsiSI Site per Sample"

    fig_box = px.box(
        dframe,
        x="sample_id",
        y="count",
        points="all",
        hover_data=["start", "end", "chrom"]
    )

    mean_value = dframe['count'].mean()
    std_deviation = dframe['count'].std()

    fig_box.add_shape(
        type="line",
        x0=0,
        y0=mean_value - std_deviation,
        x1=1,
        y1=mean_value - std_deviation,
        line=dict(
            color="LightSeaGreen",
            width=2,
            dash="longdashdot",
        )
    )

    fig_box.add_shape(
        type="line",
        x0=0,
        y0=mean_value + std_deviation,
        x1=1,
        y1=mean_value + std_deviation,
        line=dict(
            color="orange",
            width=2,
            dash="longdashdot",
        )
    )

    title = "Box Plot of Normalised Counts per AsiSI Site per Sample"
    subtitle = (
        f"Cases: {cases}<br>Controls: {controls}<br>Uncertain: {uncertain_samples}<br>Max: {max_percentage}"
    )
    fig_box.update_layout(title=f"{title}<br><sub>{subtitle}</sub>")

    fig_box.write_html("results.html")


if __name__ == "__main__":
    main()
