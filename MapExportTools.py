import arcpy


class ExportBookmarks(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.category = "Map Export"
        self.label = "Export Bookmarks"
        self.description = "Exports all selected bookmarks in an MXD to PNG image."
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        # parameter0
        param0 = arcpy.Parameter(
            displayName="Use Currently Opened File",
            name="useCurrentFile",
            datatype="GPBoolean",
            parameterType="Required",
            direction="Input")
        param0.value = True

        param1 = arcpy.Parameter(
            displayName="Map File",
            name="mxdFile",
            datatype="DEFile",
            parameterType="Optional",
            direction="Input")
        param1.enabled = False
        param1.filter.list = ["mxd"]

        param2 = arcpy.Parameter(
            displayName="Output Location",
            name="outLocation",
            datatype="DEFolder",
            parameterType="Required",
            direction="Input")

        param3 = arcpy.Parameter(
            displayName="Bookmarks List",
            name="exportList",
            datatype="GPString",
            parameterType="Required",
            direction="Input",
            multiValue=True)

        param4 = arcpy.Parameter(
            displayName="Export Layout",
            name="exportLayout",
            datatype="GPBoolean",
            parameterType="Required",
            direction="Input")
        param4.value = False

        param5 = arcpy.Parameter(
            displayName="Output Width",
            name="outputW",
            datatype="GPDouble",
            parameterType="Required",
            direction="Input")
        param5.enabled = False

        param6 = arcpy.Parameter(
            displayName="Output Height",
            name="outputH",
            datatype="GPDouble",
            parameterType="Required",
            direction="Input")
        param6.enabled = False

        params = [param0, param1, param2, param3, param4, param5, param6]
        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        if parameters[0].value is True:
            parameters[1].enabled = False
            mxd = arcpy.mapping.MapDocument("CURRENT")
            df = arcpy.mapping.ListDataFrames(mxd, "")[0]
            bkmkList = arcpy.mapping.ListBookmarks(mxd, "", df)
            exportList = []
            for bkmk in bkmkList:
                exportList.append(bkmk.name)
                parameters[3].filter.list = exportList
        if parameters[0].value is False:
            parameters[1].enabled = True
            if parameters[1].altered:
                mxd = arcpy.mapping.MapDocument(str(parameters[1].value))
                df = arcpy.mapping.ListDataFrames(mxd, "")[0]
                bkmkList = arcpy.mapping.ListBookmarks(mxd, "", df)
                exportList = []
                for bkmk in bkmkList:
                    exportList.append(bkmk.name)
                    parameters[3].filter.list = exportList
        if parameters[4].value is False:
            parameters[5].enabled = True
            parameters[5].value = 6.95
            parameters[6].enabled = True
            parameters[6].value = 8.16
        if parameters[4].value is True:
            parameters[5].enabled = False
            parameters[6].enabled = False
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        if parameters[1].altered:
            mxd = arcpy.mapping.MapDocument(str(parameters[1].value))
            df = arcpy.mapping.ListDataFrames(mxd, "")[0]
            bkmkList = arcpy.mapping.ListBookmarks(mxd, "", df)
            if len(bkmkList) == 0:
                parameters[1].setErrorMessage("This map document has no bookmarks!")
        if parameters[0].altered:
            if parameters[0].value is True:
                mxd = arcpy.mapping.MapDocument("CURRENT")
                df = arcpy.mapping.ListDataFrames(mxd, "")[0]
                bkmkList = arcpy.mapping.ListBookmarks(mxd, "", df)
                if len(bkmkList) == 0:
                    parameters[0].setErrorMessage("This map document has no bookmarks!")
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        # get necessary input parameters
        if parameters[0].value is True:
            mxdFile = "CURRENT"
        else:
            mxdFile = parameters[1].valueAsText
            outLocation = parameters[2].valueAsText
            exportList = parameters[3].valueAsText
            exportLayout = parameters[4].value
            outputW = parameters[5].value
            outputH = parameters[6].value
        # specify mxd file location
        mxd = arcpy.mapping.MapDocument(mxdFile)
        # specify dataframe in MXD
        df = arcpy.mapping.ListDataFrames(mxd, "")[0]
        # create a list of all bookmarks in MXD
        bkmkList = arcpy.mapping.ListBookmarks(mxd, "", df)
        # loop through the exportList
        for bkmk in bkmkList:
            if bkmk.name in exportList:
                # set the current dataframe extent to that of the current bookmark
                df.extent = bkmk.extent
                # set the output filepath
                outFile = outLocation + "\\" + bkmk.name + ".png"
                # if layout is unchecked export without the map layout design
                if exportLayout is False:
                    arcpy.AddMessage("Exporting " + outFile)
                    arcpy.GetMessage(0)
                    arcpy.mapping.ExportToPNG(mxd, outFile, df, df_export_width=outputW * 300, df_export_height=outputH * 300, resolution=300)
                # otherwise export using the map layout design
                else:
                    arcpy.mapping.ExportToPNG(mxd, outFile, resolution=300)
        del mxd
        return


class ExportDDP (object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.category = "Map Export"
        self.label = "Export Data Driven Pages"
        self.description = "Exports all selected data driven pages in an MXD to JPEG, PDF or PNG image."
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        # parameter0
        param0 = arcpy.Parameter(
            displayName="Map File",
            name="mapFile",
            datatype="DEFile",
            parameterType="Required",
            direction="Input")
        param0.filter.list = ["mxd"]
        # parameter1
        param1 = arcpy.Parameter(
            displayName="Output Location",
            name="outDir",
            datatype="DEFolder",
            parameterType="Required",
            direction="Input")
        # parameter2
        param2 = arcpy.Parameter(
            displayName="Data Driven Pages List",
            name="exportList",
            datatype="GPString",
            parameterType="Required",
            direction="Input",
            multiValue=True)
        # parameter3
        param3 = arcpy.Parameter(
            displayName="Output Format",
            name="outFormat",
            datatype="GPString",
            parameterType="Required",
            direction="Input")
        param3.filter.list = ["JPEG", "PDF", "PNG"]
        params = [param0, param1, param2, param3]
        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        if parameters[0].altered:
            mxd = arcpy.mapping.MapDocument(str(parameters[0].value))
            totalPages = mxd.dataDrivenPages.pageCount
            exportList = []
            for page in range(1, totalPages + 1):
                mxd.dataDrivenPages.currentPageID = page
                pageField = mxd.dataDrivenPages.pageNameField.name
                pageName = mxd.dataDrivenPages.pageRow.getValue(pageField)
                exportList.append(str(page) + "-" + pageName)
            parameters[2].filter.list = exportList
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        mapFile = parameters[0].valueAsText
        outDir = parameters[1].valueAsText
        exportList = parameters[2].valueAsText
        outFormat = parameters[3].value
        # open mxd for reading
        mxd = arcpy.mapping.MapDocument(mapFile)
        totalPages = mxd.dataDrivenPages.pageCount
        # loop through list of pages
        for page in range(1, totalPages + 1):
            mxd.dataDrivenPages.currentPageID = page
            pageField = mxd.dataDrivenPages.pageNameField.name
            pageName = str(page) + "-" + mxd.dataDrivenPages.pageRow.getValue(pageField)
            outPage = outDir + "\\" + pageName
            if pageName in exportList:
                arcpy.AddMessage("Exporting " + outPage)
                if outFormat == "PNG":
                    arcpy.mapping.ExportToPNG(mxd, outPage + ".png", resolution=300)
                if outFormat == "PDF":
                    arcpy.mapping.ExportToPDF(mxd, outPage + ".pdf", resolution=300)
                if outFormat == "JPEG":
                    arcpy.mapping.ExportToJPEG(mxd, outPage + ".jpg", resolution=300)


class DumpMXDs (object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.category = "Map Export"
        self.label = "Dump MXDs"
        self.description = "Exports all MXD documents in the Source Folder to the Output File Format and saves them in the Destination Folder."
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
        # parameter 1
        param1 = arcpy.Parameter(
            displayName="Destination Folder",
            name="destination",
            datatype="DEFolder",
            parameterType="Required",
            direction="Input")
        # parameter 2
        param2 = arcpy.Parameter(
            displayName="Output File Format",
            name="outFormat",
            datatype="GPString",
            parameterType="Required",
            direction="Input")
        param2.filter.list = ["PDF", "PNG", "JPEG"]

        params = [param0, param1, param2]
        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

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
        import os

        source = parameters[0].valueAsText
        destination = parameters[1].valueAsText
        outFormat = parameters[2].valueAsText

        for root, dirs, files, in os.walk(source):
            for fname in files:
                # loop for mxd files
                if fname[-3:] in ["mxd", "MXD"]:
                    filePath = source + "\\" + fname
                    mxd = arcpy.mapping.MapDocument(filePath)
                    # make files and export
                    if outFormat == "PDF":
                        savePath = os.path.join(destination + "\\" + fname[:-4] + ".pdf")
                        print savePath
                        arcpy.mapping.ExportToPDF(mxd, savePath, resolution=300)
                    elif outFormat == "PNG":
                        savePath = os.path.join(destination + "\\" + fname[:-4] + ".png")
                        print savePath
                        arcpy.mapping.ExportToPNG(mxd, savePath, resolution=300)
                    elif outFormat == "JPEG":
                        savePath = os.path.join(destination + "\\" + fname[:-4] + ".jpeg")
                        print savePath
                        arcpy.mapping.ExportToJPEG(mxd, savePath, resolution=300)
