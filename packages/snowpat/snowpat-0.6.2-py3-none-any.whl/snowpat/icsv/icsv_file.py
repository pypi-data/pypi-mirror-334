import pandas as pd
import xarray as xr
from typing import Optional

from ..pysmet import SMETFile
from .header import MetaDataSection, FieldsSection, Geometry


VERSIONS = ["1.0"]
FIRSTLINES = [f"# iCSV {version} UTF-8" for version in VERSIONS]

class iCSVFile:
    """
    Class to represent an iCSV file.
    
    Attributes:
        metadata (MetadataSection): Metadata section of the iCSV file.
        fields (FieldsSection): Fields section of the iCSV file.
        geometry (Representation class): Geometry section of the iCSV file.
        data (pd.Dataframe): Data section of the iCSV file.
        filename: The name of the iCSV file.
        skip_lines: The number of lines to skip when reading the file.
        
    Methods:
        load_file(filename: str = None): Load an iCSV file.
        parse_geometry(): Parse the geometry section of the iCSV file.
        info(): Print a summary of the iCSV file.
        to_xarray(): Convert the iCSV file to an xarray dataset.
        setData(data: pd.DataFrame, colnames: Optional[list] = None): Set the data of the iCSV file.
        write(filename: str = None): Write the iCSV file to a file.
    """
    def __init__(self, filename:str = None):
        self.metadata = MetaDataSection()
        self.fields = FieldsSection()
        self.geometry = Geometry()
        self.data: Optional[pd.DataFrame] = None
        self.filename = filename
        self.skip_lines = 0
        
        if self.filename:
            self.load_file()
            
    
    def __str__(self) -> str:
        return f"File: {self.filename}\n{self.metadata}\n{self.fields}\n{self.geometry}"
    
    def __eq__(self, value: object) -> bool:
        if not isinstance(value, iCSVFile):
            return False
        for attr in ['metadata', 'fields', 'geometry']:
            self_value = getattr(self, attr)
            value_value = getattr(value, attr)
            
            if self_value != value_value:
                return False
        return True
    
    def _parse_comment_line(self, line, section):
        if line == "[METADATA]":
            return "metadata"
        elif line == "[FIELDS]":
            self.metadata.check_validity()  # to parse fields we need valid metadata
            return "fields"
        elif line == "[DATA]":
            return "data"
        else:
            return self._parse_section_line(line, section)

    def _parse_section_line(self, line, section):
        if not section:
            raise ValueError("No section specified")
        line_vals = line.split("=")
        if len(line_vals) != 2:
            raise ValueError(f"Invalid {section} line: {line}, got 2 assignment operators \"=\"")

        if section == "metadata":
            self.metadata.set_attribute(line_vals[0].strip(), line_vals[1].strip())
        elif section == "fields":
            fields_vec = [field.strip() for field in line_vals[1].split(self.metadata.get_attribute("field_delimiter"))]
            self.fields.set_attribute(line_vals[0].strip(), fields_vec)
        elif section == "data":
            raise TypeError("Data section should not contain any comments")

        return section

    def _update_columns(self):
        self.data.columns = self.fields.fields
        for field in ["time", "timestamp"]:
            if field in self.fields.fields:
                self.data[field] = pd.to_datetime(self.data[field])          
    
    def load_file(self, filename: str = None):
        """Loads an iCSV file and parses its contents.

        Args:
            filename (str, optional): The path to the iCSV file. If not provided, the previously set filename will be used.

        Raises:
            ValueError: If the file is not a valid iCSV file or if the data section is not specified.

        Returns:
            None
        """
        if filename:
            self.filename = filename
            
        section = ""
        with open(self.filename, 'r') as file:
            first_line = file.readline().rstrip()  # rstrip() is used to remove the trailing newline
            if first_line not in FIRSTLINES:
                raise ValueError("Not an iCSV file")
        
            line_number = 1 # need to find the line number where the data starts
            for line in file:
                if line.startswith("#"):
                    line_number += 1
                    line = line[1:].strip()
                    section = self._parse_comment_line(line.strip(), section)
                else:
                    if section != "data":
                        raise ValueError("Data section was not specified")
                    self.skip_lines = line_number
                    break
        
        self.data = pd.read_csv(self.filename, skiprows=self.skip_lines, header=None, sep=self.metadata.get_attribute("field_delimiter"))
        self.fields.check_validity(self.data.shape[1]) # check if the number of fields match the number of columns
        self._update_columns()           
        self.parse_geometry()
        
    def parse_geometry(self):
        if self.metadata.get_attribute("geometry") in self.fields.get_attribute("fields"):
            self.geometry.geometry = self.metadata.get_attribute("geometry")
            self.geometry.srid = self.metadata.get_attribute("srid")
            self.geometry.column_name = self.metadata.get_attribute("column_name")
        else:
            self.geometry.geometry = self.metadata.get_attribute("geometry")
            self.geometry.srid = self.metadata.get_attribute("srid")
            self.geometry.set_location()    
            
    def info(self):
        """
        Prints information about the object and its data.

        This method prints the object itself and the head of its data.

        Args:
            None

        Returns:
            None
        """
        print(self)
        print("\nData:")
        print(self.data.head())
    
    def to_xarray(self) -> xr.Dataset:
        """
        Converts the data to an xarray dataset.

        Returns:
            xarray.Dataset: The converted xarray dataset.
        """
        arr = self.data.to_xarray()
        arr.attrs = self.metadata.metadata
        for i,var in enumerate(arr.data_vars):
            for _, vec in self.fields.miscalleneous_fields.items():
                arr[var].attrs = vec[i]
                
    def setData(self, data: pd.DataFrame, colnames: Optional[list] = None):
        """
        Sets the data of the iCSV file.

        Args:
            data (pd.DataFrame): The data to set.
            colnames (list): The names of the columns in the data.

        Returns:
            None
        """
        self.data = data
        if colnames:
            if len(colnames) != self.data.shape[1]:
                raise ValueError("Number of columns in data does not match the number of column names")
            self.fields.set_attribute("fields", colnames)
        else:
            colnames = self.data.columns.to_list()
            if colnames[0] == "0" or colnames[0] == 0:
                raise ValueError("Column names are not provided")
            self.fields.set_attribute("fields", colnames)
                # Ensure 'timestamp' is the first column if it exists
        if 'timestamp' in self.data.columns:
            cols = self.data.columns.tolist()
            if cols[0] != 'timestamp':
                cols.insert(0, cols.pop(cols.index('timestamp')))
                self.data = self.data[cols]
            self.fields.set_attribute("fields", self.data.columns)

            
        
                
    def write(self, filename: str = None):
        """
        Writes the metadata, fields, and data to a CSV file.

        Args:
            filename (str, optional): The name of the file to write. If not provided, the current filename will be used.

        Returns:
            None
        """
        
        if filename:
            self.filename = filename
            
        self.metadata.check_validity()
        self.fields.check_validity(self.data.shape[1])
        
            

        
        with open(self.filename, 'w') as file:
            file.write(f"{FIRSTLINES[-1]}\n")
            file.write("# [METADATA]\n")
            for key, val in self.metadata.metadata.items():
                file.write(f"# {key} = {val}\n")
            file.write("# [FIELDS]\n")
            for key, val in self.fields.all_fields.items():
                fields_string = self.metadata.get_attribute("field_delimiter").join(str(value) for value in val)
                file.write(f"# {key} = {fields_string}\n")
            file.write("# [DATA]\n")
            
        self.data.to_csv(self.filename, mode='a', index=False, header=False)
    
        
