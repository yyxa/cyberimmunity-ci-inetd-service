# Первичное моделирование угроз изначальной архитектуры

Изначальная диаграмма визуализации простого сценария работы

![1](https://cdn-0.plantuml.com/plantuml/png/VPJFJl905CNtVOe9--zB2hJ-MHWUX0rH5oJI4C4z1P4GY5sIk31nvRPK2XLQU8LxtyWpCuwbZR9g2kVyxhtd41gzVkk-_z2vixfujg_RtPRN5nNxlw2KzhJY4UruBcYBbuo7FC1pnu5eUhIXKB2FzoNxFAI8OigWcL4gQ4q9li-EFk8dIa3PGPzMHAidEdPnPBKq4gD2Mj8UGsSOnxx0MmpgdWuKic-uOoNCA04xuId5XbyjyclbazOyWZM36KPrMAH176X0hGYebnUSuEfO6mIjb1SxyRZfcRmUiTM76XEg-nCDhXV13i18CJyOxb2TJB4Q4Kcge8CSBZFaPvxeoVIfYKwHw8A8UkY0sJvj1INb1kU6Fy3LYQenqYZNiZgs-7U50CMbi45wKzlDi8gwDEzs1N-WDWIGCgpkIv45f_JNuAzglo9CJLfoW178MXPgrO7q_vcS1RLPIZRnRiAd-8GdNqI6_FARZ0E3jY5pJydqrWvaPwTape_i7BBNShEgI9NOHl_cJ8AoAX36w2uFH4eCqlr6BewgBPTeGMMq5tBBKksINJI5b2AgngrtWx-1Bm00)

---

### Скомпрометированный модуль контроля за собственным жизненым циклом:

| компрометирующее действие | нарушенные цб |
|----------|----------|
| передача ложных логов о своей работе | - |
| подлог конфигурации | 1, 2, 3, 4 |
| остановка работы сервиса или непередача конфигурации в обработчик сетевых подключений | 2, 4 |

![2](https://cdn-0.plantuml.com/plantuml/png/VPG_JnjH4CJx-nGhKXF9DdR-516V8Mr8OGKAf62XuFG-Y8EGKLmYfOYKAktX-E05VEUlCFkDCc-VN-nt2gxG7RE_sPqvUVzisFyq_7poCJlbt-CFnwVzmL1sMiy52zIOwmKUzLhmm8TAptM4cY-cSZ30FGhHdC-tckivPYXHKJF1Gd07n_zN6w_qAnmfZzGlTgH_9YSjUVRsw33rRJTywLVW5ZMT9_JKNFXK4brZYKBp21-Ri8AZWTChbD6adV8xpRlkz8AZ5GeRzDVD0aYd0T190NlD1IzvUXa617CKuM0T7mnYQ5_WyDji2Wl11V1U2kuIp2ZN1tEwi9DHciNCKmLBR-w3r6zw6Ppn9n2xAR578Zl2ajuv7WIkMUDrv8zujRCkPm7LopBsi_lED_J-3MEKrz8YxwVjEE52l7UpvZafKzkJMBwfDVSYoJYwndI8QGUCWQvYTEQs4lYERcplaSSy6MD6zUvgDr_BhzW4oYqpxNy-Fl7l_vFfDA9RbFMso9ACkXI_s2RkDiGlAVxHhDmQjX3lmySOG_KTaZEEfLeuNfA2UolmpKRppOupgjA9LxPtycsOJpfQOC48zuy6X_p1-0i0)

### Скомпрометированный модуль работы с безопасным хранилищем:

| компрометирующее действие | нарушенные цб |
|----------|----------|
| передача ложных логов о работе ci-inetd сервиса | - |
| подлог конфигурации | 1, 2, 3, 4 |
| непередача конфигурации в модуль журналирования | 2, 4 |

![2](https://cdn-0.plantuml.com/plantuml/png/VPJFpj905CNtVOh9vngJKbh_B0pl8Iw8i22HXW3kAOY4G6H9uiB4bTjIALHeuHNkVIFFp3YnCqPMJR_ltD-vzvo6zcJQ7Ky_3Zzu8pm7xmUZRZmLJ_vpGINTwCWBkl9Mq0Kl5SzvXkULTw8JqvbImGdU3vpmd3BAgO9cGwMW4nNuVrNx4t-c0fGhzEMJw4x4qBSjcuubh58wq0sc6zXn8l2MWtgZEwMS6EvI2Iigm2vuJRdXDyMpSRzdcmJkNITUOBu20TFgkapJUASfWGrekLkkS7gk1mGTrImMusKdDg5zmce_bKsgGYWqk6M3Gu0HvT-hCPsgkobN5fca2hfBSnaaV-6LTgPVcXZQn0X4T4HtU2Tq4LIuDMuDVuQh2zLbfb6HvmrzqNWZKtmjV92-g-qsM0MNrWi-OdwdDWIGAgoUI967oSPRsS0xK09GcfgYE6kJcR6H0bdENYqyavJ_vkT1RLQJVVmm5L3-OCPTHmR-zL-nNYgeYNs8eqTYloOE8NxnI1mwufSGVtDxLpMhFC_wYpJvoYB1MPfcLL1IOeEZF-1zhNwtQ0ygU-ALtDlvGAIFFPfIYJZR_RY7NutV)

### Скомпрометированный модуль журналирования:

| компрометирующее действие | нарушенные цб |
|----------|----------|
| подлог конфигурации | 1, 2, 3, 4 |
| непередача конфигурации в модуль контроля за собственным жизненным циклом | 2 |
| подлог журналирования | 4 |

![3](https://cdn-0.plantuml.com/plantuml/png/VLIzJXj16EplALQaJgIpyUMdY7YFaC8A54YnXS3fVIO48L1S8gM8b2hjuVZm1dpsAyptHfdHQiNTAb1PkvwVxvjPtTxfP7Wo-JBwd1tpz-ZJqV5mF74x-Ik7DJPOsXaUxDhXdeV6PZR5XXTpjp_62fMpakTRAss61Meqn5nXxN07p_-RrfLzWwVA0_7h7JSyTQEyQzbBB6bLuHORcbxHpah7KuqL8LjKLaRTSm5fuwdjxH9rrE-vha4_tUdEpiXjo1PJcos2ais3Gj-zE3aywAhifcDUSFSwi1oMgCB6Thu_ZgbzXSSVUQ5I2l11VRShFA0mitnSc-pAQN7Kii12gWvRcIj9-suNmHb_W-AWgrXGaILXI-yIzmu-xV4wwa-vkhTI4GIf8ij6kNlvNZ6-SteElpGTHvXfqtR3I_Bdcb22Q3XwAL16flXzydk13obSnhIYWG3gvWOQTIh-aybbHCUXrCJl63xg9pdjGHJoZ__1E8waFwZmZmJd11VFWVCMU43mw-V0WmJyXk2VQTUXMcMu2aynPghouDNzwZ4YGRh2HH36JQlof5moYeJnLdCdZq8-NMg5DOFSEnmVy5Fn3m00)

### Скомпрометированный модуль чтения данных конфигурации:

| компрометирующее действие | нарушенные цб |
|----------|----------|
| - | - |

![4](https://cdn-0.plantuml.com/plantuml/png/VPJDxj9G4CNtVOe9hZKfqFgnC3o3QpP4M918GmJt54H287P9uiB4bTjIALHeuHLctiXpx_LQslXdrHJE_ERCEOJEPDhxEFqq-k2CyHo-7uvxmPGQxWlYdAzya0LVP4jynaiXSvdXUP68kW6VE2O9yRwNKEQSSCe5D1lEYO-SuVlYxYFvmXae5-Zp1lKcD7AfkhDPsubTCU_vYgqRx9EGy9O2U-KRnn9Qy58B2yu0psJDgLtGhF9RzPkEii1eWM4CwiiI0vB805fLGBjkS8MpKpD0VD2py2JBRc03-mnNl_IQM0UG6N2RdhqRzAjq3tHaMLuDHAplvbJlIHIQ-AOSg2JbgwpCUlvji5wLw8E8alWc2q3En5cznwtbpt1wfijC3Cft71Jq_2rIf3VaWlH3kzl0YZwtRFY0-KWx190BM0-LY1oCAa0BWAO1QCJQPcOtA84gPwUzpXJWoVmSgAqhrSTFMm6d3sPA8ohbR_-JIMJHBcJ-8vbnxK7syf7C-oTx1TdtUhMwIHtPoVpoR8IgAn2MAAyCH4aiql-BtDrrMs_HWSfgNokNjTuLkpeKSuweEeEWZt-3Fm00)

### Скомпрометированный модуль обработки сетевых подключений:

| компрометирующее действие | нарушенные цб |
|----------|----------|
| ложные данные входящего запроса | 1, 2, 3, 4 |

![5](https://cdn-0.plantuml.com/plantuml/png/VPIzZjfG48LxFyLeKsyam-By5D4-Gzfi2XGea8A50kanX204Yaka595IfJKE1WTiU8MPDygvzt9bV9LGMTuzyvsPSomUXwFsfz7d_aTlW6VlGs_G3aTqvpydBlZ4MvdoKLR41xoKCf4ndaU9wIdaFISa4Tut4ic4KywuX6R91V6ES_o_lFgJVEKSb2FqnHsrXzJtgUxPS3pXbV26Jt1TmayYmbi6x8dFd4XamJCjB3a7F9S5PzQWKUSttPjsCiLeYM4CwijI0vBO09frm8Exu1ndPsQ0UCk9ELPcJw4Dx0ks-grj4Xr0Ri0Fpkaja95ZTJ764tqpPzeZLLZYit9NASetcHjh_cEGBNhsjjkfOmDWqHAVPGhIWJXtYrnPap5kptMRgU45deU6xjyWHdfDFaW_zOfBcPXxgugtc8_rcW1oYVqZ9I8FemhG1A1X01gniA5P1oLGxQprhcC5-6-07jHsArN8Bzi1PpTcgaLKrD__9PFOedt8WbioitKBiXStP13SlrEblB-8NqBymsrPbwg3sviFq0Qf6WDdXWghM9Ia3WukuFLLpswZ7bJrYLTgR-TBK3xrqOGBXFVO3JluWVWB)

### Скомпрометированный модуль запуска и контроля сервисов:

| компрометирующее действие | нарушенные цб |
|----------|----------|
| неправильное управление запуском и контролем сервисов | 1, 2, 3, 4 |

![6](https://cdn-0.plantuml.com/plantuml/png/VPG_RnD14CNx-nIZK0V9Tcp-52YVWPPGM2H59695nFG-Xn15Zd29H854HRinljmI--AlyEORyMPNgvDNn9MrqPlVctdlbCEByV3J-FFPn-ASlwSVJi-7ex7iTPuBrdZ4KY-nqbl10n-DJdN2tvNEvMY46awqvFjEIvrYWGeDDJEi1VVmgFbi_wHVuKbPKR_Ua-65d7LasxERUTBBuGwFT9tHJqlXgq9DoGPEomI-2i86dd2lDwYIGNURtyjlkjTBZZPmOT0kMqIGpYEWjmquo1UyvjbL710iuUAnUdKqIe5zWSUVOED203w23xBJ-oGpn_PYZhjmCwhWiJ2iO6Fkbg9-q-jeZRyHsS-G0oBP43PqB_4Wy7c9jybWmhjzQ78HMGDvzlRak2XOqVuRvYYlnJw8Ns77cKxZmMt7IqBcjgTHqV20qaHISDG0FGAw4H0GDocrv602g-TxM7XYW2SJBAXEMraZlrC9g7RCj8jOrZ_-9zDvGdSe6-oInQtxbBtO8QCWoLvIzZClEFPfaTNnsqiHMc7mLdZT1cAIX1n49FDg2ywhBAZQVsT5leyJyifspJu1SzWUTLWpiCEJqJ7_A_m3)