def generate_latex_table(data):
    # Проверка на пустой список
    if not data or not all(isinstance(row, list) for row in data):
        raise ValueError("Input must be a non-empty list of lists")
    
    num_columns = len(data[0])
    
    # Проверяем, что все строки имеют одинаковое количество столбцов
    if not all(len(row) == num_columns for row in data):
        raise ValueError("All rows must have the same number of columns")
    
    # Заголовок LaTeX документа с поддержкой кириллицы
    latex_code = "\\documentclass{article}\n"
    latex_code += "\\usepackage[utf8]{inputenc}\n"
    latex_code += "\\usepackage[T2A]{fontenc}\n"
    latex_code += "\\usepackage[russian]{babel}\n"
    latex_code += "\\begin{document}\n\n"

    # Заголовок таблицы в LaTeX
    latex_code += "\\begin{table}[h]\n"
    latex_code += "\\centering\n"
    latex_code += "\\begin{tabular}{ | " + " | ".join(["c"] * num_columns) + " | }\n"
    latex_code += "\\hline\n"
    
    # Добавление строк в таблицу
    for row in data:
        latex_code += " & ".join(map(str, row)) + " \\\\ \\hline\n"
    
    # Закрываем таблицу
    latex_code += "\\end{tabular}\n"
    latex_code += "\\caption{Пример таблицы}\n"
    latex_code += "\\end{table}\n\n"

    # Завершение документа
    latex_code += "\\end{document}\n"
    
    return latex_code

def generate_latex_image(path, width="0.8\\textwidth", caption="Example Image"):
    # Заголовок LaTeX документа c поддержкой графики
    latex_code = "\\documentclass{article}\n"
    latex_code += "\\usepackage{graphicx}\n"
    latex_code += "\\begin{document}\n\n"
    
    # Параметры картинки
    latex_code += "\\begin{figure}[h]\n"
    latex_code += "    \\centering\n"
    latex_code += f"    \\includegraphics[width={width}]{{{path}}}\n"
    latex_code += f"    \\caption{{{caption}}}\n"
    latex_code += "\\end{figure}\n\n"
    
    # Завершение документа
    latex_code += "\\end{document}\n"

    return latex_code