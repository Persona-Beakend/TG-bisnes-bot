<div align="center">

  <img src="https://upload.wikimedia.org/wikipedia/commons/8/82/Telegram_logo.svg" alt="Telegram Logo" width="120" />

  <h1>TG Business Bot</h1>

  <p>Асинхронний Telegram-бот для звичок, побудований на Python за допомогою aiogram 3.x та Docker.</p>

</div>

---

## 🛠 Інструкція із запуску проєкту

### Крок 1. Отримання токена в Telegram
1. Відкрийте офіційного бота [@BotFather](https://t.me/BotFather) у Telegram.
2. Відправте команду `/newbot` та виконайте вказівки (вкажіть назву та юзернейм бота).
3. Скопіюйте наданий токен (наприклад, `123456789:ABCdefGhIJKlmNoPQRsTUVwxyZ`).

---

### Крок 2. Налаштування змінних середовища
Створіть у кореневій папці проєкту файл з назвою `.env` та додайте наступний вміст:

```env
BOT_TOKEN=ваш_токен_від_botfather
DATABASE_URL=sqlite+aiosqlite:///bot.db
