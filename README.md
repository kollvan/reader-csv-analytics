# reader-csv-analytics
---
reader-csv-analytics - консольное приложение для создания отчётов, по хранящимся в csv файлах данным.

## Содержание
---
- [Технологии](#-технологии)
- [Использование](#-использование)

## Технологии
---
- [python](https://docs.python.org/3/)
- [pytest](https://docs.pytest.org/)
- [tabulate](https://pypi.org/project/tabulate/)

## Использование
---

Запуск по умолчанию:

```bash
python main.py
```
![without arguments](https://github.com/kollvan/reader-csv-analytics/blob/a3b29d99e8205cc2ea96098797fe3576c4a93f11/Screenshot_1.png)<br>
Запуск с указанием ключей:
```bash
python main.py --files programming.csv --report median-coffee
```
![with arguments](https://github.com/kollvan/reader-csv-analytics/blob/a3b29d99e8205cc2ea96098797fe3576c4a93f11/Screenshot_2.png)<br>
