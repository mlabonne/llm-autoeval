import datasets
from typing import List
import string

from sklearn.metrics import balanced_accuracy_score

from nltk.stem.porter import *
import re

import numpy as np

def process_docs(dataset: datasets.Dataset) -> datasets.Dataset:
    def _process_doc(doc):
        out_doc = {
            "query": doc["inputs"],
            "choices": doc["multiple_choice_targets"],
            "gold": doc["answer"],
        }
        return out_doc

    return dataset.map(_process_doc)
