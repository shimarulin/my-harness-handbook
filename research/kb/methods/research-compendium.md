# Research Compendium: воспроизводимые исследовательские пакеты

| Параметр | Значение |
|---|---|
| Статус | draft |
| Обновлено | 2026-09-30 |

## Что это

**Research Compendium** — коллекция всех цифровых частей исследовательского проекта (data, code, texts: protocols, reports, questionnaires, metadata), организованная так, чтобы воспроизведение всех результатов было straightforward. Концепция введена **Gentleman & Temple Lang (2004)** в «Statistical Analyses and Reproducible Research»: compendium — одновременно контейнер элементов документа и его вычислений и средство распространения, управления и обновления коллекции.

## Ключевые концепции

### Три принципа

1. **Files should be organized in a conventional folder structure**
2. **Data, methods, and output should be clearly separated**
3. **The computational environment should be specified**

### Структуры

Basic Compendium:

```
compendium/
├── data/
│   └── my_data.csv
├── analysis/
│   └── my_script.R
├── DESCRIPTION
└── README.md
```

Executable Compendium (добавляет фиксацию среды и запуск):

```
compendium/
├── CITATION
├── code/          # analyse_data.R, clean_data.R
├── data_clean/    # derived
├── data_raw/      # read-only + datapackage.json
├── Dockerfile     # computational environment
├── figures/
├── LICENSE
├── Makefile       # точка входа воспроизведения
├── paper.Rmd      # literate programming
└── README.md
```

### Три типа файлов

| Тип | Примеры | Правило |
|---|---|---|
| Read-only | raw data (`data_raw/`), metadata (`datapackage.json`, `CITATION`) | Не править |
| Human-generated | code, paper (`paper.Rmd`), docs (`README.md`) | Source of truth |
| Project-generated | clean data, figures, output | Не коммитить вручную / регенерировать |

### Публикация (7 шагов)

Придумать структуру → создать → git-репозиторий → добавить всё для воспроизведения → сделать максимально чистым и простым → peer check → опубликовать.

Платформы: GitHub/GitLab (с Binder link), Zenodo (DOI), Open Science Framework (OSF), supplementary material к статье.

### Инструменты и экосистема

| Инструмент | Роль |
|---|---|
| **rrrpkg** (rOpenSci) | R package как compendium: стандартная узнаваемая организация |
| **rrtools** (Ben Marwick) | Инструкции, шаблоны, функции для compendium под journal article с R |
| **o2r ERC** | Executable Research Compendium: контейнерный формат, инкапсуляция runtime environment; OJS-плагин, Docker-execution |
| **The Turing Way** | Community-driven guide по воспроизводимой науке; раздел про compendia |
| **NCEAS** | Ресурсы по reproducible research practices |

## Сильные и слабые стороны

Сильные: peer review (проверяемость всего пакета), понимание исследования, обучение, воспроизводимость как проверяемое свойство.

Слабые (границы применимости): базовый compendium не решает проблему зависимостей и среды без контейнеризации (Dockerfile/ERC); ориентация на финальный упакованный артефакт, а не на ежедневный процесс заметок; требует дисциплины окружения для каждого цикла — overhead оправдан только для runnable-исследований.

### Перенос на разработку ПО

Структура compendium ≈ project layout: разделение raw/derived data, code, output + фиксированная среда (Dockerfile) + точка входа (Makefile) + документ (README/paper). Три типа файлов переносятся на правила репозитория: read-only не править, generated не редактировать вручную, human-generated — source of truth. ERC-механика ≈ reproducible build + CI-артефакт с DOI (Zenodo).

Применимо в разработке: spike с кодом, бенчмарки, сравнение производительности библиотек. Не применимо как основа всей базы знаний: ландшафтные обзоры и накопление выводов между циклами в эту структуру не ложатся (см. `research/inbox/research-and-notes/research-process.md`, обработка — фаза 4 плана).

## Источники

- The Turing Way, Research Compendia: https://book.the-turing-way.org/reproducible-research/compendia
- rOpenSci: https://ropensci.org; rrrpkg: https://github.com/ropensci/rrrpkg
- rrtools: https://github.com/benmarwick/rrtools
- o2r (Opening Reproducible Research): https://o2r.info
- NCEAS: https://learning.nceas.ucsb.edu
- Входные материалы inbox: `documentation-process/reference/research-compendium.md`
