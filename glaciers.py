import codecs
import csv
import re
import utils
import matplotlib.pyplot as plt


class Glacier:
    def __init__(self, glacier_id, name, unit, lat, lon, code):
        if len(glacier_id) != 5:
            raise ValueError("The unique ID must be comprised of exactly 5 digits")
        if (lat < -90.) | (lat > 90.) | (lon < -180.) | (lon > 180.):
            raise ValueError("the latitude should be between -90 and 90, the longitude between -180 and 180")
        if (len(unit) != 2) | ((unit.isupper() == False) & (unit != "99")):
            raise ValueError("The political unit must be a string of length 2, composed only of capital letters or the special value ”99”")

        self.glacier_id = glacier_id
        self.name = name
        self.unit = unit
        self.lat = lat
        self.lon = lon
        self.code = code
        self.mass_balance_measurement = {}

    def add_mass_balance_measurement(self, year, mass_balance, partial):
        str_year = str(year)
        if str_year > "2021":
            raise ValueError("The year of measurement cannot be in the future")
        if (str_year not in self.mass_balance_measurement.keys()) & (not partial) & (mass_balance != ''):
            int_mass_balance = int(mass_balance)
            self.mass_balance_measurement[str_year] = [int_mass_balance, partial]
        elif (str_year not in self.mass_balance_measurement.keys()) & partial & (mass_balance != ''):
            int_mass_balance = int(mass_balance)
            self.mass_balance_measurement[str_year] = [int_mass_balance, partial]
        elif (str_year in self.mass_balance_measurement.keys()) & partial & (mass_balance != ''):
            int_mass_balance = int(mass_balance)
            ini = int(self.mass_balance_measurement[str_year][0])
            new = ini + int_mass_balance
            self.mass_balance_measurement[str_year][0] = new
        else:
            pass

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
        self.glacier_id_list = []
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

        for item in self.Glacier_Collections:
            self.glacier_id_list.append(item.glacier_id)

    def read_mass_balance_data(self, file_path):
        with open(file_path, "r", encoding="utf-8") as csvfile:
            read = csv.reader(csvfile)
            head = next(read)
            for i in read:
                if i[2] not in self.glacier_id_list:
                    raise ValueError(f"The mass measurement data item with "
                                     f"glacier ID {i[2]} is not defined in the glacier collection")
        for glacier in self.Glacier_Collections:
            with open(file_path, "r", encoding="utf-8") as csvfile:
                read = csv.reader(csvfile)
                head = next(read)
                for i in read:
                    if i[1] == glacier.name:
                        glacier.add_mass_balance_measurement(i[3], i[11], i[4] != '9999')

    def find_nearest(self, lat, lon, n=5):
        """Get the n glaciers closest to the given coordinates."""

        float_lat = float(lat)
        float_lon = float(lon)

        if (float_lat < -90.) | (float_lat > 90.) | (float_lon < -180.) | (float_lon > 180.):
            raise ValueError("the latitude should be between -90 and 90, the longitude between -180 and 180")
        dic = {}
        for i in self.Raw_Glacier_Collections:
            lati = float(i['LATITUDE'])
            loni = float(i['LONGITUDE'])
            if (lati < -90.) | (lati > 90.) | (loni < -180.) | (loni > 180.):
                raise ValueError("the latitude should be between -90 and 90, the longitude between -180 and 180")

            namei = i['NAME']
            dic[namei] = utils.haversine_distance(float_lat, float_lon, lati, loni)
        sorted_dic = sorted(dic.items(), key=lambda d: d[1], reverse=False)
        order = [i[0] for i in sorted_dic]
        return order[0:n]

    def filter_by_code(self, code_pattern):
        """Return the names of glaciers whose codes match the given pattern."""
        if (type(code_pattern) != int) & (type(code_pattern) != str):
            raise TypeError("Please use a valid code type like string or integer")
        code_ = str(code_pattern)
        if len(code_) != 3:
            raise ValueError("Please use the code with exact 3 digits")
        for i in code_:
            if (not i.isdigit()) & (i != "?"):
                raise ValueError("Please input the code only with digit or '?'")

        glacier_names = []
        ques_mark_num = code_.count('?')
        if ques_mark_num == 0:
            for i in self.Raw_Glacier_Collections:
                three_digit = i['PRIM_CLASSIFIC'] + i['FORM'] + i['FRONTAL_CHARS']
                if three_digit == code_:
                    glacier_names.append(i['NAME'])
        elif ques_mark_num == 1:
            index = int(code_.find('?'))
            for i in self.Raw_Glacier_Collections:
                if (index == 0) & (i['FORM'] == code_[1]) & (i['FRONTAL_CHARS'] == code_[2]):
                    glacier_names.append(i['NAME'])
                elif (index == 1) & (i['PRIM_CLASSIFIC'] == code_[0]) & (i['FRONTAL_CHARS'] == code_[2]):
                    glacier_names.append(i['NAME'])
                elif (index == 2) & (i['PRIM_CLASSIFIC'] == code_[0]) & (i['FORM'] == code_[1]):
                    glacier_names.append(i['NAME'])
        elif ques_mark_num == 2:
            index = int(re.search("\\d", code_).start())
            value = re.search("\\d", code_).group()
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
        shrunk_percentage = '{:.0%}'.format(negative_change / has_mass_balance)
        display1 = "This collection has " + glaciers_num + " glaciers."
        display2 = "The earliest measurement was in " + earliest_year + "."
        display3 = shrunk_percentage + " of glaciers shrunk in their last measurement."
        print('\n' + display1, '\n' + display2, '\n' + display3)

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
        x = [grow_glacier_name + ": " + grow_glacier_year, shrunk_glacier_name + ": " + shrunk_glacier_year]
        y = [sorted_dic[-1][1], sorted_dic[0][1]]
        plt.figure(figsize=(8, 7))
        plt.bar(x, y, 0.4)
        plt.xlabel("X-axis: Glaciers and their extreme year")
        plt.ylabel("Y-axis: Mass balance measurements")
        plt.title("Extreme chart")

        plt.savefig(output_path)
        plt.show()
