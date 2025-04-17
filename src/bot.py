import json
import asyncio
from aiogram import Bot, Dispatcher, types
from datetime import datetime, timedelta
from decouple import config

TOKEN = config('API', default='')
bot = Bot(token=TOKEN)
dp = Dispatcher()

FILTER_BY_WEEK = True


# --- SENDING DATA ---

async def send_reviews(chat_id):
    try:
        with open("reviews.json", encoding='utf-8') as f:
            reviews = json.load(f)

        if FILTER_BY_WEEK:
            one_week_ago = datetime.now() - timedelta(weeks=1)

        for idx, data in reviews.items():
            try:

                if not data.get('date'):
                    continue

                if FILTER_BY_WEEK:
                    review_date = datetime.strptime(data['date'], "%Y-%m-%d")
                    if review_date < one_week_ago:
                        continue

                await bot.send_message(
                    chat_id,
                    f"\U0001F4DD Review #{idx}\n\n"
                    f"⭐ Stars: {data.get('rating', 'N/A')}\n"
                    f"👤 Author: {data.get('author', 'N/A')}\n"
                    f"📅 Date: {data.get('date', 'N/A')}\n"
                    f"💬 Review: {data.get('review', 'N/A')}"
                )

            except (ValueError, KeyError) as e:
                print(f"Processing error of {idx} review : {e}")
                continue

        print("Reviews have been sent successfully!")
    except Exception as e:
        print(f"Critical error: {e}")


# --- DATA PROCESSING ---

@dp.message()
async def handle_message(message: types.Message):
    url = message.text.strip()
    if not url.startswith("http"):
        await message.answer("Please send the correct link")
        return

    try:
        from parser import Parser
        parser = Parser(url)
        parser.run()
        await send_reviews(message.chat.id)
        await message.answer("Reviews have been successfully processed and sent!")
    except Exception as e:
        await message.answer(f"Processing error: {str(e)}")
        print(f"Parsing error: {e}")


# --- MAIN ---

async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
