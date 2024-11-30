import logging
from logging import FileHandler
from datetime import datetime
from typing import List

from sqlalchemy import select, or_
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from api.exceptions.source import SourceNotFoundException
from models import SourceModel
from database import get_async_db
from parsers.core import ParserManager
from utils.raise_if import raise_if_none
from utils.source import update_source_with_parsing_results


class UpdateService:
    def __init__(self):
        self.__logger = logging.getLogger()
        self.__logger.setLevel(logging.INFO)
        self.__logger.addHandler(FileHandler("update_service.log"))

        self.__scheduler = AsyncIOScheduler()
        self.__scheduler.add_job(self._update_sources, trigger="interval", hours=12)

    def start(self) -> None:
        if not self.__scheduler.running:
            self.__scheduler.start()
            self.__logger.info("Scheduler is running now")
        else:
            self.__logger.warning("Scheduler is already running")

    async def _update_sources(self) -> None:
        self.__logger.info("Updating started")

        current_time_ts = datetime.now().timestamp()

        async for db in get_async_db():
            result = await db.execute(
                select(SourceModel).filter(
                    or_(
                        SourceModel.last_check_ts is None,
                        current_time_ts - SourceModel.last_check_ts > 12 * 60 * 60,
                    )
                )
            )

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

                parser = await ParserManager.get_parser_by_source_type(
                    source.source_type
                )
                parsing_results = await parser.parse(source.url)

                updated_source = await update_source_with_parsing_results(
                    source, parsing_results
                )

                await db.commit()
                await db.refresh(updated_source)

                success_updates += 1

        self.__logger.info(
            f"Updated successfully: {success_updates}/{len(unupdated_sources)}"
        )
        self.__logger.info("Updating ended")
