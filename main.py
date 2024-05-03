import sys
import tkinter as tk
from datetime import datetime
from tkinter import filedialog, messagebox, ttk


from pdf import PDF
from nlp import get_tag
from summarize import summarize

COLORS = [
    # light blue
    (0, 0.92, 0.92),
    # light green
    (0, 0.92, 0),
    # light yellow
    (0.92, 0.92, 0),
    # light red
    (0.92, 0, 0),
    # light purple
    (0.92, 0, 0.92),
    # light orange
    (0.92, 0.46, 0),
    # light brown
    (0.46, 0.23, 0),
    # light gray
    (0.46, 0.46, 0.46),
    # light pink
    (0.92, 0.46, 0.46),
    # light olive
    (0.46, 0.46, 0),
    # light navy
    (0, 0, 0.46),
    # light teal
    (0, 0.46, 0.46),
    # light magenta
    (0.46, 0, 0.46),
    # light lime
    (0, 0.46, 0),
    # light peach
    (0.92, 0.77, 0.62),
    # light mint
    (0.62, 0.92, 0.77),
]


class App:
    def __init__(self, master):
        self.master = master
        self.master.title("PDF Analyzer")
        self.master.geometry("800x800")
        self.frame = tk.Frame(self.master, width=1500, height=1000)
        self.frame.pack()

        # file explorer using filedialog
        self.filepath_label = tk.Label(self.frame, text="pdf 파일 경로")
        self.filepath_label.pack()
        self.filepath_entry = tk.Entry(self.frame, width=300)
        self.filepath_entry.pack()
        self.filepath_dialog = tk.Button(
            self.frame, text="파일 선택", command=self.open_file
        )
        self.filepath_dialog.pack()

        self.filename = None

        self.start_button = tk.Button(self.frame, text="시작", command=self.run)
        self.start_button.pack()
        self.end_button = tk.Button(self.frame, text="종료", command=self.close)
        self.end_button.pack()

        self.pbar = ttk.Progressbar(
            self.frame, orient="horizontal", length=200, mode="determinate"
        )
        self.pbar.pack()

        self.result = ttk.Treeview(
            self.frame,
            height=15,
            selectmode="extended",
            columns=2,
            show="headings",
        )

        self.result["columns"] = ("단어", "빈도수")
        self.result.column("단어", width=100)
        self.result.column("빈도수", width=100)
        self.result.heading("단어", text="단어")
        self.result.heading("빈도수", text="빈도수")
        self.result.pack()

        # log frame
        bottom_frame = tk.Frame(self.frame)
        bottom_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        self.log = tk.Text(bottom_frame, height=10, width=100)
        self.log.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(bottom_frame, command=self.log.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.log.config(yscrollcommand=scrollbar.set)

    def __del__(self):
        self.logger("Closing UI...")

    def open_file(self):
        self.filename = filedialog.askopenfilename(
            filetypes=(("Excel files", "*.pdf"),)
        )
        self.filepath_entry.insert(0, self.filename)
        # init pdf
        self.pdf = PDF(self.filename)

    def close(self):
        self.master.destroy()
        sys.exit()

    def logger(self, message):
        self.log.insert(tk.END, f"{datetime.now()} {message}\n")
        self.log.see(tk.END)

    def save(self):
        try:
            # add `output` suffix to the filename
            self.pdf.save(
                self.filename.replace(".pdf", "_output.pdf"),
            )
            messagebox.showinfo("완료", "완료되었습니다.")
        except Exception as exc:
            messagebox.showinfo(f"에러가 발생했습니다: {exc}")

    def run(self):
        if not self.filename:
            messagebox.showinfo("경고", "파일을 선택해주세요.")
            return

        self.logger("Start analyzing...")
        self.pbar["value"] = 0

        self.logger("Extracting text from PDF...")
        self.pdf.get_all_text()

        self.logger("Extracting nouns from text...")
        tags = get_tag(self.pdf.text)

        self.pdf.add_highlights([tag[0] for tag in tags[:15]], COLORS)

        for tag, freq in tags[::-1]:
            self.result.insert("", 0, values=(tag, freq))

        self.logger("Summarizing paragraphs...")
        paragraphs = self.pdf.extract_paragraph()
        summarized = summarize(paragraphs, progress_bar=self.pbar)

        with open(f"{self.filename}_summarized.txt", "w") as file:
            for line in summarized:
                file.write(line + "\n")

        self.save()


from konlpy import utils
import os

folder_suffix = [
    # JAR
    '{0}',
    # Java sources
    '{0}{1}bin',
    '{0}{1}*',
    # Hannanum
    '{0}{1}jhannanum-0.8.4.jar',
    # Kkma
    '{0}{1}kkma-2.0.jar',
    # Komoran3
    '{0}{1}aho-corasick.jar',
    '{0}{1}shineware-common-1.0.jar',
    '{0}{1}shineware-ds-1.0.jar',
    '{0}{1}komoran-3.0.jar',
    # Twitter (Okt)
    '{0}{1}snakeyaml-1.12.jar',
    '{0}{1}scala-library-2.12.3.jar',
    '{0}{1}open-korean-text-2.1.0.jar',
    '{0}{1}twitter-text-1.14.7.jar',
    '{0}{1}*',
]

javadir = '%s%sjava' % (utils.installpath, os.sep)
print(f"javadir:", javadir)
args = [javadir, os.sep]
for f in folder_suffix:
    print(f.format(*args))

root = tk.Tk()
app = App(root)
root.mainloop()
