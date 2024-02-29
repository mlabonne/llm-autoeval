from typing import Dict


def doc_to_text(doc: Dict) -> str:
    return "Topic: {topic}.\nQuestion: {q}\nAnswer: ".format(
        topic=doc["topic_name"], q=doc["question"],
    )

def doc_to_text_mmlu_style(doc: Dict) -> str:
    return f"{doc['question'].strip()}\nA. {doc['opa']}\nB. {doc['opb']}\nC. {doc['opc']}\nD. {doc['opd']}\nAnswer:"
    


COP_TO_STR_ANSWER = {
    0: "opa",
    1: "opb",
    2: "opc",
    3: "opd",
}

COP_TO_LETTER = {
    0: "A",
    1: "B",
    2: "C",
    3: "D",
}


def doc_to_target(doc: Dict) -> str:
    correct_answer = doc[COP_TO_STR_ANSWER[doc["cop"]]]
    return correct_answer

def doc_to_target_mmlu_style(doc: Dict) -> str:
    correct_answer = COP_TO_LETTER[doc["cop"]]
    return correct_answer

def doc_to_choice(doc: Dict) -> list:
    choices = [doc["op" + label] for label in ['a', 'b', 'c', 'd']]
    return choices
