# Research Compendium

## Определение

**Research Compendium** — коллекция всех цифровых частей исследовательского проекта, включая data, code, texts (protocols, reports, questionnaires, metadata), созданная таким образом, что воспроизведение всех результатов straightforward【turn3fetch0】.

> «We introduce the concept of a compendium as both a container for the different elements that make up the document and its computations (i.e. text, code, data,...), and as a means for distributing, managing and updating the collection» — Gentleman, R. and Temple Lang, D. (2004)【turn5fetch0】

---

## Три принципа【turn3fetch0】【turn4fetch0】

1. **Files should be organized in a conventional folder structure**
2. **Data, methods, and output should be clearly separated**
3. **The computational environment should be specified**

---

## Структура

### Basic Compendium【turn3fetch0】

```
compendium/
├── data/
│   ├── my_data.csv
├── analysis/
│   └── my_script.R
├── DESCRIPTION
└── README.md
```

### Executable Compendium【turn4fetch0】

```
compendium/
├── CITATION
├── code/
│   ├── analyse_data.R
│   └── clean_data.R
├── data_clean/
│   └── data_clean.csv
├── data_raw/
│   ├── datapackage.json
│   └── data_raw.csv
├── Dockerfile
├── figures/
│   └── flow_chart.jpeg
├── LICENSE
├── Makefile
├── paper.Rmd
└── README.md
```

---

## Три типа файлов【turn4fetch0】

| Тип | Примеры |
|---|---|
| **Read-only** | Raw data (`data_raw/`), metadata (`datapackage.json`, `CITATION`) |
| **Human-generated** | Code (`clean_data.R`), paper (`paper.Rmd`), documentation (`README.md`) |
| **Project-generated** | Clean data (`data_clean/`), figures (`figures/`), other output |

---

## Инструменты и ресурсы

### rOpenSci

**Сайт:** https://ropensci.org【turn2search3】

> «Transforming science through open data, software & reproducibility. rOpenSci fosters a culture of open and reproducible research using shared data and reusable software»【turn2search3】

### rrrpkg (R Package Research Compendium)

**GitHub:** https://github.com/ropensci/rrrpkg【turn5fetch0】

> «The goal of a research compendium is to provide a standard and easily recognisable way for organising a reproducible research project with R»【turn5fetch0】

### rrtools

**GitHub:** https://github.com/benmarwick/rrtools【turn2search4】

> «The goal of rrtools is to provide instructions, templates, and functions for making a basic compendium suitable for writing a reproducible journal article or report with R»【turn2search4】

### o2r (Opening Reproducible Research)

**Сайт:** https://o2r.info【turn1search1】

**ERC (Executable Research Compendium)** — контейнерный формат, закрывающий gap сохранения зависимостей через инкапсуляцию runtime environment【turn1search1】.

Проект реализует:
- ERC-based publishing workflow
- OJS (Open Journal System) plugin для journal submissions
- Docker-based execution environment

### The Turing Way

**Сайт:** https://book.the-turing-way.org/reproducible-research/compendia【turn3fetch0】

> «The Turing Way is an open source community-driven guide to reproducible, ethical, inclusive and collaborative data science»【turn1search1】

### NCEAS

**Сайт:** https://learning.nceas.ucsb.edu【turn2search9】

Resources for reproducible research practices.

---

## Публикация

### Платформы【turn4fetch0】

- **GitHub/GitLab** (с Binder link)
- **Zenodo** (research archive с DOI)
- **Open Science Framework (OSF)**
- **Supplementary material** к paper publication

### Процесс【turn4fetch0】

1. Think about a good folder structure
2. Create folder structure
3. Make the compendium into a git repository
4. Add all files needed for reproducing results
5. Try to have the compendium as clean and easy to use as possible
6. Have a peer check the compendium
7. Publish your compendium

---

## Зачем Research Compendium?【turn4fetch0】

- **Peer review**: Peers can check what you have done much more thoroughly
- **Understanding research**: Look at the compendium to understand what someone did
- **Teaching**: Research compendia can be great examples for teaching
- **Reproducibility studies**: Other researchers can attempt to redo your computations

---

## Источники

- Turing Way Research Compendia: https://book.the-turing-way.org/reproducible-research/compendia【turn3fetch0】
- rOpenSci: https://ropensci.org【turn2search3】
- rrrpkg: https://github.com/ropensci/rrrpkg【turn5fetch0】
- rrtools: https://github.com/benmarwick/rrtools【turn2search4】
- o2r: https://o2r.info【turn1search1】
- NCEAS: https://learning.nceas.ucsb.edu【turn2search9】
- Gentleman & Temple Lang (2004): "Statistical Analyses and Reproducible Research"【turn5fetch0】
