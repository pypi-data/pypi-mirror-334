from typing import Optional


def generate_image(
    image_path: str,
    width: str = "\\textwidth",
    caption: Optional[str] = None,
    label: Optional[str] = None,
):
    """
    Generates LaTeX code to include an image.

    Args:
    - image_path (str): The path to the image file.
    - width (str): The width of the image (e.g., `0.5\textwidth`, `5cm`). Defaults to `\textwidth`.
    - caption (str): A caption for the image. Default is None.
    - label (str): A label for referencing the image in the document. Default is None.

    Returns:
    - str: A string of LaTeX code to include the image.
    """
    latex_code = []
    latex_code.append("\\begin{figure}[htbp]")
    latex_code.append(f"\\centering")
    latex_code.append(f"\\includegraphics[width={width}]{{{image_path}}}")

    if caption:
        latex_code.append(f"\\caption{{{caption}}}")

    if label:
        latex_code.append(f"\\label{{{label}}}")

    latex_code.append("\\end{figure}")
    return "\n".join(latex_code)
