from typing import List


def generate_latex_table(data: List[List[str]]):
    cols = len(data[0])
    for row in data:
        if len(row) != cols:
            raise ValueError("Incorrect table size")

    result = ["\\begin{tabular}{" + '|c' * cols + "|}"]
    for row in data:
        result.append(' & '.join(map(str, row)) + ' \\\\')
    result.append("\\end{tabular}")
    return '\n'.join(result)
