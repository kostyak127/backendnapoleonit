from dotenv import load_dotenv
import os

load_dotenv()


class TokenConfig:
    secret = os.getenv('secret', 'SUPER_SECRET')
