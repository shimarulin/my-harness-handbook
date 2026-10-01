# API Specifications

Опциональный модуль для формальных контрактов между системами.

---

## Что такое API Specification

**API Spec** — формальное описание контракта для взаимодействия между системами:
- Формат запросов и ответов
- Типы данных
- Аутентификация и авторизация
- Обработка ошибок
- Версионирование

**Это НЕ**:
- Реализация (это код)
- Требования (это Requirements/EARS)
- Документация для пользователей (хотя может генерировать её)

**Это**:
- Контракт между системами
- Вход для кодогенерации
- Основа для контрактного тестирования
- Источник документации

---

## Форматы

### 1. OpenAPI 3.x (REST APIs)

**Для**: HTTP REST APIs

**Официальный сайт**: [openapis.org](https://www.openapis.org)

**Пример**:
```yaml
openapi: 3.0.3
info:
  title: Export API
  version: 1.0.0
  description: Data export service API

servers:
  - url: https://api.example.com/v1

paths:
  /exports:
    post:
      summary: Request data export
      operationId: createExport
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/ExportRequest'
      responses:
        '202':
          description: Export accepted
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ExportResponse'
        '400':
          description: Invalid request
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Error'
        '429':
          description: Rate limit exceeded

  /exports/{id}:
    get:
      summary: Get export status
      operationId: getExportStatus
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: string
            format: uuid
      responses:
        '200':
          description: Export status
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ExportStatus'

components:
  schemas:
    ExportRequest:
      type: object
      required:
        - format
      properties:
        format:
          type: string
          enum: [csv, json]
        filters:
          type: object
          properties:
            date_from:
              type: string
              format: date
            date_to:
              type: string
              format: date

    ExportResponse:
      type: object
      properties:
        export_id:
          type: string
          format: uuid
        status:
          type: string
          enum: [pending, processing, completed, failed]
        status_url:
          type: string

    Error:
      type: object
      properties:
        code:
          type: string
        message:
          type: string

  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT

security:
  - bearerAuth: []
```

### 2. AsyncAPI (Event-Driven APIs)

**Для**: Событийно-ориентированные системы (message queues, streams)

**Официальный сайт**: [asyncapi.com](https://www.asyncapi.com)

**Пример**:
```yaml
asyncapi: 2.6.0
info:
  title: Export Events
  version: 1.0.0
  description: Events for data export workflow

servers:
  production:
    url: redis://redis.example.com:6379
    protocol: redis

channels:
  export.requested:
    description: Export request submitted
    publish:
      operationId: publishExportRequested
      message:
        $ref: '#/components/messages/ExportRequested'
    subscribe:
      operationId: receiveExportRequested
      message:
        $ref: '#/components/messages/ExportRequested'

  export.completed:
    description: Export file ready
    subscribe:
      operationId: receiveExportCompleted
      message:
        $ref: '#/components/messages/ExportCompleted'

  export.failed:
    description: Export failed
    subscribe:
      operationId: receiveExportFailed
      message:
        $ref: '#/components/messages/ExportFailed'

components:
  messages:
    ExportRequested:
      payload:
        type: object
        required: [export_id, user_id, format]
        properties:
          export_id:
            type: string
            format: uuid
          user_id:
            type: string
          format:
            type: string
            enum: [csv, json]
          filters:
            type: object

    ExportCompleted:
      payload:
        type: object
        required: [export_id, download_url]
        properties:
          export_id:
            type: string
            format: uuid
          download_url:
            type: string
            format: uri
          expires_at:
            type: string
            format: date-time

    ExportFailed:
      payload:
        type: object
        required: [export_id, error_code, error_message]
        properties:
          export_id:
            type: string
            format: uuid
          error_code:
            type: string
          error_message:
            type: string
```

### 3. GraphQL SDL

**Для**: GraphQL APIs

**Пример**:
```graphql
type Query {
  """Get export status by ID"""
  export(id: ID!): Export
}

type Mutation {
  """Request a new data export"""
  createExport(input: ExportInput!): ExportResponse!
}

type Export {
  id: ID!
  status: ExportStatus!
  downloadUrl: String
  expiresAt: DateTime
  createdAt: DateTime!
}

input ExportInput {
  format: ExportFormat!
  filters: ExportFilters
}

enum ExportFormat {
  CSV
  JSON
}

enum ExportStatus {
  PENDING
  PROCESSING
  COMPLETED
  FAILED
}

input ExportFilters {
  dateFrom: Date
  dateTo: Date
}

type ExportResponse {
  exportId: ID!
  status: ExportStatus!
  statusUrl: String!
}

scalar DateTime
scalar Date
```

### 4. gRPC / Protocol Buffers

**Для**: Высокопроизводительные внутренние сервисы

**Пример**:
```protobuf
syntax = "proto3";

package export.v1;

service ExportService {
  rpc CreateExport(CreateExportRequest) returns (CreateExportResponse);
  rpc GetExportStatus(GetExportStatusRequest) returns (GetExportStatusResponse);
}

message CreateExportRequest {
  ExportFormat format = 1;
  ExportFilters filters = 2;
}

enum ExportFormat {
  EXPORT_FORMAT_UNSPECIFIED = 0;
  CSV = 1;
  JSON = 2;
}

message ExportFilters {
  string date_from = 1;  // ISO 8601 date
  string date_to = 2;    // ISO 8601 date
}

message CreateExportResponse {
  string export_id = 1;
  ExportStatus status = 2;
  string status_url = 3;
}

enum ExportStatus {
  EXPORT_STATUS_UNSPECIFIED = 0;
  PENDING = 1;
  PROCESSING = 2;
  COMPLETED = 3;
  FAILED = 4;
}

message GetExportStatusRequest {
  string export_id = 1;
}

message GetExportStatusResponse {
  string export_id = 1;
  ExportStatus status = 2;
  string download_url = 3;
  string expires_at = 4;  // RFC 3339
}
```

---

## Инструменты

### Проектирование

| Инструмент | Назначение | Ссылка |
|-----------|-----------|--------|
| **Stoplight** | Visual OpenAPI editor + governance | [stoplight.io](https://stoplight.io) |
| **Swagger Editor** | Онлайн редактор | [editor.swagger.io](https://editor.swagger.io) |
| **Postman** | API design + testing + docs | [postman.com](https://www.postman.com) |
| **Insomnia** | Design + testing | [insomnia.rest](https://insomnia.rest) |

### Валидация

| Инструмент | Назначение | Ссылка |
|-----------|-----------|--------|
| **Spectral** | Linting for OpenAPI/AsyncAPI | [stoplight.io/open-source/spectral](https://stoplight.io/open-source/spectral) |
| **openapi-lint** | Валидация структуры | — |
| **AsyncAPI Generator** | Генерация из AsyncAPI | [asyncapi.com/tools](https://www.asyncapi.com/tools) |

### Кодо-генерация

| Инструмент | Назначение | Ссылка |
|-----------|-----------|--------|
| **OpenAPI Generator** | 40+ языков | [openapi-generator.tech](https://openapi-generator.tech) |
| **Specmatic** | Contract testing | [specmatic.io](https://specmatic.io) |
| **Postman Collection Runner** | Тесты из спецификации | — |

### Документация

| Инструмент | Назначение | Ссылка |
|-----------|-----------|--------|
| **Redoc** | Красивая документация | [redocly.com/redoc](https://redocly.com/redoc) |
| **Swagger UI** | Интерактивная документация | — |
| **Stoplight Elements** | React components | [elements.stoplight.io](https://elements.stoplight.io) |

---

## Workflow: Requirements → API Spec → Code

```
Requirements (EARS)
    ↓
Approach (Technical Design)
    ↓
API Specification (OpenAPI/AsyncAPI)
    ↓
┌─────────────────────────────────────┐
│ Code Generation (client + server)  │
│ Mock Server (for testing)          │
│ Documentation (auto-generated)     │
│ Contract Tests                     │
└─────────────────────────────────────┘
```

### Пример: EARS → OpenAPI

```
EARS:
REQ-EXP-004: When a user requests export, the system shall acknowledge 
the request within 2 seconds and return an export ID

    ↓

OpenAPI:
POST /exports
  requestBody: { format: string, filters: object }
  responses:
    202: { export_id: uuid, status: "pending" }
    400: { error: "Invalid format" }
```

---

## AI-Agent Integration

### Prompt: Генерация OpenAPI из Approach

```
Based on this technical approach, generate OpenAPI 3.0 specification:

Approach:
[paste approach.md content]

Requirements:
[paste requirements.md content]

Generate:
1. Complete OpenAPI spec with all paths
2. Request/response schemas
3. Error responses
4. Security schemes
5. Examples for each endpoint
```

### Prompt: Генерация тестов из API Spec

```
Based on this OpenAPI spec, generate:
1. Contract tests (validate request/response schemas)
2. Integration tests for each endpoint
3. Error handling tests

OpenAPI:
[paste spec]

Tech stack: Python + pytest + httpx
```

---

## Связь с другими модулями

### ← Requirements (вход)
**Как**: Требования определяют что должен делать API

### ← Approach (вход)
**Как**: Архитектурные решения определяют структуру API

### → Implementation (выход)
**Как**: Код генерируется или пишется на основе спецификации

### → BDD (выход)
**Как**: Сценарии могут проверять соответствие контрактам

### → Tests (выход)
**Как**: Контрактные тесты проверяют соответствие спецификации

---

## Анти-паттерны

### ❌ Код без спецификации
**Проблема**: Сначала код, потом пытаемся документировать
**Решение**: Спецификация до кода

### ❌ Спецификация без версионирования
**Проблема**: Изменения ломают клиентов
**Решение**: Версионирование, breaking changes отдельно

### ❌ Неполные спецификации
**Проблема**: Нет описания ошибок, нет примеров
**Решение**: Каждая спецификация включает ошибки и примеры

---

## References

- [OpenAPI Specification](https://www.openapis.org)
- [AsyncAPI Specification](https://www.asyncapi.com)
- [GraphQL Specification](https://graphql.github.io/graphql-spec/)
- [Protocol Buffers](https://protobuf.dev)
- [Stoplight](https://stoplight.io)
- [Previous: BDD](./bdd.md)
- [Back to Modules Index](./README.md)
