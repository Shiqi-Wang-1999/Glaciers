from pathlib import Path
from glaciers import Glacier, GlacierCollection

file_path = Path("C:/PycharmProjects/data/sheet-A.csv")
#collection = GlacierCollection(file_path)
# print(collection.Raw_Glacier_Collections)
#print(collection.filter_by_code("6?9"))

#print(collection.find_nearest(-41.45,-71,10))
file_path1 = Path("C:/PycharmProjects/data/sheet-EE.csv")

#collection.read_mass_balance_data(file_path1)
#collection.summary()
#print(collection.sort_by_latest_mass_balance(6))
# for glacier in collection.Glacier_Collections:
#     print(glacier.mass_balance_measurement)

plot_path = Path("C:/PycharmProjects/output/figure 1")
dic = {'1971': [980, False], '1972': [320, False], '1973': [1570, False], '1974': [510, False], '1975': [1700, False], '1976': [1400, False], '1977': [-1400, False]}

glacier = Glacier("","","",11.,1.,123)
glacier.mass_balance_measurement = dic

glacier.plot_mass_balance(plot_path)