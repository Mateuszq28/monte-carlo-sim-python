# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import codecs

filename_in = "2023-09-21 sam spis treści.txt"
filename_out = "tableofcontents.tex"

with codecs.open(filename_in, 'r', 'utf-8') as f:
    text = f.read()

text = text.split("\n")

out_text = []
for line in text:
    x1 = "    "
    x2 = x1 + x1
    x3 = x2 + x1
    x4 = x3 + x1
    x5 = x4 + x1

    ch = "\\chapter{"
    y1 = "\\section{"
    y2 = "\\subsection{"
    y3 = "\\subsubsection{"
    y4 = "\\paragraph{"
    y5 = "\\subparagraph{"

    line = line.replace("\"", ",,", 1)
    line = line.replace("\"", "''", 1)

    if line[0] != "#"[0]:
        line = line.replace(x5, y5)
        line = line.replace(x4, y4)
        line = line.replace(x3, y3)
        line = line.replace(x2, y2)
        line = line.replace(x1, y1)

        if len(line) > 1:
            line = line[:-1] + "}"
            if line[0] != "\\"[0]:
                line = ch + line

    else:
        line = line[1:].strip(" ")[:-1]

    
    out_text.append(line)

    if ch in line:
        temp_line = line.strip(ch)
        temp_line = temp_line.lower()
        temp_line = temp_line.replace(" ", "-")
        prefix = "\\label{chpt:"
        out_text.append(prefix + temp_line)

out_text = "\n".join(out_text)

with codecs.open(filename_out, 'w', 'utf-8') as f:
    f.write(out_text)



# create chapter files
chapters = out_text.split("\r\n\r\n\r\n")[1:-1]
num_chap = len(chapters)
print("num of chapters: " + str(num_chap))
for i in range(num_chap):
    name = "{:0>2}".format(i+1) + ".tex"
    fname = "chapters/" + name
    with codecs.open(fname, 'w', 'utf-8') as f:
        f.write(chapters[i])

