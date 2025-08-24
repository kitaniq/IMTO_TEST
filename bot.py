import asyncio
import os
from pathlib import Path
from dotenv import load_dotenv
import pandas as pd
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, FSInputFile
from config import PDF_AI, PDF_PRODUCT, XLSX_AI, XLSX_PRODUCT

def run_bot():
    load_dotenv(".secret.env")
    API_TOKEN = os.getenv("TOKEN")

    bot = Bot(token=API_TOKEN)
    dp = Dispatcher()

    # ------------------ Хранение выбранной пользователем программы ------------------
    user_program = {}

    # PDF-файлы
    program_pdf_files = {
        "AI": PDF_AI,
        "PRODUCT": PDF_PRODUCT
    }

    # XLSX-файлы с данными
    program_xlsx_files = {
        "AI": XLSX_AI,
        "PRODUCT": XLSX_PRODUCT
    }

    # Названия программ для кнопок
    program_names = {
        "AI": "Искусственный интеллект",
        "PRODUCT": "Управление ИИ продуктами"
    }

    # ------------------ Загружаем FAQ из XLS ------------------
    FAQ = {}
    for key, path in program_xlsx_files.items():
        if Path(path).exists():
            df = pd.read_excel(path)
            questions = {}
            for col in df.columns:
                answer = "\n".join(str(v) for v in df[col].dropna())
                questions[col] = answer
            FAQ[key] = questions
        else:
            FAQ[key] = {}

    # ------------------ /start ------------------
    @dp.message()
    async def start(message: types.Message):
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text=name, callback_data=f"program_{key}")]
                for key, name in program_names.items()
            ]
        )
        await message.answer("Привет! Какая программа тебя интересует?", reply_markup=keyboard)

    # ------------------ Callback ------------------
    @dp.callback_query()
    async def callback_handler(callback: types.CallbackQuery):
        user_id = callback.from_user.id
        data = callback.data

        # Выбор программы
        if data.startswith("program_"):
            program_key = data.split("_")[1]
            user_program[user_id] = program_key
            await callback.answer()

            keyboard = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text="Скачать учебный план", callback_data="action_download_pdf")],
                    [InlineKeyboardButton(text="Задать вопрос", callback_data="action_ask_question")]
                ]
            )
            await callback.message.answer(
                f"Ты выбрал программу: {program_names[program_key]}\nЧто хочешь сделать?",
                reply_markup=keyboard
            )
            return

        # Действия
        program = user_program.get(user_id)
        if not program:
            await callback.message.answer("Сначала выбери программу командой /start.")
            return

        if data == "action_download_pdf":
            pdf_file = program_pdf_files.get(program)
            pdf_path = Path(pdf_file)
            if pdf_path.exists():
                await bot.send_document(chat_id=user_id, document=FSInputFile(str(pdf_path)))
            else:
                await callback.message.answer("Учебный план пока недоступен.")
            await callback.answer()
            return

        elif data == "action_ask_question":
            questions = FAQ.get(program, {})
            if not questions:
                await callback.message.answer("Пока нет доступных вопросов.")
                await callback.answer()
                return
            keyboard = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text=q, callback_data=f"faq_{q}")] for q in questions.keys()
                ]
            )
            await callback.message.answer("Выбери вопрос:", reply_markup=keyboard)
            await callback.answer()
            return

        elif data.startswith("faq_"):
            question = data[4:]
            answer = FAQ[program].get(question, "Ответ пока недоступен.")
            await callback.message.answer(f"Вопрос: {question}\n\nОтвет:\n{answer}")
            await callback.answer()
            return

    # ------------------ Запуск бота ------------------
    async def main():
        await dp.start_polling(bot)

    import logging
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())

# ------------------ Вызов ------------------
# run_bot()
