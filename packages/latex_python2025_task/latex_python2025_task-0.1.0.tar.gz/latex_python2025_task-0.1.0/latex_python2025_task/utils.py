from typing import Any
from pdflatex import PDFLaTeX


def create_tex_table(table: list[list[Any]]) -> str:
    declared_cols = "c"
    if 0 < len(table):
        declared_cols = "|" + "c|" * len(table[0])
    content = ""
    for row in table:
        content = content + "\\hline " + " & ".join(str(elem) for elem in row) + "\\\\" + "\n"
    content = content + "\\hline"
    return (f"\\begin{{table}}[h!]\n"
            f"\\centering\n"
            f"\\begin{{tabular}}{{ {declared_cols} }}\n"
            f"{content}\n"
            f"\\end{{tabular}}\n"
            f"\\end{{table}}\n")


def wrap_with_tex_document(content: str, graphics_is_icluded: bool = True) -> str:
    return (f"\\documentclass{{article}}\n" +
            (f"\\usepackage{{graphicx}}\n" if graphics_is_icluded else "") +
            f"\\begin{{document}}\n"
            f"{content}\n"
            f"\\end{{document}}\n")


def create_tex_image(image: str) -> str:
    return f"\\includegraphics[width=\\textwidth]{{{image}}}\n"


def create_tex_content_from_table(table: list[list[Any]]) -> str:
    return wrap_with_tex_document(create_tex_table(table))


def create_pdf_file(tex_file: str, pdf_file: str):
    pdfl = PDFLaTeX.from_texfile(tex_file)
    pdfl.set_pdf_filename(pdf_file)
    pdfl.create_pdf(keep_pdf_file=True, keep_log_file=False)
