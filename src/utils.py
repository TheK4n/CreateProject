from os import mkdir, path, system, chdir
from pathlib import Path

__all__ = ['get_script_name', 'is_camel_case', 'make_dirs', 'write_files',
           'git_init', 'create_symbolic_link', 'secret', 'error_pars', 'init_venv']

from sys import stderr


def get_script_name(project_name: str, splitter: str = '-') -> str:
    project_name = project_name.strip()

    if project_name[0] == '.':
        project_name = project_name[1:]

    g = (i for i in project_name)  # генератор
    shift = 0  # сдвиг
    flag = False  # флаг если 2 подряд большие буквы
    for i in range(len(project_name)):
        char = next(g)

        if char.isupper():  # если большая
            start_ = project_name[:i + shift]  # 1 часть до большой буквы
            end_ = project_name[i + shift:]  # 2 часть с большой буквы и до конца
            try:
                if end_[1].isupper():
                    if not flag:
                        flag = True
                    else:
                        continue
                else:
                    flag = False
            except IndexError:
                continue
            project_name = start_ + splitter + end_  # соединяет через тире
            shift += 1

    return project_name.lower().strip('-').strip()


def is_camel_case(string: str) -> bool:
    bid = False
    for i in ['-', '_', '.']:
        if i in string[1:-1]:
            bid = True

    return string != string.lower() and string != string.upper() and not bid


def to_null(is_quiet: bool) -> str:
    return "1>/dev/null"if is_quiet else ""


def make_dirs(project_path, dirs: list[str]):
    for i in dirs:
        mkdir(path.join(project_path, i))


def write_files(project_path, files):
    for filename, content in files:
        with open(path.join(project_path, filename), 'w') as f:
            f.write(content)


def git_init(project_path, is_quiet: bool = False) -> bool:
    text_to_null = to_null(is_quiet)

    status = True
    chdir(project_path)
    status = status and True if system(f'git init {text_to_null}') == 0 else False
    status = status and True if system(f'git add . {text_to_null}') == 0 else False
    status = status and True if system(f'git commit -m "Initial commit" {text_to_null}') == 0 else False
    chdir('..')
    return status


def create_symbolic_link(link_path) -> bool:
    home_path = str(Path.home())
    home_bin = path.join(home_path, 'bin')

    if path.exists(link_path):
        # если существует папка /home/user/bin
        if path.exists(home_bin) and path.isdir(home_bin):
            # создает символическую ссылку в /home/user/bin
            return True if system(f'ln -s {link_path} {home_bin}') == 0 else False
        else:
            raise FileNotFoundError(f'"{home_bin}" doesn\'t exists')
    else:
        raise FileExistsError


def secret(project_path) -> bool:
    # рекурсивно запрещает всем читать, изменять, выполнять проект
    return True if system(f'chmod og-rwx -R {project_path}') == 0 else False


def init_venv(project_path: str, is_quiet: bool) -> str:
    venv_path = path.join(project_path, "venv")
    system(f'virtualenv {venv_path} {to_null(is_quiet)}')  # виртуальное окружение
    return venv_path


def error_pars(script_name: str, msg: str):
    print(f'{script_name}: error: {msg}', file=stderr)
    exit(1)
