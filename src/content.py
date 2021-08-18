
gitignore = r'''# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# PyInstaller
#  Usually these files are written by a python script from a template
#  before PyInstaller builds the exe, so as to inject date/other infos into it.
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Logs
*.log

# Unit test / coverage reports
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
.hypothesis/
.pytest_cache/

# Translations
*.mo
*.pot

# Django stuff:
local_settings.py
db.sqlite3

# Flask stuff:
instance/
.webassets-cache

# Scrapy stuff:
.scrapy

# Sphinx documentation
docs/_build/

# PyBuilder
target/

# Jupyter Notebook
.ipynb_checkpoints

# IPython
profile_default/
ipython_config.py

# pyenv
.python-version

# celery beat schedule file
celerybeat-schedule

# SageMath parsed files
*.sage.py

# Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# Spyder project settings
.spyderproject
.spyproject

# Rope project settings
.ropeproject

# mkdocs documentation
/site

# mypy
.mypy_cache/
.dmypy.json
dmypy.json

# Pyre type checker
.pyre/

.idea
*.iml
out
gen
'''

main_py = r'''#!/usr/bin/env python3

from sys import argv
from src.utils import *


def main(args: list[str]):
    pass


if __name__ == '__main__':
    main(argv[1:])
'''

utils_py = '''__all__ = []

'''

tests_py = fr'''import unittest
from src.utils import *


class TestMain(unittest.TestCase):
    def test(self):
        self.assertEqual(True, 1)


if __name__ == '__main__':
    unittest.main()

'''

readme_md = r'''<h1 align="center">{project_path}</h1>

<p align="center">
  <a href="https://github.com/{github_nickname}">
    <img src="https://img.shields.io/github/followers/{github_nickname}?label=Follow&style=social">
  </a>
  <a href="https://github.com/{github_nickname}/{project_path}">
    <img src="https://img.shields.io/github/stars/{github_nickname}/{project_path}?style=social">
  </a>
</p>

---

## Content
* [Project description](#chapter-0)
* [Installation](#chapter-1)  
* [Usage](#chapter-2)


<a id="chapter-0"></a>
## Project description

<a id="chapter-1"></a>
## Installation

Clone repository, install virtual environment and installing dependencies:

```bash
git clone https://github.com/{github_nickname}/{project_path}.git
cd {project_path}
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```


<a id="chapter-2"></a>
## Usage

```bash
chmod u+x {script_name}
./{script_name}
```

'''

license_ = r'''MIT License

Copyright (c) {year} {github_nickname}

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''