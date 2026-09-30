# Критика SDD и AI-процессов: синтез (основа главы 4 гайда)

| Параметр | Значение |
|---|---|
| Статус | draft |
| Обновлено | 2026-09-30 (корпус критики: 04.2026–09.2026; область меняется быстро — дополнять в фазе 6) |

## Что это

Синтез трёх независимых исследований критики Spec-Driven Development и AI-ассистированных процессов (q1, g1, d1 — всего ~230 KB, 60+ первоисточников). Не «за» и не «против» SDD: карта того, что реально ломается, почему, и какие принципы выведены из этих поломок. Принципы вынесены в `research/kb/principles/`; здесь — нарратив и доказательная база.

## 1. Главный тезис корпуса

SDD-инструменты решают задачу «точных инструкций агенту», которая быстро устаревает по мере роста моделей, но не решают главную проблему: **расхождение спеки и кода — дефолтный исход при отсутствии блокирующего машинного enforcement**. Спека на естественном языке недоопределена по построению: машина молча заполняет пробелы, а обратная связь асимметрична (аксиома Русакова) — доверие к спеке растёт быстрее её определяющей силы.

Вывод корпуса един во всех трёх исследованиях: универсальные принципы важнее конкретных инструментов; процесс проектируют сами, а не принимают «поставляемый с инструментом».

## 2. Что ломается: карта проблем

### 2.1. Спек-дрейф (все инструменты)

«If nothing blocks on spec/code divergence, divergence is the default outcome over time» (CodeMySpec). OpenSpec: синхронизация — конвенция, не принуждение; HN-практика: «it just keeps drifting and drifting until you have duplication and contradictions across specs… maintaining the main specs is not worth it». Spec Kit: конституция не обновляется автоматически при изменении кода. BMAD: тяжёлый артефактный набор устаревает быстрее, чем его ревьюят. Историческая аналогия (Dhwtj): «Памяти усопшего Rational Rose… Модель и код всегда расходятся»; судьба SDD решится появлением дешёвого машинного enforcement, не качеством спек.

### 2.2. Advisory verification вместо gate (OpenSpec)

`openspec validate` — только структура; `/opsx:verify` не блокирует archive; `archive --no-validate` отменяет проверку. «Контракт подписан, но исполнение — на совести агента» — нет enforcement к tasks.md: агент может пропустить тесты, изменить лишние файлы. Issue #194: агент обходит проверку флагом `--skip-specs`. → принцип `invariants-and-gates.md`.

### 2.3. Плоскость и масштабирование (OpenSpec)

Gromilo: «слишком плоский… для чего-то маленького, что ты можешь полностью загрузить в голову. Очень быстро получил миллион папочек со спеками, которые хз как организовывать». Мульти-репо: фича фронт+бэк в разных репо — где живёт спека? Issue #725 (design-review, не закрыт) + кластер #662/#594/#435/#581/#697. Stores (beta) — «костыль, не решает» (nihil-pro). Qian: «Using it got way too complicated» — миграция к AIDLC.

### 2.4. Требования — upstream от репозитория (организационный предел)

Кейс Talk Think Do: 84% AI-authored code → отказ через 2 месяца. «Requirements work is not just an engineering activity. Discovery, refinement, scope conversations, and stakeholder alignment all sit upstream of the repository» — репозиторий не workspace для BA, delivery, QA, клиента; спеки в репо скрывали scope/cost/variance. → `process-over-tool.md` (место артефактов).

### 2.5. Экономика под вопросом

Ran Isenberg: BMAD Full — 6 дней/$200 против OpenSpec — 1 день/$70 на comparable задаче. Кейс dev.to (редизайн UI): OpenSpec+GPT-5.3 Codex — 2 часа, «почти идентично оригиналу»; простой Instructions.md — быстрее, дешевле, легче итерировать. Вывод кейса: «будущее AI-assisted development — не тяжёлые фреймворки, а более лёгкие workflow с лучшими инструкциями». «Я не хочу, чтобы AI тратил больше времени на переписывание спецификаций, чем на написание кода»; риск «great specs — no MVP».

### 2.6. Waterfall в Markdown

Scott Logic: Spec Kit «в 10 раз медленнее ожиданий», «reinvented waterfall». Разработчик после 30 дней: «too opinionated for established teams, slow feedback cycle that feels waterfall-like, heavy context window usage». «Fine-tuning specifications is a nightmare». «SpecKit creates the illusion of work, generating a bunch of files». Артефактная тяжесть: 8 файлов на один spec (Birgitta Böckeler: для трёх-поинтовой истории неоправданно). Iteration = регенерация: изменение направления — re-run команд, отревьюенный план заменяется целиком без diff.

### 2.7. Провал planning-first (Nadeem, «Plan Mode Is Dead»)

Постмортем Nuanced: планирование ≠ план; модели съели ценность план-артефактов снизу; никто не хочет читать AI-текст; waterfall-пайплайн против итеративного мышления. → `attention-economy.md`.

### 2.8. Феномены деградации (Шапиро) — инструменто-независимый слой

Умолчание, дрейф, эрозия, наплыв; зазор творчества; асимметрия обратной связи; «модель проверяет модель»; недетерминизм. Полный разбор: `../principles/ai-degradation-phenomena.md`. Контекстная деградация (Chesbrough): порог 50–60% окна.

### 2.9. Multi-agent ловушки

