from dotenv import load_dotenv, find_dotenv
from os import environ

load_dotenv(find_dotenv())

PAGE_ACCESS_TOKEN = environ.get('PAGE_ACCESS_TOKEN')

