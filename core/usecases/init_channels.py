from typing import List
from core.database import Session, engine
from sqlalchemy import select
from core.logger import logger
from core.entities.channel import Channel
from core.repositories import ChannelRepository


class Init_channels:
    def __init__(self, channel_repository: ChannelRepository):
        self.channel_repository = channel_repository

    def __call__(self) -> None:
        if (len(self.channel_repository.get_all()) == 0):
            self.channel_repository.add_channels()
