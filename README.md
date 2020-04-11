# crawler

## Settings

### Global
- type : "google"/"local" #Defines which crawler type will be created.
- onlyOnce: true/false #Stores all pares file names/pathes in a memo file and will not return a file if it is already in the memo file.
- memo : "" #Defines the path to a memo file, which will contain all found files/sheets. 

### Local Crawler
- extension: "" #Applies a filter for the given extension, returns all if extensions is set to "".
- path: "" #Defines a folder which will be the strating point for searching

### Google Crawler
- credentials : "" #Path to a file which contains the googleApi credentials.
- spreadsheets : "" #Only spreadsheets which contains this string will be returned ("" will return all spreadsheets)
- worksheets : "" #Only worksheets (tables) which contains this string will be returned ("" will return all worksheets) 
- enableWorksheets : true/false #Defines if crawler will return spreadsheets or worksheets
- returnType : "path"/"data" #Defines if the crawler will return a string (path to spreadsheet/worksheet) or a object which poitns to a spreadsheet/worksheet