from pathlib import Path
from typing import List
import subprocess

list_2d = [[1,2,3],
           [4,5],
           [6,7,8,9],
           [0]]


def return_universal_start():
    return """\\documentclass{article}
\\usepackage{graphicx}
\\begin{document}
"""

def return_universal_end():
    return """\\end{document}"""


def return_header(list_2d: List[List[int]]) -> str:
    width = max(map(len, list_2d))
    header = """\\begin{table}
\t\\centering\n"""
    header += "\t\\begin{tabular}" + "{|" + (width * "c|") + "}\n"
    header += "\t\\hline\n"
    return header 


def return_end() -> str:
    return """\t\\end{tabular}
\\end{table}
    """


def format_one_row(list_1d: List[int]) -> str:
    formated_row = "\t" + " & ".join([str(num) for num in list_1d]) + " \\" + "\\" + " \\hline" + "\n"
    return formated_row


def format_all_rows(list_2d: List[List[int]]) -> str:
    string_values = [[str(x) for x in row] for row in list_2d] 
    table_width = max(map(len, string_values))
    body = ""

    for row_line in string_values:

        while len(row_line) < table_width:
            row_line.append(' ')
        body += format_one_row(row_line)
    
    return body


def return_latex_table(list_2d: List[List[int]]) -> str:
    table = return_header(list_2d)
    table += format_all_rows(list_2d)
    table += return_end()
    return table



def make_image_latex(path: Path = "png_example"):
    latex = """
\\begin{figure}[h]
    \\centering
    \\includegraphics[width=0.8\\textwidth]""" + f"{ '{'+ str(path) +'}'}"
    latex += """
\\end{figure}
"""
    return latex


def make_full_latex_file(list_2d: List[List[int]] = list_2d,
                         path = "file.tex"):
    latex_code = return_universal_start() + "\n\n" + return_latex_table(list_2d) + "\n\n" + make_image_latex() + "\n\n" + return_universal_end()

    with open(path, "w") as f:
        f.write(latex_code)


def write_pdf(path = "file.tex"):
    make_full_latex_file()
    subprocess.run(["pdflatex", path], check=True)
    print("PDF успешно создан!")

if __name__ == "__main__":
    write_pdf()