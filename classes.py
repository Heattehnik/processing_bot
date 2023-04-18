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


class Protocol:
    def __init__(self):
        self.protocol_number = None
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

    def __str__(self):
        return f'{self.ngr}\n{self.si_type}\n{self.si_number}\n{self.owner}\n{self.address}\n{self.readings_start}\n' \
               f'{self.water_temp_start}\n{self.verification_date}\n{self.valid_until}\n{self.conclusion}\n' \
               f'{self.air_temp}\n{self.humidity}\n{self.atm_pressure}\n{self.qmin}\n{self.qmax}\n{self.standart}\n' \
               f'{self.verifier}\n'

    # def



