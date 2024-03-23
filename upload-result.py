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

def main(directory: str, elapsed_time: float) -> None:
    file_path = "/workspace/lm-evaluation-harness/result.log"
    summary = open(file_path, "r").read()
    upload_to_github_gist(
        summary, f"{MODEL.split('/')[-1]}-MedTasks.md", GITHUB_API_TOKEN
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
