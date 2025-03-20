def generate_latex_image(filepath: str, width: int, height: int, unit_of_measurement: str = "px") -> str:
    latex_code = [
        "\\begin{figure}[h]",
        "\\centering",
        f"\\includegraphics[width={width}{unit_of_measurement}, height={height}{unit_of_measurement}]{{{filepath}}}",
        "\\end{figure}"
    ]
    
    return "\n".join(latex_code)