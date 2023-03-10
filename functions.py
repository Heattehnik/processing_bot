import sqlite3
from env import DATA_BASE
import openpyxl as op
from classes import Data
import datetime
from dateutil.relativedelta import relativedelta

# connect = sqlite3.connect('processing.db', check_same_thread=False)
connect = sqlite3.connect(DATA_BASE, check_same_thread=False)
cursor = connect.cursor()


def ngr_check(ngr: str) -> bool:
    cursor.execute(f'SELECT * FROM si_types WHERE ngr = "{ngr}"')
    res = cursor.fetchone()
    if res:
        return True
    else:
        return False


def insert_data(data: object, user_id: int) -> bool:
    cursor.execute(f"SELECT si_number FROM uploaded_data WHERE si_number = '{data.si_number}'")
    result = cursor.fetchone()
    if not result:
        cursor.execute('INSERT INTO uploaded_data (act_num, ngr, si_type, si_number, owner,'
                       'address, readings, water_temp, verification_date, valid_date, air_temp, humidity,'
                       'atm_pressure, qmin, qmax, intern, standart, phone, processing_date, user_id, valid_for, '
                       'conclusion, verifier_surname, verifier_name, verifier_patronymic) '
                       'VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',
                       (data.act_num, data.ngr, data.si_type, data.si_number, data.owner, data.address, data.readings,
                        data.water_temp, data.verification_date, data.valid_date, data.air_temp, data.humidity,
                        data.atm_pressure, data.qmin, data.qmax, data.intern, data.standart, data.phone,
                        data.processing_date, user_id, data.valid_for, data.conclusion, data.verifier_surname,
                        data.verifier_name, data.verifier_patronymic))
        connect.commit()
        return True
    else:
        return False


def choose_date(date):
    cursor.execute(f"SELECT * FROM uploaded_data WHERE verification_date LIKE '%{date}%'")
    result = cursor.fetchall()
    return result


def choose_verifier(verifier):
    cursor.execute(
        f"SELECT verifier FROM real_verifiers WHERE intern_1 LIKE '%{verifier}%' OR intern_2 LIKE '%{verifier}%'"
        f"OR intern_3 LIKE '%{verifier}%' OR intern_4 LIKE '%{verifier}%' OR intern_5 LIKE '%{verifier}%'"
        f"OR intern_6 LIKE '%{verifier}%' OR intern_7 LIKE '%{verifier}%' OR intern_8 LIKE '%{verifier}%'"
        f"OR intern_9 LIKE '%{verifier}%' OR intern_10 LIKE '%{verifier}%' OR intern_11 LIKE '%{verifier}%'"
        f"OR intern_12 LIKE '%{verifier}%' OR intern_13 LIKE '%{verifier}%' OR intern_14 LIKE '%{verifier}%'"
        f"OR intern_15 LIKE '%{verifier}%' OR intern_16 LIKE '%{verifier}%' OR intern_17 LIKE '%{verifier}%'"
        f"OR intern_18 LIKE '%{verifier}%' OR intern_19 LIKE '%{verifier}%' OR intern_20 LIKE '%{verifier}%'")
    fetch = cursor.fetchone()
    return fetch


def user_reg(user_id, name, surname, nickname):
    cursor.execute('INSERT INTO login_id (user_id, name, surname, nickname) VALUES (?,?,?,?)', (user_id, name, surname, nickname))
    connect.commit()
    print('Пользователь зарегистрирован!')

def user_delete(user_id):
    cursor.execute(f'DELETE FROM login_id WHERE user_id = "{user_id}"')
    connect.commit()
    print('Пользователь удален!')


def is_allowed_id(user_id: int):
    cursor.execute(f'SELECT user_id FROM login_id WHERE user_id = "{user_id}"')
    res = cursor.fetchone()
    if type(res) == tuple:
        return res[0]
    else:
        return 0


