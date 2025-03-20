import os

from dotenv import load_dotenv
from outline_wiki_api.client import OutlineWiki

load_dotenv()
URL = os.getenv('OUTLINE_URL')
TOKEN = os.getenv('OUTLINE_TOKEN')

app = OutlineWiki(url=URL, token=TOKEN)