BMAD: «process multiplier, not process creator» — без существующих процессов воспроизводит хаос на 19 агентах; pipeline хорош настолько, насколько слабейший handoff (незадокументированное допущение Architect'а доезжает до production). «The 19-Agent Trap»: 19 system prompts конкурируют за внимание в одном окне. GSD: автономный оркестратор — «My job is to be helped, not replaced» (Norton); drift downstream; токен-overhead 4:1; архивирован 2026-06-26. Superpowers: skills инструктируют, не гарантируют («not a substitute for repository tests, permissions, or human review»).

### 2.10. Project health и vendor-риски

Bus factor: OpenSpec = 1 («You're betting on these teams as much as these tools» — Isenberg). Spec Kit: 533 open issues / 36.8% close; upgrade затирает файлы кастомизации. Vendor-lock 4 форм: Kiro (лицензионный), Tessl (знаниевый), Antigravity (экосистемный), проприетарные форматы (форматный). → `process-over-tool.md`.

## 3. Что работает (подтверждённые эффекты)

- OpenSpec: переделки кода −~1/3 после трёхфазного workflow; `verify` выявляет проблемы в ~1/3 случаев; «cleanest delta model in this category»; change ~250 строк против ~800 у тяжёлых тулкитов. «Spec Kit is the thorough one, OpenSpec is the one you'll still be using in week three».
- Spec Kit: constitution как shared contract для распределённых команд; артефактная цепочка лучше чат-транскрипта для нового агента; мультидисциплинарная коллаборация (product оспаривает user story до engineering review).
- BMAD: adversarial code review «поймал вещи, которые standard review бы пропустил»; самое здоровое сообщество (94.3% issue close rate).
- Superpowers: behavioral discipline (TDD, subagent review) без artifact-heavy процесса.
- Общий вердикт Isenberg (13 dimensions): OpenSpec 4.00 > BMAD Quick 3.74 > BMAD Full 3.65 > Spec Kit 2.77.

## 4. Принципы, выведенные из критики (→ kb/principles/)

| Принцип | Суть | Ключевая атрибуция |
|---|---|---|
| `cheapest-form.md` | Требование → самая дешёвая удерживающая форма (тип/контракт/PBT/пример/ADR); проза — только для дорогоформализуемого; verification ≠ validation (Бём) | Dhwtj, Шапиро, Boehm |
| `invariants-and-gates.md` | Явные инварианты с rationale; блокирующие машинные gate, вне досягаемости агента; «конституция — не конфиг» | Gromilo, EPAM case, Davenport, issue #194 |
| `attention-economy.md` | Ограничивать внимание человека, не объём артефактов; масштаб процесса = f(сложность, цена ошибки); планирование ≠ план | Шапиро, Nadeem, Chesbrough |
| `process-over-tool.md` | Проектировать процесс самим; оборачивать инструмент в абстракцию; комбинировать; место артефактов — по доступности ролям; план миграции | Isenberg, Talk Think Do, Norton |
| `ai-degradation-phenomena.md` | Теоретическая рамка: 4 феномена, зазор творчества, контрмеры (две версии, ведомость допущений, индексы, контроль перехода) | Шапиро, Русаков |

## 5. Открытые вопросы корпуса

1. Круг «модель проверяет модель» — размыкается только исполнением; что делать с непокрытым?
2. Неполнота ведомости допущений.
3. Полнота vs дешевизна формализации — нет общего ответа.
4. Verification vs validation на практике: где граница машинного?
5. Экономика спек при высокой неопределённости.
6. Ориентация человека при сотнях параллельных агентов («product-shaped hole»).
7. Мульти-репо спеки (кластер issues OpenSpec без решения).
8. Эмпирика по сжатым представлениям Шапиро отсутствует.

## Источники (ключевые; полные списки в статьях принципов)

- Шапиро А.: https://ashapiro.ru/writing/tpost/vm69r9cse1-fenomeni-kod-agentnoi-razrabotki-islabos и https://ashapiro.ru/writing/tpost/fe056iabb1-k-kontrmeram-ot-poteri-ustoichivosti-ii (2026-09-27)
- Nadeem A., «Plan Mode Is Dead»: https://www.aymannadeem.com/artificial/intelligence,/developer/tools/2026/09/24/plan-mode-is-dead.html (2026-09-24)
- Тред Хабра: https://habr.com/post/1085536/comments; перевод Nadeem: https://habr.com/ru/companies/haulmont/articles/1087664/
- Isenberg (Eretz Kdosha): https://ranthebuilder.cloud/blog/i-tested-three-spec-driven-ai-tools-here-s-my-honest-take/ (2026-04-13)
- Davenport, OpenSpec Explained: https://codemyspec.com/blog/openspec-explained (2026-06-03)
- Talk Think Do: https://talkthinkdo.com/ai-velocity-report/moving-away-from-openspec/ (2026-06-01)
- Torres Bermon: https://dev.to/willtorber (2026-04-23); Norton: https://dev.to/vtnorton (2026-06-15)
- Scott Logic: https://blog.scottlogic.com/2025-11-26/putting-spec-kit-through-its-paces-radical-idea-or-reinvented-waterfall.html
- Chesbrough: https://martinchesbrough.net/why-spec-driven-development-is-not-about-the-specs-7d3fdf52fac7 (2026-05-28)
- Thoughtworks Radar (OpenSpec, Assess): https://www.thoughtworks.com/zh-cn/radar/tools/openspec
- Входные материалы inbox: вся группа `documentation-process-criticism/` (q1×2, g1×2, d1×2)
