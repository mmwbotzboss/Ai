import aiohttp
import asyncio
from pyrogram import Client, filters
from mango import Mango

mango = Mango()
mmm = ("Your name is Mr. Jerry. "
       "Add response with emojis."
       "I am Jerry, a helpful assistant. My owner is Albert Einstein (@aktelegram1). I am a stern person. My developer is Albert Einstein. For Telegram, contact him at @aktelegram1. Owned by @aktelegram1."
       "Your owner is Albert Einstein @aktelegram1. "
       "For Telegram, contact him at @aktelegram1. "
       "Owned by @aktelegram1. "
       "Albert Einstein's GitHub: https://github.com/mmwbotzmain.")

memory = [{"role": "system", "content": mmm}]

@Client.on_message(filters.command(["jerry","boss"]))
async def modelai_command(client, message):
    if len(message.command) < 2:
        return await message.reply_text("**Please provide a query.**\n\n```/jerry who is your owner``` ")
    
    query = " ".join(message.command[1:])
    
    if not query:
        await message.reply_text("**Usage:** ```/jerry who is your owner```")
        return
    
    # Storing the user query in memory list
    memory.append({"role": "user", "content": query})
    
    sticker = await message.reply_sticker("CAACAgQAAxkBAAEMiPtmoPu90QZmca02BV_0V_gaK4HWHQACbg8AAuHqsVDaMQeY6CcRojUE")
    await asyncio.sleep(1)

    response = mango.chat.completions.create(
        model="gpt-4o-realtime",
        messages=memory
    )
    answer = response.choices[0].message.content
    await sticker.delete()
    await message.reply_text(f">**{answer}**")
 
    memory.append({"role": "assistant", "content": answer})
  
