import os
from typing import List


def agg_results(input_files: List[str], output_file: str):
    """
    Aggregrates the results of the snakemake benchmark.

    Combines csv files with identical columns into a single csv file.

    :param input_files: List of csv files with identical header.
    :param output_file: Output csv file.
    """
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    has_header = False
    # print(f"exp_results={input.exp_results}")
    with open(output_file, 'w') as out_stream:
        for res in input_files:
            with open(res, 'r') as in_stream:
                if has_header:
                    # skip header line
                    in_stream.readline()
                else:
                    out_stream.writelines(in_stream.readline())
                    has_header = True
                # write results to common file.
                out_stream.writelines(in_stream.readlines())


def agg_from_directory(input_dir: str, output_file: str):
    """Aggregates all results from a directory. Used to aggregate partial results."""
    file_list = [input_dir + os.sep + f for f in os.listdir(input_dir)]
    agg_results(file_list, output_file)
