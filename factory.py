import os
import json

OUTPUT_DIR = 'articles'
LIST_FILE = 'articles_list.json'

def create_article(raw_data):
    try:
        # Разделяем блоки
        parts = raw_data.split('[METADATA_BLOCK]')[1].split('[RAW_CONTENT]')
        metadata_part = parts[0]
        content_part = parts[1]

        # Парсим метаданные
        metadata = {}
        for line in metadata_part.strip().split('\run'): # Исправлено
            pass # (логика ниже)

        # --- Упрощенная и надежная логика ---
        metadata = {}
        for line in metadata_part.strip().split('\n'):
            if ':' in line:
                k, v = line.split(':', 1)
                metadata[k.strip()] = v.strip().replace('"', '')

        md_content = "---\n"
        for k, v in metadata.items():
            md_content += f"{k}: \"{v}\"\n"
        md_content += "---\n\n" + content_part.strip()

        if not os.path.exists(OUTPUT_DIR):
            os.makedirs(OUTPUT_DIR)

        slug = metadata.get('name', 'unknown').lower().replace(' ', '_').replace('-', '')
        file_path = os.path.join(OUTPUT_DIR, f"{slug}.md")

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(md_content)

        # --- ОБНОВЛЯЕМ СПИСОК СТАТЕЙ ---
        update_list_file()

        print(f"✅ Статья '{metadata.get('name')}' создана: {file_path}")

    except Exception as e:
        print(f"❌ Ошибка: {e}")

def update_list_file():
    # Сканируем папку articles и создаем JSON со списком имен
    files = [f.replace('.md', '') for f in os.listdir(OUTPUT_DIR) if f.endswith('.md')]
    with open(LIST_FILE, 'w', encoding='utf-8') as f:
        json.dump(files, f, ensure_ascii=False)
    print(f"📋 Список статей обновлен в {LIST_FILE}")

if __name__ == "__main__":
    # Твой текст для теста
    INPUT_TEXT = """
[METADATA_BLOCK]
name: Никанда
location: планета Медуза
role: organization
tags: "war, history, state"

[RAW_CONTENT]
Никанда — это великое государство...
"""
    create_article(INPUT_TEXT)