# ------------------ Factory functions ------------------        
                
def read(filename: str) -> iCSVFile:
    """
    Reads an iCSV file and returns an iCSVFile object.

    Args:
        filename (str): The path to the iCSV file.

    Returns:
        iCSVFile: An iCSVFile object representing the contents of the file.
        
    The iCSVFile object has the following attributes:
        - metadata: The metadata section of the iCSV file.
            access attributes via metadata.get_attribute("key")
        - fields: The fields section of the iCSV file.
            access attributes via fields.get_attribute("key")
        - geometry: The geometry section of the iCSV file.
            get the location via geometry.get_location()
        - data: The data section of the iCSV file.
            As a pandas DataFrame.
        - filename: The name of the iCSV file.
        - skip_lines: The number of lines to skip when reading the file.
    """
    icsv = iCSVFile(filename)
    return icsv

def from_smet(smet: SMETFile) -> iCSVFile:
    """
    Converts an SMETFile object to an iCSVFile object.

    Args:
        smet (SMETFile): The SMETFile object to convert.

    Returns:
        iCSVFile: The converted iCSVFile object.
    """
    icsv = iCSVFile()
    _set_fields_and_location(icsv, smet)
    _set_metadata(icsv, smet)
    icsv.data = smet.data
    _check_validity_and_parse_geometry(icsv, icsv.data.shape[1])
    print(icsv.fields)
    return icsv

def _set_fields_and_location(icsv, smet):
    icsv.fields.set_attribute("fields", smet.meta_data.fields)
    loc = smet.meta_data.location
    _set_location_attributes(icsv, loc)

def _set_location_attributes(icsv, loc):
    if not loc.epsg and not loc.is_latlon():
        raise ValueError("EPSG code not provided")
    elif loc.is_latlon():
        loc.epsg = 4326
        x = loc.longitude
        y = loc.latitude
    else:
        x = loc.easting
        y = loc.northing
    z = loc.altitude
    geometry = f"POINTZ({x} {y} {z})"
    icsv.metadata.set_attribute("geometry", geometry)
    srid = f"EPSG:{loc.epsg}"
    icsv.metadata.set_attribute("srid", srid)
    icsv.metadata.set_attribute("field_delimiter", ",")

def _set_metadata(icsv:iCSVFile, smet:SMETFile):
    icsv.metadata.set_attribute("nodata", smet.meta_data.nodata)
    icsv.metadata.set_attribute("station_id", smet.meta_data.station_id)
    _set_meta_data_attributes(icsv, smet.optional_meta_data.adjusted_dict)
    _set_meta_data_attributes(icsv, smet.other_meta_data)
    for key, value in smet.acdd_meta_data.adjusted_dict:
        icsv.metadata.set_attribute(key, value)

def _set_meta_data_attributes(icsv:iCSVFile, meta_data):
    for key, value in meta_data.items():
        if value:
            if isinstance(value, list) and len(value) == len(icsv.fields.fields):
                icsv.fields.set_attribute(key, value)
            elif isinstance(value, str) and len(value.split(" ")) == len(icsv.fields.fields):
                icsv.fields.set_attribute(key, value.split(" "))
            else:
                icsv.metadata.set_attribute(key, value)

def _check_validity_and_parse_geometry(icsv, ncols:int):
    icsv.metadata.check_validity()
    icsv.fields.check_validity(ncols)
    icsv.parse_geometry()