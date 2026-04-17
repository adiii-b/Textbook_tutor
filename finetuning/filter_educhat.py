import re
from datasets import load_dataset

dataset = load_dataset("ecnu-icalk/educhat-sft-mixture-all-data-en", split="train")

def has_structure(text):
    bullet_count= len(re.findall(r'^\s*[-*•]\s+', text, re.MULTILINE))
    return 2<= bullet_count <=10

def is_english(text):
    chinese_chars = sum(1 for c in text if '\u4e00' <= c <= '\u9fff')
    return chinese_chars / max(len(text.split()), 1) < 0.1

def length_check(text):
    return 40 <= len(text) <= 250

def no_repetitions(text):
    sentences = [s.strip() for s in re.split(r'[.!?]', text) if s.strip()]
    for i in range(len(sentences)):
        for j in range(i + 1, len(sentences)):
            a = set(sentences[i].lower().split())
            b = set(sentences[j].lower().split())
            if len(a) > 3 and len(b) > 3:
                overlap = len(a & b) / len(a | b)
                if overlap > 0.6:
                    return False
    return True

def ends_correctly(text):
    return text.strip().endswith(('.', '!', '?', '。', '！', '？'))

def has_explanation(text):
    return any(keyword in text for keyword in ['because', 'for example', 'this means', 'the reason', 'think of it', 'imagine', 'in other words', 'which is why'])