import logging
from logging import FileHandler, Formatter
from datetime import datetime
from typing import List

from sqlalchemy import select, or_
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from api.exceptions.source import SourceNotFoundException
from models import SourceModel
from database import AsyncSessionLocal
from parsers.core import ParserManager
from utils.raise_if import raise_if_none
from utils.source import update_source_with_parsing_results


class UpdateService:
    def __init__(self):
        file_handler = FileHandler("update_service.log", encoding="utf-8")
        file_handler.setFormatter(
            Formatter("%(asctime)s - %(levelname)s - %(message)s")
        )

        self.__logger = logging.getLogger(__name__)
        self.__logger.setLevel(logging.INFO)
        self.__logger.addHandler(file_handler)

        self.__scheduler = AsyncIOScheduler()
        self.__scheduler.add_job(
            self._update_sources, trigger="interval", hours=12, max_instances=1
        )

    def start(self) -> None:
        if not self.__scheduler.running:
            self.__scheduler.start()
            self.__logger.info("Scheduler is running now")
        else:
            self.__logger.warning("Scheduler is already running")

    async def _update_sources(self) -> None:
        self.__logger.info("Updating started")

        current_time_ts = datetime.now().timestamp()

        unupdated_sources = []
        async with AsyncSessionLocal() as db:
            try:
                result = await db.execute(
                    select(SourceModel).filter(
                        or_(
                            SourceModel.last_check_ts == None,
                            current_time_ts - SourceModel.last_check_ts > 12 * 60 * 60,
                        )
                    )
                )
            except Exception as e:
                self.__logger.error(e, exc_info=True)
                return

            unupdated_sources: List[SourceModel] = result.scalars().all()
            self.__logger.info(f"Unupdated sources: {len(unupdated_sources)}")

            success_updates = 0
            for source in unupdated_sources:
                try:
                    source = raise_if_none(source, SourceNotFoundException())
                except SourceNotFoundException:
                    logging.error(
                        f"Unable to update source {source.url} with type {source.source_type}"
                    )
                    continue
                except Exception as e:
                    self.__logger.error(e, exc_info=True)
                    continue

                try:
                    parser = ParserManager.get_parser_by_source_type(source.source_type)
                    parsing_results = await parser.parse(source.url)

                    updated_source = await update_source_with_parsing_results(
                        source, parsing_results
                    )

                    await db.commit()
                    await db.refresh(updated_source)
                except Exception as e:
                    self.__logger.error(e, exc_info=True)
                    continue

                success_updates += 1

        self.__logger.info(
            f"Updated successfully: {success_updates}/{len(unupdated_sources)}"
        )
        self.__logger.info("Updating ended")
