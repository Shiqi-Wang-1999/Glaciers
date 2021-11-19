from pathlib import Path
from glaciers import Glacier, GlacierCollection

file_path = Path("C:/PycharmProjects/data/sheet-A.csv")
collection = GlacierCollection(file_path)

print(collection.Raw_Glacier_Collections)