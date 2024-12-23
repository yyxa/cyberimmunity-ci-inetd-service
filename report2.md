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

![1](https://cdn-0.plantuml.com/plantuml/png/PDBTQkf04C3n-pp5uWCi9dxVdKEfKB0WMde_ZMCOI7Rjx6nR-_HLuqOpNkyFPlAV_0i2BB6fimEmK4a7S686nT2QbQ-suXag71W8fYc6VPClBcRf-HjuXzogVA7K_A8sM29zTMYkqCoy8JVaG7mYCqMcPdqc8P1t3tYgyCIQ9oQX4khd7opZJKwK7Dz99oJ7BRhRnuoL7bcpzYnR0OdXQaRA5DQyx7gYK2Atfdr_1GTLDoplirFUjFlZPgholBFNTnLuPk_gzQNgFBsSwx-3-lYRXgcwfxWR_8mOv1sPzfIOIdikwzsUgZLmI4O57IMpf1fReN8MtJ3re-cexMLM50HTCghe3h3nxdgLOPP15EzYyu6SPHNxUFXhlcfocuQ2y3wdc0iKAJ5faomGMsx0ZrXHX2er3GiE4CVyW8gK9OX5ezxWqTRKQd1oXPaRyOqUuwZFLXm5IsPZnVE--URxvhrnNuc_SywPVEIC7I_nl6MdRpBlZ1_ImIF86n4l49nAZEMShudlUCMvlCVhDRlEE08EHe7xiLcmzCCWRF5kDrX0n2yCHlJYTFBc9I-mkfH4Fc5zQLKDFF3WuL-mHJ2qbluDZjPm4ijNWhMLYYM-8laWKopboehbBvmMelgXfdvxaanJkK_jQGAHRQhLJe5A-OOTwYDlhJ-W8JEk5QWscdoWCpuq6buW7o7b0SoHn7XToOmrD9DOV-bnh2G96X5I9I1Ru_KpNBX_j8vFKJ4p5-3DjPJoGfgY-QUgHlwhauEJizVlZjM9Ab7rCSgZVh6VbxfXaEKuvTze6bAdC7jEEe3td08szHF9sOR1joq3GwfRVgi-rBp4f98AHdfQSrpgSfi-FZvvHE71kQT3zwfdyrYBxFz7_dgUBggGRMNB3in2lpGD8TGRg9uGJeDpK-fC3NdJtR3wHpliuP4Xong10lRAC8DQDXJsgY7QwvK4yRjW7Wqrh23qjuydnuOfMhY5ZvuXK6JIy-RREVHqlMs2EwUJoTlgZweU53pdoYhpKBt2-1VVo3cdT4QIF41D52iwUM4ThYVpUVOt_X989pDjMWKkwEyMSFCVewZ2t6PCo_MZ7Kr5RPhgciWzJe6bxwwz_Sk5JN-Y923C_K8WThyRXp77YWiOsxX-wECn7lZlzGy0)

#### Дублирование целей безопасности

---

| Цель Безопасности | Комментарий |
|----------|----------|
| 1. При любых обстоятельствах входящие запросы для критичных сервисов обрабатываются только указанными в конфигурационном файле сервисами соответствующими этому запросу. | Защита ценности 1. |
| 2. ci-inetd делает всё от него зависящее чтобы запустить критичный сервис при пользовательском запросе. | Защита ценности 2.  |
| 3. Время простоя сервисов не превышает заданное. | Защита ценности 3.  |
| 4. При любых обстоятельствах критичные данные мониторинга сохраняют целостность и аутентичность | Защита ценности 4.  |

### Моделирование атак

---

| Атакованный компонент | ЦБ1 | ЦБ2 | ЦБ3 | ЦБ4 | Кол-во нарушений |
| :-- | :-: | :-: | :-: | :-: | :-: |
| 20. LogStorage | 🟢 | 🟢 | 🟢 | 🔴 | 1/4 |
| 19. LogForwarder | 🟢 | 🟢 | 🟢 | 🔴 | 1/4 |
| 18. LogReceiver | 🟢 | 🟢 | 🟢 | 🔴 | 1/4 |
| 17 Terminator | 🟢 | 🟢 | 🟢 | 🟢 | 0/4 |
| 16 PermissionTerminator | 🟢 | 🟢 | 🟢 | 🟢 | 0/4 |
| 15. CriticalExecutor | 🟢 | 🟢 | 🟢 | 🟢 | 0/4 |
| 14. CriticalEntitySender | 🟢 | 🟢 | 🟢 | 🟢 | 0/4 |
| 13. PortStatus | 🟢 | 🟢 | 🟢 | 🟢 | 0/4 |
| 12. IdStatus | 🟢 | 🟢 | 🟢 | 🟢 | 0/4 |
| 11. StatusManager | 🟢 | 🟢 | 🟢 | 🟢 | 0/4 |
| 10 ActionManager(пропустил) | 🟢 | 🟢 | 🟢 | 🟢 | 0/4 |
| 9. ExecutorEntitySender | 🟢 | 🟢 | 🟢 | 🟢 | 0/4 |
| 8. Executor | 🟢 | 🟢 | 🟢 | 🟢 | 0/4 |
| 7. PermissionExecutor | 🟢 | 🔴 | 🟢 | 🟢 | 1/4 |
| 6. LogAnalyzer | 🟢 | 🟢 | 🟢 | 🟢 | 0/4 |
| 5. RequestVerifier | 🟢 | 🔴 | 🟢 | 🟢 | 1/4 |
| 4. ConfigParser | 🔴 | 🔴 | 🔴 | 🔴 | 4/4 |
| 3. ConfigFile | 🔴 | 🔴 | 🔴 | 🔴 | 4/4 |
| 2. RequestForwarder | 🟢 | 🔴 | 🟢 | 🟢 | 1/4 |
| 1. PortListener | 🟢 | 🔴 | 🟢 | 🟢 | 1/4 |

🟢 - ЦБ не нарушена 🔴 - ЦБ нарушена

![2](https://cdn-0.plantuml.com/plantuml/png/RDBDJi904C3nUvzYW_U6bW_AJMCaCS64WF4-jaCpIRkBixCgFhr0NQ23v_abi_rFxxq0IsYRP0SiLD8Eh9X1FapDqjKRSGmr3Wnuq-P3qqVP_8GMZh-0A-IEPNDpnrWfMfpe6akapxCi_fCpyuhSaWLnqSqKcPhLaNXFpjxWgSAJr3mo2PNGF7rZ6IvoekJuIbeXsM_GNZvhhFGeDIl7iX6GuF_CI9ayDSzLJ-HAPAdfvYzWeJulo_hi43g-_VPbyxujBhQR5_tvBBsgrvUgy_HqimSBpVudBbDr3t7N-17GonioRIaobVPOrjajrIjW7uqAEefcGGrsGkNCpylKBwUZTfTPaXUqqQYY5M3hhEzcmoI18Cw6zXqvIMfsuRUvCiPf60YYQEzJp0KY4KWYI86uHvGoIaC0SO8u4202AH8DYCOdGB882yR6zXN-t8Y_wnZ3Ga51aSRUdJ_pviyQiYU2U-H8z089OcHylYAsErq6auwqzcclBuWOd6f8ESTAaA90hkVShX07ansNrs7UGoFKvJqlNCVRRKzWf19s-p8uF1uF4L7Dz4mlgMVVkWRCajR0_byDRSdUkiIBRs_Lg3jELtAgK6y46K4qBdWIdUkKKcuxK5x0V1hi-lwwcs6lzlVp_3R37t5V6Bt6ZM6kmJDYEc9rwHOfaehuGdFNEg_n1UcDvIeGJ7gMF3uTZOxMR4I4KdBmb5WDkIrqva8p3TsAVyr_WjtImPBv6OoRoH3dwjvHai-tXHBdUhh1SwxUcCPpNjYDwvZy1d-aK8X_cqXrTE9T7GJuNzCRbCqCcuOe-RxYBlwNhyTVtE203zwL7m00)


![3](https://cdn-0.plantuml.com/plantuml/png/PDBDQi904C3nUvvYiFV5n8-OMqkfKB0WMdgV9cDOI7RjxAIjVVgYSTMCv_s5sVnd7uCWIzSsoHvPR6dtw0H6sTZ0ojTRyOmrZG03jDbuQDBYP9QUVv0hubwb1IYsEB4DbMI_BsgXK0xlnArrA3wI71wOAkNci3ww4AntTr_C5PuPU6OhjiJcvPVAxYfdIavlf1ChXosvwozDbPuOM7kMhQ1quMmcocG6Ngk1o9H83VJdR-YmlWnBXwmm4Ez-VxDYQ1TNsv-hohcvgJUK-L3EJpjxSjWS_k8mLNTcO4DV7GNv8BOx6vbAUophtSxMQ-GGZGewYMPf6-g5ofbTXgddfgFscrdP8EIYKKKhfDQxyrR6IOATUDUrdyH9KhFlzl3VVDNaDWq5uRrFyIvG9CUuJR90RBa1Fs954QhKD2muW9tmKrIaB44i6d43qzRKIh1pXPaRyGsFiTLd4qV1ajbOyPjlllc-UM-U7Ff2EMNydZ9AQ8tdBINonWjlSjySF82yiQ4b5YEE4Sxfsj2A2ihvBLwlAV4c0N0m2jpNAg3fXywohlk-4y2A3Gp7vjdfzDLpMYAwvZb_G7ojLHKyjE3H7x2kO7Gr_JCSRU0avay6rWeHQ-ZAy3kE4Cg55U6Fb9QYGbTJs9yarLJlKt-QGAIRghLJe5AweGJraRUH7z2GALS1gagJNV0cXqf3I-HZINXe1GQEyLhmZ6Hfnh7yakFOIE8qmgMQWso3rtEuIFxHEgwYScOkmPjBAU65D47JTr6D_1Sd1oTdBzySYnDH8kfZb4VzSZ-_aMpOER9I-ecc8JM2sGiZ0tZ7AM2HdKZAAWRRjWmCgMpvhVWGynmRaLGociTjnwKbj-lZOvF7nZquTtJ8NWrq7bkHuN_aRs3fWWRPMhRkG2s4xZJKeDP0yuHGwfoRMcTQoBlkXjO_sc4FZnHPrmWKi5UA6RQoeR1L3T5Mhzm3j7BcKL6Z1aBxzV7e61YdXN_dCq-mK6QQfzstSsJf1ji4UwVJwUlcIrKE2fuBOUM5grvWz8Dk-89ISuQhynvgebZPoKljS3jPcUV_lklapFDCcjQ0S_gx1TpzPHGqcAl6j5u_sD5KqASfNqNkSGeqVNVj_NzSwFJFXGI4kGquOlVxub3cM70EOn-V7_9uY0V-m_u2)

![3](https://cdn-0.plantuml.com/plantuml/png/PDBDRk8m4C3nUvx2OkyH2H-1swvMHQf49GHLxzDaY4PAR3eUjwLFNo0ruEbvVj4uV_kl5s09VPSTW8LgEe0LCoh7kLcxTYUEeSMH0M_wSfoQOdanAySVm0toe8gbKMnnOLkiaTwlQg5GPPwHUx8WBfBAA3CtcxFndfpL-ZJymzYeBsQv-SyaL4Fty8brkF6PajCxQONak4Dx-wUfqfFSR1pBJa22_p4JPShSF3Q9A9KeSZFCdy12UrrMfEnKEPxzzycMgLtSx31NcQlyBc4ggrJEBvVspq9t_8hBvYavnTtYMq0lByYqfyXKsdDPP_VKRe1zD2he99eLTJW8bREyBbFlJKSTRcPDNj16euesWBspVfYDimo2E1lwL-GiQzc5W_bklcfocuQ2yDwdU1SeacFS9baWjjo07x6Y25Lg6XOSm4xuAIfIbY0MZRY1QMjg9TYvmioD-8R7sEgpYQDWoMoi-CqtttpVl3TF3dsXd39-JnabjCRpbX9vuuKtkMyE7a3UsD0IYn772ETqRMX51UNy5g_Nb7YJ03WO1Uvh5T3qGsTPrttV2M351ePZy-nq-kevBH5Tyvm_8BxMgWeUMl3e3rXNCBkQ_XcEDd0IyoS3QuM8DNHb-1r72EN2Yl17IajHeQifx4-IQghtgJzD8D9DrTefK2dTK8BwoDl83sZ8bAi0LQN9BdYJGwMX9VAn93oq0WF7U2ruHh8qurX-oN5i974QuLBDGRR1wpbS9Fze7LTHEJENuCsbbF12cg3fkwX6_ekJWvEpbs-EnOae4VKnogD-kP_VI3Ri75af_KJJa1h1x8MH0RpZ5B38JYHb5ODjMmQ6LBRyLdo8UOwDI2ePpUEsuzAIs_NniSbZunwSEpfahmOwZwt8y3_oDx1qGODiBLjte1P2TnfgK6kWUK8eTSvDhJCjv5rtG-iVxR27HugiQmGAs2l535lPKDYgXcYhL-u1MZdpgAXH0w7z-dXq38pJmh_pcITOA3FDq-xRER9qWss2lTFfz7NpfIe71S-5iFB2LIym-a4tV46fESFLUGyrKQpivALsk9sipFD_ttLovdacJMl0EVtT0kx-CWeQp5LZMgyVx6WgwDEKhoBtE0MQlhls_ZykTFhdGWB2t0OSiVjzSIXpB3Y7iO_F3tayn0D_Ody1)

![4](https://cdn-0.plantuml.com/plantuml/png/PDB1Qi90483XUvvYiFTWeYPwQoaL2XP4I-zJCuQ5PDVERjhQf-zgtEYE9y5yC9b_ycWTiklQ9ZduNxLJ1zGEHlauXPMfjyumrZG2jD3cuzXaYxDP6lv1heXxbIr0iFcPRMX7wdjGSu5AU2TkbKPd0Yb1c0BM9sEjClfE5rBFKdXcvV_0vkMNTjsLpk21gH9yUiErK-wu9NrTQWg2Jr9O6tPRXwwp5pGH9a_XjOf4BaIMGl_y3JNMmxGiPhvpsE3-rHQnzR7ZRKNeChs96CiobiNvR4yQc-DV65R4n2VUq5T7rdqGgxqAR1QpKrgZzwfU8zjWfh6P1BDK3VL2vCo7OUABar7xowoKTQI34KKhfDReorN6IOA-WkxQJ-8agTbq1_XllcfocuQ2yDwdU1SeacFS9baWjjo07x6Y25Lg6XOSm4xuAIfIbY0MZRY1QMjg9TYvmioD-8R7sEgpYQDWoMoi-CqtttpVl3TF3dsXd39-JnabjCRpbX9vuuKtkMyE7a3UsD0IYn772ETqRMX51UNy5g_Nb7YJ03WO1Uvh5T3qGsTPrttV2M351ePZy-nq-kevBH5Tyvm_8BxMgWeUMl3e3rXNCBsQ_XcEDd0IyoS3QuM8DNHb-1r72EN2Yl17IajHeQifx4-IQghtgJzD8D9DrTefK2dTK8BwoDl83sZ8bAi0LQN9BdYJGwMX9VAn93oq0WF7U2ruHh8qurX-oN5i974QuLBDGRR1wpbS9Fze7LTHEJENuCsbbF12cg3fkwX6_ekJWvEpbs-EnOae4VKnogD-kP_VI3Ri75af_KJJa1h1x8MH0RpZ5B38JYHb5ODjMmQ6LBRyLdo8UOwDI2ePpUEsuzAIs_NniSbZunwSEpfahmOwZwt8y3_oDx1qGODiBLjte1P2TnfgK6kWUK8eTSvDhJCjv5rtG-iVxR27HugiQmGAs2l535lPKDYgXcYhL-u1MZdpgAXH0w7z-dXq38pJmh_pcITOA3FDq-xRER9qWss2lTFfz7NpfIe71S-5iFB2LIym-a4tV46fESFLUGyrKQpivALsk9sipFD_ttLovdacJMl0EVtT0kx-CWeQp5LZMgyVx6WgwDEKhoBtE0MQlhls_ZykTFhdGWB2t0OSiVjzSIXpB3Y7iO_F3tayn0D_Oty1)

![5](https://cdn-0.plantuml.com/plantuml/png/PDB1Ri8m30RWUv_2OlUAjj32RTCqf4bCGZ3jxb5JHMeJvZZRsDCFA2aaNEklSVmxZrQGnNLjiaSMjLLxr0AZV9p2qZGRCOmDZG0jTFauDDdyR1Q6Vv1hubvbSuZOxCpMj2NrFQXPX2fu9-wKHZ6ULF519QnEnbfbz9qkOprDuPdLyGEsBx-qTLSwZUdaXcfHSjYGlWuq0NXWggD_YXHMXcKZACvUP16PF8NNEX1v9B8K-leRQco6bbd8Za7x4UxlDm_jRB2NUfHqbTwa6CegbELvRqyQsyEVRrQ6v9ZnchuSMVaWLZlbsJHaftoDtgbcXMozcOIcy6QXMkf54OfyQ1OzkJZKVZDBPOMqDrbeQgJEwCjMnac2JenstITnaZHit1x-cw-QtAQX8BptATu5YkGOjqaMY2qtu4UiA4ALceO51x0JVegAb2M8HIDkODgQMWbshZ1p8xxXCRRwRE8eM38RAtxppJVVD-_DaqDVAAUCtrD62QtnlAL4tdZXJUwRWmUGDpQqn6B4CS8vNHjQKK4vlyNhDINU900EHe7xMWKq_T1PrdNVTm9OiO7Xs3mxdRvwJaj4rppd3uYljQg2XnOy-WFM5Oolfd-6emsSnFp9m5eXOWrT6Nx74KAvi2ByaT9ILEXg2lkJf9hgVUfF4uXqKxLs2bHADvIWFl8syWCQCkKgG5LfiWlUv51fQ8byB0aFhS30CLuBdf4ipJYMNt8S6qcSHhXKSv1jy7eE5ya_MiTLLCxC9NXpAIMya2Pe-YwgaV_YvE3axEMROt4YIaHzZFAeN-xdDv8DEqTMIZ_HDAH6C7jXP03lE0KiiXD9MSLWsvQ18PKjlnKVOfvZ8v9AHlEuxRYqv7PzV6posBW7vuuEsQk1pcChCloF_0qiNT0WMylM7QY5q9s66jGQQ9uGIfrpK-jC2tdNtT3wHpliuP4Ywng10lPACSDMDXIsgY7QwfLxW5REF2fgr41elpuU7GFZjF3lVEO95ifCyxJxTeuitM2ROEzqEdtTVAdAGS5p8QoySDKBZ7xG3LzGQivmTTv3JHGhEtcf7MudA_FyttUTd7cUITCQS4v_ju2xluo21dFLcDRh1pkQ2leqvQl8FKw1fk-klV-F2vt-kP20CBS1H-n-NnpA70lEOUpZyqCU3_70_zXV)

![6](https://cdn-0.plantuml.com/plantuml/png/PD9HQy8m4C3nztwAuDwBRRNLjuqnOU10TEpzrfxbe4tSvRBDVVgfDMhYStzmlV_bqGgmkBvBTi12DUr0YnhburGjJRiHmz3YI85LVJuEJJO_cONX7-06UL3PN4LiTc9hh96-BseMeKgz8_UaGOmdbOfCgLP7OoqPVQVBM4zJzSmaL4Ftyekrkz9fJ2StL0l9VeFwkj0avaMgLePb8o3Edb6X7XYR2EQfUcq2baSYIzNm_Gqqj9UHMSWEeVqAz_yt3-sXThXkLBfARog6iWfbURhRauPk_-U7bI4vD5xZbqCh7yYq9S-c8JlsDNfBxGhOUZC9JU7DWZeSH16A_38iUd9nrE4yIxA2sfkeQ0FO6ts-oZX9m8dHhlz4JfAMZVjllkfoqmQ2yBjFiHT89KWXWOUghxr1soXF3OeY1OYg7W2J_gHA9HvRzI4eDt2Jk5WGmnLcRzHllDsn65ku5aZfYy6xttppVRCxg_M5eH-KKc8_Kq8HBV2SKSHlTXBqdvkz5v3NDJJ5uCY6c4xftj2SbfJQZtYzfoZexmC7ey3zp2TyU5iD-_56GqrWn4qSTitH-V3qcAQONTXB-mNpYxMi0L0EtFaBzYDeNn_-7OvMS1BQRmRMbYpMq9snd-m8KocpOlehnIAgfJMrdaoIQ2hMwUaqWSWlgiyT0nNJ0qN8ZxWL_u66n7CjGPLhSWD1lorxOufu36KySp3O4AzBEyw6nZRaVxmTIqbK8JJL9SXMUBs2YsXBwpYAf6Tkm9joAkQ5j0pzYrKZ_jtPtjcWz-64dR0ILXyYlImSJDzc2tQ5g9WUKJI4Zc3ssd03hZa5REGwafASmPKj0KFCIpvZ7spUXeOb2QDvNRLTAc9tlNrSSDVeZREcWzUgAVrOXMpzH_wQZcw_A5lI5Xru2wr2DsYeCr3U8HIhVLEeJ0NvZgiXjWx-OGqF1AarCWhOEuyvh6H3OgSQeftUx1oOgtxqg4u9eRjzl3hn62dX1Zxp1WCIQTxklfmTHzVS93Wu7muloWzLtYXuJfZLJhHwXj5lUh3N59i1Zivdo8baKiaRN-5gCebhP6STxtaxvgALu5HzDu1tVnZXtdB4rzdZWiMyMPKA5LLjKD2rRBeGPLR6jx3SO8xJzxtUGEJNtYkQfeOl2TBEP6QRgudKf_u5PURwcgb0cxg9WeLshhFkxKKoX0vNoNoRdUQFRalY5tG0ksomRjO_pnJ3faC_fRZaOYJ1srsG-F4I3tnf_m40)

![7](https://cdn-0.plantuml.com/plantuml/png/PD9HQy8m4C3nztwAmxqNssghRnjZmi21wDZxhJrBe4tSvRBDVVgfDMhY-mykzxyyMa4MrtV93bbKhNQe1KRvE8MbQJTY65iQ0Lheyt5eild9B0p_83V4Wyhc4B7PYQsf9lLzKRC8LV1Et2kDOZof838bh8x6McNqdIvZFKtXcPMe6hkNNwhTbKvZEhcXMfJiDwIl2qrYNgImCYmRGN7sZ8eOvIcyDW79uO6fYLYMme3UK6DxcPc5x53Qxt3_m7be3xd3VQFKLNgJCPHLAClJuPuqTli_FwmCoI7ochuSMVaWLblbsJHany16RrMxGhRUJ49JUBDG7GsY24L-6HRzkJoAEjndgQoGzYOgsY3rHfzFCquIT6Aqwp-9awHbutRmttorvAOH1D4zf-WBE18uO60HPPiR9B6yYf5boK0KvG0CpiUH8x5Cb8MHRp2nFM447hX2zOtoQjfTu1f4PmIIinbckb-zUg-wkjNGJyeejLyefPXcU4uevYyxgdIVcxqNaDSsDCRWm4QOpkZMq9JcbDbF-BobkDBT1mv6WVkrdF3X3JNinwjLDO4HDz5icyEp_iaHZJ4xi-VsA-PdFgi7DnsuzG3s8zY_Flm772tW9BBV3QpDMQoX6sC_sm6cCcR5z3TAH5HTQwe_dIGfbDRqX6K2aLzKdpi1Ag4xYf4VSGj-WORKSyr1jTJa1YhTXlJ66F4OodccOB0HFkTsc0yDRSHlt8xhI7GXDDKvo1Rul82BU4lhE8fapro1D-DKp0jfEVetgqRykzEzqrxdup4xOIMiFa9wv9VrlCuNx09H2TsZQ0WTmEobuGtuo2bW0xSZALrbOAyf619UyWdxOFCsCYn96CthGBi4OdVUFYwuRNJZFDB1QrMJ_HX2rlyZVpL7jr-KBMcB3ho5kjuD1QWpi7w7KABwfb2P0FcEgo6s3lvX3Gy4gJKo2jWRZsa6sP3OgOPefpS_1wPgFtfKQmsXktsyElOOAU46FlC60n9ftkw-d2r7Lziak7BMxxzVVwXoe-0vObOxqkePHd_epbwYaNeuEfyX9vAPlKE-pnqzrFFArpbCgQAh-Rd7_M-7NC00MYg-CQGf8QhEVdoBemgt6crwPHChBO8FsmIkXC4TdxzLBip9Xqwd9sjIkbSqJGal4gGzoSnsLnDPzB8Nb8dRrqm5sinD52mqbZhBtbuaG-HmGURh_3I_Tws7Nz01xBB1kbdzwwNYDntv6LwBro89tkvwn8-NUE2Fzby0)

![8](https://cdn-0.plantuml.com/plantuml/png/PD91Qy9040NWkxzYiFV592OnjvPIeM11jFG-JSQmaEpQsKbR--kBnbLtlNym-zxRHoV8ClJTP8yikjPxD0BJTAPWPTkjMCQMfe0E-dGMcgGwcQNb7-I6U5H91H5RdDY6QjBV5xM8K0dlnBqsADQJ4Y9JmFfedDFMtEaYrhc2PzQYQ-nUVgaUhZIFwVo66j5os9Av1fh7F5EmjYnRGHdS6MKnIXMyDW59Ov8e6C4R6cmlzn9uO6f2Modm8UvVM8LsuQqF77LTgfiUGrc6iZWjzsImE_pvOqL8SWKR-Xh8oGUntcdFyf0T6xPcfzirilDc7fhCcwNkQ1HPADBBiUZJfQ5Bne5MsWaPRvBGD4YzDUTjPfC93cBDq7yI_pTVDRjf0q7uxgVO5qWbS22GGzLhtw1jnAb1A5A0A6hlcFGdLIfnRDL3KDx0JU9YGGolCFj6_SRJCShQmY2GwCNWtM---RxPdTNQypgN_OyNXdvIGh7zGZ65DCDpGY6_sP7NFJG7Bo7lsD0OWmCRO3gX1qDJcbDYF-7rWKAlwwUuG-1-BISqlEuCwtYbuanWH2OQn-RalDzfqHYpCtjbls9-fbaLt11mynzOHz306lu3ZXPm4jZl1jRcBDRGlR6VxG1J2RDY-Xj5cQYQgwcsFqcgAL-d_Ma2aIwgvew0YkYHGkH7t8B_G4EiN7DGBJN9WDUjAmsD4O-Xb6SA1XlWTMw7wT3G1loFjsCHYLi8b-eAP0kyNiD5kALr74LPpzo2D-5Kp0jfAVetgqRy-xE3irxxmoaxOIMiFa1wvC_MyovTi6j4HVI4eY5q0BCtXXlmcLF01jAH52yPf6mn629UyWdxOFCsC2mfOpHlIhPBIUpEjuy4Gx-pSPxfuBMgQZ-M8cl_aR-gqFa5iZLjte5QgEMwmOMAWU8EeSZPDxdAb93lkXgQ_sYDDJnIP5uZKC3UAwPHoeR4eXgYHMzw3aoTVbHKiu1GRX-lJnMJbN05dtcBWIpIlDjzEPj2Lrqbs3llzo-A3rNUA7YEcDMENFKCep_qQ6yeCZqSdI-G4ycoIjvgXSl9ihXAUjO16TeX5wq0vzHt9NZNXv5VO6xPfldy_fgc_7sQmX5xmbVhbahTU2-u96lxq13NZOvlS-bGZesl7XFfMAO2RI8JEVbrpj2vRBTxhOtl9PeXK5m9yrrwJZ_9biClw02MRB1kSfzCBicA4psXgEZMey7RtNxuyGeFV4Z_1G00)

![9](https://cdn-0.plantuml.com/plantuml/png/PDB1Re90483XEqyniNSYeA2tDarDcjZ4QDFx54Qo2UpQsTcszkch8EYkzuyCyyy-Ma4MrpRH0LbKgGwe1IRfD8QrgNTY66kQ05feqwblacLdLeP_a2lYNYLB2DYYOrigINsFQX6W0jw9MwLHp40A24mEcxEnLXbzf_DGpsDuPYMgnERbbqftfVEGpcwe5YN77UdhGhEGPp5i3CjEK9oze2n4QGolbKVIa2GnzE0DDTRZl2Hmfyp30lT_juG7fih_u1JStpY8NSGt8NrP-3BlJlUaiJd-3HDpdvmoR-dBaPKFOhLN0vlxx9pOwBsgDyXsC3FVP8DPgOPwaVaY7OS5houDqlONMYihfCUmlgcGMgClnvb64JenshMVn55Kit47-6--wdBQ1eBmUqwn5w1I0WaX3rLVUuEsYASI8IIIL5KF48V-K54fZwtwGCGDNC2DbU3a2hCtwZUUxhgCaxXMBC6BYNU_-URxPdUMDVsWX6BxcM8AQOxdb49-i-DQRy_iF8UyZg491eSsm7H2juPcjA34ViJhBOMrtcwAsmFkPpRXmbjgs8tNwse28pBHxfZ3iy794KqmExVdzWlcvowh0xS5VF0Nx4RGmIxyEnmjuIImtmoiBLYieHjZFzaXfX9cnVHNYhoefjRKV3n9lb1QqoEM2KHkKLtk2AY8xYX4ViGj-GSqn8vh0QfCampKUYr7GnF4OoZbcO711dXTs54wDB81_-Bjk8f45q9JdODiYTSBk0Ytj8xpoFVC5NWJJiMya9QYVx5gnByztJdjTpySinDMmke3f4T-lvxNwO9T82gYUnGDeKEOlJJSW0-S0ZQKZgGuOv2onM28UCcdx8FDsy2m9CzeNXLjbuBOghUF17UCtZWFTF1QDNm_5Y6RJyXVG-Xsyx9zshm3Pw6PwmODXO6r7KAHsZUvoXIGLryDoR__7skuxv5Q8wE0lN6OTY4R4ejgY1QzwJamK_teK0Sh2EKAyl8O65N2zNpcDGPyf7bJVJbnz1xoHUY8IHkRPDVE1eDtguzMtYvuZfdRZhK7Xj5lkhEN59a-3j1do8naFhDKzSfLkvXIHTVJqu-xm8wuZ0LeN_UD8MqNeghjnxSuiFXkeqrdhQoqU7onJU1A6Qpq5AvpOKxUTxjzloQbzugYAUF51sbFVcOBRrcNbB-cJAMxcGgqYKpaBBGodMNlC3v38BX2vklqJB-NhOU_e0DOii6wMVFTPAGcvjylD4s_uVz2Gf6wErMnEdA5uiSBFF0v_WS0)

![10](https://cdn-0.plantuml.com/plantuml/png/PD9HQy8m4C3nztwAuDwBRRMjRnjZmi21wDZxhJtBGPkuosMR-_HJQwk9xp-utF_oQ0LONDT6Us2XYlQWHKtIQQnMfjcAOMXmei2gBftw9bcSpTBm3t2DtAjaeG9Mdja6AwJlKPK1AjGxSaSQn0oaK879rVfah2MZxtGUwdcidfc4AcXVVh5oLpeFwUo6QY4vR55V5vg5F8lLsh1i1SJP2yf2bCRgjVP86f8aLZru0mtDE2y9t37piC3zwyBQvHNte5GFZBMFYlYcfCyBN-RdsprfQ0z_myZS9yVE6_noQEK3cNOqiBdFJesDtb6p1hQ3cVac6yoIMkn5vejq71PykpHesvzeHLPGZsLzKmDsHb-kCuqYS6AqwpwHewXXu_wRiPRS9e8WklSf-W916eBjE0l4bXi4ego85KMAxGXn08_D9oX8Ne9OnCeDXYH3B3jZNw7wHhoQPYezPSkDZI7P39xkLw_Ug-hkQN9gw1jbDB8VQKG9JV2yfOJVxA3IUcQsdaFUhg4X1hisndH6ruR6DANCliVhDIMLrZPmC0hSz_k98hocXelnA58J674JExjc_wHpT413p4vittx2_AIKjGAK0pT-WuiHRE4Y_2iSpU0ajbyCh4rPhA4hOp_OBgOoPiNqPqf5L5LhgZwS92cKrlI0PG9HqTGYTmfKIZUK83_YPlm36aO5rnHKlYOUgBHgiZQ6YCSGym2M61lZTMfx-L3FnloBb-D24bK8JTK7sGolPt2H_ALr74YoPox0ct4gveMq7Fs3LIF-pV7MSRlvxf2Ti19M7oCzyai_B_E6dI4gfJiK3Q5Tc3qtl05BJW7hkXr98v-1lOx0a7BBRza7cxUnOKd2QFP2ooKGk-dbuuAXNoySNmVtwgdinn2o-eZyETNHjfRjfPrt00jYLYrX1NK65kyGIjMwcQjCW7p3rH1RzJ_eOLsGMYEZWBqgC3j1DYI6wds-4XmW0DATwlmq67C9KsDxxcnIUxGSsPXFvJp_18SBTvULbuVbGAcudrYbCgym8F7cDMej5Ae7Chv-9ne-zQBj9qOg9vtEwU9JcLSQdWFcjWFjXs6ep8qzHttRE7kV83EIgLPS58qAKwheA3yuWKziZqiQG4iFbeRymvf7k1PfqzufeBG8FcmJk9KCRlG0ZxWmHs-RpRRqPEMrecbMy291sfFChEzDyzVSoQ6-7iuQnxBdiUtFwwmfdgN7caRNryrQ5nxPQ-KWIa91NX_kSMPFfvzGIjb_w8USMclSEDqdeSzKbCbvhVtxjL_nEYePOeSBCb_cd-SxrrZy2pg0NJPODzv_QtNuaazuHgc-vcwW-kwsouyNUE1F9xy0)

![11](https://cdn-0.plantuml.com/plantuml/png/PDB1Re90483XEqyniNSYe82tDarDcjZ4QDFxL4Qo2UpQsQMjVVgYkEYE9nBo9SFymwDroAvhc-ZGFzLE7L0xcAJJ65QctZh3MDC4q4ARJaEJBCvcQVW7kI8ULB80mSepsz2ErFUeIe4AU2TkbKPdF2b0c1pM9sEjClfEvrBFOtXcrR_0vkMNTjsLpYMTtL3jb3jkILyNcacUnR0sxBOENMSlA9CeZU6r2aWgIHB30DvGOptEIuJhC_i5xhzErYwlU02b04LyKp6a1JmmLI7FpyTxqjWS__pCF2Hzw0rzTMJT1x7QAy_c8Jj5DdglwZMozMOMcioRfMfe45aeqd6O-EzI4NUuqKfPHtfC6veAgJNwSfvf566VGdVj9t4KrMow0_mtMpKv2KD1UCyftWLOy5D05iPZc11MQWo9wCO3jE0FHXEN6XSIRr31XWPikSBCZVocTQfz89X8WfkcR-QRxttVcpTGUgI8GhwYa7oQuJaXNrPyN-XMJN4Nyfg6XWYwx24TqTZGb6AA-0BBCVc5RYN1LO5x-afeUSqAQxnKiXA8f8b6qxHEpexRD4Hsnds-HdwMsnNWHWhU-GHh13EivGzmD8SJZ-yChCKYrj38y2MxI4N2YlGD1PaenzRaR4zITb2sfYqU4uYqgRft05H0R-HZVzJDvGKQGkMAQPJJ9852jwOqD4GzGWdF50piOHbpBmdrs9CtkOvBIQo3iAdw89jZEO0B_u_MyOkKpSmpU2FPIdWXBK6_YchK7tIAdTEZyqDn8af4lOVjiyR1z4lIi06g0dh7eQ7KXTbR8mEOSmgOcquaXTyPn6i8Xa1QFX4VOfuz8v8oHhE_zhgigjtyzKcBcyQ-E3aTqgkopkDQfFEF_9LJkieIsRhjeWEruDZJi025WHydX0BhtYmvcPNa6pwDp5Rz5psics9B_fdRYhUL0ekAKJg6UtZWU-u3)

![12](https://cdn-0.plantuml.com/plantuml/png/PDB1Qi90483XUvvYiVTWeaQzjPGA1GkYfVUf6SD0icjd9stjqpSQLztn54W-cDr_ykW5MDgcJlRTaxQq1ojca0zJitJLHXn3XGC3tZJvC3RP_6GMZd-0I-HUPNEbPYUrnYtIzmND59gQT-I6B8WBPAf8OLP7uZqvUuSBXIUfUMRgNa3zyelRzYedIevlf1MImmRjzJ9ZfKUfMJcMZO2q_cn6okIfUIqZaIkHfQR__WOMgikmB6PTtd3s-vEfobta-9ugy3IzgHTBrRauhUl9Gdtu2yCAyy1OnguhlCQl5hry8DEEWbLzZtcTtL6r0lR1gAgZO1PKOozKq_moJFrjkco_dYLvGHkCobe2DiwULpDC4kXIsBRvH4wIYbsx_s--QdQR1eBmtK-nBr0arqtQz82uyWP0rHD5g5BJSE01ueIVeYBb2EBGY3SmRKsj12UlCFD6VBFBhfMrYIFBo5mSU-URRxwPdLbj57sbd3B-G1abjCJpWHBvubamF51xZo7lMD4SYsEEOSxfJj62LfJpEtpUKH8C8uqx0EvROT3k9rBBKnZxdj6IXw5dm8en71shaulHwrEQmxhaAN-4VRaHEm3AW0T_m7O5yslTlo2lDVA9-RD2WYkHhEXMyNiUmvGBAyoVA7MYUhwcNcUIdAPodRhJ12BjtIzYfq2bT4y9uiDlhLyMb5ck5QWAJMOX6FQz3fc31GRDjW0Fn_XSyKGlJJZMRsZD6ggYA3uXvNYTWdQDtojy9L8Avzgq83Yht3pTW3tNGS4EgHhzGxA0_ylplVFBLs_Fa9dM9Dd4404LRfU_wssyWbTAlr1Ak8wH_BMIuTp87B2ncLRA2WPJnWmCgJJ2W-GXPU1OYIJ7g9xLD56DR-jDPPoXtskd3HsoO_jkIkkGlVyeFwCwZCgoNTXo1ZQ5NcawVAX9e7fYAFNwfbIP6lBsgs7Y7-wmXuS5qjUuriIt5dDKouR0HZL46xtwD5XuysXHWmf2SprvUWQCLyA_ywddM72UwaNxvHmOklrjWeEBqUXDzI4hZOBdJ5XvvgiN6FsaUxv68rqgdZv2J0HpbRon5QudStwXFkkavtaYHQl0UVNT0cx_C8egaYl6j1m_sZ6fgCkaGYkoGHU8UmFj7LyvpFHFXGI4kJ7uOflVGnn_B3YVTyTBoR-waCZZ2Hxum_iR)

![13](https://cdn-0.plantuml.com/plantuml/png/PD9HQy903C3nTp_5uTwBhLhrRMDC63WG7NlFsbW2xPtBfTlSfvzQhthn-NwGz9y-UW6Mjga7Us2XWlPWnGopKM9MhjgAOwXmQC2R9Xl59bsSpTBn3t29tAbqeTJyh3PO87ttQAxGpBmZDsH1N20pHNApFX7loTaxd2iyJSmpar01zSil5krLJfMSt4Wh98Sjskl7J9GU9sRjMBO2qlgB6IkJ9UQrZ4IcH9gOxlqDB5Jzi3HcnxnXz_lDLELvRo_lAl0ikQaNIzKvFv_hoK9z-0l3SXEROzqDVhNevGEPTXJSr3mmbh4zzNLsHzKQs0Ueiew3MLADdL1HitwY-jrqsku-A_A2DXZLjGHidBtSPZGOG2lEjiqdyd-nrPAJG114ztEAlW29V23AmdWC4y9A3I4HCKRt3FZ1QE9IuqBY3KPnmWISuGfLD_9L3zFGZGQ36ZTZTrMzr-zrLnayht7IFZjMz40nHNn94GKqmNT4WUpupckLL6uRyggA1WXss4Swfg6YCIKKypcsGmgyLb7NbL3tE4zeU4qkgOvanKbcvFcyaq0aJMnMLUsmtQZJ0Da9z_WA-ObrjeUgj7XhLcmYXOqCVWzVK_Zn-LR1O2AI5Rqglk0EKh6m8drDeH5LTZMLZPFl2pCGMvw9hotIN9shyXyl3aGQNPcV7Q8gf3SAS3vmKxqOKvHn9Q1Qr2G1hrN9Q6W0F4AQPmm6zh5DkAj3NVRr2ctwEObz4GuLnLZsG3Z5tpvsmG_juv-LcQSdyCRwEF12dgv-4UN0xpLppQE3qtsu4JNQWO_ZpUF1-BD-j3vG8RtZuW3jmF2Dak6qtA8Cv7fseqK6yHk18PHd7uaFkG3sbKWoZ6ftHSkimlvs2wLWw7UQnz8XRrKmKxggqWpkcYx_T91dFlB5PID6mh8dsrJPdPGb02nzEJqKElsKjl8EFlYPz040)

![14](https://cdn-0.plantuml.com/plantuml/png/PDBDQi904C3nUvvYiVTWulUjfLGeM10jlK-JCGmaktPsjgrz-gfnendF-uEP_2UFNe0bD7Mo1nOgQ0zMp20VfcRbggquXWe71hnfyc7VP8kpMJh-0IwHMvKjb9gVrGOBfEyEpHMQcNVaXYo8YsIcoDIiJyHxSlOEJnMUfEQPIQY0-kKNYt2L4oN7Dz8AoM6BzlenOwL7gLaxbgs017yn8sNorBoMFP4haQMcVNy32rKtBEkpOzwu-_rcglAyivTt5NYMtjJhIzLvUZxNauNwy1U7gRh7k1ly2kZb0vbs59bAUohhx8wgDR2FPcmU6Ci-74Muf1fRffhctKJrj-coxNbMv0LjD2fh2TWuUpdDC4aWYBEX-KHEaefTsFytOpMvJKD1UEzJl0iK4HktJHU8BJS0ggueGfNQXWK7i5D-YegK9OX58svWsffO2NQkC7CZlh5n-ZokSIAmweqLl_dcUzytRzx8Yg6lb5B27oYXY1PupYYIDvuuqB-rBmuE7aFadg4fGW670ALqRMXE6QNy3g_N53addeL-1FItst2LQbi5gz71G8MnOeTtzyp-yUZr0Ks1MV0PVmHgKL7Z06Md3F-ag7NtOKdr1TwNy1poPuCYP6B8q9NXznmWbCeE27-YM8drjLQ_Jr9LORNMNfKLTDKMATN4mCPqGn4K8NifFw0gAHap4DegPS4vsLRzDWKB0ZdR73mSuZNZSRuqvb1-ITCtK-aoQS8pK2xnUWvVqNyf2IRWwfPUWZsL3OKTCdFq3t60_9T7MqUdhzuUYYlH8qv2Y80ATVxVywCzHsvClr1C40ImVs7aubUy0nOKau2IEe-uJy0JIulCn9EKWqCZybQyvjaQJTREq6NJsHJmfTlDLYQdwggxtuRtU-tUjQazRSSIKdTMjURh6rPBWB76MqUnwho6khLiqMsje0Z9EskS-SujKki52jYh4hFRoeQDRUsGNgZEfyrStVSgTdW7UV5fzVImHEe2DtERvrXOvPiNtHPxQ5ExVpFY78z6R-uUxz9UU4w4coVQZy3e9ztm1Thl5EFx0NR6PghQb-LPj5Egx44-R-Nky5XAseJMPz2Sql4ez9giMsEWhiZRoBBNByi39NxpFXAIpJtrzJDgLjn_eG9jMWIq_7_ujYhvGy4ftll-q9B74ppmzy1l)

![15](https://cdn-0.plantuml.com/plantuml/png/PDBDQi904C3nUvvYiVTW4Z_qrb8g52o8bjwdoHW6abqxEzlMFdtLk6h6StumE__9enTW2MsJx825Ijg15JF8XwbPkdeZZg76WG5lsdpODzdyP1QEVu0hv4vbSwLc9xN64kdxWcOAJSqxSaiMn4KoLMHYLaVYFJbxXoSAZrFpp2HKGlFoYsMuoh6IenjfXMI_GNjTPgHqaPgLOza8IF1dKoYJf-QrwebSYImrtVSti51VXcLzTiWRttx_CbLv5ctSKmMUfZVr-b9rdfpEzMIXsV_5OQhk8UuQlm9w-K2cBKMcqXxBEhkbUWNiencPFYeYMb237IdC0sFLP_bbfFhTTDhkFaloWZOQrRK2R9qztsQO9134sT1-8YT9pIxip7ypLhFRD124xtwAVO4WREEswG5nvGs0gYUAKANISE01x9IVeYBb2EBGYZSmJKoi13klCFj6V6EJPJsESIAmweiLxtppxVVDpgoiq1VAADNlAQMObdZEAUOtFN5WOF0G6WyLtM0nr1726KqLBIYdJB_5wvHY1ou6H-pZ6EW7G7_z4mQ95TmJmMhKTKKOAtRuu50TdOrU7aDDJajzeJy0jQoeSO2oKuQ_KyIwTtzDzHckLt0RwKyAzdCsfEXMwNSwH2ZZ7H3-I8aG6qYjGO-aoi9AhRqgA-WgBMBK9C0cDACOYf2zuXzGbQuPSn3QAdd1URKd-kq6B0WKR0lmw0YlkHuNIsCen2zkzsOgMIP9U07A5LuluIl-BoN1vMVcynhi6M_8x91PeB-p0-G_FnsSdhzuSyAkM0yxYI02AiJvVokEzXAv2Vr4CK4GmlwLuf6lU0SiBEy0Ikiyx3u5Jy8jCcTFN0uTAPPdUDMJBPgiXQ7ZfhCfu4kscwsCJzKJiz-63thjthEfVMd74b9tLhKMr2TC9C1OuzHH8ZgleMujMtHRAoX2yluMPxvla58lK4nykyOSjB9XOrixf9UgYzjc8UUzWXrk82-_gXwV6AGeS3EtUee5aw-UTLlieKtj_Ss8SpOQlTvylNDxuJbXRZsHVXX6FsYchz1-vxY-xs5dR2QgVMqcivLIPBl5VSkpeyTSqaQqE8Fcb8wlGh_9kdKDr1NvErds-sNP5U9txoCcsTrJNp-ZvkNyCnLeip8WvF_3jvNXZnWdUE_wGuiVZ_30FmE_0000)

![16](https://cdn-0.plantuml.com/plantuml/png/PDBDQi904C3nUvvYiVTWulUjfLGeM10jlK-JCGmaktPsjgrz-gfnendF-uEP_2UFNe0bD7Mo1nOgQ0zMp20VfcRbggquXWe71hnfyc7VP8kpMJh-0IwHMvKjb9gVrGOBfEyEpHMQcNVaXYo8YsIcoDIiJyHxSlOEJnMUfEQPIQY0-kKNYt2L4oN7Dz8AoM6BzlenOwL7gLaxbgs017yn8sNorBoMFP4haQMcVNy32rKtBEkpOzwu-_rcglAyivTt5NYMtjJhIzLvUZxNauNwy1U7gRh7k1ly2kZb0vbs59bAUohhx8wgDR2FHWKTHREa6bkXSkRTCFMZvUQ1iLHbs_Eio0lQ25NM4h1nzdAQOP9046T3yucS91MxiFyljcfo4eQ2yBwdU1SW4H2YB8p7C26ib10ImSHuW1PKC9gurBYGU8CgDZHWonLcRkGtBNtIKI7163PDt_nyx_lcfwcXHueev6iAoQSPdXFovSJtJcVN50x0iMPe1AFB7jmHZGrDAQQ8Bt4Sa-zqoeY3MiGzVJcozAeoP_PYKJbWIHrxDLC_FMirQ0JlZFiyW7-MkzL1L1gylmYsbj9Eblu0HNCeyVZEG5eiP0sz6RvY5wv8KE6-eS2IgcXEbUrHieNIdBPO9W0jcchl3X0Lq3i6P80y8CdBbC8CAmPKRc1WS3fLEniZvCEKu4o1m1wECVSIKuyzUPDn_0b45q93zG4snt485VuVfUDxP7Vc6RYHN2Mue9P4lmfhv1-t2-rky-94b0Jm27iFrzl6GVHBqh0XiWBwGD6GwaBihP45p2b5c9jk98NB2A8r148WBP-83X7FdX5A5j4ShHoNDRd_C3vfSitemSdna5wLJA4ktxn6kfLhuoisVdEj5a8fjlQDTI-hAPQrd2KYtvKjfBNEcyrkLWmrw2e5qdxT8mhKT2du5TkaU27I9ggAASz6DKiNxX0F_Azz0W00)

![17](https://cdn-0.plantuml.com/plantuml/png/PD9DQ_904C3nkvzYyRal9hxVdb8g52o8bjwdPWm3oQwTdRIrdxxHxKOpdWBP7ypcF_aV15YQkXeSsoVjwGXEp30VMRFsvKuyGub30y7K-QXlikN5h3n_0HV8KMLBfHONjSKzqcU75WhDpIjoJGx49p9NP6OsPn82UNU7PmfFhNbaQbz0zVID--OgfqfERgGJajCEtVLZ9agFhTbubfs0DE7FZ9N9hNakUY9N8hCcdh-0Wx8RblLPcpVT_VvcglBYQkEv2ZotD_NwKdMUNTRruA0w_QHXgcuRTuiV3GPvGwO39QRIdijwTw1o0noIKK77oQoemYXKphmRfduq7JLkPar1q7L9pJ_6eWyBmDgx4C5eC80sXMlgT-JVPgic9s4e2EzxYdS15WWboi9u31F2IWaX4J14zotuWz74fSQ5n1jKiQ41MwumxqP-y-3LCeX1ZD5DqpVppTVlUpD3S9nwftrwhEYUOehq1KKKq0JF4GLyqhTEiwXokz1OLZH0qDC-HG0F5OqfeLYVuJYam6aM3Au8tCD7mfQNHDZ6ytcHG6IMs2whob6xNgK1iXFTqvV8JnQ-wW0r0-_CmJQ2pRNbTt0qXHDVtoXOIrYieXUbpxM7LCoiI5zHc8fofIRtxoHPJSltf78LRdNr6yfiYTHdunkh19rjizKH0XNIAmNGWhgfUHbJPBaIK6NrSS1fbYmD3L2FaE4PWq7xE2QwQq9TxPit3EYd9A9Tage7iYcEVRW8VjWW_4AbM_G8tjXy2hoGPj3Fh1hr1urSerKxEOGJLcBK-_YyQ2MiFvaMzb4RqXkk3WGUB5yhNim5lu1viqsbQ9c7VKVW2NaKHkm9WKJxYkMbl6f_pM7wWk6NXojB0LzokBBAk9zR6Rox1jxzr-wpRl85QISZPDdPt5gzKwkrx6M8PH0biBPoroWKioVfLs-Sq0LaMYXkJ6GstyazFF0dxnq0)


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

