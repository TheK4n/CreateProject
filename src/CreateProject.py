import subprocess
from argparse import Namespace
from datetime import datetime
from os import mkdir, chdir, system, path
from os import name as os_name
from shutil import rmtree

from pathlib import Path
from sys import stderr

from src.content import *


class NotCamelCaseError(Exception):
    pass


class MutualOptionsError(Exception):
    pass


class ForbiddenScriptNameError(Exception):
    pass


class CreateProject:
    create_project_script_name = 'create-project'
    _dirs = ['test', 'src']

    def __init__(self, project_path: str):

        if not self.is_camel_case(project_path):
            raise NotCamelCaseError(f'\'{path.basename(project_path)}\' must be CamelCase')
        else:
            self.__project_path = project_path

        self._is_quiet = False
        self._is_secret = False

    @property
    def project_path(self):
        return self.__project_path

    @property
    def base_project_path(self):
        return path.basename(self.__project_path)

    @staticmethod
    def is_camel_case(project_name: str) -> bool:
        bid = False
        for i in ['-', '_', '.', '/']:
            if i in path.basename(project_name)[1:-1]:
                bid = True
        return project_name != project_name.lower() and project_name != project_name.upper() and not bid

    def _make_it_quiet(self):
        self._is_quiet = True
        return self._is_quiet

    def _make_it_secret(self):
        self._is_secret = True
        return self._is_secret

    @staticmethod
    def get_script_name(project_name: str, splitter: str = '-') -> str:
        project_name = path.basename(project_name.strip())

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

    def _get_script_name(self, splitter: str = '-') -> str:
        return self.get_script_name(self.project_path, splitter)

    def _be_quiet(self, command_: str, ) -> str:
        if not self._is_quiet:
            return command_
        if os_name == 'posix':
            return command_ + ' 1>/dev/null'
        return command_

    def _error_pars(self, msg: str, exit_code: int = 1):
        print(f'{self.create_project_script_name}: error: {msg}', file=stderr)
        if exit_code != 0:
            exit(1)
        return exit_code


class CreateProjectParser(CreateProject):
    __FORBIDDEN_SCRIPT_NAME = ['src', 'test', 'README.md', 'requirements.txt', 'LICENSE', 'timetests.py',
                               'unittests.py', 'utils.py',
                               'Dockerfile', '.git', '.gitignore', '.gitattributes', 'venv']

    def __init__(self, project_path: str, args: Namespace):
        super().__init__(project_path)

        if args.quiet:
            self._make_it_quiet()
        if args.secure:
            self._make_it_secret()

        if args.script_name is None:
            script_name = self._get_script_name()
            if script_name in self.__FORBIDDEN_SCRIPT_NAME:
                script_name += '_'
            self._script_name = script_name
        else:
            if len(args.project_name) > 1 and args.create_link:
                raise MutualOptionsError(
                    'you can\'t use --create-link and --script-name together if more then 1 project')

            else:
                if args.script_name in self.__FORBIDDEN_SCRIPT_NAME:
                    raise ForbiddenScriptNameError(f'you can\'t use script name \'{args.script_name}\'')
                else:
                    self._script_name = args.script_name


class CreateProjectCreator(CreateProjectParser):

    def __init__(self, project_path: str, args: Namespace):
        super().__init__(project_path, args)
        self.__args = args

        self.__create_project_path()

        if self.__args.git_login is None:
            self.github_nickname = subprocess.check_output(['git', 'config', 'user.name']).decode().strip()
        else:
            self.github_nickname = self.__args.git_login

        self.__make_dirs()
        self.__write_files()
        self.__init_venv()

        if os_name == 'posix':

            script_name_path = path.join(self.project_path, self._script_name)

            system(f'chmod u+x \'{script_name_path}\'')  # разрешение на запуск

            if self.__args.secure:
                self.__make_secret()

            if self.__args.create_link:

                link_path = path.abspath(script_name_path)
                try:
                    self.__create_symbolic_link(link_path)
                except FileNotFoundError as e:
                    self._error_pars(str(e), exit_code=0)
                except FileExistsError as e:
                    self._error_pars(str(e), exit_code=0)

        self.__git_init()  # last
        if not self.__args.quiet:
            print(f'project \'{self.base_project_path}\' created')

    def _try_mkdir(self):
        try:
            mkdir(self.project_path)
            if not self._is_quiet:
                print(f'mkdir: created directory \'{self.project_path}\'')
        except PermissionError:
            self._error_pars(f'permission denied: \'{self.project_path}\'')

    def __create_project_path(self):

        try:
            return self._try_mkdir()
        except FileExistsError:
            if self.__args.no_ask_force:
                rmtree(self.project_path)
                if not self._is_quiet:
                    print(f'project \'{self.project_path}\' removed')
                self._try_mkdir()

            elif self.__args.ask_force:
                ans = input(
                    f'{self.create_project_script_name}: re-write existing project \'{self.project_path}\'? [Y/n] ')

                if ans in {'Y', 'y'}:
                    rmtree(self.project_path)
                    if not self._is_quiet:
                        print(f'project \'{self.project_path}\' removed')
                    self._try_mkdir()
                else:
                    raise StopIteration

            else:
                self._error_pars(f'project \'{self.project_path}\' already exists, use -f', exit_code=0)
                raise StopIteration
        except FileNotFoundError:
            self._error_pars(f'no such directory \'{path.dirname(self.project_path)}\'', exit_code=1)
            raise StopIteration

    def __make_dirs(self):
        for i in self._dirs:
            mkdir(path.join(self.project_path, i))

    def __write_files(self):

        files = (
            ('.gitignore', gitignore),
            ('.gitattributes', gitattributes),
            ('README.md',
             readme_md.format(project_path=self.project_path, github_nickname=self.github_nickname,
                              script_name=self._script_name)),
            (self._script_name, main_py),
            ('requirements.txt', ''),
            ('LICENSE', licenses[self.__args.license_].format(year=datetime.now().year,
                                                              github_nickname=self.github_nickname)),
            (path.join(self._dirs[0], 'unittests.py'), unittests_py),
            (path.join(self._dirs[0], 'timetests.py'), timetests_py),
            (path.join(self._dirs[1], 'utils.py'), utils_py)
        )
        for filename, content in files:
            with open(path.join(self.project_path, filename), 'w') as f:
                f.write(content)

    def __init_venv(self) -> str:
        venv_path = path.join(self.project_path, "venv")
        system(self._be_quiet(f'virtualenv \'{venv_path}\''))  # виртуальное окружение
        return venv_path

    @staticmethod
    def __create_symbolic_link(link_path: str) -> int:
        home_path = str(Path.home())
        home_bin = path.join(home_path, 'bin')

        if path.exists(link_path):
            # если существует папка /home/user/bin
            if path.exists(home_bin) and path.isdir(home_bin):
                # создает символическую ссылку в /home/user/bin
                return system(f'ln -s \'{link_path}\' \'{home_bin}\'')
            else:
                raise FileNotFoundError(f'\'{home_bin}\' doesn\'t exists')
        else:
            raise FileExistsError(f'\'{link_path}\' already exists')

    def __git_init(self):
        chdir(self.project_path)
        system(self._be_quiet(f'git init'))
        system(self._be_quiet(f'git add .'))
        system(self._be_quiet(f'git commit -m "Initial commit"'))
        chdir('..')

    def __make_secret(self) -> int:
        """рекурсивно запрещает всем читать, изменять, выполнять проект"""
        return system(f'chmod og-rwx -R \'{self.project_path}\'')
