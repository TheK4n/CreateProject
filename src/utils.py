from os import mkdir, path, system, chdir
from pathlib import Path

__all__ = ['get_script_name', 'is_camel_case', 'make_dirs', 'write_files',
           'git_init', 'create_symbolic_link', 'secret', 'error_pars']

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


def is_camel_case(string):

    bid = False
    for i in ['-', '_', '.']:
        if i in string[1:-1]:
            bid = True

    return string != string.lower() and string != string.upper() and not bid


def make_dirs(project_path, dirs: list[str]):
    for i in dirs:
        mkdir(path.join(project_path, i))


def write_files(project_path, files):
    for filename, content in files:
        with open(path.join(project_path, filename), 'w') as f:
            f.write(content)


def git_init(project_path, is_quiet=False):
    chdir(project_path)
    system(f'git init {"--quiet" if is_quiet else ""}')
    system(f'git add . {"--quiet" if is_quiet else ""}')
    system(f'git commit -m "Initial commit" {"--quiet" if is_quiet else ""}')
    chdir('..')


def create_symbolic_link(link_path):
    home_path = str(Path.home())
    home_bin = path.join(home_path, 'bin')

    if path.exists(link_path):
        # если существует папка /home/user/bin
        if path.exists(home_bin) and path.isdir(home_bin):
            # создает символическую ссылку в /home/user/bin
            system(f'ln -s {link_path} {home_bin}')
        else:
            raise FileNotFoundError(f'"{home_bin}" doesn\'t exists')
    else:
        raise FileExistsError


def secret(project_path):
    # рекурсивно запрещает всем читать, изменять, выполнять проект
    system(f'chmod og-rwx -R {project_path}')


def error_pars(script_name, msg: str):
    print(f'{script_name}: error: {msg}', file=stderr)
    exit(1)
