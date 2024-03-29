import math
import os

from pytablewriter import MarkdownTableWriter

BENCHMARK = os.getenv("BENCHMARK")


def get_acc_norm(data):
    accs = [
        data["results"][k]["acc_norm"]
        if "acc_norm" in data["results"][k]
        else data["results"][k]["acc"]
        for k in data["results"]
    ]
    acc = sum(accs) / len(accs) * 100
    return acc


def get_mcg(data):
    accs = [data["results"][k]["multiple_choice_grade"] for k in data["results"]]
    acc = sum(accs) / len(accs) * 100
    return acc


def calculate_average(data, task):
    task = task.lower()
    print(data)

    if BENCHMARK == "openllm":
        if task == "arc":
            return data["results"]["arc_challenge"]["acc_norm,none"] * 100
        elif task == "hellaswag":
            return data["results"]["hellaswag"]["acc_norm,none"] * 100
        elif task == "mmlu":
            return data["results"]["mmlu"]["acc,none"] * 100
        elif task == "truthfulqa":
            value = data["results"]["truthfulqa_mc2"]["acc,none"]
            return 0.0 if math.isnan(value) else value * 100
        elif task == "winogrande":
            return data["results"]["winogrande"]["acc,none"] * 100
        elif task == "gsm8k":
            return data["results"]["gsm8k"]["exact_match,strict-match"] * 100

    elif BENCHMARK == "nous":
        if task == "agieval":
            return get_acc_norm(data)
        elif task == "gpt4all":
            return get_acc_norm(data)
        elif task == "bigbench":
            return get_mcg(data)
        elif task == "truthfulqa":
            value = data["results"]["truthfulqa_mc"]["mc2"]
            return 0.0 if math.isnan(value) else value * 100

    raise NotImplementedError(f"Could not find task {task} for benchmark {BENCHMARK}")


def make_table(result_dict, task):
    """
    Generate table of results.
    Based on https://github.com/mlabonne/llm-autoeval/blob/master/llm_autoeval/table.py
    """
    md_writer = MarkdownTableWriter()
    md_writer.headers = ["Task", "Average", "Version", "Metric", "Value", "", "Stderr"]

    values = []

    average = round(calculate_average(result_dict, task), 2)

    for k, dic in result_dict["results"].items():
        version = result_dict["versions"].get(k, "N/A")
        n = str(result_dict["n-shot"][k])

        if "alias" in dic:
            k = dic.pop("alias")

        for (mf), v in dic.items():
            m, _, f = mf.partition(",")
            if m.endswith("_stderr"):
                continue

            if m + "_stderr" + "," + f in dic:
                se = dic[m + "_stderr" + "," + f]
                if se != "N/A":
                    se = "%.4f" % se
                values.append([k, version, f, n, m, "%.4f" % v, "±", se])
            else:
                values.append([k, version, f, n, m, "%.4f" % v, "", ""])
            k = ""
            version = ""

    md_writer.value_matrix = values
)
    return md_writer.dumps(), average


def make_final_table(result_dict, model_name):
    """Generate table of results with model name.

    Args:
    result_dict (dict): A dictionary where keys are headers and values are the values in the table.
    model_name (str): The name of the model to be included in the table.

    Returns:
    str: A string representing the markdown table.
    """
    md_writer = MarkdownTableWriter()
    # Add 'Model' as the first header and then the rest from the dictionary keys
    md_writer.headers = ["Model"] + list(result_dict.keys())

    # The values in the table will be the model name and then the values from the dictionary
    values = [
        f"[{model_name.split('/')[-1]}](https://huggingface.co/{model_name})"
    ] + list(result_dict.values())

    # The table only has one row of values
    md_writer.value_matrix = [values]

    # Return the table as a markdown formatted string
    return md_writer.dumps()
