Для omp сервер Context7 добавляется блоком в `mcpServers` — ниже два готовых варианта конфигурации (remote HTTP и локальный stdio), команды проверки и типовые причины сбоев.

## Формат конфигурации omp

omp читает MCP-серверы из файлов с полем `mcpServers`, транспорт указывается полем `type` (`stdio` — по умолчанию для `command`, `http` / `sse` — для `url`). Где хранить:

| Скоуп | Путь |
|---|---|
| Проект (для всего репозитория) | `.omp/mcp.json` |
| Пользователь (личные серверы) | `~/.omp/agent/mcp.json` |
| Профиль | `~/.omp/profiles/<name>/agent/mcp.json` |
| Совместимый fallback | `mcp.json` / `.mcp.json` в корне проекта |

Полный справочник полей и схему см. в [docs MCP omp](https://omp.sh/docs/mcp); `$schema` — `https://raw.githubusercontent.com/can1357/oh-my-pi/main/packages/coding-agent/src/config/mcp-schema.json`【turn0fetch0】.

## Вариант 1 — Remote HTTP (рекомендуется)

```json
{
  "$schema": "https://raw.githubusercontent.com/can1357/oh-my-pi/main/packages/coding-agent/src/config/mcp-schema.json",
  "mcpServers": {
    "context7": {
      "type": "http",
      "url": "https://mcp.context7.com/mcp",
      "headers": {
        "Authorization": "Bearer ${CONTEXT7_API_KEY}"
      }
    }
  }
}
```

Ключ берётся из личного кабинета `context7.com/dashboard` — он поднимает rate-limit и даёт доступ к приватным источникам; без ключа endpoint тоже работает, но с публичными лимитами. omp разворачивает `${VAR}` и `${VAR:-default}` из переменных окружения при загрузке файла — сам ключ в конфиг не вписываем【turn0fetch0】【turn3fetch0】.

## Вариант 2 — Локальный stdio (npx)

```json
{
  "$schema": "https://raw.githubusercontent.com/can1357/oh-my-pi/main/packages/coding-agent/src/config/mcp-schema.json",
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp"],
      "env": {
        "CONTEXT7_API_KEY": "${CONTEXT7_API_KEY}"
      }
    }
  }
}
```

Требуется Node.js ≥ 20.18.1. Ключ можно передать и флагом: `"args": ["-y", "@upstash/context7-mcp", "--api-key", "YOUR_API_KEY"]` (флаг имеет приоритет над env-переменной)【turn1fetch0】【turn3fetch0】.

## Проверка

После создания файла внутри omp:

```
/mcp reload          # перечитать конфиги
/mcp list            # убедиться, что context7 в списке и подключён
/mcp test context7   # тест: версия сервера + число тулов
```

Успешный тест показывает имя, версию, количество инструментов и до 10 имён тулов. Инструменты видны в `/tools` как `mcp__context7_…`. Затем в запросах достаточно писать обычным языком или добавлять фразу `use context7`【turn0fetch0】【turn3fetch0】.

## Типовые ошибки

- **`stdio server requires "command"`** — omp считает сервер локальным, потому что не задан `type`. Для remote-варианта обязательно `"type": "http"`; `url` без `type` не выбирает транспорт автоматически【turn0fetch0】.
- **401 / 403** — env-переменная `CONTEXT7_API_KEY` не установлена в окружении, из которого запущен omp, либо рядом остался старый явный `Authorization`-заголовок, перекрывающий авторизацию. Проверьте значение переменной и перезапустите omp; для OAuth-серверов дополнительно есть `/mcp reauth <name>`【turn0fetch0】.
- **Таймаут при подключении** — по умолчанию 30 с на сервер. Увеличьте полем `"timeout": 60000` в описании сервера (или переменной `OMP_MCP_TIMEOUT_MS` для процесса) и повторите `/mcp reload`【turn0fetch0】.
- **Сервер не появляется в `/mcp list`** — проверьте, что JSON валиден и есть верхнеуровневый `mcpServers`, что имя не дублируется в более приоритетном источнике, и что проектная конфигурация не отключена (`mcp.enableProjectConfig`). Напоминание: omp также автоимпортирует серверы из Claude Code, Cursor, VS Code, Codex и т.д. — дубликат из них перекрывается вашим определением【turn0fetch0】.
- **Не подключился после правки файла** — используйте `/mcp reconnect context7` для разового переподключения без полной переоценки источников【turn0fetch0】.


---
---

Для настройки **Context7** в **OMP (Oh My Pi)** необходимо подключить его как удаленный MCP-сервер, используя транспорт `http`. Context7 работает и без регистрации (анонимно), но для повышения лимитов запросов рекомендуется получить бесплатный API-ключ на [context7.com/dashboard](https://context7.com/dashboard).

Настроить подключение можно двумя способами:

### Способ 1: Через слэш-команду (быстрый)
Выполните следующую команду прямо в интерфейсе OMP:

```bash
/mcp add context7 --url https://mcp.context7.com/mcp --transport http
```
*Если вы хотите использовать API-ключ, добавьте его через флаг `--token`:*
```bash
/mcp add context7 --url https://mcp.context7.com/mcp --transport http --token ВАШ_API_КЛЮЧ
```

### Способ 2: Через файл `.omp/mcp.json`
Создайте или отредактируйте файл `.omp/mcp.json` в корне вашего проекта и добавьте следующий блок:

```json
{
  "mcpServers": {
    "context7": {
      "type": "http",
      "url": "https://mcp.context7.com/mcp",
      "headers": {
        "Authorization": "Bearer ВАШ_API_КЛЮЧ"
      }
    }
  }
}
```
> 💡 **Безопасность ключа:** OMP умеет подставлять переменные окружения. Чтобы не хранить токен в файле в открытом виде, задайте переменную в терминале (например, `CONTEXT7_API_KEY`), а в конфиге используйте синтаксис: `"Authorization": "Bearer ${CONTEXT7_API_KEY}"`.

---

### Применение и проверка
1. Если вы редактировали JSON-файл вручную, обязательно перезагрузите конфигурацию серверов:
   ```bash
   /mcp reload
   ```
2. Убедитесь, что сервер успешно подключен и инструменты доступны:
   ```bash
   /mcp list
   /mcp test context7
   ```

### Как использовать в промптах
После настройки OMP сможет использовать инструменты `resolve-library-id` и `query-docs` для подтягивания самой свежей документации. Чтобы гарантированно задействовать Context7, добавляйте в свои запросы следующие триггеры:
* `use context7` — для общего поиска документации по запросу.
* `use library /vercel/next.js` — для явного указания конкретной библиотеки (и её версии, если нужно).
