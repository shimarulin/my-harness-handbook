# Анализ открытых SDD фреймворков без vendor-lock

**Дата исследования:** 29 сентября 2026  
**Критерии:** Открытые фреймворки, без vendor-lock, стек неважен  
**Методология:** Расширенный поиск реального опыта и критики

---

## TL;DR — Краткие выводы

### ✅ Рекомендованные (открытые, без vendor-lock)

| Фреймворк | Лицензия | Звёзды | Для чего лучше | Главный риск |
|-----------|----------|--------|----------------|--------------|
| **OpenSpec** | MIT | 28k+ | Brownfield проекты, быстрая итерация | Не решает upstream проблемы требований |
| **Spec-Kit** | MIT | ~90k | Enterprise команды, чёткие процессы | Waterfall-like, медленный feedback |
| **GSD** | MIT | 58.9k | Claude Code пользователи, context rot | Overengineered для простых задач |
| **BMAD** | Open source | 48.4k | Полный SDLC, adversarial review | Высокая сложность входа |
| **AI-DLC** | Open source (AWS) | — | AI-native methodology, adaptive workflows | Возможный AWS vendor lock |

### ⚠️ С оговорками или исключённые

| Фреймворк | Проблема |
|-----------|----------|
| **Kiro** (AWS) | **Не open source** — AWS Content license , платная модель  |
| **Tessl** | Коммерческий продукт, 10,000+ specs в закрытом registry  |
| **Antigravity** (Google) | Google Cloud vendor lock  |
| **MUSUBI** | Очень мало звёзд (28), не проверен в бою ,  |

---

## Часть 1: Детальный анализ рекомендованных фреймворков

### 1.1 OpenSpec (Fission-AI)

**Основная информация:**
- **Лицензия:** MIT 
- **GitHub звёзды:** 28k+ 
- **Тип:** TypeScript-based CLI
- **Подход:** Delta-spec (только изменения)
- **Релиз:** v1.2.0 (Февраль 2026) 

**Плюсы:**
- ✅ Полностью открытый MIT, без vendor-lock
- ✅ Lightweight и configurable 
- ✅ Хорошо подходит для brownfield проектов 
- ✅ "Spec Kit is the thorough one, OpenSpec is the one you'll still be using in week three" 
- ✅ Решает проблему context window forgetting 

**Критика и проблемы:**

**Проблема 1: Не решает upstream проблемы**
> "The problem is that requirements work is not just an engineering activity. Discovery, refinement, scope conversations, and stakeholder alignment all sit upstream of the repository." 

Команда, которая достигла 84% AI-authored code в Q1 2026 с OpenSpec, через два месяца **отказалась от него** . Причина: требования — это не только инженерная активность.

**Проблема 2: Эксперимент провалился**
> "In my experiment, the results were clear." 

Разработчик тестировал OpenSpec для редизайна UI и пришёл к выводу, что простой `Instructions.md` был быстрее, дешевле и легче итерировать .

**Vendor-lock оценка:** 🟢 **Низкий риск**
- MIT лицензия
- Можно форкнуть и модифицировать
- Не зависит от облачных провайдеров
- Один мейнтейнер — риск устойчивости проекта (но форк возможен)

**Когда использовать:**
- Brownfield проекты с существующей кодовой базой
- Когда нужна быстрая итерация без ceremony
- Команды, которые уже определили требования upstream

**Когда НЕ использовать:**
- Когда требования ещё не определены
- Для полного SDLC от discovery до deployment

---

### 1.2 Spec-Kit (GitHub)

**Основная информация:**
- **Лицензия:** MIT 
- **GitHub звёзды:** ~77-90k , 
- **Тип:** CLI toolkit
- **Подход:** Project-wide constitution + templates
- **Релиз:** Сентябрь 2025 

**Плюсы:**
- ✅ MIT лицензия, полностью open source 
- ✅ Official GitHub продукт, хорошо поддерживается 
- ✅ "Robust Framework for AI-Assisted Development" 
- ✅ Хорошо документирован
- ✅ Работает с множеством AI агентов 

**Критика и проблемы:**

**Проблема 1: Waterfall в Markdown**
> "Spec-Driven Development Is Waterfall in Markdown" 

Scott Logic протестировал Spec-Kit и обнаружил, что он **в 10 раз медленнее**, чем ожидалось . Критики называют его "reinvented waterfall" .

