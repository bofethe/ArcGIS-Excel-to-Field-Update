import arcpy
import pandas as pd

### UPDATE ###
# Add the paths to the gdb and excel sheet and specefiy the columns with the data you want
gdbPath = r"PATH"
excelSheetPath = r'PATH'
columns = 'A:B'
arcpy.env.workspace = gdbPath
arcpy.env.overwriteOutput = True

### UPDATE ###
# Add the names of the layers you want to add the info in
targetFeatureClasses = ['']

### UPDATE ###
# Add the old field name you want to use and the new field you want to create
oldFieldName = ''
newFieldName = ''

# Get the excel data in a dictionary
groupDic = {}
reducedSheet = pd.read_excel(excelSheetPath, header=0, usecols=columns, keep_default_na=True)
for i in range(len(reducedSheet)):
    row = reducedSheet.iloc[i]
    
    ### UPDATE ###
    # Update the index values
    oldIndex = 0
    newIndex = 1

    groupDic[str(row[oldIndex]).strip()] = str(row[newIndex]).strip()

featureClasses = arcpy.ListFeatureClasses()

# Loop through all the feature classes and select only the ones you want
counter = 0
for fc in featureClasses:
    if fc in targetFeatureClasses:

        # add the new field name if it's not already established
        existingFields = [f.name for f in arcpy.ListFields(fc)]
        if newFieldName not in existingFields:
            arcpy.management.AddField(fc, newFieldName, 'TEXT', field_length=200)
        
        # update the new field based on the key-value 
        with arcpy.da.UpdateCursor(fc, [oldFieldName, newFieldName]) as uc:
            for row in uc:
                if row[1] != groupDic[row[0]]:
                    counter +=1
                    row[1] = groupDic[row[0]]
                    uc.updateRow(row)
        del row, uc

print('Number of fields changed: ', str(counter))