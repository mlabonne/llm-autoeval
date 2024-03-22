import json
import logging
import os
import argparse
import time

from lighteval.evaluator import make_results_table

from llm_autoeval.table import make_table, make_final_table
from llm_autoeval.upload import upload_to_github_gist

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

MODEL_ID = os.getenv("MODEL_ID")
BENCHMARK = os.getenv("BENCHMARK")
GITHUB_API_TOKEN = os.getenv("GITHUB_API_TOKEN")


def _make_autoeval_summary(directory: str, elapsed_time: float) -> str:
    # Variables
    tables = []
    averages = []

    # Tasks
    if BENCHMARK == "openllm":
        tasks = ["ARC", "HellaSwag", "MMLU", "TruthfulQA", "Winogrande", "GSM8K"]
    elif BENCHMARK == "nous":
        tasks = ["AGIEval", "GPT4All", "TruthfulQA", "Bigbench"]
    else:
        raise NotImplementedError(
            f"BENCHMARK should be 'openllm' or 'nous' (current value = {BENCHMARK})"
        )

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

    # Generate final table
    final_table = make_final_table(result_dict, MODEL_ID)
    summary = final_table + "\n" + summary
    return summary


def _get_result_dict(directory: str) -> dict:
    """Walk down driectories to get JSON path"""

    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".json"):
                return json.load(open(os.path.join(root, file)))
    raise FileNotFoundError(f"No JSON file found in {directory}")


def _make_lighteval_summary(directory: str, elapsed_time: float) -> str:
    result_dict = _get_result_dict(directory)
    final_table = make_results_table(result_dict)
    summary = f"## {MODEL_ID.split('/')[-1]} - {BENCHMARK.capitalize()}\n\n"
    summary += final_table
    return summary


def main(directory: str, elapsed_time: float) -> None:
    # Tasks
    if BENCHMARK == "openllm" or BENCHMARK == "nous":
        summary = _make_autoeval_summary(directory, elapsed_time)
    elif BENCHMARK == "lighteval":
        summary = _make_lighteval_summary(directory, elapsed_time)
    else:
        raise NotImplementedError(
            f"BENCHMARK should be 'openllm' or 'nous' (current value = {BENCHMARK})"
        )

    # Add elapsed time
    convert = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))
    summary += f"\n\nElapsed time: {convert}"

    # Upload to GitHub Gist
    upload_to_github_gist(
        summary,
        f"{MODEL_ID.split('/')[-1]}-{BENCHMARK.capitalize()}.md",
        GITHUB_API_TOKEN,
    )


if __name__ == "__main__":
    # Create the parser
    parser = argparse.ArgumentParser(description="Summarize results and upload them.")
    parser.add_argument(
        "directory", type=str, help="The path to the directory with the JSON results"
    )
    parser.add_argument(
        "elapsed_time",
        type=float,
        help="Elapsed time since the start of the evaluation",
    )

    # Parse the arguments
    args = parser.parse_args()

    # Check if the directory exists
    if not os.path.isdir(args.directory):
        raise ValueError(f"The directory {args.directory} does not exist.")

    # Call the main function with the directory argument
    main(args.directory, args.elapsed_time)
