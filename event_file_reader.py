import json
import zipfile
import io
import struct
import numpy as np


class Event:
    NUMBER_OF_COMPONENTS = 3

    def __init__(self):
        self.header = ""
        self.catInfo = CatalogInfo()
        self.signalData = None

    @property
    def numberOfChannels(self):
        return self.signalData.shape[0] * Event.NUMBER_OF_COMPONENTS


class Datchik:
    def __init__(self):
        self.Line = 0
        self.Introduction = False
        self.IntroID = 0
        self.x = 0
        self.y = 0
        self.z = 0
        self.introInX = 0
        self.Name = ""
        self.v=0


class EventType:
    def __init__(self):
        self.alias = ""


class CatalogInfo:
    def __init__(self):
        self.etype = EventType()
        self.timeMine = ""
        self.E = 0.0
        self.x = 0
        self.y = 0
        self.z = 0

    def printMe(self):
        print(f"E={self.E}, x={self.x}, y={self.y}, z={self.z}")


class Header:
    def __init__(self):
        self.datchiki = []
    def giveMexyz(self):
        stations=()
        times=()
        initional=()
        for d in self.datchiki:
            if d.Introduction==True:
                print('YESS')
                stations.append((d.x, d.y, d.z))
                times.append(d.introInX)
                initional[0] += d.x
                initional[1] += d.y
                initional[2] += d.z
                initional[3] += d.introInX
        for i in range(3):
            a = initional[i] / len(self.datchiki)
            initional[i] = a
    def printMe(self):
        print(f'num={len(self.datchiki)}')
        for d in self.datchiki:
            print(f'Line={d.Line}, x={d.x}, y={d.y}, z={d.z}, intro={d.introInX}, hasIntro={d.Introduction}')


def unzip_mem(zipped_buffer):
    with zipfile.ZipFile(io.BytesIO(zipped_buffer)) as archive:
        entry = archive.infolist()[0]
        with archive.open(entry) as unzipped_entry_stream:
            return unzipped_entry_stream.read()


def string_from_bytes_a(data, offset):
    str_size = int.from_bytes(data[offset:offset + 4], byteorder='little')
    offset += 4
    str_bytes = data[offset:offset + str_size]
    offset += str_size
    return str_bytes.decode('cp1251'), offset


def readXYZfromJSON(jsonObj, e):
    e.x = jsonObj['x']
    e.y = jsonObj['y']
    e.z = jsonObj['z']


def init_signal_data_array(number_of_gauges, number_of_samples=0):
    signal_data = np.empty((number_of_gauges, Event.NUMBER_OF_COMPONENTS), dtype=object)
    for m in range(number_of_gauges):
        for l in range(Event.NUMBER_OF_COMPONENTS):
            signal_data[m, l] = None if number_of_samples == 0 else np.zeros(number_of_samples, dtype=np.float32)
    return signal_data


def readGaugeData(header_json):
    h = Header()
    for d in header_json['datchiki']:
        gauge = Datchik()
        readXYZfromJSON(d, gauge)
        gauge.Line = d['Line']
        gauge.Introduction = d['Introduction']
        gauge.introInX = d['introInX']
        gauge.Name = d['Name']
        gauge.v=d['v']
        h.datchiki.append(gauge)
    return h


def readCatalogInfo(sr_json):
    ci = CatalogInfo()
    readXYZfromJSON(sr_json, ci)
    ci.E = sr_json['E']
    return ci


def readJSON(cat_json):
    return json.loads(cat_json)


def try_read(db_data):
    MODERN_DBID = 2718281828459045
    orig_db_data_offset = 0
    version_id = struct.unpack_from('q', db_data, orig_db_data_offset)[0]
    orig_db_data_offset += struct.calcsize('q')

    if version_id == MODERN_DBID:
        zipped = db_data[orig_db_data_offset:]
        data = unzip_mem(zipped)
        offset = 0

        header_json, offset = string_from_bytes_a(data, offset)
        # print(header_json)
        db_rec_json, offset = string_from_bytes_a(data, offset)

        seis_rec_json = ""
        if data[offset] == 1:  # if event is processed
            offset += 1
            seis_rec_json, offset = string_from_bytes_a(data, offset)
        header = readGaugeData(readJSON(header_json))
        catalogInfo = readCatalogInfo(readJSON(seis_rec_json))
        NUMBER_OF_GAUGES = len(header.datchiki)
        NUMBER_OF_CHANNELS = NUMBER_OF_GAUGES * Event.NUMBER_OF_COMPONENTS
        sample_length = (len(data) - offset) // (struct.calcsize('h') * NUMBER_OF_CHANNELS)
        signal_data = init_signal_data_array(NUMBER_OF_GAUGES, sample_length)

        for ch in range(NUMBER_OF_CHANNELS):
            for i in range(sample_length):
                value = struct.unpack_from('h', data, offset)[0]
                g, c = divmod(ch, 3)
                signal_data[g, c][i] = value
                offset += struct.calcsize('h')

        event = Event()
        event.signalData = signal_data

        event.header = header
        event.catInfo = catalogInfo
        # print(json.dumps(readJSON(seis_rec_json), indent=2))
        return event
    else:
        return None
def load_file_as_byte_array(file_path):
    with open(file_path, "rb") as file:
        byte_array = file.read()
    return byte_array
def load_event_from_path(file_path):
    event=try_read(load_file_as_byte_array(file_path))
    return event
