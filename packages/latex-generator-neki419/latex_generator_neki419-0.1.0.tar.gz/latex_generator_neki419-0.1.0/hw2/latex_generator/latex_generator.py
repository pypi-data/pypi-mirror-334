def generate_latex_table(table_list: list[list]):
    if not table_list:
        raise ValueError("Table cannot be empty!")

    head_col_num = len(table_list[0])
    alignment = "{" + "|c" * head_col_num + "|}"
    
    yield f"\\begin{{tabular}}{alignment}\n"
    
    for row in table_list:
        if len(row) != head_col_num:
            raise ValueError(f"The number of columns is different! Must be {head_col_num}")
        
        yield "\t\\hline\n"
        yield "\t" + " & ".join(map(str, row)) + " \\\\\n"

    yield "\t\\hline\n"
    yield "\\end{tabular}\n\n"

def generate_latex_image(image_path : str):

    yield "\\begin{figure}[h]\n"
    yield "\t\\centering\n"
    yield f"\t\\includegraphics[width=0.5\\textwidth]{{{image_path}}}\n"
    yield "\t\\caption{Generated Image}\n"
    yield "\t\\label{fig:image}\n"
    yield "\\end{figure}\n\n"

def generate_full_latex_document(table_data : list[list], image_path : str):

    yield "\\documentclass{article}\n\n"
    yield "\\usepackage{graphicx}\n\n"
    yield "\\begin{document}\n\n"

    yield from generate_latex_table(table_data)

    yield from generate_latex_image(image_path)

    yield "\\end{document}"
