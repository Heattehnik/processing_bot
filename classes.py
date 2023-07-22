import random
from docxtpl import DocxTemplate
import os


class Data:
    def __init__(self):
        self.act_num = None
        self.ngr = None
        self.si_type = None
        self.si_number = None
        self.owner = None
        self.address = None
        self.readings = None
        self.water_temp = None
        self.verification_date = None
        self.valid_date = None
        self.air_temp = None
        self.humidity = None
        self.atm_pressure = None
        self.qmin = None
        self.qmax = None
        self.intern = None
        self.standart = None
        self.standart_fif = None
        self.phone = None
        self.processing_date = None
        self.valid_for = None
        self.verifier_surname = None
        self.verifier_name = None
        self.verifier_patronymic = None
        self.conclusion = None
        self.mp = None
        self.production_date = None


class Protocol:
    def __init__(self):
        self.protocol_number = 'None'
        self.address = None
        self.si_type = None
        self.ngr = None
        self.si_number = None
        self.owner = None
        self.verification_date = None
        self.valid_until = None
        self.mp = None
        self.air_temp = None
        self.water_temp_start = None
        self.water_temp_end = None
        self.humidity = None
        self.atm_pressure = None
        self.readings_start = None
        self.readings_middle_start = None
        self.readings_middle_end = None
        self.readings_end = None
        self.standart_num = None
        self.termometr = None
        self.gigrometr = None
        self.stopwatch = None
        self.barometr = None
        self.qmin = None
        self.vminsi = None
        self.vminstd = None
        self.pmin = None
        self.qtransitional = None
        self.standart = None
        self.vtransitionalsi = None
        self.vtransitionalst = None
        self.ptransitional = None
        self.qmax = None
        self.vmaxsi = None
        self.vmaxst = None
        self.pmax = None
        self.verifier = None
        self.conclusion = None
        self.intern = None
        self.standart_fif = None
        self.production_date = ''

    def __str__(self):
        return f'{self.ngr}\n{self.si_type}\n{self.si_number}\n{self.owner}\n{self.address}\n{self.readings_start}\n' \
               f'{self.water_temp_start}\n{self.verification_date}\n{self.valid_until}\n{self.conclusion}\n' \
               f'{self.air_temp}\n{self.humidity}\n{self.atm_pressure}\n{self.qmin}\n{self.qmax}\n{self.standart}\n' \
               f'{self.verifier}\n'

    def set_temp(self):
        if self.water_temp_start > 35:
            self.water_temp_end = self.water_temp_start + random.randrange(1, 3)
        else:
            self.water_temp_end = self.water_temp_start - random.randrange(1, 3)

    def set_flow_rates(self):
        self.pmin = round(random.randrange(-4, 4) + (random.randrange(0, 100)) / 100, 2)
        self.vminstd = round(self.qmin / 3600 * 1000 * 720, 2)
        self.vminsi = round(self.vminstd + (self.vminstd * (self.pmin / 100)), 2)
        if self.qmin >= 0.06:
            self.qtransitional = round((0.15 + (random.randrange(-14, 14) / 1000)) * 1.1, 2)
        else:
            self.qtransitional = round((0.12 + (random.randrange(-11, 11) / 1000)) * 1.1, 2)
        self.vtransitionalst = round(self.qtransitional / 3600 * 1000 * 360, 2)
        if self.valid_until:
            if self.pmin > 0:
                self.ptransitional = round(random.uniform(0, 1.9), 2)
            else:
                self.ptransitional = round(random.uniform(-1.9, 0), 2)

            self.vtransitionalsi = round(self.vtransitionalst + (self.vtransitionalst * (self.ptransitional / 100)), 2)
            if self.ptransitional > 0:
                self.pmax = round(random.uniform(0, 1.9), 2)
            else:
                self.pmax = round(random.uniform(-1.9, 0), 2)
            self.vmaxst = round(float(self.qmax) / 3600 * 1000 * 120, 2)
            self.vmaxsi = round(self.vmaxst + (self.vmaxst * (self.pmax / 100)), 2)
            self.readings_end = round(self.readings_start + (self.vminsi + self.vtransitionalsi + self.vmaxsi) / 1000,
                                      3)
        else:
            if self.pmin > 0:
                self.ptransitional = round(random.uniform(0, 6), 2)
            else:
                self.ptransitional = round(random.uniform(-6, 0), 2)

            self.vtransitionalsi = round(self.vtransitionalst + (self.vtransitionalst * (self.ptransitional / 100)), 2)

            if -2 < self.ptransitional < 0 or 0 < self.ptransitional < 2:
                self.vmaxst = round(float(self.qmax) / 3600 * 1000 * 120, 2)
                if self.ptransitional > 0:
                    self.pmax = round(random.uniform(2, 5), 2)
                else:
                    self.pmax = round(random.uniform(-5, -2), 2)
                self.vmaxsi = round(self.vmaxst + (self.vmaxst * (self.pmax / 100)), 2)
                self.readings_end = round(
                    self.readings_start + (self.vminsi + self.vtransitionalsi + self.vmaxsi) / 1000, 3)
            else:
                self.qmax = ''
                self.pmax = ''
                self.vmaxsi = ''
                self.vmaxst = ''
                self.readings_end = round(self.readings_start + (self.vminsi + self.vtransitionalsi) / 1000, 3)

    def flow_rates_gost(self):
        self.readings_start = round(self.readings_start * 1000, 2)
        self.qmax = round(1.5 - random.uniform(0, 0.15), 2)
        self.vmaxst = 0.02 * 1000
        self.pmax = round(random.uniform(-2, 2), 2)
        self.vmaxsi = self.vmaxst + (self.vmaxst * (self.pmax / 100))
        self.readings_middle_start = round(self.readings_start + self.vmaxsi, 2)
        self.qtransitional = round(0.15 + random.uniform(0, 0.015), 3)
        self.vtransitionalst = 0.005 * 1000
        self.ptransitional = round(random.uniform(-2, 2), 2)
        self.vtransitionalsi = self.vtransitionalst + (self.vtransitionalst * (self.ptransitional / 100))
        self.readings_middle_end = round(self.readings_middle_start + self.vtransitionalsi, 2)
        self.qmin = round(0.03 + random.uniform(0, 0.003), 3)
        self.vminstd = 0.0025 * 1000
        self.pmin = round(random.uniform(-5, 5), 2)
        self.vminsi = self.vminstd + (self.vminstd * (self.pmin / 100))
        self.readings_end = round(self.readings_middle_end + self.vminsi, 2)
        if not self.valid_until:
            self.pmax = round(random.uniform(-5, 5), 2)
            self.vmaxsi = self.vmaxst + (self.vmaxst * (self.pmax / 100))
            self.readings_middle_start = round(self.readings_start + self.vmaxsi, 2)
            if 2 >= self.pmax >= 0 or 0 >= self.pmax >= -2:
                self.ptransitional = round(random.uniform(-5, 5), 2)
                self.vtransitionalsi = self.vtransitionalst + (self.vtransitionalst * (self.ptransitional / 100))
                self.readings_middle_end = round(self.readings_middle_start + self.vtransitionalsi, 2)
                if 2 >= self.ptransitional >= 0 or 0 >= self.ptransitional >= -2:
                    self.pmin = round(random.uniform(5, 10), 2)
                    self.vminsi = self.vminstd + (self.vminstd * (self.pmin / 100))
                    self.readings_end = round(self.readings_middle_end + self.vminsi, 2)
                else:
                    self.qmin = ''
                    self.readings_end = ''
                    self.vminstd = ''
                    self.pmin = ''
            else:
                self.qtransitional = ''
                self.readings_middle_end = ''
                self.vtransitionalst = ''
                self.ptransitional = ''
                self.qmin = ''
                self.readings_end = ''
                self.vminstd = ''
                self.pmin = ''

    def build_protocol(self):
        context = {
            'protocol_number': self.protocol_number,
            'address': self.address,
            'si_type': self.si_type,
            'ngr': self.ngr,
            'si_number': self.si_number,
            'owner': self.owner,
            'verification_date': self.verification_date,
            'mp': self.mp,
            'air_temp': self.air_temp,
            'water_temp_start': self.water_temp_start,
            'water_temp_end': self.water_temp_end,
            'humidity': self.humidity,
            'atm_pressure': self.atm_pressure,
            'readings_start': self.readings_start,
            'readings_end': self.readings_end,
            'readings_middle_start': self.readings_middle_start,
            'readings_middle_end': self.readings_middle_end,
            'standart': self.standart,
            'termometr': self.termometr,
            'gigrometr': self.gigrometr,
            'stopwatch': self.stopwatch,
            'barometr': self.barometr,
            'qmin': self.qmin,
            'vminsi': self.vminsi,
            'vminst': self.vminstd,
            'pmin': self.pmin,
            'qtransitional': self.qtransitional,
            'vtransitionalsi': self.vtransitionalsi,
            'vtransitionalst': self.vtransitionalst,
            'ptransitional': self.ptransitional,
            'qmax': self.qmax,
            'vmaxsi': self.vmaxsi,
            'vmaxst': self.vmaxst,
            'pmax': self.pmax,
            'verifier': self.verifier,
            'conclusion': self.conclusion,
            'standart_num': self.standart_num,
            'production_date': self.production_date

        }
        if not os.path.exists('protocols'):
            os.mkdir('protocols')
        doc = DocxTemplate('MI1592-2015.docx')
        if self.mp == 'ГОСТ 8.156-83':
            doc = DocxTemplate('GOST 8.156-83.docx')
        doc.render(context)
        doc.save(f"protocols/{self.verification_date}-"
                 f"{self.protocol_number.replace('/', '.')}-{self.conclusion}-"
                 f"{self.si_type.replace('/', '.')}-{self.si_number.replace('/', '.')}-"
                 f"{self.address.replace('/', '.')}.docx")
