from MapExportTools import *
from GeocodingTools import *
from DataConversionTools import *


class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Custom Python Tools"
        self.alias = "CustomPythonTools"

        # List of tool classes associated with this toolbox
        self.tools = [MapExportTools.ExportBookmarks, MapExportTools.ExportDDP, MapExportTools.DumpMXDs, DataConversionTools.batchCAD2GDB, GeocodingTools.AddressLookup, GeocodingTools.CoordinateLookup]
