import os
from jinja2 import Template

# Настройки путей
TEMPLATE_FILE = 'template.html'
OUTPUT_DIR = 'articles'
INPUT_TEXT = """
[VECTOR_DATA]
Никанда — это государство, расположенное на плаintе Медуза... (вставь сюда весь текст из нейросети)

[METADATA_BLOCK]
name: Никанда
location: планета Медуза, материк Кфэранйом
role: государство
languages: эвюамский
capital: Швань
currency: никандский крон (NKX)
status: Гражданская война

[RAW_CONTENT]
(вставь сюда сам текст статьи)
"""

def create_page(raw_data):
    # 1. Парсим данные (упрощенный парсер)
    try:
        parts = raw_data.split('[METADATA_BLOCK]')
        metadata_part = parts[1].split('[RAW_CONTENT]')[0]
        content_part = parts[1].split('[RAW_CONTENT]')[1]

        # Извлекаем метаданные в словарь
        metadata = {}
        for line in metadata_part.strip().split('\n'):
            if ':' in line:
                key, val = line.split(':', 1)
                metadata[key.strip()] = val.strip()

        # Извлекаем заголовок и контент
        title = metadata.get('name', 'Без названия')
        
        # 2. Загружаем шаблон
        with open(TEMPLATE_FILE, 'r', encoding='utf-8') as f:
            template_html = f.read()
        
        template = Template(template_html)

        # 3. Рендерим (собираем) страницу
        rendered_html = template.render(
            title=title,
            content=content_part.strip().replace('\n', '<br>'), # Превращаем переносы строк в HTML
            location=metadata.get('location', 'Неизвестно'),
            languages=metadata.replace('languages', '').split('=')[-1].strip() if 'languages' in metadata else '?', # упрощенно
            capital=metadata.get('capital', 'Неизвестно'),
            currency=metadata.get('currency', 'Неизвестно'),
            status=metadata.get('status', 'Неизвестно')
        )

        # 4. Сохраняем файл
        if not os.path.exists(OUTPUT_DIR):
            os.makedirs(OUTPUT_DIR)
        
        file_name = f"{title.lower().replace(' ', '_')}.html"
        with open(os.path.join(OUTPUT_DIR, file_name), 'w', encoding='utf-8') as f:
            f.write(rendered_html)
        
        print(f"✅ Страница '{title}' успешно создана: {file_name}")

    except Exception as e:
        print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    # В реальной жизни ты будешь подставлять сюда текст из буфера обмена
    create_page(INPUT_TEXT)
