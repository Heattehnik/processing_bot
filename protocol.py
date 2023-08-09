from functions import from_db_for_protocol, get_additional_standarts, get_standart_type
from classes import Protocol
from env import INTERNS
import datetime
from shutil import make_archive, rmtree
import os
from pathlib import Path


def get_data_for_protocol(user_id):
    source_data = from_db_for_protocol(user_id)
    protocol_list = []

    if source_data:
        for protocol in source_data:

            current_protocol = Protocol()
            current_protocol.ngr = protocol[2]
            current_protocol.mp = protocol[28]
            current_protocol.conclusion = protocol[12]
            current_protocol.verification_date = datetime.datetime.strptime(protocol[9], '%Y-%m-%d %H:%M:%S') \
                .strftime('%d.%m.%Y')
            current_protocol.verifier = f'{protocol[24]} {protocol[25]} {protocol[26]}'
            additional_standarts = get_additional_standarts(current_protocol.verifier)
            current_protocol.gigrometr = additional_standarts[23]
            current_protocol.stopwatch = additional_standarts[24]
            current_protocol.termometr = additional_standarts[22]
            current_protocol.barometr = additional_standarts[25]
            current_protocol.si_type = protocol[3]
            current_protocol.standart_num = protocol[19]
            current_protocol.qmax = float(str(protocol[17]).replace(',', '.').replace(' ', ''))
            current_protocol.qmin = float(str(protocol[16]).replace(',', '.').replace(' ', ''))
            current_protocol.atm_pressure = protocol[15]
            current_protocol.humidity = protocol[14]
            current_protocol.air_temp = protocol[13]
            current_protocol.address = protocol[6].replace('"', '').replace('\\', '/')
            current_protocol.owner = protocol[5]
            current_protocol.si_number = protocol[4]
            if protocol[10]:
                current_protocol.valid_until = datetime.datetime.strptime(protocol[10], '%Y-%m-%d %H:%M:%S') \
                    .strftime('%d.%m.%Y')
            current_protocol.readings_start = float(protocol[7].replace(',', '.').replace(' ', ''))
            current_protocol.water_temp_start = protocol[8]
            current_protocol.standart_fif = protocol[20]
            current_protocol.standart = get_standart_type(current_protocol.standart_fif)
            if protocol[30]:
                current_protocol.production_date = protocol[30]
            current_protocol.protocol_number = f"{INTERNS.get(protocol[18])}.{datetime.datetime.strptime(protocol[9], '%Y-%m-%d %H:%M:%S').strftime('%y.%m')}.{current_protocol.si_number}"
            current_protocol.set_temp()
            current_protocol.set_flow_rates()
            if current_protocol.mp == 'ГОСТ 8.156-83':
                current_protocol.flow_rates_gost()
            protocol_list.append(current_protocol)
    return protocol_list


def make_protocols(protocols):
    count = 0
    for protocol in protocols:
        protocol.build_protocol()
        count += 1
    return count


def make_zip():
    path = Path(__file__)
    print(path)
    archive_name = 'protocols'
    root_dir = os.curdir + '/protocols/'
    make_archive(archive_name, 'zip', root_dir)
    with open('protocols.zip', 'rb') as misc:
        zip_file = misc.read()
    rmtree(root_dir)
    return zip_file


if __name__ == '__main__':
    output = get_data_for_protocol(342519256)
    make_protocols(output)
