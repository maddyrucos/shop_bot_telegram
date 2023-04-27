from dotenv import load_dotenv
import os

load_dotenv()

TOKEN = os.getenv('TOKEN')

admin = os.getenv('ADMIN')

SITE = os.getenv('SITE')
LINK = os.getenv('LINK')