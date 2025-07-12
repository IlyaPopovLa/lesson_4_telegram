## Что делает проект?

Скрипты предназначены для загрузки фотографий (SpaceX, NASA APOD, NASA EPIC) и автоматически публикует их в Telegram-канале.

### Используемые сервисы

- **SpaceX API** — для получения изображений миссий
- **NASA API** — для загрузки APOD и EPIC снимков
- **Telegram Bot API** — для публикации фотографий в Telegram-канале

### Скачивание фото SpaceX

```python fetch_spacex_images.py --id <id_запуска>```
Если --id не указан, будут скачаны фото последнего запуска.

### Скачивание NASA APOD фото (Фото дня)

```python fetch_nasa_apod.py```
### Скачивание NASA EPIC фото (Фото Земли)

```python fetch_nasa_epic.py```

### Автопубликация фото в Telegram с заданным интервалом

```python publish_photos_telegram.py --token <токен_бота> --channel <ID_канала> --directory <папка_с_фото> --interval <интервал_в_часах>```
##### Аргументы:

* token — токен Telegram-бота (можно указать в .env)

* channel — ID Telegram-канала (можно указать в .env)

* directory — папка с фотографиями (по умолчанию images)

* interval — интервал между публикациями в часах (по умолчанию 4 часа)

### Настройка переменных окружения
Создайте файл .env в корне проекта и добавьте в него:
```
NASA_API_KEY=ваш_API_ключ_NASA
TELEGRAM_TOKEN=ваш_токен_бота_Telegram
CHANNEL_ID=@ваш_ID_канала
```
