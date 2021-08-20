from os import mkdir, path, system, chdir, name
from sys import stderr
from pathlib import Path


__all__ = ['get_script_name', 'is_camel_case', 'make_dirs', 'write_files',
           'git_init', 'create_symbolic_link', 'secret', 'error_pars', 'init_venv']


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


def error_pars(script_name: str, msg: str):
    print(f'{script_name}: error: {msg}', file=stderr)
    exit(1)
    return


def to_null(is_quiet: bool) -> str:
    if name == 'posix':
        return '1>/dev/null' if is_quiet else ''
    else:
        return ''


def make_dirs(project_path, dirs: list[str]):
    for i in dirs:
        mkdir(path.join(project_path, i))


def write_files(project_path, files):
    for filename, content in files:
        with open(path.join(project_path, filename), 'w') as f:
            f.write(content)


def init_venv(project_path: str, is_quiet: bool) -> str:
    venv_path = path.join(project_path, "venv")
    system(f'virtualenv {venv_path} {to_null(is_quiet)}')  # виртуальное окружение
    return venv_path


def git_init(project_path, is_quiet: bool = False) -> list[int]:
    text_to_null = to_null(is_quiet)
    status = []
    chdir(project_path)
    status.append(system(f'git init {text_to_null}'))
    status.append(system(f'git add . {text_to_null}'))
    status.append(system(f'git commit -m "Initial commit" {text_to_null}'))
    chdir('..')
    return status


def create_symbolic_link(link_path) -> int:
    home_path = str(Path.home())
    home_bin = path.join(home_path, 'bin')

    if path.exists(link_path):
        # если существует папка /home/user/bin
        if path.exists(home_bin) and path.isdir(home_bin):
            # создает символическую ссылку в /home/user/bin
            return system(f'ln -s {link_path} {home_bin}')
        else:
            raise FileNotFoundError(f'"{home_bin}" doesn\'t exists')
    else:
        raise FileExistsError


def secret(project_path) -> int:
    # рекурсивно запрещает всем читать, изменять, выполнять проект
    return system(f'chmod og-rwx -R {project_path}')
