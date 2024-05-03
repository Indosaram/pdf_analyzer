import re
from collections import Counter

from konlpy.tag import Okt


tagger = Okt()


def get_tag(text):
    # preprocess text, remove special characters, etc.
    text = re.sub("[^가-힣\.]", " ", text)
    text = re.sub(" +", " ", text)
    text = re.sub("\.+", ".", text)
    text = re.sub("\. +", "", text)

    removal = [
        "것",
        "를",
        "로",
        "을",
        
        "수",
        "저",
        "제",
        "그",
        "이",
        "의",
        "은",
        "즉",
        "거",
        "때",
        "더",
        "또",
        "뭐",
        "뭔가",
        "무엇",
        "무엇인가",
        "무언가",
        "무언가",
        "무슨",
    ]
    text = re.sub("|".join(removal), "", text)

    nouns = tagger.nouns(text)

    count = Counter(nouns)
    return count.most_common(100)
