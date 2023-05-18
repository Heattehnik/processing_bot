import sqlite3
from env import DATA_BASE

connect_main = sqlite3.connect(DATA_BASE, check_same_thread=False)
cursor_main = connect_main.cursor()
connect_data = sqlite3.connect('data.db', check_same_thread=False)
cursor_data = connect_data.cursor()
