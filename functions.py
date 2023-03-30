import sqlite3
import xml.etree.ElementTree as xml
from env import DATA_BASE
import openpyxl as op
from classes import Data
import datetime
from dateutil.relativedelta import relativedelta

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
                       'conclusion, verifier_surname, verifier_name, verifier_patronymic, xml, standart_fif, mp) '
                       'VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',
                       (data.act_num, data.ngr, data.si_type, data.si_number, data.owner, data.address, data.readings,
                        data.water_temp, data.verification_date, data.valid_date, data.air_temp, data.humidity,
                        data.atm_pressure, data.qmin, data.qmax, data.intern, data.standart, data.phone,
                        data.processing_date, user_id, data.valid_for, data.conclusion, data.verifier_surname,
                        data.verifier_name, data.verifier_patronymic, 0, data.standart_fif, data.mp))
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
    cursor.execute('INSERT INTO login_id (user_id, name, surname, nickname) VALUES (?,?,?,?)',
                   (user_id, name, surname, nickname))
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

def get_standart_fif(data):
    cursor.execute(f'SELECT standart_fif FROM standarts WHERE standart_manufacture_num LIKE "{data.standart}" AND '
                   f'standart_valid_until >= "{data.verification_date}" ')
    res = cursor.fetchone()
    if type(res) == tuple:
        return res[0]
    else:
        return 0


def get_mp(ngr):
    cursor.execute(f'SELECT mp FROM si_types WHERE ngr = "{ngr}"')
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
            data.standart_fif = get_standart_fif(data)
            data.phone = sheet_read[f'S{i}'].value
            data.processing_date = datetime.datetime.now()
            verifier = choose_verifier(data.intern)
            data.mp = get_mp(data.ngr)
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
            if data.verification_date < datetime.datetime(2022, 12, 31, 00, 00, 00):
                error = '2022 ГОД'
                break
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
            if data.valid_date is not None and data.verification_date >= data.valid_date:
                error = 'НЕКОРРЕКТНАЯ ДАТА ДЕЙСТВИТЕЛЬНО ДО'
                break
            if not isinstance(data.valid_date, datetime.datetime) and data.valid_date is not None:
                error = 'НЕКОРРЕКТНАЯ ДАТА ДЕЙСТВИТЕЛЬНО ДО'
                break
            if not data.standart_fif:
                error = 'ЭТАЛОН НЕ НАЙДЕН'
                break
            insert_data(data, user_id)
            i += 1
        return error, i
    except Exception as e:
        return e, i



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


def to_xml():
    cursor.execute('SELECT * FROM uploaded_data WHERE xml = "0"')
    result = cursor.fetchall()
    cursor.execute('UPDATE uploaded_data SET xml = "1" WHERE xml = "0"')
    connect.commit()
    return result


def make_xml():
    data = to_xml()
    i = 0
    output = []

    while i < len(data):
        result = xml.Element("gost:result")

        miInfo = xml.SubElement(result, "gost:miInfo")

        singleMi = xml.SubElement(miInfo, "gost:singleMI")

        mitypeNumber = xml.SubElement(singleMi, "gost:mitypeNumber")
        mitypeNumber.text = f'{data[i][2]}'

        manufactureNum = xml.SubElement(singleMi, "gost:manufactureNum")
        manufactureNum.text = f'{data[i][4]}'

        modification = xml.SubElement(singleMi, "gost:modification")
        modification.text = f'{data[i][3]}'

        singCipher = xml.SubElement(result, "gost:signCipher")
        singCipher.text = "ГШИ"

        miOwner = xml.SubElement(result, "gost:miOwner")
        miOwner.text = '-'

        vrfDate = xml.SubElement(result, "gost:vrfDate")
        input_date = datetime.datetime.strptime(data[i][9], '%Y-%m-%d %H:%M:%S')
        vrfDate.text = input_date.strftime('%Y-%m-%d')
        if data[i][10]:
            validDate = xml.SubElement(result, "gost:validDate")
            input_date = datetime.datetime.strptime(data[i][10], '%Y-%m-%d %H:%M:%S')
            validDate.text = input_date.strftime('%Y-%m-%d')

        type = xml.SubElement(result, "gost:type")
        type.text = "2"

        calibration = xml.SubElement(result, "gost:calibration")
        calibration.text = "false"

        if data[i][10]:
            applicable = xml.SubElement(result, "gost:applicable")

            signPass = xml.SubElement(applicable, "gost:signPass")
            signPass.text = "false"

            singMi = xml.SubElement(applicable, "gost:signMi")
            singMi.text = "false"
        else:
            inapplicable = xml.SubElement(result, "gost:inapplicable")

            reasons = xml.SubElement(inapplicable, "gost:reasons")
            reasons.text = "относительная погрешность превышает пределы допустимой"

        docTitle = xml.SubElement(result, "gost:docTitle")
        docTitle.text = f'{data[i][28]}'

        gostMeans = xml.SubElement(result, "gost:means")

        mieta = xml.SubElement(gostMeans, "gost:mieta")

        number = xml.SubElement(mieta, "gost:number")
        number.text = f'{data[i][20]}'

        conditions = xml.SubElement(result, "gost:conditions")

        temperature = xml.SubElement(conditions, "gost:temperature")
        temperature.text = f'{data[i][13]}'

        pressure = xml.SubElement(conditions, "gost:pressure")
        pressure.text = f'{data[i][15]}'

        hymidity = xml.SubElement(conditions, "gost:hymidity")
        hymidity.text = f'{data[i][14]}'

        message = xml.tostring(result, "utf-8")
        output.append(message.decode('utf-8'))

        i = i + 1

    final = "".join(output)
    doc = '<?xml version="1.0" encoding="utf-8" ?><gost:application xmlns:gost="urn://fgis-arshin.gost.ru/' \
          'module-verifications/import/2020-06-19">' + final + '</gost:application>'

    return doc, len(output)


if __name__ == "__main__":
    # print(make_xml())
    # to_xml()
    print(processing('test.xlsx', 11111))
