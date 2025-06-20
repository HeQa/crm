import os
from pathlib import Path


def print_directory_tree(startpath, max_level=None, show_hidden=False):
    print(f"Дерево каталогов проекта: {project_root}\n")
    path_text = f"Дерево каталогов проекта: {project_root}\n"
    """
    Рекурсивно печатает дерево каталогов и файлов
    :param startpath: начальная директория
    :param max_level: максимальный уровень вложенности (None - без ограничений)
    :param show_hidden: показывать скрытые файлы/папки
    """
    startpath_str = str(startpath)  # Преобразуем Path в строку
    for root, dirs, files in os.walk(startpath_str):
        if not show_hidden:
            # Исключаем скрытые папки
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            # Исключаем скрытые файлы
            files = [f for f in files if not f.startswith('.')]

        level = root.replace(startpath_str, '').count(os.sep)
        if max_level is not None and level > max_level:
            continue

        indent = '│   ' * (level - 1) + '├── ' if level > 0 else ''
        print(f"{indent}{os.path.basename(root)}/")
        path_text += f"{indent}{os.path.basename(root)}/\n"

        subindent = '│   ' * level + '├── '
        for i, file in enumerate(sorted(files)):
            if i == len(files) - 1:
                subindent = '│   ' * level + '└── '
            print(f"{subindent}{file}")
            path_text += f"{subindent}{file}\n"
    return path_text

if __name__ == "__main__":
    # Получаем корневую директорию проекта (где находится этот скрипт)
    project_root = Path(__file__).parent.resolve()


    print_directory_tree(project_root, max_level=5, show_hidden=False)
    with open('project_tree.txt', 'w', encoding='utf-8') as f:
        f.write(print_directory_tree(project_root))