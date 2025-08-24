# ITMO Program Bot

Бот и ETL-процесс для автоматического парсинга страниц образовательных программ ИТМО и предоставления пользователю удобного интерфейса в Telegram.

---

## 📌 Описание

Проект состоит из двух частей:

1. **Парсер страниц программ** (`parsing.py`)
   - Загружает информацию о программах ИТМО с сайтов: AI и Product.
   - Сохраняет данные в Excel (`data/ai.xlsx`, `data/product.xlsx`).
   - Скачивает учебные планы в формате PDF.

2. **Telegram-бот** (`bot.py`)
   - Позволяет пользователю выбрать интересующую программу.
   - Отправляет учебный план в PDF.
   - Отвечает на часто задаваемые вопросы (FAQ), используя данные из Excel.

3. **ETL с Prefect** (`etl.py`)
   - Флоу, который сначала парсит страницы, а затем запускает бота.
   - Бот работает до ручного завершения.

---

## ⚡ Стек технологий

- Python 3.11+
- `requests`, `beautifulsoup4` — парсинг HTML
- `pandas` — работа с Excel
- `aiogram` — Telegram-бот
- `prefect` — ETL-флоу
- `dotenv` — хранение токена бота

---

## 📁 Структура проекта

.
├─ bot.py # Логика Telegram-бота
├─ parsing.py # Парсер страниц ИТМО
├─ etl.py # ETL флоу с Prefect
├─ config.py # Конфигурации (пути к PDF/XLSX, URL)
├─ data/ # Скачанные Excel и PDF
├─ .secret.env # Токен Telegram-бота
└─ main.py # Точка входа


---

## ⚙️ Настройка проекта

1. Клонируем репозиторий:

bash
git clone https://github.com/kitaniq/IMTO_TEST.git
cd IMTO_TEST

2. Устанавливаем зависимости:
pip install -r requirements.txt
Создаём .secret.env с токеном Telegram-бота:
TOKEN=ваш_токен_бота

3. Запускаем ETL флоу:
python main.py