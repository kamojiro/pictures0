import os
from dotenv import load_dotenv

def load_env():
    if os.path.exists('../.env'):
        load_dotenv(dotenv_path='../.env')