import json, os
from config import SAVE_FILE

DEFAULT = {'chapters_completed': [], 'stars': {}, 'bow_level': 0}

def load():
    if os.path.exists(SAVE_FILE):
        try:
            with open(SAVE_FILE, 'r') as f: return {**DEFAULT, **json.load(f)}
        except Exception: return DEFAULT.copy()
    return DEFAULT.copy()

def save(data):
    with open(SAVE_FILE, 'w') as f: json.dump(data, f, indent=2)

def complete_chapter(data, chapter_num, stars):
    if chapter_num not in data['chapters_completed']:
        data['chapters_completed'].append(chapter_num)
    data['stars'][str(chapter_num)] = stars
    data['bow_level'] = min(4, len(data['chapters_completed']))
    save(data)