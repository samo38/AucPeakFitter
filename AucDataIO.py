import numpy as np
import struct


class AucRawData:

    # __slots__ = 'type', 'cell', 'channel', 'description', 'xvalues', 'rvalues', 'stddevs', \
    #             'temperature', 'rpm', 'seconds', 'omega2t', 'wavelength', 'delta_r'

    def __int__(self):
        self.__set_none()

    def __set_none(self):
        self.type = None
        self.cell = None
        self.channel = None
        self.description = None
        self.xvalues = None
        self.rvalues = None
        self.stddevs = None
        self.temperature = None
        self.rpm = None
        self.seconds = None
        self.omega2t = None
        self.wavelength = None

    def read(self, filename):
        encoding = 'utf-8'
        ss_reso = 100.0
        with open(filename, 'rb') as file:
            all_bytes = file.read()
        n = 0
        magic, n = AucRawData.byte2type(all_bytes, n, 4, '4s')
        if magic.decode(encoding) != "UCDA":
            return False
        version, n = AucRawData.byte2type(all_bytes, n, 2, '2s')
        if int(version) > 5:
            return False
        wvlf_new = int(version) > 4
        data, n = AucRawData.byte2type(all_bytes, n, 2, '2s')
        self.type = data.decode(encoding)
        type_list = ['RA', 'IP', 'RI', 'FI', 'WA', 'WI']
        if self.type not in type_list:
            self.__set_none()
            return False
        self.cell = int.from_bytes(all_bytes[n: n + 1], byteorder='little')
        n += 1
        self.channel = all_bytes[n: n + 1].decode(encoding)
        n += 1
        GUID, n = AucRawData.byte2type(all_bytes, n, 16, '16s')
        data, n = AucRawData.byte2type(all_bytes, n, 240, '<240s')
        desc = []
        for i in range(len(data)):
            if data[i] != 0:
                desc.append(data[i: i + 1].decode(encoding))
        self.description = ''.join(desc)
        min_radius, n = AucRawData.byte2type(all_bytes, n, 4, '<f', 3)
        max_radius, n = AucRawData.byte2type(all_bytes, n, 4, '<f', 3)
        delta_r, n = AucRawData.byte2type(all_bytes, n, 4, '<f', 3)
        n_points = int(round((max_radius - min_radius + delta_r) / delta_r))
        self.xvalues = np.round(np.linspace(min_radius, max_radius, n_points), 3)
        min_data1, n = AucRawData.byte2type(all_bytes, n, 4, '<f')
        max_data1, n = AucRawData.byte2type(all_bytes, n, 4, '<f')
        min_data2, n = AucRawData.byte2type(all_bytes, n, 4, '<f')
        max_data2, n = AucRawData.byte2type(all_bytes, n, 4, '<f')
        n_scans, n = AucRawData.byte2type(all_bytes, n, 2, '<H')
        factor1 = (max_data1 - min_data1) / 65535.0
        factor2 = (max_data2 - min_data2) / 65535.0
        std_state = min_data2 != 0.0 or max_data2 != 0.0
        temperature, rpm, seconds = [], [], []
        omega2t, wavelength = [], []
        rvalues, stddevs = [], []
        for _ in range(n_scans):
            chk, n = AucRawData.byte2type(all_bytes, n, 4, '4s')
            if chk.decode(encoding) != 'DATA':
                self.__set_none()
                return False
            data, n = AucRawData.byte2type(all_bytes, n, 4, '<f')
            temperature.append(data)
            data, n = AucRawData.byte2type(all_bytes, n, 4, '<f')
            rpm.append(round(data / ss_reso) * ss_reso)
            data, n = AucRawData.byte2type(all_bytes, n, 4, '<f')
            seconds.append(data)
            data, n = AucRawData.byte2type(all_bytes, n, 4, '<f')
            omega2t.append(data)
            data, n = AucRawData.byte2type(all_bytes, n, 2, '<H')
            if wvlf_new:
                wavelength.append(data / 10.0)
            else:
                wavelength.append(data / 100.0 + 180.0)
            data, n = AucRawData.byte2type(all_bytes, n, 4, '<f')
            n_values, n = AucRawData.byte2type(all_bytes, n, 4, '<i')
            yval = []
            sval = []
            for _ in range(n_values):
                data, n = AucRawData.byte2type(all_bytes, n, 2, '<H')
                yval.append(data * factor1 + min_data1)
                if std_state:
                    data, n = AucRawData.byte2type(all_bytes, n, 2, '<H')
                    sval.append(data * factor2 + min_data2)
                else:
                    sval.append(0.0)
            rvalues.append(yval)
            stddevs.append(sval)
            size_bytes = int((n_values + 7) / 8)
            data, n = AucRawData.byte2type(all_bytes, n, size_bytes, f'{size_bytes}s')
        self.temperature = np.array(temperature, dtype=np.float32)
        self.rpm = np.array(rpm, dtype=np.float32)
        self.seconds = np.array(seconds, dtype=np.float32)
        self.omega2t = np.array(omega2t, dtype=np.float32)
        self.wavelength = np.array(wavelength, dtype=np.float32)
        self.rvalues = np.array(rvalues, dtype=np.float32)
        self.stddevs = np.array(stddevs, dtype=np.float32)
        return True

    @staticmethod
    def byte2type(variable, idx, n, fmt, dec=-1):
        converted = struct.unpack(fmt, variable[idx: idx + n])[0]
        if 'f' in fmt and dec > 0:
            return round(converted, dec), idx + n
        return converted, idx + n
