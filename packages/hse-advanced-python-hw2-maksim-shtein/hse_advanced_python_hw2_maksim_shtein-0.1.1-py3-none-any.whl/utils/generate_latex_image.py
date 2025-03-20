from typing import Optional


def generate_latex_image(
        image_path: str,
        height: Optional[str] = None,
        centering: bool = False
):
    latex_code = ["\\begin{figure}[htbp]"]
    if centering:
        latex_code.append(f"\\centering")
    image_size = ('height=' + str(height) if height is not None else '').strip()
    latex_code.append(f"\\includegraphics[{image_size}]{{{image_path}}}")

    latex_code.append("\\end{figure}")
    return "\n".join(latex_code)