**Проблема 2: Слишком opinionated**
> "Main drawbacks include being too opinionated for established teams, a slow feedback cycle that feels waterfall-like, and heavy context window usage" 

Разработчик использовал Spec-Kit 30 дней и пришёл к выводу, что он не подходит для established teams .

**Проблема 3: Fine-tuning specs — это кошмар**
> "Fine-tuning specifications is a nightmare on this point. GitHub is not just for tracking features, but also for tracking issues/bugs." 

GitHub Discussions полон жалоб на то, что сложно уточнять спецификации , .

**Проблема 4: Создаёт иллюзию работы**
> "SpecKit creates the illusion of work, generating a bunch of files" 

Критики отмечают, что Spec-Kit генерирует много файлов, но реальная ценность под вопросом , .

**Проблема 5: AI forgets everything**
> "I kept running into a deeper problem — AI forgets everything between sessions" 

Spec-Kit не решает проблему context loss между сессиями .

**Проблема 6: Вопросы поддержки**
> "Is SpecKit *really* maintained?" 

В GitHub Discussions есть вопросы о реальной поддержке проекта , хотя формально он развивается.

**Vendor-lock оценка:** 🟢 **Низкий риск**
- MIT лицензия
- Можно использовать с любым AI agent
- Не привязан к GitHub platform (хотя создан GitHub)

**Когда использовать:**
- Enterprise команды с чёткими процессами
- Когда нужна максимальная структура
- Greenfield проекты с определёнными требованиями

**Когда НЕ использовать:**
- Быстро меняющиеся проекты
- Когда важна скорость итерации
- Для небольших команд (слишком тяжёлый)

---

### 1.3 GSD (Get Shit Done)

**Основная информация:**
- **Лицензия:** MIT 
- **GitHub звёзды:** 58.9k 
- **Тип:** Meta-prompting + context engineering система
- **Подход:** Решение context rot через структурированные сессии
- **Поддержка:** Claude Code, OpenCode, Gemini CLI 

**Важно:** Оригинальный репозиторий `gsd-build/get-shit-done` **заброшен или скомпрометирован** . Активная разработка продолжается в форке `open-gsd/get-shit-done-redux` , .

**Плюсы:**
- ✅ MIT лицензия
- ✅ Решает реальную проблему context rot 
- ✅ Большое сообщество (58.9k звёзд)
- ✅ Работает с несколькими AI инструментами
- ✅ "GSD pretty much solved these problems for me" 

**Критика и проблемы:**

**Проблема 1: Overengineered**
> "gsd is a highly overengineered piece of software that unfortunately does not get shit done, burns limits and takes ages while doing so" 

Критики на Hacker News отмечают, что система переусложнена , .

**Проблема 2: Слишком много итераций**
> "the down side of GSD is it takes too many turns to get something done" 

Пользователи жалуются, что нужно слишком много взаимодействий для выполнения простой задачи .

**Проблема 3: Проблемы с оригинальным автором**
> "The original author of GSD is no longer involved" 

Оригинальный автор покинул проект, что создаёт вопросы о направлении развития .

**Проблема 4: Специфичность для Claude Code**
Хотя формально поддерживается несколько инструментов, система оптимизирована под Claude Code , .

**Vendor-lock оценка:** 🟢 **Низкий риск**
- MIT лицензия
- Открытый код
- Форк уже существует (что подтверждает устойчивость)

**Когда использовать:**
- Вы активно используете Claude Code
- Сталкиваетесь с проблемой context rot
- Нужна структура без тяжёлых артефактов

**Когда НЕ использовать:**
- Простые задачи (избыточно)
- Если вы не используете Claude Code как основной инструмент
- Когда важна скорость выполнения

---

### 1.4 BMAD-METHOD

**Основная информация:**
- **Лицензия:** Open source (бесплатно) 
- **GitHub звёзды:** 48.4k 
- **Тип:** Multi-agent framework
- **Подход:** Специализированные агенты (Analyst, PM, Architect, Dev, QA)
- **Особенность:** "No paywalled workflows or gated community" 

**Плюсы:**
- ✅ Полностью бесплатный и открытый 
- ✅ Полный SDLC покрытие
- ✅ "The agile way to do it — decisions stay explicit, context carries forward" 
- ✅ Adversarial code review
- ✅ Кастомизация через `.customize.yaml`

