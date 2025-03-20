def generate_latex_table(data: list[list]) -> str:
    if not data or not data[0]:
        return ""
    col_spec = "|" + "|".join(["c" for _ in range(len(data[0]))]) + "|"
    latex_lines = [
        "\\begin{table}[h]",
        "\\centering",
        f"\\begin{{tabular}}{{{col_spec}}}"
        "\\hline"
    ]
    for row in data:
        formatted_row = [str(cell).replace("_", "\\_") for cell in row] #TODO add shielding
        latex_lines.append(" & ".join(formatted_row) + " \\\\")
        latex_lines.append("\\hline")
    latex_lines.extend([
        "\\end{tabular}",
        "\\end{table}"
    ])
    return "\n".join(latex_lines)