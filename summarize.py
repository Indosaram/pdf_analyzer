from tkinter.ttk import Progressbar

import nltk
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

nltk.download('punkt')


tokenizer = AutoTokenizer.from_pretrained(
    "eenzeenee/t5-base-korean-summarization"
)
model = AutoModelForSeq2SeqLM.from_pretrained(
    "eenzeenee/t5-base-korean-summarization"
)


def summarize(paragraphs, progress_bar: Progressbar):
    summarized = []

    progress_bar.configure(maximum=len(paragraphs))
    for paragraph in paragraphs:
        inputs = tokenizer(
            paragraph, max_length=512, truncation=True, return_tensors="pt"
        )
        output = model.generate(
            **inputs, num_beams=3, do_sample=True, min_length=10, max_length=64
        )
        decoded_output = tokenizer.batch_decode(
            output, skip_special_tokens=True
        )[0]
        summarized.append(nltk.sent_tokenize(decoded_output.strip())[0])

        progress_bar.step(1)

    return summarized
