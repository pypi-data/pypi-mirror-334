def generate_latex_table(data: list[list[str]], caption: str = "Table Example") -> str:
    """
    Генерирует строку с кодом LaTeX для таблицы.

    :param data: Двойной список (список списков), содержащий строки таблицы
    :param caption: Подпись к таблице
    :return: Строка с валидным кодом LaTeX
    """
    if not data or not all(isinstance(row, list) for row in data):
        raise ValueError("Invalid data")

    column_count = len(data[0])
    header = " | ".join(["c"] * column_count)

    latex_code = [ "\\begin{table}[h]", "\\centering", "\\begin{tabular}{|" + header + "|}",
                   "\\hline", " & ".join(map(str, data[0])) + " \\\\", "\\hline"]

    for row in data[1:]:
        latex_code.append(" & ".join(map(str, row)) + " \\\\")
    latex_code.append("\\hline")

    latex_code.append("\\end{tabular}")
    latex_code.append(f"\\caption{{{caption}}}")
    latex_code.append("\\end{table}")

    return "\n".join(latex_code)


def generate_latex_image(image_path: str, caption: str = "Image Example") -> str:
    """
    Генерирует строку с кодом LaTeX для вставки изображения.

    :param image_path: Путь к изображению (PNG, JPG и т. д.)
    :param caption: Подпись к изображению
    :return: Строка с валидным кодом LaTeX
    """
    return "\n".join([
        "\\begin{figure}[h]",
        "\\centering",
        f"\\includegraphics[width=0.8\\textwidth]{{{image_path}}}",
        f"\\caption{{{caption}}}",
        "\\end{figure}"
    ])