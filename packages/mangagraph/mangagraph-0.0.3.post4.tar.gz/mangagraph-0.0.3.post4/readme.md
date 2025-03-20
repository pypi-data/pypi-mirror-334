# Mangagraph

#### From Mangalib to Telegraph with ❤️

Асинхронный парсер-конвертер манги из mangalib api в telegraph

## Принцип работы

Даем **ссылку на мангу**
**(такого типа: https://mangalib.me/ru/manga/{slug_url}) и название бд**
куда мы сохраняем _(том, главу, наименование главы, ссылку на главу для чтения и зеркало на случаи_
_если главная ссылка не доступна)_ -> получаем полные данные о главах -> генерируем телеграф страницы
на каждую главу -> ссылки на страницу сохраняем в `SQLite` бд, с использованием `SQLAlchemy`

**-> На выходе**
получаем базу данных готовую к любому использованию и конечную ссылку телеграфа с зеркалом (оглавление) внутри
которой находятся все главы с именами и ссылкой для чтения

Пример страницы главы: https://graph.org/Vanpanchmen--Opasnoe-sushchestvo-01-22-4

Пример оглавления: https://graph.org/Vanpanchmen-01-22-3 (ссылки на оглавление также сохраняются в бд, в таблицу ToC_url)

## Установка

```bash
pip install -U mangagraph
```

## Использование

#### CLI

```bash
mangagraph https://mangalib.me/ru/manga/706--onepunchman
```

или

```bash
python mangagraph https://mangalib.me/ru/manga/706--onepunchman
```

#### Поиск манги

```bash
python mangagraph --q "Berserk" --limit 10
```

#### Raw

```py
from mangagraph import Mangagraph
from mangagraph.exceptions import MangagraphError

async def main():
    try:
        mgraph = Mangagraph()
        # Поиск манги по ключевому слову и с лимитом
        results = await mgraph.search_manga("Berserk", limit=3)

        for idx, result in enumerate(results, 1):
            print(f"{idx}. {result.name} / {result.rus_name}")
            print(f"   Рейтинг: {result.rating.raw_average} ({result.rating.raw_votes} отзывов)")
            print(f"   Год: {result.release_year} | Тип: {result.type} | Статус: {result.status}")
            print(f"   Ссылка: https://mangalib.me/ru/manga/{result.slug_url}")
            print()

        # Парсинг манги и загрузка телеграф
        toc_url, mirror_toc_url = await mgraph.process_manga('https://mangalib.me/ru/manga/706--onepunchman')

        print(f"Table of Contents: {toc_url}")
        print(f"Mirror: {mirror_toc_url}")
    except MangagraphError as e:
        print(f"Parser error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

import asyncio

asyncio.run(main())
```
