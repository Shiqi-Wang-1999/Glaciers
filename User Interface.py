from pathlib import Path
from glaciers import Glacier, GlacierCollection

file_path = Path("C:/PycharmProjects/data/sheet-A.csv")
collection = GlacierCollection(file_path)
# print(collection.Raw_Glacier_Collections)
#print(collection.filter_by_code("6?9"))
print(collection.find_nearest(-41.45,-71,10))
file_path1 = Path("C:/PycharmProjects/data/sheet-EE.csv")
#collection.read_mass_balance_data(file_path1)
# collection.read_mass_balance_data(file_path1)
# for glacier in collection.Glacier_Collections:
#     print(glacier.mass_balance_measurement)
