
<h1 align="center">CreateProject</h1>

<p align="center">
  <a href="https://github.com/TheK4n">
    <img src="https://img.shields.io/github/followers/TheK4n?label=Follow&style=social">
  </a>
  <a href="https://github.com/TheK4n/CreateProject">
    <img src="https://img.shields.io/github/stars/TheK4n/CreateProject?style=social">
  </a>
</p>



## Content
* [Project description](#chapter-0)
* [Usage](#chapter-1)

\
<a id="chapter-0"></a>
## Project description


Script creates python project in work directory

\
<a id="chapter-1"></a>
## Usage

```bash
create-project --help
```

\
Creates project in work directory
```bash
create-project "ProjectName"
```

\
Creates project in work directory and symbolic link in ~/bin:
```bash
create-project "ProjectName" --create-link
```

\
Creates secure Project1, Project2, Project3 with quiet mode: 
```bash
create-project Project{1..3} -sq
```

**Result:**
```text
.
└── ProjectName
    ├── project-name
    ├── README.md
    ├── LICENSE
    ├── requirements.txt
    ├── src
    │   └── utils.py
    ├── test
    │   ├── unittests.py
    │   └── timetests.py
    ├── venv
    └── .git
```

<h1 align="center"><a href="#top">▲</a></h1>
