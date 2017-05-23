# Usage
1. Download or clone
2. Open ArcCatalog
3. Open ArcToolbox and right click the ArcToolbox folder
4. Select Add Toolbox...
5. Navigate to the clone/download directory and select the .pyt file

## Tool Categories
### Data Tools
Tools for processing and/or converting data.

###### batchCAD2GDB

Creates a file gdb named CAD2FGDB.gdb at source folder, and converts any dgn/dwg files in source folder to a feature class datasets in CAD2FGDB.

### Geocoding Tools
Tools for conducting forward and reverse geocoding using [GeoPy](https://geopy.readthedocs.io/en/1.10.0/).

###### AddressLookup
Reverse geocode coordinates to get addresses using third party Geocoding API(s).

###### CoordinateLookup
Forward geocode addresses to get coordinates using third party Geocoding API(s).

### Map Export Tools
Tools for exporting, manipulating, and converting map documents, bookmarks, data driven pages.

###### ExportBookmarks
Exports all selected bookmarks in an MXD to PNG image. The use case supported by this tool is the generation of multiple basemaps without any layout elements for post-finishing in a graphic production program such as the Adobe Suite, Gimp, etc.

###### ExportDDP
Exports all selected data driven pages in an MXD to JPEG, PDF or PNG image. This tool is meant to supplement the existing data driven pages export function in ArcMap by allowing users to export multiple pages to formats other than PDF.

###### DumpMXDs
Exports all MXD documents in the Source Folder to the Output File Format and saves them in the Destination Folder. This is intended for use with map documents that have a single layout e.g. one document == one map. It is not intended to be used with data driven pages. If you need data driven pages support see the Export DDP tool.
