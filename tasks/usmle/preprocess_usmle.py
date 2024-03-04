from typing import Dict


def doc_to_text(doc: Dict) -> str:
    return "Question: {}\nAnswer:".format(doc["sent1"])


LABEL_TO_FEATURE = {
    0: "ending0",
    1: "ending1",
    2: "ending2",
    3: "ending3",
}


def doc_to_target(doc: Dict) -> str:
    correct_answer = doc[LABEL_TO_FEATURE[doc["label"]]]
    return correct_answer


def doc_to_choice(doc: Dict) -> list:
    choices = [doc[v] for v in LABEL_TO_FEATURE.values()]
    return choices
