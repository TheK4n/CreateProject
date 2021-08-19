## CreateProject


### **Usage:**

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
    │   └── tests.py
    ├── env
    └── .git
```
