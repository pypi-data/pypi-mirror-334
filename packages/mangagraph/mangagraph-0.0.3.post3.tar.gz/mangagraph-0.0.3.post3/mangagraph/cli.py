import argparse
import asyncio
import logging

from .parser        import Mangagraph
from .exceptions    import MangagraphError

mgraph = Mangagraph()

async def search_manga(query: str, limit: int = 5):
    results = await mgraph.search_manga(query, limit=limit)
    
    if not results:
        print("Не найдено подходящих манг по запросу.")
        return None

    print(f"\nНайдено {len(results)} по запросу '{query}':")
    for idx, result in enumerate(results, 1):
        print(f"\n{idx}. {result.name} / {result.rus_name}")
        print(f"   Рейтинг: {result.rating.raw_average}/10 ({result.rating.raw_votes} оценок)")
        print(f"   Год: {result.release_year} | Тип: {result.type} | Статус: {result.status}")
        print(f"   Возраст: {result.age_restriction}")

    try:
        choice = int(input(f"\nВыберите мангу (1-{len(results)}, 0 - для отмены): "))
        if choice == 0:
            return None
        if 1 <= choice <= len(results):
            return results[choice-1].slug_url
        else:
            print("Неверный номер.")
            return None
    except ValueError:
        print("Неверный запрос.")
        return None

async def main():
    parser = argparse.ArgumentParser(description="Mangagraph - Manga to Telegraph converter")

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--url', type=str, help='URL манги для обработки')
    group.add_argument('--q', type=str, help='Поиск манги по названию')

    parser.add_argument('--db', type=str, help='Имя БД (по умолчанию - название манги)')
    parser.add_argument('--limit', type=int, default=5, help='Максимальное количество результатов поиска (по умолчанию 5)')
    
    args = parser.parse_args()
    logger = logging.getLogger(__name__)
    
    mgraph = Mangagraph()
    
    try:
        if args.q:
            logger.info(f"Searching for: {args.q}")
            slug = await search_manga(args.q, args.limit)
            
            if not slug:
                logger.info("Поиск отменен или ни одна из манг не выбрана.")
                return
                
            logger.info(f"Выбрана манга: {slug}")
            manga_url = f"https://mangalib.me/ru/manga/{slug}"
        else:
            manga_url = args.url
            
        logger.info(f"Processing manga: {manga_url}")
        toc_url, mirror_toc_url = await mgraph.process_manga(manga_url, args.db)
        
        logger.info(f"База данных создана!")
        logger.info(f"Оглавление: {toc_url}")
        logger.info(f"Зеркало оглавления: {mirror_toc_url}")
        
    except MangagraphError as e:
        logger.error(f"Parser error: {e}")
    except KeyboardInterrupt:
        logger.info("Operation canceled by user.")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")

asyncio.run(main())