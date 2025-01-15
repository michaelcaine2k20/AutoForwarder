from abc import abstractmethod
from typing import Protocol


class TelegramMonitorProtocol(Protocol):
    @abstractmethod
    async def start(self) -> None:
        """Start monitoring channels"""
        pass

    @abstractmethod
    async def stop(self) -> None:
        """Stop monitoring channels"""
        pass

    @abstractmethod
    async def is_running(self) -> bool:
        """Check if monitor is running"""
        pass
