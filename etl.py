from prefect import task, flow
from pathlib import Path
from parsing import ProgramPageParser, URLS
from bot import run_bot


# ------------------ Задача 1: Парсинг страниц ------------------
@task
def parse_program_pages():
    parser = ProgramPageParser(URLS)
    parser.parse_all()
    return "Парсинг завершен"

# ------------------ Задача 2: Запуск бота ------------------
@task
def start_bot():
    run_bot()
    return "Бот запущен"

# ------------------ Флоу ------------------
@flow(name="ITMO")
def main_flow():
    parse_result = parse_program_pages()
    start_bot_result = start_bot(wait_for=[parse_result])
    return parse_result, start_bot_result
