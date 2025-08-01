### **Описание решения: Чат-бот для выбора магистерских программ ITMO**

#### **1. Постановка задачи**
Требовалось разработать Telegram-бота, который помогает абитуриентам выбрать между двумя магистерскими программами:
- **Искусственный интеллект** ([ссылка](https://abit.itmo.ru/program/master/ai))
- **AI-продукты** ([ссылка](https://abit.itmo.ru/program/master/ai_product)).

Основные функции:
- Парсинг данных с сайтов программ.
- Диалоговая система с рекомендациями на основе вводных данных пользователя.
- Простота и удобство взаимодействия.

---

#### **2. Инструменты и технологии**
Для решения задачи использовались:
- **Python 3.9+** (основной язык разработки).
- **Библиотеки**:
  - `python-telegram-bot` (v20.x) — для работы с Telegram API.
  - `beautifulsoup4` + `requests` — парсинг учебных планов.
  - `python-dotenv` — управление конфигурацией (токен бота).
  - `json` — сохранение данных о программах.
- **Git/GitHub** — контроль версий и хостинг кода.
- **VS Code** — среда разработки.

---

#### **3. Как решали задачу**

##### **3.1. Парсинг данных (parser.py)**
- **Цель**: Получить структурированные данные о программах (описание, дисциплины).
- **Решение**:
  - Использовали `requests` для загрузки HTML-страниц.
  - Применили `BeautifulSoup` для извлечения:
    - Описания программы (`program-page__desc`).
    - Списка дисциплин (искали раздел "Дисциплины" или `discipline-item`).
  - Сохранили данные в JSON-файлы (`data/ai_plan.json`, `data/ai_product.json`).

```python
import requests
from bs4 import BeautifulSoup
import json

def parse_program(url, program_name):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    program_info = {
        'name': program_name,
        'description': soup.find('div', class_='program-page__desc').get_text() if soup.find('div', class_='program-page__desc') else '',
        'subjects': []
    }
    # ... парсинг дисциплин ...
    with open(f'data/{program_name.lower().replace(" ", "_")}_plan.json', 'w') as f:
        json.dump(program_info, f, ensure_ascii=False, indent=2)
```

##### **3.2. Диалоговая система (bot.py)**
- **Цель**: Простое и интуитивное взаимодействие с пользователем.
- **Реализация**:
  - **Кнопочное меню**: Пользователь выбирает программу или сравнение.
  - **Контекстный диалог**:
    1. Бот запрашивает информацию о бэкграунде (образование, опыт).
    2. Дает персонализированные рекомендации.
  - **Обработка ошибок**: Защита от неверного ввода, команда `/cancel`.

```python
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    buttons = [["🧠 Искусственный интеллект", "🚀 AI-продукты"]]
    await update.message.reply_text(
        "Выбери программу:",
        reply_markup=ReplyKeyboardMarkup(buttons, one_time_keyboard=True)
    )
    return MENU
```

##### **3.3. Рекомендательная система**
- На основе ключевых слов в ответе пользователя (`python`, `менеджмент`, `data science`) бот предлагает курсы:
  - Для **ИИ**: машинное обучение, нейросети.
  - Для **AI-продуктов**: управление продуктами, маркетинг.

```python
if "интеллект" in choice:
    response = "Рекомендуемые курсы:\n- Машинное обучение\n- Нейросети"
else:
    response = "Рекомендуемые курсы:\n- Управление продуктами\n- Маркетинг"
```

---

#### **4. Принятые решения**
1. **Отказ от кнопок в финальной версии**:
   - Изначально бот использовал `ReplyKeyboardMarkup`, но для упрощения перешли на текстовый ввод цифр (1/2/3).
2. **Минималистичный дизайн**:
   - Убрали сложные элементы (например, сравнение программ сделали текстовым).
3. **Безопасность**:
   - Токен бота хранится в `.env`, который добавлен в `.gitignore`.

---

#### **5. Запуск проекта**
1. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```
2. Запустите парсер (один раз):
   ```bash
   python parser.py
   ```
3. Запустите бота:
   ```bash
   python bot.py
   ```

---

#### **6. Итог**
Получился простой, но функциональный бот, который:
- Парсит актуальные данные с сайта ITMO.
- Помогает выбрать программу через диалог.
- Дает персонализированные рекомендации.
