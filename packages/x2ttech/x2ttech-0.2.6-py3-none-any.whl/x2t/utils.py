
import unidecode
import re

def slugify(text):
    text = unidecode.unidecode(text).upper()
    text = re.sub(r'[^A-Z0-9]', '', text)
    return text