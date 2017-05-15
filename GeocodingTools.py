import arcpy


class AddressLookup(object):
    def __init__(self):
        self.category = "Geocoding"
        self.label = "GeoPy Address Lookup"
        self.description = "Reverse geocode coordinates to get addresses using third party Geocoding API(s) \n ***This tool requires the GeoPy python geocoding libary. For details see https://github.com/geopy/geopy"
        self.canRunInBackground = False

    def getParameterInfo(self):
        param0 = arcpy.Parameter(
            displayName="Input Feature",
            name="inFeature",
            datatype="DEFeatureClass",
            parameterType="Required",
            direction="Input")
        param0.filter.list = ["Point", "Polygon"]
        param1 = arcpy.Parameter(
            displayName="Address Field Exists",
            name="addressExists",
            datatype="GPBoolean",
            parameterType="Required",
            direction="Input")
        param1.value = False
        param2 = arcpy.Parameter(
            displayName="Address Field",
            name="addressField",
            datatype="GPString",
            parameterType="Optional",
            direction="Input")
        param2.enabled = False
        param3 = arcpy.Parameter(
            displayName="Service",
            name="service",
            datatype="GPString",
            parameterType="Required",
            direction="Input")
        param3.filter.list = ["Google", "OpenStreetMap"]
        params = [param0, param1, param2, param3]
        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        if parameters[1].altered:
            if parameters[1].value is True:
                parameters[2].enabled = True
                fieldList = []
                for field in arcpy.ListFields(str(parameters[0].value)):
                    fieldList.append(field.name)
                parameters[2].filter.list = fieldList
            else:
                parameters[2].enabled = False
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        # check for GeoPy package
        if parameters[3].value:
            import imp
            try:
                imp.find_module("geopy")
            except:
                parameters[3].setErrorMessage("Your system does not have the GeoPy package installed! \n Click \"Show Help\" for additional information.")
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        # get input feature
        inFeature = parameters[0].valueAsText
        addressExists = parameters[1].value
        addressField = parameters[2].valueAsText
        service = parameters[3].valueAsText
        # create the address field if it does not exist
        if addressExists is False:
            arcpy.AddField_management(inFeature, 'Address', 'TEXT', '', '', 150, '', 'NULLABLE')
            addressField = 'Address'
        # search for addresses and populate field
        if service == "Google":
            from geopy.geocoders import GoogleV3
            geolocator = GoogleV3()
            with arcpy.da.UpdateCursor(inFeature, [addressField, "SHAPE@Y", "SHAPE@X"], "", "Coordinate Systems\Geographic Coordinate Systems\World\WGS 1984") as ADDR:
                for row in ADDR:
                    try:
                        queryString = str(row[1])+","+str(row[2])
                        location = geolocator.reverse(queryString, exactly_one=True)
                        row[0] = location.address[:-5]
                        ADDR.updateRow(row)
                        arcpy.AddMessage("Matched: "+location.address[:-5])
                        arcpy.GetMessages()
                    except:
                        arcpy.AddMessage("No Match: "+queryString)
                        arcpy.GetMessages()

        if service == "OpenStreetMap":
            from geopy.geocoders import Nominatim
            geolocator = Nominatim(country_bias="United States of America")
            with arcpy.da.UpdateCursor(inFeature, [addressField, "SHAPE@Y", "SHAPE@X"], "", "Coordinate Systems\Geographic Coordinate Systems\World\WGS 1984") as ADDR:
                for row in ADDR:
                    try:
                        queryString = str(row[1])+","+str(row[2])
                        location = geolocator.reverse(queryString, exactly_one=True)
                        row[0] = location.address[:location.address.rfind(",")]
                        ADDR.updateRow(row)
                        arcpy.AddMessage("Matched: "+location.address[:location.address.rfind(",")])
                        arcpy.GetMessages()
                    except:
                        arcpy.AddMessage("No Match: "+queryString)
                        arcpy.GetMessages()


