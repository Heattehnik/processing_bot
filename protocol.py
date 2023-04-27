from functions import from_db_for_protocol, get_additional_standarts, get_standart_type
from classes import Protocol
import datetime


def get_data_for_protocol():
    source_data = from_db_for_protocol()
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
            current_protocol.si_type = protocol[3]
            current_protocol.standart_num = protocol[19]
            current_protocol.qmax = float(protocol[17])
            current_protocol.qmin = float(protocol[16])
            current_protocol.atm_pressure = protocol[15]
            current_protocol.humidity = protocol[14]
            current_protocol.air_temp = protocol[13]
            current_protocol.address = protocol[6]
            current_protocol.owner = protocol[5]
            current_protocol.si_number = protocol[4]
            if protocol[10]:
                current_protocol.valid_until = datetime.datetime.strptime(protocol[10], '%Y-%m-%d %H:%M:%S') \
                    .strftime('%d.%m.%Y')
            current_protocol.readings_start = float(protocol[7])
            current_protocol.water_temp_start = protocol[8]
            current_protocol.standart_fif = protocol[20]
            current_protocol.standart = get_standart_type(current_protocol.standart_fif)
            current_protocol.set_temp()
            current_protocol.set_flow_rates()
            protocol_list.append(current_protocol)
            # print(str(current_protocol))
    return protocol_list


def protocol_data_calc(protocols):
    for protocol in protocols:
        protocol.build_protocol()


if __name__ == '__main__':
    # output = get_data_for_protocol()
    # protocol_data_calc(output)
    verifiers = ['МИНГАЛЕВ', 'КОЛОСКОВ', 'МАСКАЕВ', 'БЫКОВ', 'ТОЛСТОШЕЕВ', 'НОВИКОВ', 'СМОЛЯКОВ', 'КАЙГОРОДОВ',
                 'КУТУЗОВ', 'КАНЗЕБА', 'ГРИГОРЬЕВ', 'ЛЕГЕНЬКОВ', 'ГАЛДАНОВ', 'ГАЛИМУЛЛИН', 'ЗЛОБИН', 'ПУШАНКИН',
                 'КАШПЕРКО', 'ТЕРЕНТЬЕВ', 'ПОНОМАРЁВ', 'ДЕМИДОВ', 'МИКУШИН', 'ПЫЖЬЯНОВ', 'БЕЗИК', 'ГЕРМАНЧУК',
                 'ГУСЕВ', 'МАКАРЦЕВ', 'БУЛЫГИН', 'ЛОГИНОВ', 'МАЦЕРА', 'МУЛЛАГАЛИЕВ', 'ШАКИРОВ', 'НАЗАРОВ', 'СОКОЛОВ',
                 'АВДЕЕНКО', 'СТАТКЕВИЧ', 'ЗИНЧЕНКО', 'ЗОЛОТАРЁВ', 'КВАШНИН', 'КРИВОРОТ', 'НИКОНЕНКО', 'РЯБЦОВ',
                 'ФОМИЧЕВ', 'ЗАЕВ', 'АВИЛКИН', 'ВЕСНИН', 'ЗОБНИН', 'КОМАРСКИХ', 'ЛОБАНОВ', 'ЛОГАЧЕВ', 'КОНСТАНТИНОВ',
                 'СКУЛКИН', 'МИННИКАЕВ', 'ЯДРЫШНИКОВ', 'УГРЮМОВ', 'РОДИОНОВ', 'КУТЛУЗАМАНОВ', 'ИЗМАГИЛОВ', 'ЦЕЛЬМ',
                 'ЛАМБИН', 'МЕРЗЛЯКОВ', 'ЦАРЕГОРОДЦЕВ', 'ПЕРЕЦ', 'НАЗЫРОВ', 'НАБОКИН', 'ХРАМЦОВ', 'ГАЛНЫКИН', 'ЯКОВЛЕВ',
                 'СКОРОБОГАТОВ', 'ЕФРЕМОВ', 'САЛАГАЕВ', 'КАРПОВ', 'ЧИЛЮМОВ', 'МУХАМАДЕЕВ', 'УЙМАНОВ', 'ДЕРГАЧЕВ',
                 'ПЛЮСНИН']
    print(verifiers)
    verifiers.sort()
    print(len(verifiers))
    print(verifiers)
    number = 1
    verf_dict = {}
    for verifier in verifiers:
        verf_dict[number] = verifier
        number += 1
    print(verf_dict)