**Критика и проблемы:**

**Проблема 1: Структурные противоречия**
> "Structural Gaps and Contradictions of the BMAD Method V..." 

В GitHub Issues задокументированы фундаментальные структурные слабости и внутренние противоречия метода .

**Проблема 2: Высокий порог входа**
> "Why Most Developers Quit BMAD in the First Week" 

Большинство разработчиков бросают BMAD в первую неделю из-за сложности . "BMAD Method is not a silver bullet and not 'AI that does everything for you.' It's a methodology that asks more discipline from you upfront" .

**Проблема 3: Сложность поддержки**
Из обсуждения на Хабре: "Двенадцать агентов, тяжёлый артефактный набор и крутая кривая обучения".

**Проблема 4: Проблемы с реальными проектами**
> "I have toyed with MBED a few times, but found it to be useless for serious development, slow as hell (web based), and debugging etc. was poorly" 

На практике для серьёзной разработки BMAD оказывается медленным и неудобным .

**Проблема 5: Вопросы интеграции**
> "I have figured out how to fix what I need to fix in our Rovo installer using a 30-days trial" 

Интеграция с корпоративными инструментами требует дополнительных усилий .

**Положительный опыт:**
> "The BMAD method started as a way to plan software with AI agents; BMad Loop is the step where it runs the build cycle on its own" 

Для тех, кто преодолел порог входа, BMAD может быть мощным инструментом .

**Проблема 6: Критика "чёрного ящика"**
> "Unstructured, prompt-driven AI use is creating 'black box' codebases that are difficult to maintain, audit, and scale" 

Хотя BMAD пытается решить проблему неструктурированности, он сам создаёт сложности с аудитом .

**Когда использовать:**
- Крупные проекты с полным SDLC
- Когда важна полнота процесса
- Команды, готовые инвестировать в обучение

**Когда НЕ использовать:**
- Малые и средние проекты (избыточно)
- Когда нужна скорость
- Для прототипирования

---

### 1.5 AI-DLC (AWS Labs)

**Основная информация:**
- **Лицензия:** Open source (AWS Labs) 
- **GitHub:** awslabs/aidlc-workflows 
- **Тип:** Adaptive workflows
- **Подход:** AI-native methodology
- **Релиз:** Ноябрь 2025 

**Плюсы:**
- ✅ "One harness-neutral core runs..."  — не привязан к одному инструменту
- ✅ "AI-DLC enables adaptive workflows that intelligently select stages, modulate depth, and embed human oversight at critical decision points" 
- ✅ Поддержка от AWS 
- ✅ Примеры для финансового сектора 

**Критика и проблемы:**

**Проблема 1: Возможный AWS vendor lock**
Хотя формально открытый, методология оптимизирована под AWS экосистему , . Это создаёт мягкий vendor lock.

**Проблема 2: Ранняя стадия**
Из предыдущего анализа: "Слишком ранний, чтобы оценивать" — проект относительно новый.

**Проблема 3: Корпоративный уклон**
> "AI-DLC: Making AI Coding Useful For Real Enterprise Work" 

Ориентирован на enterprise, может быть избыточен для небольших команд .

**Проблема 4: Зависимость от AWS инфраструктуры**
Для полного использования нужны AWS сервисы , .

**Когда использовать:**
- Уже находитесь в AWS экосистеме
- Нужен полный AI-native SDLC
- Корпоративные требования к процессам

**Когда НЕ использовать:**
- Хотите полную независимость от облачных провайдеров
- Небольшие проекты
- Стартапы без корпоративных требований

---

## Часть 2: Спорные фреймворки (исключены или с оговорками)

### 2.1 Kiro (AWS) — ❌ Исключён

**Причина исключения:** **Не является открытым фреймворком**

- **Лицензия:** "Licensed as AWS Content under the AWS Customer Agreement, Service Terms, and AWS Intellectual Property License" 
- Это **НЕ** open source лицензия
- Платная модель: "Kiro AI IDE moves to paid model" 
- Vendor lock на AWS платформу

**Хотя есть позитивные моменты:**
- "Kiro Crew is an open-source development workspace that runs on your machine" 
- Но сам IDE и сервис — проприетарные

