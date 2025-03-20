def generate_latex_table(data):
    """
    Функция для генерации LaTeX кода для таблицы на основе двойного списка.
    
    Args:
        data (List): двойной список
    
    Returns:
        latex_table (str): текст таблицы
    """
    if not data or not all(isinstance(row, list) for row in data):
        raise ValueError("Список не должен быть пустым")
    # Начало таблицы
    #latex_table = "\\begin{document}\n"
    latex_table = "\\begin{tabular}{|" + "c|" * len(data[0]) + "}\n"
    latex_table += "\\hline\n"
    # Добавление строк таблицы
    for row in data:
        latex_table += " & ".join(map(str, row)) + " \\\\\n"
        latex_table += "\\hline\n"

    # Конец таблицы
    latex_table += "\\end{tabular}\n"
    #latex_table += "\\end{document}"

    return latex_table

def generate_latex_image(image_path, width=None):
    """
    Функция для генерации LaTeX кода для вставки изображения.

    Args:
        image_path (str): путь к изображению
        width (float): ширина изображения
    
    Returns:
        latex_image (str): LaTeX код со вставленной картинкой
    """
    if not image_path:
        raise ValueError("Путь к файлу не корректный")

    latex_image = "\\includegraphics"
    if width:
        latex_image += f"[width={width}]"
    latex_image += f"{{{image_path}}}"

    return latex_image