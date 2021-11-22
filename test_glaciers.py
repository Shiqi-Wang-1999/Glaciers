import pytest
from glaciers import Glacier, GlacierCollection
from pathlib import Path


# def test_glacier_id():
#     with pytest.raises(ValueError) as exception:
#         glacier = Glacier('01678', 'mountain', 'CH', 46.37, 7.37, 600)
#     assert "The unique ID must be comprised of exactly 5 digits" in str(exception.value)


# Errors with appropriate error messages are thrown when invalid values are encountered
# def test_glacier_id():
#     with pytest.raises(ValueError) as exception:
#         glacier = Glacier('1678', 'mountain', 'CH', 46.37, 7.37, 600)
#     assert "The unique ID must be comprised of exactly 5 digits" in str(exception.value)
#
#
# def test_glacier_lat_lon():
#     with pytest.raises(ValueError) as exception:
#         glacier = Glacier('01678', 'mountain', 'CH', 146.37, 7.37, 600)
#
#     assert "the latitude should be between -90 and 90, the longitude between -180 and 180" in str(exception.value)


# def test_measurement_year():
#     with pytest.raises(ValueError) as exception:
#         glacier = Glacier('01678', 'mountain', 'CH', 46.37, 7.37, 600)
#         glacier.add_mass_balance_measurement("2023", 200, True)
#     assert "The year of measurement cannot be in the future" in str(exception.value)

# def test_glacier_unit():
#     with pytest.raises(ValueError) as exception:
#         glacier = Glacier('01678', 'mountain', 'CHR', 46.37, 7.37, 600)
#     assert "The political unit must be a string of length 2, composed only of capital letters or the special value ”99”" in str(exception.value)


# def test_filter_pattern():
#     with pytest.raises(ValueError) as exception:
#         file_path = Path("C:/PycharmProjects/data/sheet-A.csv")
#         collection = GlacierCollection(file_path)
#         print(collection.filter_by_code("????"))
#     assert "Please use the code with exact 3 digits" in str(exception.value)





def test_add_mass_balance_measurement():
    # file_path = Path("C:/PycharmProjects/data/sheet-A.csv")
    # collection = GlacierCollection(file_path)
    # file_path1 = Path("C:/PycharmProjects/data/sheet-EE.csv")
    # collection.read_mass_balance_data(file_path1)
    glacier = Glacier('01678', 'mountain', 'CH', 46.37, 7.37, 600)
    glacier.add_mass_balance_measurement("2002", -987, True)



