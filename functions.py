import sqlite3
import xml.etree.ElementTree as xml
from env import DATA_BASE
import openpyxl as op
from classes import Data
import datetime
from dateutil.relativedelta import relativedelta
import requests

connect = sqlite3.connect(DATA_BASE, check_same_thread=False)
cursor = connect.cursor()


def ngr_check(ngr: str) -> bool:
    cursor.execute(f'SELECT * FROM si_types WHERE ngr = "{ngr}"')
    res = cursor.fetchone()
    if res:
        return True
    else:
        return False


def from_db_for_protocol(user_id):
    cursor.execute(f"SELECT * FROM uploaded_data WHERE protocol = 0 AND user_id = {user_id}")
    result = cursor.fetchmany(3000)
    return result


def set_protocol_to_1(user_id, si_number):
    cursor.execute(f'UPDATE uploaded_data SET protocol = "1" '
                   f'WHERE protocol = "0" '
                   f'AND user_id = "{user_id}" '
                   f'AND si_number = "{si_number}"')
    connect.commit()


def get_additional_standarts(verifier):
    cursor.execute(f"SELECT * FROM real_verifiers WHERE verifier LIKE '%{verifier}%'")
    result = cursor.fetchone()
    return result


def get_standart_type(standart_fif):
    cursor.execute(f"SELECT standart_modification FROM standarts WHERE standart_fif LIKE '%{standart_fif}%'")
    result = cursor.fetchone()
    return result[0]


def insert_data(data: Data, user_id: int) -> tuple:
    cursor.execute(f"SELECT si_number, verification_date, intern  FROM uploaded_data WHERE "
                   f"si_number = '{data.si_number}'")
    result = cursor.fetchone()
    if not result:
        cursor.execute('INSERT INTO uploaded_data (act_num, ngr, si_type, si_number, owner,'
                       'address, readings, water_temp, verification_date, valid_date, air_temp, humidity,'
                       'atm_pressure, qmin, qmax, intern, standart, phone, processing_date, user_id, valid_for, '
                       'conclusion, verifier_surname, verifier_name, verifier_patronymic, xml, standart_fif, mp, '
                       'production_date) '
                       'VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',
                       (data.act_num, data.ngr, data.si_type, data.si_number, data.owner, data.address, data.readings,
                        data.water_temp, data.verification_date, data.valid_date, data.air_temp, data.humidity,
                        data.atm_pressure, data.qmin, data.qmax, data.intern, data.standart, data.phone,
                        data.processing_date, user_id, data.valid_for, data.conclusion, data.verifier_surname,
                        data.verifier_name, data.verifier_patronymic, 0, data.standart_fif, data.mp,
                        data.production_date))
        connect.commit()
    else:
        return result


def get_existing_counters(data):
    cursor.execute(f"SELECT si_number, verification_date, intern  FROM uploaded_data WHERE "
                   f"si_number = '{data.si_number}' AND xml = '1'")
    result = cursor.fetchone()
    return result


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
    existing_counters = []
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
            data.si_number = str(sheet_read[f'D{i}'].value).strip()
            data.production_date = sheet_read[f'E{i}'].value
            data.owner = sheet_read[f'F{i}'].value
            data.address = sheet_read[f'G{i}'].value
            data.readings = sheet_read[f'H{i}'].value
            data.water_temp = sheet_read[f'I{i}'].value
            data.verification_date = sheet_read[f'J{i}'].value
            data.valid_date = sheet_read[f'K{i}'].value
            data.air_temp = sheet_read[f'L{i}'].value
            data.humidity = sheet_read[f'M{i}'].value
            data.atm_pressure = sheet_read[f'N{i}'].value
            data.qmin = sheet_read[f'O{i}'].value
            data.qmax = sheet_read[f'P{i}'].value
            data.intern = sheet_read[f'R{i}'].value.partition(' ')[0].upper()
            data.standart = sheet_read[f'S{i}'].value
            data.standart_fif = get_standart_fif(data)
            data.phone = sheet_read[f'T{i}'].value
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
            if data.valid_date:
                if data.verification_date.day == data.valid_date.day:
                    error = 'НЕКОРРЕКТНАЯ ДАТА ДЕЙСТВИТЕЛЬНО ДО'
                    break
            if data.verification_date > datetime.datetime.now():
                error = 'ДАТА ПОВЕРКИ В БУДУЩЕМ ПЕРИОДЕ'
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
            if not isinstance(data.readings, float) and not isinstance(data.readings, int):
                error = 'НЕКОРРЕКТНЫЕ ПОКАЗАНИЯ СЧЕТЧИКА'
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
            inserted = get_existing_counters(data)
            if inserted:
                existing_counters.append(inserted)

            i += 1
        return error, i, existing_counters
    except Exception as e:
        return e, i, existing_counters


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


