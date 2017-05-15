import arcpy


class batchCAD2GDB (object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.category = "Data Processing"
        self.label = "Batch Cad to GDB Converter"
        self.description = "Creates a file gdb named CAD2FGDB.gdb at source folder, and converts any dgn/dwg files in source folder to a feature class datasets in CAD2FGDB."
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        # parameter0
        param0 = arcpy.Parameter(
            displayName="Source Folder",
            name="source",
            datatype="DEFolder",
            parameterType="Required",
            direction="Input")
        # parameter1
        param1 = arcpy.Parameter(
            displayName="Reference Scale",
            name="referenceScale",
            datatype="GPDouble",
            parameterType="Required",
            direction="Input")
        # parameter2
        param2 = arcpy.Parameter(
            displayName="Coordinate System",
            name="coordinateSystem",
            datatype="GPCoordinateSystem",
            parameterType="Required",
            direction="Input")
        params = [param0, param1, param2]
        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True  # or False

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        source = parameters[0].valueAsText
        referenceScale = parameters[1].value
        coordinateSystem = parameters[2].valueAsText
        import os
        # make a file gdb in source
        arcpy.CreateFileGDB_management(source, "CAD2FGDB.gdb")
        for root, dirs, files in os.walk(source):
            for fname in files:
                if fname[-3:] in ["dgn", "dwg"]:
                    for i in ["-", " ", "(", ")"]:  # check for illegal characters in name
                        if i in fname:
                            oldName = root + "\\" + fname
                            newName = root + "\\" + fname.replace(i, "_")
                            os.rename(oldName, newName)  # rename file if illegal characters found
                            cadFile = newName
                            outName = newName[:-4]
                        else:
                            cadFile = root + "\\" + fname
                            outName = fname[:-4]
                    outGDB = source + "\\CAD2FGDB.gdb"
                    arcpy.CADToGeodatabase_conversion(cadFile, outGDB, outName, referenceScale, coordinateSystem)
