import asyncio
import random
from pyrogram import filters
from pyrogram.client import Client
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton 
from pyrogram.errors import FloodWait
from info import *
from plugins.utils import create_image, get_ai_response 
from .db import *
from .fsub import get_fsub


@Client.on_message(filters.command("start") & filters.incoming) # type:ignore
async def startcmd(client: Client, message: Message):
    userMention = message.from_user.mention()
    if await users.get_user(message.from_user.id) is None:
        await users.addUser(message.from_user.id, message.from_user.first_name)
        await client.send_message(
            LOG_CHANNEL,
            text=f"#New_user_started\n\nUser: {message.from_user.mention()}\nid :{message.from_user.id}",
        )
    if FSUB and not await get_fsub(client, message):return
    await message.reply_photo(# type:ignore
        photo="https://telegra.ph/file/595e38a4d76848c01b110.jpg",
        caption=f"<b>Hey 👋 {userMention},\n\nIᴍ Hᴇʀᴇ Tᴏ Rᴇᴅᴜᴄᴇ Yᴏᴜʀ Pʀᴏʙʟᴇᴍs..\nYᴏᴜ Cᴀɴ Usᴇ Mᴇ As ʏᴏᴜʀ Pʀɪᴠᴀᴛᴇ Assɪsᴛᴀɴᴛ..\nAsᴋ Mᴇ Aɴʏᴛʜɪɴɢ...Dɪʀᴇᴄᴛʟʏ..\n\nMʏ Cʀᴇᴀᴛᴏʀ : <a href=https://t.me/mallumovieworldmain1>MMW BOTZ</a></b>",
    ) 
    return


@Client.on_message(filters.command("broadcast") & (filters.private) & filters.user(ADMIN)) # type:ignore
async def broadcasting_func(client : Client, message: Message):
    msg = await message.reply_text("Wait a second!") # type:ignore
    if not message.reply_to_message:
        return await msg.edit("<b>Please reply to a message to broadcast.</b>")
    await msg.edit("Processing ...")
    completed = 0
    failed = 0
    to_copy_msg = message.reply_to_message
    users_list = await users.get_all_users()
    for i , userDoc in enumerate(users_list):
        if i % 20 == 0:
            await msg.edit(f"Total : {i} \nCompleted : {completed} \nFailed : {failed}")
        user_id = userDoc.get("user_id")
        if not user_id:
            continue
        try:
            await to_copy_msg.copy(user_id , reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🎭  sᴜᴘᴘᴏʀᴛ 🎗️", url='https://t.me/maxmallumovieworldsupport1')]]))
            completed += 1
        except FloodWait as e:
            if isinstance(e.value , int | float):
                await asyncio.sleep(e.value)
                await to_copy_msg.copy(user_id , reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🎭  sᴜᴘᴘᴏʀᴛ 🎗️", url='https://t.me/maxmallumovieworldsupport1')]]))
                completed += 1
        except Exception as e:
            print("Error in broadcasting:", e) 
            failed += 1
            pass
    await msg.edit(f"Successfully Broadcasted\nTotal : {len(users_list)} \nCompleted : {completed} \nFailed : {failed}")
    

@Client.on_message(filters.command("ai") & filters.chat(CHAT_GROUP)) # type:ignore
async def grp_ai(client: Client, message: Message):
    query : str | None = (
        message.text.split(" ", 1)[1] if len(message.text.split(" ", 1)) > 1 else None
    )
    if not query:
        return await message.reply_text( # type:ignore
            "<b>Example Use:\n<code>/ai what is your name</code>\n\nHope you got it.Try it now..</b>"
        )
    if FSUB and not await get_fsub(client, message):return
    message.text = query # type:ignore
    return await ai_res(client, message)


@Client.on_message(filters.command("reset") &  filters.private) # type:ignore
async def reset(client: Client, message: Message):
    try:
        await users.get_or_add_user(message.from_user.id, message.from_user.first_name)
        if FSUB and not await get_fsub(client, message):return
        is_reset = await chat_history.reset_history(message.from_user.id)
        if not is_reset:
            return await message.reply_text("Unable to reset chat history.") # type:ignore
        await message.reply_text("<b>Chat history has been reset.</b>") # type:ignore
    except Exception as e:
        print("Error in reset: ", e)
        return await message.reply_text("Sorry, Failed to reset chat history.") # type:ignore


@Client.on_message(filters.text & (filters.private | filters.group))
async def ai_res(client: Client, message: Message ):
    sticker = None
    reply = None
    try:
        await users.get_or_add_user(message.from_user.id, message.from_user.first_name)
        if FSUB and not await get_fsub(client, message):return
        sticker = await message.reply_sticker(random.choice(STICKERS_IDS)) # type:ignore
        text = message.text
        if text.startswith('/'):
            return
        user_id = message.from_user.id
        history = await chat_history.get_history(user_id)
        history.append({"role": "user", "content": text})
        reply = await get_ai_response(history)
        history.append({"role": "assistant", "content": reply})
        await message.reply_text(reply) # type:ignore
        await chat_history.add_history(user_id, history)
    except Exception as e:
        print("Error in ai_res: ", e)
        reply = "Sorry, I am not available right now."
        await message.reply_text(reply) # type:ignore
    finally:
        if sticker:
            await sticker.delete()
