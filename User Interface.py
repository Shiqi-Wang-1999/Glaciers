from pathlib import Path
from glaciers import Glacier, GlacierCollection


# file_path = Path("C:/PycharmProjects/data/sheet-A.csv")
# collection = GlacierCollection(file_path)
glacier = Glacier('01678', 'mountain', 'CH', 46.37, 7.37, 600)
# glacier.add_mass_balance_measurement("2023", 200, True)
#print(collection.find_nearest("-80","120",5))
# print(collection.Raw_Glacier_Collections)
#print(collection.filter_by_code("?18"))

#print(collection.find_nearest(-41.45,-71,10))
# file_path1 = Path("C:/PycharmProjects/data/sheet-EE.csv")
# #
# collection.read_mass_balance_data(file_path1)
# for gla in collection.Glacier_Collections:
#     if gla.mass_balance_measurement:
#         print(f"{gla.glacier_id}'s measurement: ", gla.mass_balance_measurement)
# plot_path = Path("C:/PycharmProjects/output/figure 2")
#collection.plot_extremes(plot_path)
#collection.summary()
# print(collection.sort_by_latest_mass_balance(6, True))
# for glacier in collection.Glacier_Collections:
#     print(glacier.mass_balance_measurement)

# plot_path = Path("C:/PycharmProjects/output/figure 1")
# dic = {'1915': [-21558, True], '1916': [-23406, True], '1917': [-37838, True], '1918': [-26501, True], '1919': [-25907, True], '1920': [-40678, True], '1921': [-50586, True], '1922': [-35502, True], '1923': [-28392, True], '1924': [-31854, True], '1925': [-36483, True], '1926': [-32816, True], '1927': [-37185, True], '1928': [-54149, True], '1929': [-49437, True], '1930': [-41370, True], '1931': [-38284, True], '1932': [-50814, True], '1933': [-38201, True], '1934': [-57098, True], '1935': [-48728, True], '1936': [-28830, True], '1937': [-25838, True], '1938': [-33471, True], '1939': [-39977, True], '1940': [-20076, True], '1941': [-19249, True], '1942': [-36733, True], '1943': [-36676, True], '1944': [-30339, True], '1945': [-26248, True], '1946': [-32448, True], '1947': [-55195, True], '1948': [-8619, True], '1949': [-27288, True], '1950': [-28026, True], '1951': [-30272, True], '1952': [-39632, True], '1953': [-29294, True], '1954': [-27330, True], '1955': [-5082, True], '1956': [-20113, True], '1957': [-81499, True], '1958': [-80790, True], '1959': [-72174, True], '1960': [-57853, True], '1961': [-55277, True], '1962': [-34971, True], '1963': [-31795, True], '1964': [-36259, True], '1965': [-15778, True], '1966': [-14219, True], '1967': [-20853, True], '1968': [-13509, True], '1969': [-18749, True], '1970': [-22211, True], '1971': [-28830, True], '1972': [-21924, True], '1973': [-30979, True], '1974': [-13546, True], '1975': [-13970, True], '1976': [-23148, True], '1977': [-16861, True], '1978': [-12811, True], '1979': [-25006, True], '1980': [-16841, True], '1981': [-24020, True], '1982': [-33273, True], '1983': [-30852, True], '1984': [-17633, True], '1985': [-60869, True], '1986': [-72641, True], '1987': [-19216, True], '1988': [-32225, True], '1989': [-35396, True], '1990': [-113541, True], '1991': [-126085, True], '1992': [-128901, True], '1993': [-133158, True], '1994': [-167910, True], '1995': [-198290, True], '1996': [-44241, True], '1997': [-49154, True], '1998': [-68174, True], '1999': [-121675, True], '2000': [-140371, True], '2001': [-148144, True], '2002': [-49702, True], '2003': [-64698, True], '2004': [-51605, True], '2005': [-56250, True], '2006': [-56885, True], '2007': [-58108, True], '2008': [-59749, True], '2009': [-60425, True], '2010': [-54544, True], '2011': [-61981, True], '2012': [-62182, True], '2013': [-52476, True], '2014': [-53840, True], '2015': [-13284, True], '2016': [-7015, True], '2017': [-11303, True], '2018': [-13226, True], '2019': [-8110, True]}
#
# glacier = Glacier("","","",11.,1.,123)
# glacier.mass_balance_measurement = dic
#
# glacier.plot_mass_balance(plot_path)

#pytest.main()
# glacier = Glacier('01678', 'mountain', 'CH', 46.37, 7.37, 600)
# glacier.add_mass_balance_measurement("2002", "-10", False)
# glacier.add_mass_balance_measurement("2003", "30", True)
# glacier.add_mass_balance_measurement("2003", "40", True)
# glacier.add_mass_balance_measurement("2003", "-3", False)
# print(glacier.mass_balance_measurement)

# file_path1 = Path("test_used_data/glacier_collect.csv")
# collection = GlacierCollection(file_path1)
# file_path2 = Path("test_used_data/mass_data.csv")
# collection.read_mass_balance_data(file_path2)
# print(collection.sort_by_latest_mass_balance(3))
# print(collection.Glacier_Collections)