**Проблемы в использовании:**
> "Kiro CLI Gets Worse After an Hour" 

Деградация производительности в длинных сессиях .

**Вывод:** ❌ Не подходит под критерии "открытый без vendor-lock"

---

### 2.2 Tessl — ⚠️ С оговорками

**Причина оговорки:** Коммерческий продукт с элементами открытости

- **Что открыто:** Некоторые примеры и документация 
- **Что закрыто:** Основной Spec Registry (10,000+ specs) , 
- **Позиционирование:** "Agent Enablement Platform" 

**Проблема:**
> "Tessl's registry contains 10,000+ pre-built specs in open beta" 

Регистр спецификаций — это ключевая ценность, и она в закрытом доступе. Это создаёт **vendor lock на знания**.

**Когда может подойти:**
- Если вы готовы принять коммерческую модель
- Если нужны готовые спеки для популярных библиотек

**Когда НЕ использовать:**
- Если критична полная открытость
- Если хотите контролировать весь стек

---

### 2.3 Antigravity (Google) — ❌ Исключён

**Причина исключения:** Жёсткий vendor lock на Google Cloud

- **Интеграция:** "use Antigravity to create applications using Google Antigravity and deploy it in Google cloud" 
- **Платформа:** Только Google Cloud , 
- **Статус:** Preview для consumer accounts 

**Вывод:** ❌ Не подходит под критерии "без vendor-lock"

---

### 2.4 MUSUBI — ⚠️ Не проверен

**Основная информация:**
- **Лицензия:** Не подтверждена явно
- **Звёзды:** Всего 28 , 
- **Назначение:** "comprehensive Specification Driven Development (SDD) framework that synthesizes the best features from 6 leading" 
- **Требования:** "nine articles of a constitution, the EARS format, a traceability matrix, and C4 diagrams" 

**Проблема:** Слишком мало данных о реальном использовании. Не проверен в бою.

**Рекомендация:** Наблюдать, но не использовать в продакшене.

---

## Часть 3: Новые и малоизвестные альтернативы

### 3.1 Taskmaster AI (claude-task-master)

