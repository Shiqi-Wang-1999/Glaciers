from pathlib import Path
from glaciers import Glacier, GlacierCollection

file_path = Path("C:/PycharmProjects/data/sheet-A.csv")
collection = GlacierCollection(file_path)

file_path1 = Path("C:/PycharmProjects/data/sheet-EE.csv")
collection.read_mass_balance_data(file_path1)
for glacier in collection.Glacier_Collections:
    print(glacier.mass_balance_measurement)
