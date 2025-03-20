import subprocess
import os


def generate_latex_table(data):
    table = "\\begin{tabular}{|" + "|".join(["c"] * len(data[0])) + "|}\n"
    table += "\\hline\n"
    for row in data:
        table += " & ".join(map(str, row)) + " \\\\\n"
        table += "\\hline\n"
    table += "\\end{tabular}"
    
    return table


def generate_latex_image(image_path, width=None, caption=None, label=None):
    image = "\\begin{figure}[h!]\n"
    image += "\\centering\n"
    if width:
        image += f"\\includegraphics[width={width}\\textwidth]{{{image_path}}}\n"
    else:
        image += f"\\includegraphics{{{image_path}}}\n"
    if caption:
        image += f"\\caption{{{caption}}}\n"
    if label:
        image += f"\\label{{{label}}}\n"
    image += "\\end{figure}"
    
    return image


def make_document_from_latex(latex_code):
    doc = "\\documentclass{article}\n"
    doc += "\\usepackage{graphicx}\n"
    doc += "\\begin{document}\n"
    doc += latex_code
    doc += "\\end{document}\n"
    return doc


def generate_pdf_from_latex(latex_code, output_filename="output_document"):
    tex_file = f"{output_filename}.tex"
    with open(tex_file, "w") as file:
        file.write(latex_code)
    try:
        subprocess.run(["pdflatex", tex_file], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error during PDF generation: {e}")
        return None
    pdf_file = f"{output_filename}.pdf"
    if os.path.exists(pdf_file):
        return pdf_file
    else:
        print("Error occured during creation of PDF")
        return None