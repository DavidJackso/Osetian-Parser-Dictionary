# Osetian-Parser-Dictionary
Проект для МД 

## Парсер Telegram каналов

Парсер для сбора сообщений из Telegram каналов.

### Установка

1. Установите зависимости:
```bash
pip install -r requirements.txt
```

2. Получите API credentials на https://my.telegram.org:
   - Войдите в свой аккаунт
   - Перейдите в API development tools
   - Создайте приложение и получите `api_id` и `api_hash`

3. Настройте переменные окружения или используйте config.py:
```bash
export TELEGRAM_API_ID="your_api_id"
export TELEGRAM_API_HASH="your_api_hash"
export TELEGRAM_PHONE="+79991234567"
```

Или скопируйте `config.example.py` в `config.py` и заполните данные.

### Использование

Запустите парсер:
```bash
python telegram_parser.py
```

Парсер запросит:
- Username канала (например, `@channelname` или просто `channelname`)
- Лимит сообщений (или Enter для всех)

Результаты будут сохранены в файл `messages.json`.

### Программное использование

```python
from telegram_parser import TelegramChannelParser
import asyncio

async def parse():
    parser = TelegramChannelParser(
        api_id=12345678,
        api_hash='your_hash',
        phone='+79991234567'
    )
    
    await parser.connect()
    messages = await parser.parse_channel('@channelname', limit=100)
    await parser.close()

asyncio.run(parse())
```
