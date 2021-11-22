import pytest
from glaciers import Glacier, GlacierCollection
from pathlib import Path


# Errors with appropriate error messages are thrown when invalid values are encountered
def test_glacier_id():
    with pytest.raises(ValueError) as exception:
        glacier = Glacier('1678', 'mountain', 'CH', 46.37, 7.37, 600)
    assert "The unique ID must be comprised of exactly 5 digits" in str(exception.value)


def test_glacier_lat_lon():
    with pytest.raises(ValueError) as exception:
        glacier = Glacier('01678', 'mountain', 'CH', 146.37, 7.37, 600)

    assert "the latitude should be between -90 and 90, the longitude between -180 and 180" in str(exception.value)


def test_measurement_year():
    with pytest.raises(ValueError) as exception:
        glacier = Glacier('01678', 'mountain', 'CH', 46.37, 7.37, 600)
        glacier.add_mass_balance_measurement("2023", 200, True)
    assert "The year of measurement cannot be in the future" in str(exception.value)

def test_glacier_unit():
    with pytest.raises(ValueError) as exception:
        glacier = Glacier('01678', 'mountain', 'CHR', 46.37, 7.37, 600)
    assert "The political unit must be a string of length 2, composed only of capital letters or the special value ”99”" in str(exception.value)


def test_filter_pattern():
    with pytest.raises(ValueError) as exception:
        file_path = Path("C:/PycharmProjects/data/sheet-A.csv")
        collection = GlacierCollection(file_path)
        print(collection.filter_by_code("????"))
    assert "Please use the code with exact 3 digits" in str(exception.value)


# Test 'add_mass_balance_measurement' for both partial and whole-region data
def test_add_mass_balance_measurement():
    glacier = Glacier('01678', 'mountain', 'CH', 46.37, 7.37, 600)
    glacier.add_mass_balance_measurement("2002", "-10", False)
    glacier.add_mass_balance_measurement("2003", "30", True)
    glacier.add_mass_balance_measurement("2003", "40", True)
    glacier.add_mass_balance_measurement("2003", "-3", False)
    dic = {"2002": [-10, False], "2003": [70, True]}
    assert glacier.mass_balance_measurement == dic


# Test 'filter_by_code' method for both full codes and incomplete code patterns
def test_filter_by_code():
    file_path = Path("test_used_data/glacier_collect.csv")
    collection = GlacierCollection(file_path)
    list1 = ["AMEGHINO"]
    list2 = ["AGUA NEGRA", "AZUFRE", "BROWN SUPERIOR"]
    list3 = ["BAJO DEL PLOMO"]
    list4 = ["AGUA NEGRA", "ALERCE", "ALFA", "AMEGHINO", "AZUFRE",
             "BAJO DEL PLOMO", "BETA", "BONETE S", "BROWN SUPERIOR"]
    assert collection.filter_by_code("424") == list1
    assert collection.filter_by_code("?38") == list2
    assert collection.filter_by_code("??7") == list3
    assert collection.filter_by_code("???") == list4


# Test 'sort_by_latest_mass_balance' method for both directions of sorting
def test_sort_by_latest_mass_balance():
    file_path1 = Path("test_used_data/glacier_collect.csv")
    collection = GlacierCollection(file_path1)
    file_path2 = Path("test_used_data/mass_data.csv")
    collection.read_mass_balance_data(file_path2)
    # Mass measurement from small to large
    list1 = [collection.Glacier_Collections[0], collection.Glacier_Collections[4], collection.Glacier_Collections[8]]
    # Mass measurement from large to small
    list2 = [collection.Glacier_Collections[8], collection.Glacier_Collections[4], collection.Glacier_Collections[0]]
    assert collection.sort_by_latest_mass_balance(3, True) == list1
    assert collection.sort_by_latest_mass_balance(3) == list2





