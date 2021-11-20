import codecs
import csv
import re
import utils

class Glacier:
    def __init__(self, glacier_id, name, unit, lat, lon, code):
        if (type(glacier_id) == str) & (type(name) == str) \
                & (type(unit) == str) & (type(lat) == float) \
                & (type(lon) == float) & (type(code) == int):
            self.glacier_id = glacier_id
            self.name = name
            self.unit = unit
            self.lat = lat
            self.lon = lon
            self.code = code
            self.mass_balance_measurement = {}
        else:
            print("Please use the valid data type.")

    def add_mass_balance_measurement(self, year, mass_balance, partial):
        self.mass_balance_measurement[year] = [mass_balance, partial]

    def plot_mass_balance(self, output_path):
        raise NotImplementedError


class GlacierCollection:

    def __init__(self, file_path):
        self.csv_file_path = file_path
        self.Raw_Glacier_Collections = []
        self.Glacier_Collections = []
        with codecs.open(self.csv_file_path, 'r', encoding='utf-8') as fp:
            fp_key = csv.reader(fp)
            for csv_key in fp_key:
                csv_reader = csv.DictReader(fp, fieldnames=csv_key)
                for row in csv_reader:
                    self.Raw_Glacier_Collections.append(dict(row))
        for item in self.Raw_Glacier_Collections:
            three_digit = str(item['PRIM_CLASSIFIC'] + item['FORM'] + item['FRONTAL_CHARS'])
            glacier = Glacier(item['WGMS_ID'], item['NAME'], item['POLITICAL_UNIT'],
                              float(item['LATITUDE']), float(item['LONGITUDE']),
                              int(three_digit))
            self.Glacier_Collections.append(glacier)

    def read_mass_balance_data(self, file_path):
        for glacier in self.Glacier_Collections:
            with open(file_path, "r", encoding="utf-8") as csvfile:
                read = csv.reader(csvfile)
                for i in read:
                    if i[1] == glacier.name:
                        if (i[3] not in glacier.mass_balance_measurement.keys()) & (i[4] == '9999') & (i[11] != ''):
                            glacier.add_mass_balance_measurement(i[3], int(i[11]), False)
                        elif (i[3] not in glacier.mass_balance_measurement.keys()) & (i[4] != '9999') & (i[11] != ''):
                            glacier.add_mass_balance_measurement(i[3], int(i[11]), True)
                        elif (i[3] in glacier.mass_balance_measurement.keys()) & (i[4] != '9999') & (i[11] != ''):
                            ini = int(glacier.mass_balance_measurement[i[3]][0])
                            new = ini + int(i[11])
                            glacier.mass_balance_measurement[i[3]][0] = new
                        else:
                            pass
        for i in self.Glacier_Collections:
            print(i.name, " mass balance measurement:", i.mass_balance_measurement)

    def find_nearest(self, lat, lon, n=5):
        """Get the n glaciers closest to the given coordinates."""
        dic = {}
        for i in self.Raw_Glacier_Collections:
            lati = float(i['LATITUDE'])
            loni = float(i['LONGITUDE'])
            namei = i['NAME']
            dic[namei] = utils.haversine_distance(lat, lon, lati, loni)
        sorted_dic = sorted(dic.items(), key=lambda d: d[1], reverse=False)
        order = [i[0] for i in sorted_dic]
        return order[0:n]

    def filter_by_code(self, code_pattern):
        """Return the names of glaciers whose codes match the given pattern."""
        glacier_names = []
        code_ = str(code_pattern)
        ques_mark_num = code_pattern.count('?')
        if ques_mark_num == 0:
            for i in self.Raw_Glacier_Collections:
                three_digit = i['PRIM_CLASSIFIC'] + i['FORM'] + i['FRONTAL_CHARS']
                if three_digit == code_:
                    glacier_names.append(i['NAME'])
        elif ques_mark_num == 1:
            index = int(code_pattern.find('?'))
            iter = re.finditer("\d", code_pattern)
            lis = []
            for i in iter:
                lis.append(code_pattern[i.span()[0]])
            for i in self.Raw_Glacier_Collections:
                if index == 0 & (i['FORM'] == lis[0]) & (i['FRONTAL_CHARS'] == lis[1]):
                    glacier_names.append(i['NAME'])
                elif index == 1 & (i['PRIM_CLASSIFIC'] == lis[0]) & (i['FRONTAL_CHARS'] == lis[1]):
                    glacier_names.append(i['NAME'])
                elif index == 2 & (i['PRIM_CLASSIFIC'] == lis[0]) & (i['FORM'] == lis[1]):
                    glacier_names.append(i['NAME'])
        elif ques_mark_num == 2:
            index = int(re.search("\d",code_pattern).start())
            value = re.search("\d", code_pattern).group()
            for i in self.Raw_Glacier_Collections:
                if (index == 0) & (i['PRIM_CLASSIFIC'] == value):
                    glacier_names.append(i['NAME'])
                elif (index == 1) & (i['FORM'] == value):
                    glacier_names.append(i['NAME'])
                elif (index == 2) & (i['FRONTAL_CHARS'] == value):
                    glacier_names.append(i['NAME'])
        else:
            for i in self.Raw_Glacier_Collections:
                glacier_names.append(i['NAME'])

        return glacier_names

    def sort_by_latest_mass_balance(self, n=5, reverse=False):
        """Return the N glaciers with the highest area accumulated in the last measurement."""
        dic = {}
        for glacier in self.Glacier_Collections:
            if glacier.mass_balance_measurement.keys():
                els = list(glacier.mass_balance_measurement.items())
                latest = els[-1][1][0]
                dic[glacier] = latest
        sorted_dic = sorted(dic.items(), key=lambda d: d[1], reverse=not reverse)
        order = [i for i in sorted_dic]
        return order[0:n]


    def summary(self):
        raise NotImplementedError

    def plot_extremes(self, output_path):
        raise NotImplementedError