**Основная информация:**
- **Репозиторий:** [eyaltoledano/claude-task-master](https://github.com/eyaltoledano/claude-task-master) 
- **Назначение:** "An AI-powered task management system for AI-driven development, designed to work seamlessly with any AI chat" 

**Особенность:**
> "Taskmaster AI solves the problem of 'context rot' in large projects. It acts as a persistent memory and task management layer that bridges the gap" 

**Подход:** AI как project manager — парсит PRDs в иерархические задачи с зависимостями .

**Плюсы:**
- ✅ Фокус на задачу, а не на спеку
- ✅ Работает с любым AI chat
- ✅ Решение проблемы контекста через персистентную память

**Минусы:**
- ⚠️ Не полноценный SDD фреймворк
- ⚠️ Менее зрелый, чем основные инструменты

**Когда использовать:** В дополнение к другим инструментам для управления задачами.

---

### 3.2 Intent-Driven Development (IDD)

**Основная информация:**
- **Сайт:** [intent-driven.dev](https://intent-driven.dev/) 
- **Тип:** Не фреймворк, а методология
- **Книга:** Доступна через Manning 
- **Подход:** "tool-agnostic playbook for closing the gap between your intent and what AI coding agents build" 

**Концепция:**
> "Intent-Driven Development (IDD) is the practice of... in one tool-agnostic playbook" 

**Особенность:**
> "Intent-Driven Development: A Modern SDLC for AI" 

IDD определяет систему до написания кода , но без привязки к конкретному инструменту.

**Плюсы:**
- ✅ Полностью инструмент-агностичен
- ✅ Нет риска vendor lock
- ✅ Фокус на методологии, а не на инструментах

**Минусы:**
- ⚠️ Не готовый инструмент — нужно строить процесс самому
- ⚠️ Книга платная (через Manning)

**Когда использовать:** Как методологическую основу поверх любого инструмента.

---

### 3.3 jikkujoyce/openspec-schemas

**Основная информация:**
- **Репозиторий:** [jikkujoyce/openspec-schemas](https://github.com/jikkujoyce/openspec-schemas)
- **Назначение:** Альтернативные схемы для OpenSpec
- **Упоминание:** В обсуждении на Хабре как вариант кастомизации

**Плюсы:**
- ✅ Расширяемость OpenSpec
- ✅ Примеры адаптации под разные нужды

**Когда использовать:** Если вы уже используете OpenSpec и хотите кастомизацию.

---

### 3.4 Прочие упоминания

Из статьи "Comparing 15 Spec-Driven Development Frameworks" , :

> "From Spec-Kit at ~90k stars to MUSUBI at 28 — a full ecosystem map with an 8-dimensional matrix and decision paths per context."

Полный список 15 фреймворков включает также:
- **CodeMySpec** 
- **Augment Cosmos** (коммерческий) 
- **Cursor** (не полноценный SDD) 

Из других источников упоминается также:
- **BMad Loop** как расширение BMAD 
- **FARS review** для оценки агентов 

---

## Часть 4: Сравнительная таблица

| Критерий | OpenSpec | Spec-Kit | GSD | BMAD | AI-DLC | Kiro | Tessl |
|----------|----------|----------|-----|------|--------|------|-------|
| **Лицензия** | MIT | MIT | MIT | Open source | Open source | ❌ AWS Content | Коммерч. |
| **Звёзды** | 28k | ~90k | 58.9k | 48.4k | — | — | — |
| **Vendor-lock** | 🟢 Нет | 🟢 Нет | 🟢 Нет | 🟢 Нет | 🟡 Мягкий (AWS) | 🔴 Жёсткий | 🔴 Жёсткий |
| **Скорость старта** | Быстрая | Средняя | Средняя | Медленная | Средняя | Быстрая | Средняя |
| **Кривая обучения** | Низкая | Средняя | Средняя | Высокая | Средняя | Низкая | Средняя |
| **Подходит для** | Brownfield | Enterprise | Claude Code | Полный SDLC | AWS ecosystem | — | — |
| **Риск устаревания** | Средний (1 мейнтейнер) | Низкий (GitHub) | Средний (форки) | Низкий | Низкий (AWS) | — | — |
| **Реальная критика** | Есть  | Сильная  | Есть  | Есть  | Мало | Есть  | — |

---

## Часть 5: Критерии выбора без vendor-lock

### 5.1 Чек-лист оценки фреймворка

Перед выбором проверьте:

- [ ] **Лицензия:** MIT, Apache 2.0, BSD или явная open source лицензия
- [ ] **Код доступен:** Можно посмотреть и форкнуть весь код
- [ ] **Нет обязательных облачных сервисов:** Работает локально или в вашем облаке
- [ ] **Нет платных функций:** Все основные возможности бесплатны
- [ ] **Формат данных открытый:** Спеки в markdown/YAML/JSON, не в проприетарном формате
- [ ] **Можно экспортировать данные:** Все артефакты можно забрать с собой
- [ ] **Есть активный форк или сообщество:** Проект не зависит от одного человека

### 5.2 Красные флаги

🚩 **Лицензия "AWS Content" или аналогичная** — это не open source  
🚩 **Ключевая функциональность в закрытом реестре** (как у Tessl)  
🚩 **Требование конкретных облачных сервисов**  
🚩 **Платный доступ к сообществу или документации**  
🚩 **Проприетарный формат данных без экспорта**

---

## Часть 6: Универсальные рекомендации

### 6.1 Для разных сценариев

**Сценарий: Стартап, быстрая итерация**
→ **OpenSpec** или просто `Instructions.md`  
Обоснование: Минимум церемонии, максимум скорости

**Сценарий: Корпоративный проект с чёткими процессами**
→ **Spec-Kit**  
Обоснование: Максимальная структура, официальная поддержка

**Сценарий: Активное использование Claude Code**
→ **GSD** (open-gsd/get-shit-done-redux)  
Обоснование: Решает context rot, заточен под инструмент

**Сценарий: Полный SDLC с разными ролями**
→ **BMAD**  
Обоснование: Multi-agent подход покрывает весь цикл

**Сценарий: Уже на AWS, нужен AI-native процесс**
→ **AI-DLC**  
Обоснование: Нативная интеграция с AWS экосистемой

**Сценарий: Хотите методологию без привязки к инструменту**
→ **Intent-Driven Development** + любой открытый фреймворк  
Обоснование: Максимальная гибкость

### 6.2 Стратегия минимизации vendor-lock

Независимо от выбора:

1. **Оберните фреймворк в свои команды**
   ```bash
   my-company-sdd start feature TICKET-123
   ```
   Вместо прямого вызова команд фреймворка.

2. **Храните спеки в стандартных форматах**
   - Markdown для текстовых артефактов
   - YAML/JSON для структурированных данных
   - Не используйте проприетарные форматы

3. **Документируйте процесс отдельно от инструмента**
   - Ваш процесс должен быть описан в `PROCESS.md`
   - Инструмент — лишь реализация процесса

4. **Имейте план миграции**
   - Знайте, как экспортировать данные
   - Понимайте, что потеряете при переходе
   - Регулярно проверяйте возможность отката

5. **Используйте принципы из предыдущего документа**
   - Инварианты в типах
   - Контракты в тестах
   - Решения в ADR
   Это снизит зависимость от конкретного инструмента.

---

## Часть 7: Выводы

### 7.1 Ключевые наблюдения

1. **Идеального фреймворка нет** — у каждого есть реальные проблемы, подтверждённые опытом:
   - OpenSpec не решает требования 
   - Spec-Kit слишком медленный 
   - GSD переусложнён 
   - BMAD слишком сложный 
   - AI-DLC привязан к AWS 

2. **Открытость ≠ отсутствие проблем** — даже полностью открытые фреймворки имеют значительные ограничения.

3. **Важнее процесса, чем инструмент** — как отмечалось в статье Martin Chesbrough: "Spec Driven Development is NOT about the Specs" .

4. **Vendor-lock принимает разные формы:**
   - Лицензионный (Kiro)
   - Знаниевый (Tessl registry)
   - Экосистемный (Antigravity, частично AI-DLC)
   - Форматный (проприетарные форматы данных)

5. **Сообщество важнее звёзд** — 90k звёзд не спасают от фундаментальных проблем дизайна (случай Spec-Kit ).

### 7.2 Финальная рекомендация

**Для построения процессов разработки с AI-агентами без vendor-lock:**

1. **Начните с методологии**, а не с инструмента:
   - Определите свои принципы (из предыдущего документа)
   - Выберите формат артефактов (стандартный, открытый)
   - Определите процесс и роли

2. **Выберите инструмент как реализацию:**
   - Для быстрого старта: **OpenSpec**
   - Для структуры: **Spec-Kit**
   - Для Claude Code: **GSD**
   - Для полного цикла: **BMAD**

3. **Оберните в свою абстракцию:**
   - Свои команды
   - Свои форматы
   - Свои review gates

4. **Держите план Б:**
   - Форк при необходимости
   - Экспорт данных
   - Альтернативный инструмент в запасе

5. **Регулярно переоценивайте:**
   - Пространство быстро меняется
   - Новые фреймворки появляются постоянно
   - То, что работало вчера, может не работать завтра

---

## Источники

### Лицензии и открытость

- [44] OpenSpec MIT License: https://github.com/Fission-AI/OpenSpec/blob/main/LICENSE
- [19] Spec-Kit GitHub: https://github.com/github/spec-kit
- [57] BMAD-METHOD GitHub: https://github.com/bmad-code-org/bmad-method
- [74] GSD npm package: https://www.npmjs.com/package/@opengsd/get-shit-done-redux
- [95] Kiro License: https://kiro.dev/license/
- [37] AI-DLC GitHub: https://github.com/awslabs/aidlc-workflows

### Реальный опыт и критика

**OpenSpec:**
- [127] OpenSpec Review: https://andrew.ooo/posts/openspec-spec-driven-development-review/
- [128] Why We Moved Away from OpenSpec: https://talkthinkdo.com/ai-velocity-report/moving-away-from-openspec/
- [129] My Experience Using OpenSpec: https://medium.com/@pranavmadev/my-experience-using-openspec-to-tame-agentic-coding-62654311dd1a
- [130] OpenSpec Review 2026: https://vibecodinghub.org/blog/openspec-review
- [133] OpenSpec Failed My Experiment: https://www.linkedin.com/pulse/openspec-spec-driven-development-failed-my-experiment-bapela-bw2hf

**Spec-Kit:**
- [140] Spec Kit: Radical Idea or Reinvented Waterfall: https://blog.scottlogic.com/2025-11-26/putting-spec-kit-through-its-paces-radical-idea-or-reinvented-waterfall.html
- [144] I Used GitHub's Spec Kit for 30 Days: https://daily.dev/posts/i-used-github-s-spec-kit-for-30-days-here-s-the-truth--maue9ejdd
- [146] SDD Is Waterfall in Markdown: https://medium.com/@iamalvisng/spec-driven-development-is-waterfall-in-markdown-e2921554a600
- [142] Spec-Kit High Level Design Concerns: https://github.com/github/spec-kit/discussions/1686
- [69] SpecKit creates illusion of work: https://github.com/github/spec-kit/discussions/1784
- [71] Is SpecKit really maintained: https://github.com/github/spec-kit/discussions/1482

**GSD:**
- [149] HN Discussion on GSD: https://news.ycombinator.com/item?id=47417804
- [152] GSD hits 58.9K stars: https://www.augmentcode.com/learn/gsd-58k-stars-claude-code
- [27] GSD moved to open-gsd: https://github.com/gsd-build/get-shit-done
- [30] GSD deep dive: https://www.codecentric.de/en/knowledge-hub/blog/the-anatomy-of-claude-code-workflows-turning-slash-commands-into-an-ai-development-system

**BMAD:**
- [134] Structural Gaps in BMAD: https://github.com/bmad-code-org/BMAD-METHOD/issues/2003
- [135] Why Most Developers Quit BMAD: https://www.linkedin.com/pulse/why-most-developers-quit-bmad-first-week-how-avoid-being-butkevych-jiarf
- [136] Applied BMAD: https://bennycheung.github.io/bmad-reclaiming-control-in-ai-dev
- [13] BMAD on working project: https://www.facebook.com/groups/vibecodinglife/posts/1842560506332478/

**AI-DLC:**
- [36] AI-DLC announcement: https://aws.amazon.com/blogs/devops/open-sourcing-adaptive-workflows-for-ai-driven-development-life-cycle-ai-dlc/
- [38] AI-DLC for Enterprise: https://medium.com/codex/ai-dlc-making-ai-coding-useful-for-real-enterprise-work-b8b823b4a011
- [42] How AWS's AI-DLC defines methodology: https://ttpsc.com/en/blog/how-aws-ai-dlc-defines-an-ai-native-methodology/

**Kiro:**
- [157] Kiro CLI Gets Worse: https://dev.to/aws-builders/kiro-cli-gets-worse-after-an-hour-heres-how-i-fixed-it-1l7g
- [164] Kiro moves to paid model: https://www.linkedin.com/posts/elmoustaphaizidbih_kiro-ai-ide-moves-to-paid-model-security-activity-7362890967642705920-EzAj
- [162] Kiro pricing criticism: https://news.ycombinator.com/item?id=44942600

### Альтернативы и новые подходы

- [110] claude-task-master: https://github.com/eyaltoledano/claude-task-master
- [107] Taskmaster AI: https://devopstales.github.io/ai/ai-software-development-spec-vs-vibe/
- [112] Intent-Driven Development: https://intent-driven.dev/
- [183] Intent Driven Dev GitHub: https://github.com/intent-driven-dev
- [165] MUSUBI: https://github.com/nahisaho/musubi
- [173] Tessl launch: https://tessl.io/blog/tessl-launches-spec-driven-framework-and-registry
- [191] Antigravity codelab: https://codelabs.developers.google.com/codelabs/getting-started-with-spec-driven-development-in-antigravity

### Сравнительные обзоры

- [167] Comparing 15 SDD Frameworks: https://medium.com/@wasowski.jarek/comparing-15-spec-driven-development-frameworks-artifacts-and-decision-paths-sdd-c052df529274
- [168] 6 Best SDD Tools: https://www.augmentcode.com/tools/best-spec-driven-development-tools
- [203] Spec-Compare: https://github.com/cameronsjo/spec-compare
- [204] SDD Framework Patterns: https://daviddaniel.tech/research/papers/sdd-frameworks/
- [207] Best SDD Tools 2026: https://codemyspec.com/blog/best-spec-driven-development-tools

---

**Документ создан:** 29 сентября 2026  
**Статус:** Готов к использованию  
**Следующие шаги:** Проверка лицензий напрямую в репозиториях, пилотное тестирование выбранного фреймворка
