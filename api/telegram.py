from fastapi import APIRouter

from telegram.instance import monitor

router = APIRouter()


@router.post("/start")
async def start():
    """starts the telegram client"""
    return await monitor.start_client()


@router.post("/channels/{channel_username}")
async def add_channel(channel_username: str):
    """Add a new channel to monitor"""
    return await monitor.add_channel(channel_username)


@router.delete("/channels/{channel_username}")
async def remove_channel(channel_username: str):
    """Remove a channel from monitoring"""
    return await monitor.remove_channel(channel_username)


@router.get("/channels")
async def list_channels():
    """List all monitored channels"""
    return {"channels": monitor.get_monitored_channels()}


@router.get("/channels/all")
async def list_all_channels():
    """List all channels the bot is a member of"""
    return await monitor.get_all_channels()
