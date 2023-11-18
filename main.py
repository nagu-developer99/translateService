import pdb
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
import pytz
from datetime import datetime
import asyncio
import nest_asyncio
import PyPDF2
import requests
import random
nest_asyncio.apply()


# Replace 'YOUR_TOKEN' with your Bot's API token
TOKEN = '<......>'

async def handle_messages(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.message

    if message.text:
        # Handle text messages
        user_text = message.text.upper()
        if user_text == 'NY':
            timezone = pytz.timezone('America/New_York')
            time_now = datetime.now(timezone).strftime('%Y-%m-%d %H:%M:%S')
            await message.reply_text(f'The current time in New York is {time_now}.')
        elif user_text == 'LN':
            timezone = pytz.timezone('Europe/London')
            time_now = datetime.now(timezone).strftime('%Y-%m-%d %H:%M:%S')
            await message.reply_text(f'The current time in London is {time_now}.')
        else:
            await message.reply_text('Please send either NY or LN.')

    elif message.document and message.document.mime_type == 'application/pdf':
        # Handle PDF documents
        file = await message.document.get_file()
        write_file_path_to = os.path.join(os.getcwd(), f'file_{random.randint(11111, 99999)}.pdf')

        res = requests.get(file.file_path)
        write_file_to = f'downloads{file.file_id}'
        with open(write_file_path_to, 'wb') as f:
                f.write(res.content)
                f.close()

        with open(write_file_path_to, 'rb') as f:
            pdf_reader = PyPDF2.PdfReader(f)
            pdf_text = '\n'.join([_.extract_text() for _ in pdf_reader.pages]).strip()
        try:
            res = requests.get(f'http://127.0.0.1:8000/translate/?text={pdf_text}')
            await message.reply_text(res.json()['translated_text'])
        except:
            await message.reply_text('Unable to translate')

async def main() -> None:
    application = Application.builder().token(TOKEN).build()

    message_handler = MessageHandler(filters.ALL, handle_messages)
    application.add_handler(message_handler)

    await application.run_polling()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
