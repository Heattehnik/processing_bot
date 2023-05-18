import sqlite3
from env import DATA_BASE

connect_main = sqlite3.connect(DATA_BASE, check_same_thread=False)
cursor_main = connect_main.cursor()
connect_data = sqlite3.connect('data.db', check_same_thread=False)
cursor_data = connect_data.cursor()

cursor_data.execute(f'SELECT * FROM articles')
articles = cursor_data.fetchall()

for article in articles:
    cursor_main.execute(f'SELECT type_1, type_2, type_3, type_4, type_5, type_6 FROM si_types WHERE ngr = "{article[12]}"')
    types = cursor_main.fetchone()
    filtered_types = []
    for type_ in types:
        if type_:
            filtered_types.append(type_)
    i = len(filtered_types)
    while i > 0:
        clean_type = filtered_types[i - 1]
        cursor_data.execute(f'SELECT id, title FROM main.types WHERE title = "{clean_type}"')
        aim_type = cursor_data.fetchone()
        cursor_data.execute(f'INSERT INTO types_meters_links (type_id, article_id, article_order, type_order) '
                            f'VALUES (?,?,?,?)', (aim_type[0], article[0], 1, i, ))
        connect_data.commit()
        i -= 1
