from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.telegram.instance import MonitorDep

router = APIRouter()


@router.post("/start")
async def start_monitoring(monitor: MonitorDep):
    """starts the telegram client"""
    await monitor.start()
    return {"status": "started"}


class VerificationCode(BaseModel):
    code: str


@router.post("/verify")
async def provide_verification_code(
    verification: VerificationCode, monitor: MonitorDep
):
    """Endpoint to provide verification code"""
    try:
        await monitor.provide_verification_code(verification.code)
        return {"status": "success", "message": "Verification code provided"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/stop")
async def stop_monitoring(monitor: MonitorDep):
    """stops the telegram client"""
    await monitor.stop()
    return {"status": "stopped"}


@router.get("/status")
async def get_status(monitor: MonitorDep):
    """gets the status of the telegram client"""
    is_running = await monitor.is_running()
    return {"running": is_running}


@router.post("/channels/{channel_username}")
async def add_channel(channel_username: str, monitor: MonitorDep):
    """Add a new channel to monitor"""
    return await monitor.add_channel(channel_username)


@router.delete("/channels/{channel_username}")
async def remove_channel(channel_username: str, monitor: MonitorDep):
    """Remove a channel from monitoring"""
    return await monitor.remove_channel(channel_username)


@router.get("/channels")
async def list_channels(monitor: MonitorDep):
    """List all monitored channels"""
    return {"channels": monitor.get_monitored_channels()}


@router.get("/channels/all")
async def list_all_channels(monitor: MonitorDep):
    """List all channels the bot is a member of"""
    return await monitor.get_all_channels()
