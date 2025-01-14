import json
import logging
from typing import Dict, Optional

from fastapi import HTTPException
from telethon import TelegramClient, events, utils
from telethon.tl.types import Channel, PeerChannel

from settings import settings

# Set up logging to help with debugging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Class to manage our Telegram client and channel monitoring
class TelegramMonitor:
    def __init__(self):
        self.client: Optional[TelegramClient] = None
        self.monitored_channels: Dict[int, str] = {}

    async def start_client(self):
        """Initialize and start the Telegram client"""
        if self.client is None:
            self.client = TelegramClient(
                f'sessions/session',
                settings.telegram.API_ID,
                settings.telegram.API_HASH
            )
            # await self.client.start(bot_token=settings.telegram.BOT_TOKEN)

            await self.client.start(phone=settings.telegram.PHONE)

            logger.info(f"Telegram client started successfully. adding channels {settings.telegram.CHANNELS}")
            channels = settings.telegram.CHANNELS.split(',')
            for channel_username in channels:
                await self.add_channel(channel_username)

            # Set up event handler for new messages
            @self.client.on(events.NewMessage())
            async def handle_new_message(event):
                logger.info(f"Received new message: {event.text[:50]}...")
                await self._process_event(event, 'new')
                # await self.forward_message(event.message)

            @self.client.on(events.MessageEdited())
            async def handle_message_edited(event):
                # logger.info(f"Received edited message: {event.text[:50]}...")
                await self._process_event(event, 'edit')
                # await self.forward_message(event.message)

            @self.client.on(events.MessageDeleted())
            async def handle_message_deleted(event):
                # logger.info(f"Received deleted message: {event.chat_id}")
                await self._process_event(event, 'delete')
                # await self.forward_message(event.message)

    async def _process_event(self, event, event_type):
        try:
            chat = await event.get_chat()
            real_id, peer_type = utils.resolve_id(event.chat_id)
            if real_id not in self.monitored_channels:
                logger.info(
                    f"Received event({event_type}) from unmonitored channel({chat.title}) => real_id: {real_id}, peer_type: {peer_type}")
                return

            chat = await event.get_chat()
            logger.info(f"chat: {chat}")
            sender = await event.get_sender()
            logger.info(f"sender: {sender}")
            message = event.message
            logger.info(f"message: {message}")

            message_data = {
                'event_type': event_type,
                'source_channel_id': event.chat_id,
                'message_id': event.id,
                'text': event.text,
                'timestamp': event.date,
                'sender_id': sender.id if sender else None,
                'sender_name': sender.username if sender else None
            }

            logger.info(f"new Event:{'-' * 200}")
            logger.info(json.dumps(message_data, default=str))
            logger.info(f"{'-' * 200}")

            await self.forward_message(message)
            await self.send_message(message)
        except Exception as e:
            logger.error(f"Error processing event: {str(e)}")

    async def add_channel(self, channel_username: str):
        """Add a new channel to monitor"""
        try:
            channel_entity = channel_username
            if channel_username.isnumeric():
                channel_entity = PeerChannel(channel_id=int(channel_username))
            channel = await self.client.get_entity(channel_entity)
            if isinstance(channel, Channel):
                self.monitored_channels[channel.id] = channel_username
                logger.info(f"Added channel: {channel_username}")
                return {"status": "success", "channel_id": channel.id}
            else:
                raise HTTPException(status_code=400, detail="Not a valid channel")
        except Exception as e:
            logger.error(f"Error adding channel {channel_username}: {str(e)}")
            raise HTTPException(status_code=400, detail=str(e))

    async def remove_channel(self, channel_username: str):
        """Remove a channel from monitoring"""
        channel_id = None
        for cid, cusername in self.monitored_channels.items():
            if cusername == channel_username:
                channel_id = cid
                break

        if channel_id:
            del self.monitored_channels[channel_id]
            logger.info(f"Removed channel: {channel_username}")
            return {"status": "success", "channel": channel_username}
        else:
            raise HTTPException(status_code=404, detail="Channel not found")

    def get_monitored_channels(self):
        """Get list of currently monitored channels"""
        return self.monitored_channels

    async def get_all_channels(self):
        """Fetch all channels the bot is a member of"""
        channels = await self.client.get_dialogs()
        return [{
            'id': channel.id,
            'name': channel.name,
            'username': channel.entity.username if isinstance(channel.entity, Channel) else None
        } for channel in channels if isinstance(channel.entity, Channel)]

    async def send_message(self, message):
        try:
            await self.client.send_message(settings.telegram.TARGET_CHANNEL_ID, message)
        except Exception as e:
            logger.error(f"Error sending message: {str(e)}")

    async def forward_message(self, message):
        try:
            await self.client.forward_messages(settings.telegram.TARGET_CHANNEL_ID, message)
        except Exception as e:
            logger.error(f"Error forwarding message: {str(e)}")
