from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.telegram.instance import monitor

router = APIRouter()


@router.post("/start")
async def start():
    """starts the telegram client"""
    return await monitor.start_client()


class VerificationCode(BaseModel):
    code: str


@router.post("/verify")
async def provide_verification_code(verification: VerificationCode):
    """Endpoint to provide verification code"""
    try:
        await monitor.provide_verification_code(verification.code)
        return {"status": "success", "message": "Verification code provided"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


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
