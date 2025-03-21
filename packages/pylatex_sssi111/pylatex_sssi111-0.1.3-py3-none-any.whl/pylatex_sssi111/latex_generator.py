from typing import Any, List, Optional


def escape_latex(value: Any) -> str:
    replacements = {
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
        "\\": r"\textbackslash{}",
        "\n": r"\newline ",
        "\t": r"\texttabulartest ",
    }
    return "".join(replacements.get(c, c) for c in str(value))


def generate_table_latex(rows: List[List[Any]]):
    if not isinstance(rows, list):
        raise ValueError("Input must be a list of lists")

    if not rows:
        return ""

    num_columns = len(rows[0])
    if any(len(row) != num_columns for row in rows):
        return ""

    escaped_rows = [[escape_latex(cell) for cell in row] for row in rows]

    column_format = "l" * num_columns
    table_body = "\n".join("    " + " & ".join(row) + r" \\" for row in escaped_rows)

    return (
        f"\\begin{{tabular}}{{{column_format}}}\n"
        f"{table_body}\n"
        f"\\end{{tabular}}\n"
    )


def generate_image_latex(
    image_path: str,
    width: str = "\\textwidth",
    placement: str = "htbp",
    caption: str = None,
    label: str = None,
):
    if not image_path:
        raise ValueError("Image path cannot be empty")

    if any(c in image_path for c in " #$%&~^"):
        raise ValueError("Image path contains invalid characters")

    if not isinstance(width, str):
        raise TypeError("Width must be a string")

    latex_image = []
    latex_image.append("\\begin{figure}" + f"[{{{placement}}}]")
    latex_image.append(f"\\centering")
    latex_image.append(f"\\includegraphics[width={width}]{{{image_path}}}")

    if caption:
        latex_image.append(f"\\caption{{{caption}}}")

    if label:
        latex_image.append(f"\\label{{{label}}}")

    latex_image.append("\\end{figure}\n")
    return "\n".join(latex_image)


def generate_latex_headers(filename: str, data: List[str]):
    with open(filename, "w") as f:
        f.write("\\documentclass{article}\n")
        f.write("\\usepackage[utf8]{inputenc}\n")
        f.write("\\usepackage{graphicx}\n")
        f.write("\\begin{document}\n\n")
        for data_row in data:
            f.write(data_row)
        f.write("\\end{document}\n")
