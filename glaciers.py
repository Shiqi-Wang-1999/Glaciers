class Glacier:
    def __init__(self, glacier_id, name, unit, lat, lon, code):
        if (type(glacier_id) == str) & (type(name) == str) \
                & (type(unit) == str) & (type(lat) == float) \
                & (type(lon) == float) & (type(code) == int):
            self.glacier_id = glacier_id
            self.name = name
            self.unit = unit
            self.lat = lat
            self.lon = lon
            self.code = code
        else:
            print("Please use the valid data type.")

    def add_mass_balance_measurement(self, year, mass_balance, partial):
        raise NotImplementedError

    def plot_mass_balance(self, output_path):
        raise NotImplementedError

        
class GlacierCollection:

    def __init__(self, file_path):
        self.csv_file_path = file_path

    def read_mass_balance_data(self, file_path):
        raise NotImplementedError

    def find_nearest(self, lat, lon, n):
        """Get the n glaciers closest to the given coordinates."""
        raise NotImplementedError
    
    def filter_by_code(self, code_pattern):
        """Return the names of glaciers whose codes match the given pattern."""
        raise NotImplementedError

    def sort_by_latest_mass_balance(self, n, reverse):
        """Return the N glaciers with the highest area accumulated in the last measurement."""
        raise NotImplementedError

    def summary(self):
        raise NotImplementedError

    def plot_extremes(self, output_path):
        raise NotImplementedError
