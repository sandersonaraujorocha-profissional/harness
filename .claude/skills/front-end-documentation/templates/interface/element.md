# <element-id>

## About

- **Type:** <screen | global segment | local segment | sub-screen | component>
- **Parent:** [<parent-id>](../<folder>/<parent-id>.md)

<brief description>

## Layout

### <theme>

#### Horizontal

```text
+----------------------------------------------------------+
| <child-a>                                                |
+----------------------+-----------------------------------+
| <child-b>            | <child-c>                         |
|                      |                                   |
+----------------------+-----------------------------------+
```

| Element | X | Y | Width | Height |
|---|---|---|---|---|
| <child-a> | 0% | 0% | 100% | 10% |
| <child-b> | 0% | 10% | 30% | 90% |
| <child-c> | 30% | 10% | 70% | 90% |

#### Vertical

```text
+----------------------+
| <child-a>            |
+----------------------+
| <child-b>            |
+----------------------+
| <child-c>            |
|                      |
+----------------------+
```

| Element | X | Y | Width | Height |
|---|---|---|---|---|
| <child-a> | 0% | 0% | 100% | 8% |
| <child-b> | 0% | 8% | 100% | 22% |
| <child-c> | 0% | 30% | 100% | 70% |

## Children

| Element | Type | File |
|---|---|---|
| <child-a> | <type> | [<child-a>](../<folder>/<child-a>.md) |

## States

| State | When | Shown |
|---|---|---|
| loading | <instruction, storage key or state.<element-id>> | <what appears> |
| empty | <condition> | <what appears> |
| error | <condition> | <what appears> |
| no permission | <condition> | <what appears> |
| success | <condition> | <what appears> |

## Instructions

### I1 <name>

- **Type:** <navigation | request | screen update>
- **Trigger:** <user action or event>
- **Input**
  - **Source:** <field, storage key, state, route parameter or previous instruction>
  - **Structure:**

    | Field | Type | Required |
    |---|---|---|
    | <field> | <type> | <yes or no> |

- **Process:**
  1. <step>
- **Output**
  - **Destination:** <screen, element, storage key or API route>
  - **Structure:**

    | Field | Type |
    |---|---|
    | <field> | <type> |

## Validations

| Field | Rule | Message | DB reference |
|---|---|---|---|
| <field> | <rule> | <message> | [<table>.<column>](../../database/tables/<table>.md) |

## Business errors

- [E-01](../errors.md)
