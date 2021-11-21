import codecs
import csv
import re
import utils
import matplotlib.pyplot as plt


class Glacier:
    def __init__(self, glacier_id, name, unit, lat, lon, code):
        if (type(glacier_id) == str) & (type(name) == str) \
                & (type(unit) == str) & (type(lat) == float) \
                & (type(lon) == float) & (type(code) == int):
            # if len(glacier_id) != 5:
            #     raise ValueError("The unique ID must be comprised of exactly 5 digits")
            if (lat < -90.) | (lat > 90.) | (lon < -180.) | (lon > 180.):
                raise ValueError("the latitude should be between -90 and 90, the longitude between -180 and 180")
            if (len(unit) != 2) | ((unit.isupper() == False) & (unit != "99")):
                raise ValueError("The political unit must be a string of length 2, composed only of capital letters"
                                 " or the special value ”99”")

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
        if not self.mass_balance_measurement:
            print("There is no mass balance measurement of this glacier")
        else:
            x = self.mass_balance_measurement.keys()
            y = [self.mass_balance_measurement[i][0] for i in x]
            plt.figure(figsize=(8, 7))
            plt.bar(x, y, 0.4)
            plt.xlabel("X-axis: Years")
            plt.ylabel("Y-axis: Mass balance measurements")
            plt.title("Mass measurements chart")

            plt.savefig(output_path)
            plt.show()


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
                head = next(read)
                for i in read:
                    if i[3] > "2021":
                        raise ValueError("The year of measurement cannot be in the future")
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
            if i.mass_balance_measurement:
                print(i.name, " has mass balance measurement:", i.mass_balance_measurement)

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
            iter_ = re.finditer("\\d", code_pattern)
            lis = []
            for i in iter_:
                lis.append(code_pattern[i.span()[0]])
            for i in self.Raw_Glacier_Collections:
                if index == 0 & (i['FORM'] == lis[0]) & (i['FRONTAL_CHARS'] == lis[1]):
                    glacier_names.append(i['NAME'])
                elif index == 1 & (i['PRIM_CLASSIFIC'] == lis[0]) & (i['FRONTAL_CHARS'] == lis[1]):
                    glacier_names.append(i['NAME'])
                elif index == 2 & (i['PRIM_CLASSIFIC'] == lis[0]) & (i['FORM'] == lis[1]):
                    glacier_names.append(i['NAME'])
        elif ques_mark_num == 2:
            index = int(re.search("\\d", code_pattern).start())
            value = re.search("\\d", code_pattern).group()
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
            if glacier.mass_balance_measurement:
                measurement_list = list(glacier.mass_balance_measurement.items())
                latest = measurement_list[-1][1][0]
                dic[glacier] = latest
        sorted_dic = sorted(dic.items(), key=lambda d: d[1], reverse=not reverse)
        order = [i[0] for i in sorted_dic]
        return order[0:n]

    def summary(self):
        glaciers_num = str(len(self.Glacier_Collections))
        measure_years = []
        for glacier in self.Glacier_Collections:
            if glacier.mass_balance_measurement:
                measurement_list = list(glacier.mass_balance_measurement.items())
                latest = measurement_list[0][0]
                measure_years.append(int(latest))
        earliest_year = str(min(measure_years))
        has_mass_balance = 0
        negative_change = 0
        for glacier in self.Glacier_Collections:
            if glacier.mass_balance_measurement:
                has_mass_balance += 1
                measurement_list = list(glacier.mass_balance_measurement.items())
                if measurement_list[-1][1][0] < 0:
                    negative_change += 1
        shrunk_percentage = '{:.0%}'.format(negative_change/has_mass_balance)
        display1 = "This collection has " + glaciers_num + " glaciers."
        display2 = "The earliest measurement was in " + earliest_year + "."
        display3 = shrunk_percentage + " of glaciers shrunk in their last measurement."
        print('\n'+display1, '\n'+display2, '\n'+display3)

    def plot_extremes(self, output_path):
        dic = {}
        for glacier in self.Glacier_Collections:
            if glacier.mass_balance_measurement:
                measurement_list = list(glacier.mass_balance_measurement.items())
                latest = measurement_list[-1][1][0]
                dic[glacier] = latest
        sorted_dic = sorted(dic.items(), key=lambda d: d[1], reverse=False)
        print(sorted_dic)
        grow_glacier_name = sorted_dic[-1][0].name
        grow_glacier_year = list(sorted_dic[-1][0].mass_balance_measurement.keys())[-1]
        shrunk_glacier_name = sorted_dic[0][0].name
        shrunk_glacier_year = list(sorted_dic[0][0].mass_balance_measurement.keys())[-1]
        x = [grow_glacier_name+": "+grow_glacier_year, shrunk_glacier_name+": "+shrunk_glacier_year]
        y = [sorted_dic[-1][1], sorted_dic[0][1]]
        plt.figure(figsize=(8, 7))
        plt.bar(x, y, 0.4)
        plt.xlabel("X-axis: Glaciers and their extreme year")
        plt.ylabel("Y-axis: Mass balance measurements")
        plt.title("Extreme chart")

        plt.savefig(output_path)
        plt.show()