class CoordinateLookup (object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.category = "Geocoding"
        self.label = "GeoPy Coordinate Lookup"
        self.description = "Forward geocode addresses to get coordinates using third party Geocoding API(s) \n ***This tool requires the GeoPy python geocoding libary. For details see https://github.com/geopy/geopy"
        self.canRunInBackground = False

    def getParameterInfo(self):
        param0 = arcpy.Parameter(
            displayName="Input Feature",
            name="inFeature",
            datatype="DEFeatureClass",
            parameterType="Required",
            direction="Input")
        param0.filter.list = ["Point", "Polygon"]
        param1 = arcpy.Parameter(
            displayName="Coordinate Fields Exists",
            name="coordinatesExists",
            datatype="GPBoolean",
            parameterType="Required",
            direction="Input")
        param1.value = False
        param2 = arcpy.Parameter(
            displayName="Address Field",
            name="addressField",
            datatype="GPString",
            parameterType="Required",
            direction="Input")
        param3 = arcpy.Parameter(
            displayName="Lat Field",
            name="latField",
            datatype="GPString",
            parameterType="Optional",
            direction="Input")
        param3.enabled = False
        param4 = arcpy.Parameter(
            displayName="Lon Field",
            name="lonField",
            datatype="GPString",
            parameterType="Optional",
            direction="Input")
        param4.enabled = False
        param5 = arcpy.Parameter(
            displayName="Service",
            name="service",
            datatype="GPString",
            parameterType="Required",
            direction="Input")
        param5.filter.list = ["Google", "OpenStreetMap"]

        params = [param0, param1, param2, param3, param4, param5]
        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        if parameters[0].altered:
            fieldList = []
            for field in arcpy.ListFields(str(parameters[0].value)):
                fieldList.append(field.name)
            parameters[2].filter.list = fieldList

            if parameters[1].value is True:
                parameters[3].enabled = True
                parameters[4].enabled = True
                parameters[3].filter.list = fieldList
                parameters[4].filter.list = fieldList
            else:
                parameters[3].enabled = False
                parameters[4].enabled = False
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        if parameters[5].value:
            import imp
            try:
                imp.find_module("geopy")
            except:
                parameters[5].setErrorMessage("Your system does not have the GeoPy package installed! \n Click \"Show Help\" for additional information.")
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        # get input feature
        inFeature = parameters[0].valueAsText
        coordinatesExists = parameters[1].value
        addressField = parameters[2].valueAsText
        latField = parameters[3].valueAsText
        lonField = parameters[4].valueAsText
        service = parameters[5].valueAsText
        # create the address field if it does not exist
        if coordinatesExists is False:
            arcpy.AddField_management(inFeature, 'Lat', 'DOUBLE', '', '', 12, '', 'NULLABLE')
            latField = 'Lat'
            arcpy.AddField_management(inFeature, 'Lon', 'DOUBLE', '', '', 12, '', 'NULLABLE')
            lonField = 'Lon'
        # search for addresses and populate field
        if service == "Google":
            from geopy.geocoders import GoogleV3
            geolocator = GoogleV3()
            with arcpy.da.UpdateCursor(inFeature, [addressField, latField, lonField]) as ADDR:
                for row in ADDR:
                    try:
                        location = geolocator.geocode(row[0])
                        row[1] = location.latitude
                        row[2] = location.longitude
                        ADDR.updateRow(row)
                        arcpy.AddMessage("Matched: "+row[0])
                        arcpy.GetMessages()
                    except:
                        arcpy.AddMessage("No Match: "+row[0])
                        arcpy.GetMessages()

        if service == "OpenStreetMap":
            from geopy.geocoders import Nominatim
            geolocator = Nominatim(country_bias="United States of America")
            with arcpy.da.UpdateCursor(inFeature, [addressField, latField, lonField]) as ADDR:
                for row in ADDR:
                    try:
                        location = geolocator.geocode(row[0])
                        row[1] = location.latitude
                        row[2] = location.longitude
                        ADDR.updateRow(row)
                        arcpy.AddMessage("Matched: "+row[0])
                        arcpy.GetMessages()
                    except:
                        arcpy.AddMessage("No Match: "+row[0])
                        arcpy.GetMessages()
