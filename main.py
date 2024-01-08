import json
import logging
import os
import argparse
import time

from llm_autoeval.table import make_table, make_final_table
from llm_autoeval.upload import upload_to_github_gist

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

MODEL = os.getenv("MODEL")
BENCHMARK = os.getenv("BENCHMARK")
GITHUB_API_TOKEN = os.getenv("GITHUB_API_TOKEN")


def main(directory: str, elapsed_time: float) -> None:
    # Variables
    tables = []
    averages = []

    # Tasks
    if BENCHMARK == "openllm":
        tasks = ["ARC", "HellaSwag", "MMLU", "TruthfulQA", "Winogrande", "GSM8K"]
    elif BENCHMARK == "nous":
        tasks = ["AGIEval", "GPT4All", "TruthfulQA", "Bigbench"]
    else:
        raise NotImplementedError(f"BENCHMARK should be 'openllm' or 'nous' (current value = {BENCHMARK})")

    # Load results
    for task in tasks:
        file_path = f"{directory}/{task.lower()}.json"
        if os.path.exists(file_path):
            json_data = open(file_path, "r").read()
            data = json.loads(json_data, strict=False)
            table, average = make_table(data, task)
        else:
            table = ""
            average = "Error: File does not exist"

        tables.append(table)
        averages.append(average)

    # Generate tables
    summary = ""
    for index, task in enumerate(tasks):
        summary += f"### {task}\n{tables[index]}\nAverage: {averages[index]}%\n\n"
    result_dict = {k: v for k, v in zip(tasks, averages)}

    # Calculate the final average, excluding strings
    if all(isinstance(e, float) for e in averages):
        final_average = round(sum(averages) / len(averages), 2)
        summary += f"Average score: {final_average}%"
        result_dict.update({"Average": final_average})
    else:
        summary += "Average score: Not available due to errors"

    # Add elapsed time
    convert = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))
    summary += f"Elapsed time: {convert}"

    # Generate final table
    final_table = make_final_table(result_dict, MODEL)
    summary = final_table + "\n" + summary

    # Upload to GitHub Gist
    upload_to_github_gist(
        summary, f"{MODEL.split('/')[-1]}-{BENCHMARK.capitalize()}.md", GITHUB_API_TOKEN
    )


if __name__ == "__main__":
    # Create the parser
    parser = argparse.ArgumentParser(description="Summarize results and upload them.")
    parser.add_argument("directory", type=str, help="The path to the directory with the JSON results")
    parser.add_argument("elapsed_time", type=float, help="Elapsed time since the start of the evaluation")

    # Parse the arguments
    args = parser.parse_args()

    # Check if the directory exists
    if not os.path.isdir(args.directory):
        raise ValueError(f"The directory {args.directory} does not exist.")

    # Call the main function with the directory argument
    main(args.directory)