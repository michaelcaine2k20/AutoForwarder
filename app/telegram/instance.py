from fastapi import Depends
from typing import Annotated

from app.telegram.base import TelegramMonitorProtocol
from app.telegram.client import TelegramMonitor

_monitor: TelegramMonitorProtocol | None = None


async def get_monitor() -> TelegramMonitorProtocol:
    global _monitor
    if _monitor is None:
        _monitor = TelegramMonitor()
    return _monitor


MonitorDep = Annotated[TelegramMonitorProtocol, Depends(get_monitor)]
