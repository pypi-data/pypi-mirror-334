from itertools import repeat


def get_tex_table(
    dlist: list[list[str] | None],
    alignment: str,
    vseparator: bool,
    hseparator: bool,
    external_border: bool,
) -> str:
    """
    Task 2.1
    A function that receives DLIST, the data to generate a table,
    and returns the code to generate it in LaTeX in string format.
    The document class will be standalone.
    Only supported single line for rules.
    """

    # processing bool variables
    # vertical and horizontal separators and vertical border
    vsep = "|" if vseparator else " "
    hsep = "\n \\hline" if hseparator else ""
    vborder = "|" if external_border else ""

    # header and footer of the tex code (string result)
    nb_columns = len(dlist[0]) if dlist else 0
    header = """\\documentclass[class=article, crop=false]{standalone}\n\\begin{document}\n\\begin{center}\n\\begin{tabular}"""
    header += f"{{ {vborder}{vsep.join(repeat(alignment, nb_columns))}{vborder} }}"
    footer = """\\end{tabular}\n\\end{center}\n\\end{document}"""

    # forming the body of the table
    body_lines = []
    for i, line in enumerate(dlist):
        assert len(line) == nb_columns, (
            f"Expected {nb_columns} columns at line {i}, but got {len(line)}.\nLine: {line}"
        )
        body_lines.append(f" {' & '.join(line)} ")

    # joining lines of the table
    body = f"\\\\{hsep}\n".join(body_lines)

    # adding external borders if needed
    if external_border:
        body = f" \\hline\n{body}\\\\\n \\hline"

    str_result = "\n".join([header, body, footer])
    return str_result


def get_tex_image(
    img_filename: str, img_position: str = "h", img_centering: bool = True
):
    """
    Task 2.2
    A function that receives an image path,
    and returns the code to generate it in LaTeX in string format.
    img position tells where in the page to place it.
    Valid params:
    h for here, t for top, b for bottom, p for special page
    If img centering puts the image in the center of its position.
    The document class will be standalone.
    Images should be stored in the child 'data' folder.
    """
    # We follow the recommendation of the doc and don't use the file extention
    img_filename = img_filename.rsplit(".", 1)[0]

    # plus we don't allow images with multiple dots or white spaces
    assert all(c not in " ." for c in img_filename), (
        "the image file name should not have white spaces or multiple dots"
    )

    # header and footer of the tex code
    header = """\\documentclass[class=article, crop=false]{standalone}\n\\usepackage{graphicx}\n\\graphicspath{ {../data/} }\n\\begin{document}"""
    header += f"\n\\begin{{figure}}[{img_position}]"

    body = f" \\includegraphics{{{img_filename}}}"
    if img_centering:
        body += "\n \\centering"
    footer = """\\end{figure}\n\\end{document}"""

    return "\n".join([header, body, footer])
