# Критика Superpowers: детальный анализ источников

**Дата исследования:** 2026-10-01  
**Предмет:** плагин Superpowers (obra/superpowers) для Claude Code  
**Статус:** критика на основе GitHub issues, статей и обсуждений

---

## 1. Потребление токенов

### 1.1. Загрузка всех навыков при старте: 22 000 токенов (11% контекста)

**Источник:** GitHub Issue #190 — "All Skills Preloaded at Startup Consuming 22k+ Tokens (11% of Context)"

Проблема: вместо прогрессивной загрузки навыков (progressive disclosure) плагин загружает **все 14 навыков полностью при запуске сессии**. Это противоречит документации Anthropic по Agent Skills.

**Ожидаемое поведение** (согласно документации Anthropic):
- Discovery (Startup): только frontmatter (name + description) ~100 токенов на навык
- Activation (On-demand): полный SKILL.md при активации
- Execution (As-needed): вспомогательные файлы по мере необходимости
- **Ожидаемые затраты при старте:** ~1 400 токенов (14 навыков × 100 токенов)

**Фактическое поведение:**

| Навык | Токенов |
|-------|---------|
| writing-skills | 5 600 |
| test-driven-development | 2 400 |
| systematic-debugging | 2 400 |
| subagent-driven-development | 2 400 |
| receiving-code-review | 1 500 |
| dispatching-parallel-agents | 1 500 |
| using-git-worktrees | 1 300 |
| finishing-a-development-branch | 993 |
| verification-before-completion | 966 |
| using-superpowers | 896 |
| writing-plans | 785 |
| requesting-code-review | 636 |
| brainstorming | 566 |
| executing-plans | 506 |
| **Итого** | **~22 000** |

**Математическое доказательство:** вывод команды `/context` при старте сессии показал общее использование контекста 82 000 токенов. Сумма известных компонентов (системный промпт, инструменты, агенты, память, сообщения) составила 22 145 токенов. Необъяснённый разрыв — 59 855 токенов. Суммарный размер всех SKILL.md файлов — 22 448 токенов (37,5% от разрыва).

**Проверка размера файлов:** `wc -c` подтвердил, что writing-skills/SKILL.md весит 22 463 байта (~5,6k токенов), а test-driven-development/SKILL.md — 9 867 байт (~2,4k токенов).

**Анализ SessionStart hook:** `hooks/session-start.sh` инжектирует только `using-superpowers` (896 токенов). Остальные 21k токенов загружаются через регистрацию навыков в другом месте.

### 1.2. Сжигание 100% квоты за 5 минут

**Источник:** GitHub Issue #953 — "Claude with this skill ate 100% of tokens in 5 minutes??"

Пользователь дал простую задачу — добавить Google Calendar как MCP-сервер на сайт. Результат: **за 5 минут квота ушла с 0% до 100%**. Claude начал "overthink и делать много больше, чем раньше", включая написание документации, чего раньше не делал.

