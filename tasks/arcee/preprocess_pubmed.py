import re
from typing import Dict

import datasets

def process_docs(dataset: datasets.Dataset):
    ds_slice =dataset.select(range(1000))
    print(f"!!! ds={ds_slice}")
    return ds_slice
    #return dataset


def doc_to_text_pubmed500(doc):
    return " ".join([doc["title"], doc["doc"]])


def doc_to_text(doc: Dict):
    return doc["text"]
