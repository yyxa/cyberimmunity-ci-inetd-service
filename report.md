# Отчёт о выполнении задачи "Киберимунный ci-inetd сервис"

- [Отчёт о выполнении задачи "Киберимунный ci-inetd сервис"](#отчёт-о-выполнении-задачи-киберимунный-ci-inetd-сервис)
  - [Постановка задачи](#постановка-задачи)
    - [Опции](#опции)
  - [Известные ограничения и вводные условия](#известные-ограничения-и-вводные-условия)
    - [Контекст](#контекст)
    - [Цели и Предположения Безопасности (ЦПБ)](#цели-и-предположения-безопасности-цпб)
        - [Активы/ценности, ущербы и неприемлемые события](#активыценности-ущербы-и-неприемлемые-события)
        - [Цели безопасности](#цели-безопасности)
        - [Предположения безопасности](#предположения-безопасности)
  - [Описание системы](#описание-системы)
    - [Компоненты](#компоненты)
    - [Алгоритм работы решения](#алгоритм-работы-решения)
    - [Описание Сценариев (последовательности выполнения операций), при которых ЦБ могут нарушаться](#описание-сценариев-последовательности-выполнения-операций-при-которых-цб-могут-нарушаться)
    - [Политики безопасности](#политики-безопасности)
  - [Запуск приложения и тестов](#запуск-приложения-и-тестов)
    - [Запуск приложения](#запуск-приложения)
    - [Запуск тестов](#запуск-тестов)
    - [Ожидаемый результат](#ожидаемый-результат)

## Постановка задачи

1. Провести первичное моделирование угроз с использованием высокоуровневой архитектуры и потоковых диаграмм.
  Ожидаемый результат: в drawio файле диаграммы последовательности для каждого домена безопасности с анализом критичности для заданных целей безопасности. Формат диаграмм - plantuml + пояснения в самой диаграмме какие цели безопасности и каким образом нарушаются  (если применимо)
2. Спроектировать и проанализировать первичную политику архитектуры для системы с учётом заданных целей безопасности
  Ожидаемый результат: диаграмма в drawio файле в нотации политики архитектуры + таблица с обоснованием уровней доверия и сводным анализом доверенной кодовой базы
3. Переработать первоначальную архитектуру, оптимизировать доверенную кодовую базу
  Ожидаемый результат: переработанная диаграмма в drawio файле в нотации политики архитектуры + таблица с  описанием каждого компонента, обновлением диаграммы последовательности (реализация функциональных сценариев), обоснованием уровней доверия и сводным анализом доверенной кодовой базы
4. Реализовать прототип на языке Python или C++ применяя MILS и FLASK (изоляция доменов и контроль взаимодействия)
    Ожидаемый результат:
    - код: публичный проект в gitflic и github репозиториях c MIT лицензией. Код должен схематично реализовывать описанные базовые сценарии работы фермы. Реализация должна содержать монитор и политики безопасности. Политики безопасности должны обеспечивать реализацию предложенной в п. 3 политики архитектуры.
    - тесты: Должны быть написаны юнит-тесты для политик безопасности. Должны быть написаны автоматические сквозные тесты.
    - документация: репозиторий должен содержать README.md файл с описанием на русском языке шагов по запуску кода проекта. В папке docs должен находиться drawio файл с результатами выполнения пп. 1-3 (взять этот файл и добавить результаты на вкладку "Решение").

### Опции

---

1. использование jupyter блокнота для реализации решения допускается
2. использование docker контейнеров для запуска сущностей необязательно, но приветствуется
3. использование брокера сообщений и асинхронного IPC необязательно, но приветствуется
4. создание автоматических сквозных негативных тестов необязательно, но поощряется дополнительными CPI баллами
5. идеи по доработке постановки этой учебной задачи с целью повышения интереса к её изучению и решению приветствуются

## Известные ограничения и вводные условия

### Контекст

---

У владельца вычислительного комплекса для обработки пользовательских сетевых запросов требуется запускать обслуживающие программы (демоны). Обслуживающие программы бывают и большие, и маленькие. Если сразу запускать обслуживающие программы в ожидании запроса, то обслуживающие программы потребляют ресурсы вычислительного комплекса вхолостую когда запросов нет.

Владелец вычислительного комплекса, что ему нужна специальная, система которая будет ждать сетевой запрос и запускать соответствующих обработчиков запросов когда такой запрос поступит.

### Цели и Предположения Безопасности (ЦПБ)

---

#### Активы/ценности, ущербы и неприемлемые события

---

| Ценность | Негативное событие | Величина ущерба | Комментарий |
|----------|----------|----------|----------|
| 1. Критичные данные | Запуск неавторизованного сервиса для обработки критичных данных. | Высокий | Например по GDPR / обработки персональных данных и т.п. |
| 2. Доступность критичного сервиса | Критичный сервис не запущен и не может обрабатывать критичные данные | Высокий | Соглашение о доступности сервиса требует конкретного уровня реакции на запросы.|
| 3. Вычислительные ресурсы | Запущенные сервисы простаивают без дела потребляя ресурсы. | Средний | Финансовые потери. |
| 4. Критичные журналы работы сервиса | Утрата или искажение критичных данных | Средний | Ухудшения анализа происходящего с сервисами |

#### Цели безопасности

---

| Цель Безопасности | Комментарий |
|----------|----------|
| 1. При любых обстоятельствах входящие запросы для критичных сервисов обрабатываются только указанными в конфигурационном файле сервисами соответствующими этому запросу. | Защита ценности 1. |
| 2. ci-inetd делает всё от него зависящее чтобы запустить критичный сервис при пользовательском запросе. | Защита ценности 2.  |
| 3. Время простоя сервисов не превышает заданное. | Защита ценности 3.  |
| 4. При любых обстоятельствах критичные данные мониторинга сохраняют целостность и аутентичность | Защита ценности 4.  |

#### Предположения безопасности

---

1. ОС доверена (KasperskyOS)
2. Файл конфигурации доступен только для чтения

### Описание системы

---

### Компоненты

---

### Алгоритм работы решения

---

![1](https://cdn-0.plantuml.com/plantuml/png/ND1DJiCm4CNnlKynwfvHtU-oGC158ZETfgCudc0xS7rGh0WDw_zFR_5UImsvpcDqx_e1Jo_m5eKOdk71CQfpqsyLaYca2XkF4BKl6mW5nfrjEuHxeDhHWsdWt8otPe-Gk7vh7Zf9JUojE21a_fov_1iwM7P484rtwLizsdfQwasgQB8p9mlF28Npbn1tomqhErjs-ME3nBYgYrLN1CfIxTBL6hz5k0KUDPNM_TQvFkiy_NHQnRfD146qzrVC3o1vRy_dn1KD1N-015I4meNTa0OXfDX68SX8AK4K1YhQ9VZmoOwTNvZv8zuithtbCC6E8csykpFpthutOvdu8w-vadEksF4AwuATxkIoDR1gpA3J8nZ0tsJCfSPoIRpa3Q_b3JO_sBK67HzeUvGXy5Dz5qfaFO87Zs7YK_ugRr5zh6Xf7SHcFjRqAD_6jWPvOD3PYq7UewB980yCkWSmE8eCYi3WU2y61SHgDoaKWO8n1t0mMIHXeX5sBnQQdJTPc7YbOdwMCrnUSOd_ItRqP2WZ76nGMm_7ClAVV1-OoBy8_FzEvnizaWjUOIiJLBl1xGLuRbhFXoUntsQuMMikLYUNX2p7tpsmesVzUtsCwWaXI4ihWH6xf8zCjF43kotcYBGM0N0ZPpAcHwcAjPKsz8Y1bxUdss1crlvVQ1wgPcQ7hBoeStMxlaNgXfqoKMdyP5P96sUXBVWBbxoG2Q_alOe7Ea1AuQj4XymsMbeVfpqouvz0cBFRTjI3uMd_zEN34xLq3eHhPSGkCEWYhRDB4_yAfweqpKkun_wP8LZJdKRf32mEg5S_gXiVrVrzriRXKQIdNRYaFv_HZMIE0vaO34Gba-8bQBRTG2jmvattuQMAYB5s_vQm2DWscFWgnBuE4apadKutfS2rToQUvNSTOjkvsn3NVMEB7TYwe9NcCkMIXbv3Nie4gNCjh4rs9LD2vOgsCET87k5lwf5v4uLxGLp58KFPQ_yDSXyBVZ7y0W00)

#### Дублирование целей безопасности

---

### Описание Сценариев (последовательности выполнения операций), при которых ЦБ могут нарушаться

---

![2](https://cdn-0.plantuml.com/plantuml/png/dLJDRjDS4DtxAKRzretYdpW_Yq_TiE0Da4fLHOaRh2PESHmGGaXDWafHaRe4iIYmOcjAGgAqILvXxXinO-TUvvfIsggIQzzxPiwPCpFPwKNrCEftsePnH2z-mp-g1n5icGLeTrkzBQZte6F1Vw7Nr05M0GxgZMY_ySnh77fX2ZHrZ5s0m8jUTiF3VJz84RQES0eGUi_xNY-NoD5XfG8qki61tqflI_gjczms_SZl1deQLmUM2z3pmXT-mzjFofQmiWwhPB13lzsMg8gEgX9hw4TwfchEnM81cdMlqmtMJff5msY5tVuHu2TSu4oSu0nZlABd56F-4kT6nuRj_wdA6b0NyBiOueInE06Sun8NuYrz_CJOw9GIe5q3Yu2VipkPmge1zM2NEhc7tyGxoZvaDYsFGUtTtkK6xr64MGDd7M5q7AcZT2STJWtSl0v7wYZVMqT5wN2bZkgTTBXaN34ln9L2JFFUIanBIJ5LQ-mxQU5e9w_5vFIjqFC2IS06Vn771Bh42VsVOmnF0p6WWoLnyE5G3FWjdH1JLUFAQluCnnKVYLEyeaynecmhkZqblKl32vfg4Y_ePi6nz8p5EL1KZ3-OcE8Q_hPFIzm40d5g5Z3W-cmbGRNs8yMbd0FWN80hUZyMGtX2dYe_iiRQScvCwkpjuRPihLNy5zIHMItp1bjnciNov-8MgtDj9G-Fqot5sSPeMt8yy2jDmrICy4fyOFD83guq-jc63vQT6t0kZcVb0dyHmnZZzMGz2Y8_UlMuoIqT4yCrAy9OAYXJMEacJv8gOdObtxmDxMf-BWZCuJ6ZU2EczyYN5LLMHPNJio8TLfGydi8vw6MKbPYgFaaZPcGn6jy6crtCiRbqbZGzWK_OH5ho-EyMkfBRbaryBR5lf0KZyPwt73Q9izwPwinvw1BRfOSjSJOtjdi3DpzebCRYZ8OeI3p4kHXHw9WJyv1TYZEWp3DOqvnGy83-pX9cN2hZUa0WkMIKzZhv1TcXHx_J_Wq0)

### Политики безопасности

---

```python {lineNo:true}



```

## Идеи на будущее для улучшения

## Запуск приложения и тестов

### Запуск приложения

---

см. [инструкцию по запуску](README.md)

### Запуск тестов

---

_Предполагается, что в ходе подготовки рабочего места все системные пакеты были установлены, среда разработки настроена в соответсвии с руководством, на которое приведена ссылка выше._

Запуск примера: открыть окно терминала в Visual Studio code, в папке с исходным кодом выполнить

```sh
make all
```

запуск тестов:

```sh
make test
```

//www.plantuml.com/plantuml/png/PDBTQkf04C3n-pp5uWCi9dxVdKEfKB0WMde_ZMCOI7Rjx6nR-_HLuqOpNkyFPlAV_0i2BB6fimEmK4a7S686nT2QbQ-suXag71W8fYc6VPClBcRf-HjuXzogVA7K_A8sM29zTMYkqCoy8JVaG7mYCqMcPdqc8P1t3tYgyCIQ9oQX4khd7opZJKwK7Dz99oJ7BRhRnuoL7bcpzYnR0OdXQaRA5DQyx7gYK2Atfdr_1GTLDoplirFUjFlZPgholBFNTnLuPk_gzQNgFBsSwx-3-lYRXgcwfxWR_8mOv1sPzfIOIdikwzsUgZLmI4O57IMpf1fReN8MtJ3re-cexMLM50HTCghe3h3nxdgLOPP15EzYyu6SPHNxUFXhlcfocuQ2y3wdc0iKAJ5faomGMsx0ZrXHX2er3GiE4CVyW8gK9OX5ezxWqTRKQd1oXPaRyOqUuwZFLXm5IsPZnVE--URxvhrnNuc_SywPVEIC7I_nl6MdRpBlZ1_ImIF86n4l49nAZEMShudlUCMvlCVhDRlEE08EHe7xiLcmzCCWRF5kDrX0n2yCHlJYTFBc9I-mkfH4Fc5zQLKDFF3WuL-mHJ2qbluDZjPm4ijNWhMLYYM-8laWKopboehbBvmMelgXfdvxaanJkK_jQGAHRQhLJe5A-OOTwYDlhJ-W8JEk5QWscdoWCpuq6buW7o7b0SoHn7XToOmrD9DOV-bnh2G96X5I9I1Ru_KpNBX_j8vFKJ4p5-3DjPJoGfgY-QUgHlwhauEJizVlZjM9Ab7rCSgZVh6VbxfXaEKuvTze6bAdC7jEEe3td08szHF9sOR1joq3GwfRVgi-rBp4f98AHdfQSrpgSfi-FZvvHE71kQT3zwfdyrYBxFz7_dgUBggGRMNB3in2lpGD8TGRg9uGJeDpK-fC3NdJtR3wHpliuP4Xong10lRAC8DQDXJsgY7QwvK4yRjW7Wqrh23qjuydnuOfMhY5ZvuXK6JIy-RREVHqlMs2EwUJoTlgZweU53pdoYhpKBt2-1VVo3cdT4QIF41D52iwUM4ThYVpUVOt_X989pDjMWKkwEyMSFCVewZ2t6PCo_MZ7Kr5RPhgciWzJe6bxwwz_Sk5JN-Y923C_K8WThyRXp77YWiOsxX-wECn7lZlzGy0