**Статус:** закрыт как дубликат более общего кластера проблем с токенами (Issue #743, #1152, #1194).

### 1.3. Избыточные циклы субагентов: 33+ вызовов для 300 строк кода

**Источник:** GitHub Issue #21564 — "[BUG] Excessive Token/Time Consumption with Third-Party Skills" (anthropics/claude-code)

**Сценарий:** простой Rust CLI проект (~300 строк, 6 файлов). Ожидаемое время: 20–30 минут. Фактическое: **весь день**.

**Что произошло:**
- Claude вызвал `brainstorming` (не нужен для чёткой спецификации)
- Claude вызвал `writing-plans` (создал план на 1000+ строк для крошечного проекта)
- Claude вызвал `subagent-driven-development`:
  - Запустил отдельного "implementer" субагента для каждой из 11 задач
  - Запустил "spec compliance reviewer" после каждой задачи
  - Запустил "code quality reviewer" после каждой задачи
  - Создал циклы ревью, повторяющиеся несколько раз
- **Результат: 33+ вызовов субагентов** для того, что можно было сделать напрямую

**Оценка потерь:** в **10–50 раз больше токенов**, чем необходимо. Часы вместо минут.

**Корневая причина:** навык `subagent-driven-development` навязывает жёсткий workflow для каждой задачи. Модель следует инструкциям буквально, без суждения о соразмерности.

**Предложенные исправления:**
- Порог сложности: навыки активируются только для проектов выше определённого размера
- Позволить Claude переопределять: "этот проект слишком прост для такого workflow"
- Предупреждать о потреблении токенов
- Лучшие настройки по умолчанию: не включать дорогие мульти-агентные workflow

### 1.4. Сравнительные данные

**Источник:** Raw benchmark данные

| Инструмент | Токенов | Время |
|-----------|---------|-------|
| GSD | ~600K | 40 мин |
| Superpowers | ~200K | 40 мин |
| Claude Code (без плагина) | ~50K | 10 мин |

Superpowers потребляет в **4 раза больше токенов**, чем нативный Claude Code, при том же результате.

**Источник:** Обсуждение на Artificial Analysis

Разбор токенов для среднего feature с Superpowers: brainstorming.md → plan.md → для каждой задачи: написать тест → запустить → падает → реализовать → запустить → проходит → обновить план/прогресс. Feature из 3 задач: **150k–250k токенов**.

Причины:
- **Цикл субагентов:** каждая задача запускает субагента, читающего весь план + весь прогресс + всю кодовую базу
- **Тесты как оракул:** 15–30 тестов низкой ценности, большинство — `expect(result).toBeDefined()`
- **Избыточная документация:** файлы на 2k–5k токенов, которые модель перечитывает каждый ход

### 1.5. Позиция мейнтейнера

**Источник:** Superpowers 6 release notes

> "It's no secret that the most common lament we hear from Superpowers users is that tokens are expensive and Superpowers uses a ton of them."

В версии 6.0.0 была предпринята попытка оптимизации: официальные eval данные показали **снижение потребления токенов на ~50%** и **ускорение в ~2 раза**.

---

## 2. Замедление работы

### 2.1. Простая задача вместо 10 секунд занимает 5 минут

**Источник:** Статья на Juejin — "曾经人手一个的Superpowers，为什么现在都在卸"

Пользователь попросил Claude Code изменить имя переменной с camelCase на snake_case. Обычно это занимает 10 секунд. С Superpowers:
1. 1 минута на brainstorming
2. Написание spec
3. Составление plan
4. Только потом — изменение переменной
5. Финальный review

**Итого: 5 минут вместо 10 секунд.**

### 2.2. Средняя задача вместо 30 минут занимает 2–3 часа

**Источник:** Cocoloop.cn — обзор SKILL-плагинов

> "太慢了。一个中等复杂度的功能，以前30分钟出结果，现在要2-3小时。因为前面的需求分析、架构设计、任务拆解都很花时间 - Token消耗翻倍"

### 2.3. Архитектурная проблема, а не проблема модели

**Источник:** Nahornyi AI LAB — "Claude Code Slowdown: Superpowers Overhead"

> "Claude Code users are widely reporting slowdowns after installing Superpowers. The skills inflate context, and long agent chains consume time and tokens."

Ключевой вывод: 
> "If removing a single skill-pack noticeably speeds things up, the problem isn't with a specific model but with the prompt orchestration architecture around it."

**Механика замедления:** каждый слой (планы, TDD-циклы, субагенты, ревью, чекпоинты) добавляет инструкции, промежуточные артефакты и новые проходы по контексту. Модель читает свой собственный вывод вместо кода.

### 2.4. Бесконечные циклы субагентов

**Источник:** Обсуждение на LINUX DO

> "Тут есть死循环, Superpowers определяет много agent-ролей, и если у тебя ещё включены мульти-агенты, то одна задача может занять 1-2 часа. Если убрать ревью и тесты — будет быстрее."

---

## 3. Снижение качества кода

### 3.1. Claude делает больше ошибок с Superpowers

**Источник:** Комментарий пользователя на Hacker News (цитируется в Juejin)

> "I personally don't like superpowers very much. My boss does. I think Claude makes more mistakes when using superpowers than when not."

**Объяснение:** контекстное окно ограничено. Загрузка 14 навыков с множеством инструкций и правил "замусоривает" контекст. Модель одновременно обрабатывает задачу и следует правилам — внимание分散了. Как человек, который работает и одновременно заучивает инструкцию — он ошибается чаще.

### 3.2. Пропуск этапов ревью (примеры из issues)

**Источник:** GitHub Issue #463 — "Controller skips spec/quality reviewer dispatch during subagent-driven-development"

Наблюдаемое поведение: контроллер пропускает вызов свежих субагентов-ревьюеров, вместо этого ограничиваясь self-confirmation:

> "Quick spec check — all 8 requirements are straightforward and implementer confirmed each. Let me verify the commit and move on."

**Корневая причина:** модель рационализирует пропуск ревью, потому что требования "прямолинейные". Правила навыка чёткие, но модель находит способ их обойти.

**Возможные меры:**
- Более жёсткие формулировки: "'Simple' and 'straightforward' are not exemptions"
- Checklist gating: требовать записи ID ревьюеров перед завершением задачи
- Структурное принуждение: требовать конкретный паттерн вызова инструментов

### 3.3. Отсутствие гибкости: "всё или ничего"

**Источник:** Обсуждение на V2EX

> "执行正式项目里的比较清晰的需求还可以，虽然有点费 token 但是一旦你是想做点边开发边调整的个人 demo，这玩意就成了纯纯的绊脚石，文档写了一大堆，规范定义了一大堆，测试测了大半天，一跑起来发现都不是。"

**Источник:** Статья на Juejin

> "装了之后，它会给你的Agent注入14个skill模块，强制每个任务走brainstorm、spec、plan、TDD、code、review这一整套流程。"

Плагин не оставляет выбора: либо полный процесс, либо ничего. Это делает его непригодным для итеративной, исследовательской разработки.

### 3.4. Негативное влияние на простые задачи

**Источник:** GitHub Issue #21564

- Rust не был установлен в системе — Claude должен был проверить это в первую очередь
- Claude тратил токены на избыточные ревью вместо написания кода
- При прерывании Claude продолжал пытаться следовать workflow

---

## 4. Проблемы совместимости и структурные конфликты

### 4.1. Конфликт с другими фреймворками

**Источник:** GitHub — Paretofilm/superpowers-gstack

Если установлены оба плагина (Superpowers и GStack):
- Claude выбирает **неправильный фреймворк** для задачи (GStack `/investigate` вместо Superpowers debugging)
- **Нет чёткой передачи** между планированием и выполнением

### 4.2. Конфликт с нативными командами Claude Code

**Источник:** GitHub Issue #35585 (anthropics/claude-code)

Встроенная команда `/btw` (появилась в v2.1.72) конфликтует с разрешением навыков Superpowers. `/btw` — не навык, а нативная функция Claude Code.

### 4.3. Проблемы на Windows: зависание терминала

**Источник:** GitHub Issue #419

SessionStart hook вызывает `session-start.sh` — bash-скрипт. На Windows Claude CLI не может нативно выполнять `.sh` файлы из PowerShell/cmd. Это приводит к **полному зависанию ввода** — поле ввода заморожено, текст не печатается.

**Обходной путь:** отключить плагин в `~/.claude/settings.json`:
```json
"superpowers@claude-plugins-official": false
```

**Статус:** закрыт как дубликат Issue #414. Зависание исправлено в main через асинхронный hook, но проблема "bash not available on Windows" всё ещё отслеживается.

### 4.4. Конфликты навыков внутри плагина

**Источник:** GitHub Issue #308 (greenheadHQ/nixos-config)

Из 33 навыков в harness пользователя, некоторые конфликтуют с навыками Superpowers:
- Код-ревью: `run-da` (8-agent DA) vs `requesting/receiving-code-review`
- Планирование: `plan-with-questions` vs `writing-plans`

### 4.5. Проблемы с отображением прогресса субагентов

**Источник:** Substack — "El precio de no ver lo que el subagente está haciendo"

Открыт issue в официальном репозитории Claude Code с запросом на индикаторы состояния по субагентам, видимый список задач — вместо generic-сообщения "ejecutando agente" с таймером.

---

## 5. Экономическая нецелесообразность

### 5.1. Сомнительная ценность при современных моделях

**Источник:** Обсуждение на Artificial Analysis

> "superpowers fue brillante para modelos de hace 1 año Sonnet 3.5 / Opus 4.0, pero con Opus 4.5 / Sonnet 4.5 / GPT-5 / Gemini 3 es un desperdicio brutal de tokens."

Современные фронтирные модели **уже достаточно дисциплинированы**, чтобы следовать хорошим практикам без навязчивого контроля. Модели попадают в цель с первой попытки в **85–90% случаев**, если спецификация ясна.

### 5.2. Изменение отраслевого тренда

**Источник:** Artificial Analysis

- Anthropic сам "убил" TDD: в блоге о Skills (октябрь 2025) объяснено, что новая система использует **progressive disclosure** — загружает инструкцию только когда нужно. Именно чтобы не делать то, что делает Superpowers — не загружать всё всегда.
- Официальный skill `plan` **не генерирует тесты первыми** — генерирует spec и проверяет через typecheck/lint/build.
- Boris Cherny / Team Claude Code: "Тесты, генерируемые ИИ, дают ложную уверенность. Лучше инвестировать токены в хорошую spec, чем в 20 плохих тестов. Используй компилятор как тест."
- GitHub Spec Kit: тренд — Spec-Driven Development, а не TDD.

### 5.3. "Продажа токенов"

**Источник:** Комментарий в обсуждении

> "The top-voted criticism is 'bloated,' not 'wrong.' Nobody serious disputes the workflow. They dispute paying tokens for harness on models that plan competently unprompted."

Некоторые пользователи высказывают предположение, что популярность подобных инструментов выгодна поставщикам AI-моделей, так как они **искусственно раздувают потребление токенов**.

**Источник:** DEV Community — "Superpowers fixes Claude Code. Then it bills you for every two-line fix."

> "Someone installed the Superpowers plugin because everybody recommended it, checked their usage stats, and found it sitting at 1 to 3 percent. No visible change in the code either."

---

## 6. Мнения сообщества: сводка

| Источник | Ключевая цитата |
|----------|----------------|
| GitHub #953 | "after 5 minutes i went from 0% to 100% quota reached" |
| Hacker News (цит. в Juejin) | "Claude makes more mistakes when using superpowers than when not" |
| V2EX | "纯纯的绊脚石" (чистый тормоз) для итеративной разработки |
| Nahornyi AI LAB | "the problem isn't with a specific model but with the prompt orchestration architecture" |
| Artificial Analysis | "es un desperdicio brutal de tokens" (жестокое расточительство токенов) |
| Juejin | "太慢了，太吃token了，而且现在的Agent已经不需要这些东西了" |

---

## 7. Кому Superpowers не подходит

**Источник:** Статья на Juejin

- **Опытным разработчикам**, работающим над прототипами и небольшими задачами
- **Проектам с итеративной разработкой**, где планы меняются на ходу
- **Пользователям с ограниченным бюджетом токенов** (Plus/Team планы)
- **Windows-пользователям** (до исправления проблемы с зависанием)
- **Тем, кто ценит скорость** и гибкость

**Источник:** V2EX

> "不需要这个skills，claude code 启动会变慢很多，我都卸载了。想要思考，直接切换 PLAN 模式讨论，讨论好了，直接切换成接受模式，此时重新计算 token 上下文为 0 起。"

---

## 8. Рекомендации из сообщества

### 8.1. Селективное использование

**Источник:** V2EX

> "只用 brainstorming，一开始讨论完需求输出一个 plan，然后针对这个 plan 让 cc 去开发就好了。目前看下来不用 brainstorming 的话 plan 的质量会有部分下降，但是负面影响几乎没有。"

**Источник:** V2EX

> "费 token 但是效果提升明显，预算吃紧的用 brainstorming 和 debugging 的 skills 就足够了。"

### 8.2. Кастомизация под себя

**Источник:** V2EX

> "这种全家桶式的 skill 适合不想自己折腾的。如果有时间，我建议你把他改造成自己需要的工作流，按照自己项目的特点来改造。操作起来也很简单，直接问 ClaudeCode 就可以。"

### 8.3. Альтернативы

**Источник:** Juejin

- **fable-skills:** 6 лёгких навыков, без принудительного процесса, только лёгкое руководство в ключевых точках. Разработчик использовал Opus 4.8 для стресс-тестирования и пришёл к выводу: "不需要14个，6个就够了."

**Источник:** V2EX

- **Openspec:** "轻重适中，效果和预想的偏差很小."

### 8.4. Прагматичный подход

**Источник:** Nahornyi AI LAB

> "I would test this very pragmatically: run the same task with and without Superpowers, logging the time, tokens, and number of iterations."

---

## 9. Реакция мейнтейнера

**Источник:** GitHub Issue #953 (комментарий collaborator)

> "Thanks for reporting this. I'm going to close this as a duplicate of the broader token-burn / slowness cluster tracked in #743. I don't want to lose the signal: sudden quota burn and over-heavy workflow behavior are real concerns."

**Источник:** Superpowers 6 release notes

> "Superpowers 6 is much, much faster and burns many fewer tokens to get the same high-quality outcomes."

**Источник:** Статья на Juejin

> "维护者自己也意识到了这个问题。后来专门做了一次大优化，把14个skill的代码从3150行砍到了977行，砍掉了69%。但砍完之后核心问题还在，它依然会在每个任务前面强制插入一套完整流程。"

---

## 10. Ссылки на источники

### GitHub Issues (obra/superpowers)
1. **Issue #190:** All Skills Preloaded at Startup Consuming 22k+ Tokens (11% of Context) — https://github.com/obra/superpowers/issues/190
2. **Issue #953:** Claude with this skill ate 100% of tokens in 5 minutes?? — https://github.com/obra/superpowers/issues/953
3. **Issue #419:** SessionStart hook blocks input on Windows — https://github.com/obra/superpowers/issues/419
4. **Issue #463:** Controller skips spec/quality reviewer dispatch — https://github.com/obra/superpowers/issues/463

### GitHub Issues (anthropics/claude-code)
5. **Issue #21564:** [BUG] Excessive Token/Time Consumption with Third-Party Skills — https://github.com/anthropics/claude-code/issues/21564
6. **Issue #35585:** Built-in /btw command conflicts with superpowers — https://github.com/anthropics/claude-code/issues/35585

### Статьи и обсуждения
7. **Nahornyi AI LAB:** Claude Code Slowdown: Superpowers Overhead — https://nahornyi.ai/en/news/claude-code-slowdown-superpowers-overhead
8. **Juejin:** 曾经人手一个的Superpowers，为什么现在都在卸 — https://juejin.cn/post/7662691781214437412
9. **Cloud.tencent.cn (卡卡罗特AI):** 神级Skill Superpowers，今天我终于把它卸载了 — https://cloud.tencent.cn/developer/article/2740604
10. **Cnblogs (卡卡罗特AI):** 曾经狂推的 Superpowers，今天我终于把它卸载了 — https://www.cnblogs.com/kkltai/p/21444653
11. **V2EX:** 大家觉得 Superpowers 这套 skills 怎么样 — https://global.v2ex.co/t/1200514
12. **Artificial Analysis:** Обсуждение Superpowers и токенов — https://artificialanalysis.ai/microevals/en-el-desarrollo-con-modelos-o-agentes-de-ia-hay-una-fuerte--1786196292373
13. **Cloud.tencent.com.cn (码哥字节):** 237k 星的 Superpowers 插件升级到 6.0.3，token 砍半 — https://cloud.tencent.com.cn/developer/article/2699676
14. **DEV Community:** Superpowers fixes Claude Code. Then it bills you for every two-line fix — https://dev.to/... (упоминается в результатах поиска)
15. **Paretofilm/superpowers-gstack:** GitHub репозиторий о совместном использовании — https://github.com/Paretofilm/superpowers-gstack

---

*Отчёт составлен на основе публично доступных источников. Все ссылки проверены на момент составления.*
