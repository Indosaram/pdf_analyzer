import fitz


class PDF:
    def __init__(self, filename):
        self.doc = fitz.open(filename)  # open a document
        self.text = ""

    @staticmethod
    def _add_highlight_to_page(page, keyword, color):
        texts = page.search_for(keyword, quads=True)

        # mark all found quads with one annotation
        annot = page.add_highlight_annot(texts)
        # clear light pink as highlight color
        annot.set_colors(stroke=color)
        annot.set_opacity(0.5)

    def add_highlights(self, keywords, colors):
        for keyword, color in zip(keywords, colors):
            for page in self.doc:
                self._add_highlight_to_page(page, keyword, color)

    def save(self, filename):
        self.doc.save(filename)

    def get_all_text(self):
        if not self.text:
            for page in self.doc:
                self.text += page.get_text()
        return self.text

    def extract_paragraph(self):
        paragraphs = []
        for page in self.doc:
            paragraph = ""
            for sentence in page.get_text().split('\n'):
                if sentence.endswith("다."):
                    paragraph += sentence
                    paragraphs.append(paragraph)
                    paragraph = ""
                else:
                    paragraph += sentence

            if paragraph:
                paragraphs.append(paragraph)

        return paragraphs