def from_db_to_xml():
    query = '''SELECT result_docnum, verification_date, valid_date, si_type, verifier_surname, verifier_name 
    FROM uploaded_data WHERE fsa = 0 and result_docnum NOT NULL
    '''
    cursor.execute(query)
    return cursor.fetchall()


def set_fsa_to_1(result_docnum):
    query = '''UPDATE uploaded_data SET fsa=1 WHERE result_docnum IS ?'''
    cursor.execute(query, (result_docnum,))
    connect.commit()


def get_verifier_snils(verifier_surname):
    query = '''SELECT snils FROM real_verifiers WHERE verifier LIKE ? '''
    cursor.execute(query, (f'%{verifier_surname}%',))
    return cursor.fetchone()


def make_fsa_xml():
    # Получаем данные из базы данных
    data_from_db = from_db_to_xml()

    # Создаем корневой элемент
    root = xml.Element("Message")
    root.set("xmlns:xsi", "http://www.w3.org/2001/XMLSchema-instance")
    root.set("xsi:noNamespaceSchemaLocation", "schema.xsd")

    # Создаем элемент VerificationMeasuringInstrumentData
    vmi_data_element = xml.SubElement(root, "VerificationMeasuringInstrumentData")

    # Проходим по данным из базы и создаем элементы VerificationMeasuringInstrument
    count_records = 0
    file_counter = 1

    for data in data_from_db:
        # Если достигнуто максимальное количество записей, создаем новый файл
        if count_records == 1000:
            save_xml_file(root, file_counter)
            file_counter += 1
            count_records = 0
            # Обновляем корень и элемент для нового файла
            root = xml.Element("Message")
            root.set("xmlns:xsi", "http://www.w3.org/2001/XMLSchema-instance")
            root.set("xsi:noNamespaceSchemaLocation", "schema.xsd")
            vmi_data_element = xml.SubElement(root, "VerificationMeasuringInstrumentData")

        vmi_element = xml.SubElement(vmi_data_element, "VerificationMeasuringInstrument")

        # Добавляем подэлементы с данными
        number_verification_element = xml.SubElement(vmi_element, "NumberVerification")
        number_verification_element.text = data[0]

        date_verification_element = xml.SubElement(vmi_element, "DateVerification")
        date_verification_element.text = data[1][:10]
        if data[2]:
            date_verification_end_element = xml.SubElement(vmi_element, "DateEndVerification")



        tmi_element = xml.SubElement(vmi_element, "TypeMeasuringInstrument")
        tmi_element.text = data[3]
        aproved_employee_element = xml.SubElement(vmi_element, "ApprovedEmployee")
        name_element = xml.SubElement(aproved_employee_element, "Name")
        last_name_element = xml.SubElement(name_element, "Last")
        first_name_element = xml.SubElement(name_element, "First")
        first_name_element.text = data[5]
        last_name_element.text = data[4]
        result_element = xml.SubElement(vmi_element, "ResultVerification")
        result_element.text = '2'
        if data[2]:
            date_verification_end_element.text = data[2][:10]
            result_element.text = '1'


        # Пример использования get_verifier_snils для получения SNILS
        verifier_surname = data[4]
        snils_data = get_verifier_snils(verifier_surname)

        if snils_data:
            snils_element = xml.SubElement(aproved_employee_element, "SNILS")
            snils_element.text = snils_data[0]

        # Добавьте остальные элементы данных по аналогии...
        set_fsa_to_1(data[0])
        count_records += 1

    # Сохраняем последний XML-файл
    if count_records > 0:
        save_xml_file(root, file_counter)


def save_xml_file(root, file_counter):
    # Сохраняем XML-файл
    save_method_element = xml.SubElement(root, "SaveMethod")
    save_method_element.text = "1"
    xml_tree = xml.ElementTree(root)
    xml_tree.write(f"dyachenko_{file_counter}.xml", encoding="utf-8", xml_declaration=True)


def to_xml(user_id):
    cursor.execute(f'SELECT * FROM uploaded_data WHERE xml = "0" AND user_id = "{user_id}"')
    result = cursor.fetchall()
    cursor.execute(f'UPDATE uploaded_data SET xml = "1" WHERE xml = "0" AND user_id = "{user_id}"')
    connect.commit()
    return result


def make_xml(user_id):
    data = to_xml(user_id)
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


def file_send(file_name, user, organization, chat_id):
    url = 'http://127.0.0.1:8000/api/v1/verifications/upload/'
    file = {'file': open(file_name, 'rb')}
    data = {'user': user, 'organization':organization, 'chat_id': chat_id}
    response = requests.post(url, data=data, files=file)
    if response.status_code == 200 or response.status_code == 201:
        return response.json()


if __name__ == '__main__':
    make_fsa_xml()