def processing(file, user_id):
    try:
        wb_read = op.open(filename=file, data_only=True)
        sheet_read = wb_read['Лист1']
        i = 2
        error = None
        while sheet_read[f'B{i}'].value:
            data = Data()
            data.act_num = sheet_read[f'A{i}'].value
            data.ngr = str(sheet_read[f'B{i}'].value).replace(' ', '')
            data.si_type = sheet_read[f'C{i}'].value
            data.si_number = sheet_read[f'D{i}'].value
            data.owner = sheet_read[f'E{i}'].value
            data.address = sheet_read[f'F{i}'].value
            data.readings = sheet_read[f'G{i}'].value
            data.water_temp = sheet_read[f'H{i}'].value
            data.verification_date = sheet_read[f'I{i}'].value
            data.valid_date = sheet_read[f'J{i}'].value
            data.air_temp = sheet_read[f'K{i}'].value
            data.humidity = sheet_read[f'L{i}'].value
            data.atm_pressure = sheet_read[f'M{i}'].value
            data.qmin = sheet_read[f'N{i}'].value
            data.qmax = sheet_read[f'O{i}'].value
            data.intern = sheet_read[f'Q{i}'].value.partition(' ')[0].upper()
            data.standart = sheet_read[f'R{i}'].value
            data.phone = sheet_read[f'S{i}'].value
            data.processing_date = datetime.datetime.now()
            verifier = choose_verifier(data.intern)
            if verifier:
                splited_verifier = verifier[0].split(' ')
                data.verifier_surname = splited_verifier[0]
                data.verifier_name = splited_verifier[1]
                data.verifier_patronymic = splited_verifier[2]
            ngr = ngr_check(data.ngr)
            if data.valid_date:
                data.valid_for = relativedelta(data.valid_date, data.verification_date).years + 1
            else:
                data.valid_for = 0
            if data.valid_date:
                data.conclusion = 'Пригодно'
            else:
                data.conclusion = 'Непригодно'
            if not ngr:
                error = 'РЕЕСТРОВЫЙ НОМЕР НЕ НАЙДЕН'
                break
            if not data.verification_date:
                error = 'НЕТ ДАТЫ ПОВЕРКИ'
                break
            if not data.intern:
                error = 'НЕ УКАЗАН ПОВЕРИТЕЛЬ'
                break
            if not data.si_type:
                error = 'НЕ УКАЗАН ТИП СИ'
                break
            if not data.ngr:
                error = 'НЕ УКАЗАН РЕЕСТРОВЫЙ НОМЕР'
                break
            if not verifier:
                error = 'УКАЗАННЫЙ ПОВЕРИТЕЛЬ НЕ НАЙДЕН'
                break
            if not isinstance(data.verification_date, datetime.datetime):
                error = 'НЕКОРРЕКТНАЯ ДАТА ПОВЕРКИ'
                break
            if not isinstance(data.valid_date, datetime.datetime) and data.valid_date != None:
                error = 'НЕКОРРЕКТНАЯ ДАТА ДЕЙСТВИТЕЛЬНО ДО'
                break
            insert_data(data, user_id)
            i += 1
    except:
      pass
    return error, i


def make_file(date):
    try:
        data = choose_date(date)
        item_count = 2
        wb = op.Workbook()
        sheet = wb.active
        file_name = f'{date}.xlsx'
        for item in data:
            ngr = sheet[f'A{item_count}']
            ngr.value = item[2]
            date = sheet[f'B{item_count}']
            date.value = item[9].partition(' ')[0]
            valid_for = sheet[f'C{item_count}']
            si_type = sheet[f'D{item_count}']
            si_type.value = item[3]
            is_valid = sheet[f'E{item_count}']
            if item[10]:
                delta = relativedelta(datetime.datetime.strptime(item[10], '%Y-%m-%d %H:%M:%S'),
                                      datetime.datetime.strptime(item[9], '%Y-%m-%d %H:%M:%S')).years
                valid_for.value = delta + 1
                is_valid.value = 'Пригодно'
            else:
                is_valid.value = 'Непригодно'
                valid_for.value = 0
            intern = item[16].upper().partition(' ')[0]
            verifier = choose_verifier(intern)
            fio = verifier[0].split(' ')
            f = sheet[f'F{item_count}']
            f.value = fio[0]
            i = sheet[f'G{item_count}']
            i.value = fio[1]
            o = sheet[f'H{item_count}']
            o.value = fio[2]
            item_count += 1
        wb.save(file_name)
        return file_name
    except:
        pass


