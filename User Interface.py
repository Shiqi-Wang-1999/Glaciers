from pathlib import Path
from glaciers import Glacier, GlacierCollection

file_path = Path("C:/PycharmProjects/data/sheet-A.csv")
collection = GlacierCollection(file_path)

glacier = Glacier("","","",0.,0.,123)