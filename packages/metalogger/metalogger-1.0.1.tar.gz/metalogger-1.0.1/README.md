# Metalogger

Асинхронный логгер для Python с поддержкой:
- Ротации логов
- Цветного вывода в консоль
- Фильтрации записей
- Интеграции со стандартным logging
- Уникальные уровни логгирования

## Установка
```bash
pip install metalogger

```
## Пример использования

```
from metalogger import Metalog, ConsoleHandler, FileHandler

metalog = Metalog(
    handlers=[
        ConsoleHandler(),
        FileHandler("app.log")
    ]
)