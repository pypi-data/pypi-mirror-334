from typing import Any, List


def generate_table(data: List[List[Any]]):
    row_length = len(data[0])
    if row_length == 0:
        raise ValueError("Rows must have at least one element")

    if any(len(row) != row_length for row in data):
        raise ValueError("All rows must have the same number of elements")

    row_to_tex = lambda row: " & ".join(map(str, row)) + r" \\"

    body = "\n".join(map(row_to_tex, data))
    header = "\\begin{tabular}{|" + "c|" * row_length + "}\n\\hline"
    footer = "\\hline\n\\end{tabular}"

    return "\n".join([header, body, footer])
