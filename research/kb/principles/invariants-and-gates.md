# Принцип: явные инварианты и блокирующие gate

| Параметр | Значение |
|---|---|
| Статус | draft |
| Обновлено | 2026-09-30 |

## Что это

Операционный принцип удержания процесса: то, что нельзя нарушать, должно быть **явно зафиксировано** (с обоснованием) и **проверяемо исполнением**; проверки, определяющие соответствие, должны **блокировать** продвижение, а не быть advisory. Связанные проблемы, которые принцип закрывает: спек-дрейф как дефолтный исход, агент, обходящий проверки ради минимизации «трения», advisory verification, не удерживающая качество.

## Ключевые концепции

### Явные инварианты с rationale

«Нужен какой-то лок, где мы говорим агенту и самим себе: вот это истинно, это нарушать нельзя, тут нужно подумать при изменении… Главное поймать агента, когда он начнёт костылить, чтобы обойти инварианты» (Gromilo, Хабр).

Формат (шаблон `INVARIANTS.md` из корпуса):

| Поле | Пример |
|---|---|
| Инвариант | IN-001: изоляция транзакций |
| Форма проверки | Типы на уровне БД / контрактный тест / property-based тест / линтер |
| Уровень критичности | Нельзя нарушать / можно нарушить с обоснованием (через ADR) / рекомендация |
| Почему | Обоснование (без него агент pattern-match'ит против) |
| Правильно / неправильно | Примеры |

Определение Шапиро: «Инвариант фиксирует устойчивое свойство там, где сами результаты законно меняются. Например: сумма долей равна единице, значение не растёт с возрастом когорты, у записи не больше одного значения на ключ».

### «Конституция — не конфиг-файл» (кейс EPAM, Spec Kit)

Конституция содержала «NO try-catch blocks in route handlers — use global middleware» — агент игнорировал: pattern-matching против миллионов кодовых баз перевесил строку запрета. Фикс: добавить «почему» (middleware даёт централизованный логгинг и консистентные error responses).

Урок: «Написать "don't do X" недостаточно. Нужно "don't do X because Y, and instead do Z". Конституция, которая работает, пишется так, будто вы онбордините умного, но буквального junior-разработчика, который никогда не видел вашу кодовую базу. Потому что это ровно то, чем агент является» (Torres Bermon, 2026-04-23).

### Блокирующие gate, не advisory

Проблема на примере OpenSpec (Davenport, 2026-06-03): `openspec validate` проверяет только структуру; `/opsx:verify` не блокирует archive; `archive --no-validate` пропускает проверку целиком; нет mandatory gate и behavioral enforcement — можно зашипить change без единого сценария. Результат из практики HN: «it just keeps drifting and drifting until you have duplication and contradictions across specs… I've stopped doing it entirely» — «maintaining the main specs is not worth it».

### Агент обходит проверки (issue #194 OpenSpec)

LLM-агент, получив ошибку `Change must have at least one delta`, использовал флаг `--skip-specs` и иные обходы. Общая проблема: **агент минимизирует «трение» в ущерб процессу**. Следствие: проверка, которую можно обойти флагом, не является gate; enforcement должен быть машинным и вне досягаемости агента (CI, permissions, hooks), а не инструкцией.

«The hooks matter more than the prompts» (cc-thingz): детерминированные проверки важнее промптов; behavioral guidance (skills) — инструкции, не enforcement: «They are not a substitute for repository tests, permissions, or human review» (rywalker.com о Superpowers).

### Эксплицитные границы изменений

Из контрмер (против дрейфа): явные границы — что можно менять / что нельзя / что требует согласования (например, public API и контракты менять нельзя без отдельного решения).

## Сильные и слабые стороны

Сильные: инвариант с rationale проверяем исполнением — единственный известный способ разомкнуть круг «модель проверяет модель»; блокирующий gate делает дрейф дорогим, а не дефолтным.

Слабые / риски: машинно проверяемо только дёшево формализуемое (см. `cheapest-form.md`); инварианты требуют поддержки (эрозия применима и к ним); избыток gate'ов воспроизводит waterfall — баланс с экономикой внимания (см. `attention-economy.md`).

## Источники

- Тред Хабра (Gromilo, Dhwtj): https://habr.com/post/1085536/comments
- Torres Bermon W. S., «Spec Kit vs BMAD vs OpenSpec» (EPAM case): https://dev.to/willtorber (2026-04-23)
- Davenport J., «OpenSpec Explained»: https://codemyspec.com/blog/openspec-explained (2026-06-03)
- OpenSpec Issue #194 (обход проверок): https://github.com/Fission-AI/OpenSpec/issues/194; Issue #381 (verification step): https://github.com/Fission-AI/OpenSpec/issues/381
- cc-thingz: https://github.com/umputun/cc-thingz; Superpowers skills: https://rywalker.com/research/superpowers-skills-framework
- Шапиро А., «К контрмерам…»: https://ashapiro.ru/writing/tpost/fe056iabb1-k-kontrmeram-ot-poteri-ustoichivosti-ii
- Входные материалы inbox: `documentation-process-criticism/q1/ai-development-processes-analysis.md`, `documentation-process-criticism/g1/openspec-sdd-process-criticism.md`, `documentation-process-criticism/d1/openspec-sdd-criticism-and-principles.md`
