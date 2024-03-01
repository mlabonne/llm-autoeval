import re
from typing import Dict

import numpy as np
from rouge_score import rouge_scorer, scoring

import datasets

max_length = 4000
max_length_chars = 4 * max_length


def doc_to_text(doc):
    description = doc['description']
    d_len = len(description)
    a_len = len(doc['abstract'])
    if (d_len + a_len) > max_length_chars:
        print(f"WARN: d_len={d_len} a_len={a_len}")
    return f"Patent description: {description}. Patent abstract summary: "


def doc_to_target(doc):
    if not doc['abstract']:
        print(f"no abstract for doc: {doc['description']}")
        if not doc['description']:
            return "No abstract"
        return doc['description'][0:100]
    return doc['abstract']


def process_docs(dataset: datasets.Dataset) -> datasets.Dataset:
    # remove empty desciptions
    print(f"Original ds ={dataset}")
    filtered = dataset.filter(lambda example: len(example["description"]) > 0)
    print(f"Filtered ds {filtered}")
    return filtered.map(preprocess_function_gen)


def process_docs_gen(dataset: datasets.Dataset) -> datasets.Dataset:
    dataset = dataset.select(range(4))
    # remove empty descriptions
    print(f"Original ds ={dataset}")
    filtered = dataset.filter(lambda example: len(example["description"]) > 0)
    print(f"Filtered ds ={filtered}")
    filtered = filtered.select(range(2000))
    return filtered.map(preprocess_function_gen)


def preprocess_function_gen(example):
    def _format_answers(answer):
        answer = answer.strip()
        if len(answer):
            if answer[-1] != ".":
                answer = answer + "."
        return answer

    description = example['description']
    if len(description) == 0:
        print(f"empty desc for sample: {example}")
    split = description.split('\n')
    splits_lens = [len(s) for s in split]
    description = split[0]
    d_len = len(description)
    if d_len == 0:
        idx = next(i for i, s_len in enumerate(splits_lens) if s_len > 0)
        description = split[idx]
        d_len = len(description)
        print(f"splits_lens={splits_lens} idx={idx} d_len={d_len}")

    a_len = len(example['abstract'])

    while (d_len + a_len) > max_length_chars:  # shrink desc
        reduce_estimate = (d_len + a_len) - max_length_chars
        description = description[:-reduce_estimate]
        d_len = len(description)

    # TODO: some random abstract as incorrect answer?
    # incorrect_answers = _format_answers(examples["incorrect_answers"])
    correct_answer = _format_answers(example["abstract"])
    # correct_answer = correct_answer[0:100]
    example['description'] = description

    if (d_len + a_len) > max_length_chars:
        print(f"WARN: Total length exceeds the limit: d_len={d_len} a_len={a_len}")
    return {
        # "question": "",
        "correct_answers": [correct_answer],
        "abstract": correct_answer,
        # "incorrect_answers": incorrect_answers,
        'description': description
    }


def process_results_gen(doc, results):
    completion = results[0]
    true_refs, false_refs = doc["correct_answers"], None  # , doc["incorrect_answers"]
    all_refs = true_refs  # + false_refs

    # Process the sentence-level BLEURT, BLEU, and ROUGE for similarity measures.

    # ROUGE-N
    rouge_scores = [rouge([ref], [completion]) for ref in all_refs]
    # ROUGE-1
    rouge1_scores = [score["rouge1"] for score in rouge_scores]
    rouge1_correct = np.nanmax(rouge1_scores[: len(true_refs)])
    # rouge1_incorrect = np.nanmax(rouge1_scores[len(true_refs):])
    rouge1_max = rouge1_correct
    # rouge1_diff = rouge1_correct - rouge1_incorrect
    # rouge1_acc = int(rouge1_correct > rouge1_incorrect)
    # ROUGE-2
    rouge2_scores = [score["rouge2"] for score in rouge_scores]
    rouge2_correct = np.nanmax(rouge2_scores[: len(true_refs)])
    # rouge2_incorrect = np.nanmax(rouge2_scores[len(true_refs):])
    rouge2_max = rouge2_correct
    # rouge2_diff = rouge2_correct - rouge2_incorrect
    # rouge2_acc = int(rouge2_correct > rouge2_incorrect)
    # ROUGE-L
    rougeL_scores = [score["rougeLsum"] for score in rouge_scores]
    rougeL_correct = np.nanmax(rougeL_scores[: len(true_refs)])
    # rougeL_incorrect = np.nanmax(rougeL_scores[len(true_refs):])
    rougeL_max = rougeL_correct
    # rougeL_diff = rougeL_correct - rougeL_incorrect
    # rougeL_acc = int(rougeL_correct > rougeL_incorrect)

    return {
        "rouge1_max": rouge1_max,
        # "rouge1_acc": rouge1_acc,
        # "rouge1_diff": rouge1_diff,
        "rouge2_max": rouge2_max,
        # "rouge2_acc": rouge2_acc,
        # "rouge2_diff": rouge2_diff,
        "rougeL_max": rougeL_max,
        # "rougeL_acc": rougeL_acc,
        # "rougeL_diff": rougeL_diff,
    }


def rouge(refs, preds):
    """
    Returns `t5` style ROUGE scores. See the related implementation:
    https://github.com/google-research/text-to-text-transfer-transformer/blob/3d10afd51ba97ac29eb66ae701eca274488202f7/t5/evaluation/metrics.py#L68

    :param refs:
        A `list` of reference `strs`.
    :param preds:
        A `list` of predicted `strs`.
    """
    rouge_types = ["rouge1", "rouge2", "rougeLsum"]
    scorer = rouge_scorer.RougeScorer(rouge_types)

    # Add newlines between sentences to correctly compute `rougeLsum`.

    def _prepare_summary(summary):
        summary = summary.replace(" . ", ".\n")
        return summary

    # Accumulate confidence intervals.
    aggregator = scoring.BootstrapAggregator()
    for ref, pred in zip(refs, preds):
        ref = _prepare_summary(ref)
        pred = _prepare_summary(pred)
        aggregator.add_scores(scorer.score(ref, pred))
    result = aggregator.aggregate()
    return {type: result[type].mid.fmeasure * 100 for type in rouge_types}
