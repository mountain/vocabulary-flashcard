import glob

card_template = """\\begin{flashcard}{%s}
    \\vspace*{\\fill}
    \\begin{center}
        \\begin{minipage}[c]{.45\\textwidth}
            \includegraphics[width=\\textwidth]{cards/%s/%s/%s}
        \end{minipage}
        \\begin{minipage}[c]{.45\\textwidth}
            \\begin{itemize}\setlength\itemsep{12pt}
            \item Explanation: \\ %s
            \item Example: \\ %s
            \end{itemize}
        \end{minipage}
    \end{center}
    \\vspace*{\\fill}
\end{flashcard}"""

paper_template = """\documentclass[avery5371, grid,frame]{flashcards}

\\usepackage{graphicx}
\\usepackage{geometry}

\geometry{a4paper, landscape, margin=0.2in}
\cardfrontstyle[\large\slshape]{headings}
\cardbackstyle{empty}

\\begin{document}

\\renewcommand{\cardpaper}{a4paper}
\\renewcommand{\cardpapermode}{landscape}
\\renewcommand{\cardrows}{2}
\\renewcommand{\cardcolumns}{2}
\setlength{\cardheight}{3.5in}
\setlength{\cardwidth}{5.0in}
\setlength{\\topoffset}{0.50in}
\setlength{\oddoffset}{0.50in}
\setlength{\evenoffset}{0.50in}

%s

\end{document}"""


def gen(env):
    cards = ""
    index, word, explanation, pngs, examples = env
    for png, example in zip(pngs, examples):
        cards += card_template % (word, index, word, png, explanation, example)
    paper = paper_template % cards
    with open("cards/%s/%s/%s.tex" % (index, word, word), "w") as f:
        f.write(paper)


def iteration():
    for wpath in glob.glob("cards/*/*"):
        word = wpath.split('/')[-1]
        index = word[0]

        pngs = []
        examples = []
        for pngfile in glob.glob(wpath + "/*.png"):
            png = pngfile.split('/')[-1]
            example = png[len(word) + 3:-4]
            pngs.append(png)
            examples.append(example)

        with open(wpath + "/explanation.txt", "r") as f:
            explanation = f.read()

        yield index, word, explanation, pngs, examples


def main():
    for env in iteration():
        gen(env)


if __name__ == "__main__":
    main()
