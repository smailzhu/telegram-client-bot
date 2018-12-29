from telethon import TelegramClient, sync, events
from telethon.errors import MultiError
from telethon import functions, types
import asyncio
import logging
import requests
api_id = api_id
api_hash = api_id

logging.basicConfig(level=logging.WARNING)

with TelegramClient('session_name', api_id, api_hash) as client:
    @client.on(events.NewMessage(outgoing=True, pattern='(?i)info'))
    @client.on(events.NewMessage(incoming=True, pattern='(?i)@smailzhu tell me more'))
    async def info_handler(event):
        chat = await event.get_chat()
        sender = await event.get_sender()
        msg_id = event.reply_to_msg_id
        result = await client(functions.channels.GetMessagesRequest(
            channel = chat,
            id = [msg_id]
        ))
        
        msg = f'Group name: {result.chats[0].title}\n'\
              f'Group id: `{result.chats[0].id}`\n'\
              '---Sender Information---\n'\
              f'Sender id: `{result.messages[0].from_id}`\n'
        for user in result.users:
            if user.id == result.messages[0].from_id:
                msg += f'Sender name: **{user.first_name} {user.last_name if user.last_name != None else ""}**\n'\
                       f'Sender username: {user.username}\n'\
                       f'Sender lang_code: {user.lang_code}\n'
                break
        if result.messages[0].fwd_from:
            if result.messages[0].fwd_from.channel_id:
                msg += '\n---Forward from **Channel**---\n'
                channel_id = result.messages[0].fwd_from.channel_id
                for chat in result.chats:
                    if chat.id == channel_id:
                        msg += f'Channel name: **{chat.title}**\n'\
                               f'Channel id: `{channel_id}`\n'
                        break
            if result.messages[0].fwd_from.from_id:
                user_id = result.messages[0].fwd_from.from_id
                for user in result.users:
                    if user.id == user_id:
                        if user.bot:
                            msg += '\n---Forward from **Bot**---\n'
                        else:
                            msg += '\n---Forward from **User**---\n'
                        msg += f'Sender name: **{user.first_name} {user.last_name if user.last_name != None else ""}**\n'\
                               f'Sender username: {user.username}\n'
                        break
                msg += f'sender id: `{user_id}`'
        try:
            await event.reply(msg)
        except Exception as e:
            pass

    client.start()
    logging.info('Listening...')
    client.run_until_disconnected()
    client.disconnect()