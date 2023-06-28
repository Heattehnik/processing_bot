import sqlite3
from env import DATA_BASE
from datetime import datetime
from dateutil.relativedelta import relativedelta
from time import sleep
from functions import connect, cursor


def compare_dates():
    cursor.execute(f'SELECT verification_date, valid_date FROM uploaded_data WHERE si_number = "I3223557"')
    fetch = cursor.fetchone()
    date1 = datetime.strptime(fetch[0][:10], '%Y-%m-%d')
    date2 = datetime.strptime(fetch[1][:10], '%Y-%m-%d')
    if date1.day == date2.day:
        print(f'{date1.date()}\n'
              f'{date2.date()}')
        print('Found')
    else:
        print(date1.date(), date2.date())
        print('Not found')


def strip_numbers():
    cursor.execute('SELECT si_number FROM uploaded_data WHERE si_number LIKE " %" or si_number LIKE "% "')
    fetch = cursor.fetchall()
    for counter in fetch:
        striped_number = counter[0].strip()
        cursor.execute("""
                            UPDATE uploaded_data
                            SET si_number = ?
                            WHERE si_number = ?;
                        """, (striped_number, counter[0]))
        connect.commit()



if __name__ == '__main__':
    strip_numbers()
