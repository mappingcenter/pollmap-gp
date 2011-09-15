# ---------------------------------------------------------------------------
# SUMMARIZE SCRIPT v1.2
# Alex Yule 3/2/11
# last updated 3/23/11 11:35 AM
# Created on: 2011-03-04 11:56:37.00000
# Description: Summarize a set of specified fields in feature class within the provided extent
# ---------------------------------------------------------------------------

# Import arcpy module
import arcpy
from string import join
#from os import path

# connect to database using sde connection file
db = r"D:\Data\SDE_CONNECTIONS\niflheim_express1_collegefootball_webeditor.sde"
features = db  + "\\collegefootball.DBO.features"

def status(msg): #logging function
    #print msg
    arcpy.AddMessage(msg)
    arcpy.SetProgressorLabel(msg)

# Script arguments
RESULTS = r'%scratchworkspace%\results' # arcpy.GetParameterAsText(2)
if RESULTS == '#' or not RESULTS:
    RESULTS = r'%scratchworkspace%\results' # provide a default value if unspecified

FEATURE_SET = arcpy.GetParameterAsText(0)

FIELDS = arcpy.GetParameterAsText(1) # the fields to summarize

# create list of statistics fields (and type) for summary stats command
allfields_list = []
field_list = []
w_clause_list = []

stats_field = FIELDS.split()
for field in FIELDS.split():
    w_clause_list.append("["+str(field)+"]>0")
    field_list.append(str(field))
    field_list.append("SUM")
    allfields_list.append(field_list)
    field_list = [] 
stats_fields = allfields_list
w_clause = join(w_clause_list, " OR ")

try:
    # Local variables:
    features_Layer = "features_Layer"
    
    # Process: Make Feature Layer
    arcpy.MakeFeatureLayer_management(features, features_Layer)
    
    # Select all features that have positive votes for at least one team
    arcpy.SelectLayerByAttribute_management(features_Layer,"NEW_SELECTION",w_clause)
    # Select all features that intersect the extent
    arcpy.SelectLayerByLocation_management(features_Layer, "INTERSECT", FEATURE_SET, "", "SUBSET_SELECTION")
    
    # Run summary stats on the selected features
    arcpy.Statistics_analysis(features_Layer, RESULTS, stats_fields, "")
    # Pass the results out of the tool
    arcpy.SetParameterAsText(2, RESULTS)
    
except arcpy.ExecuteError:
    # Get the tool error messages 
    msgs = arcpy.GetMessages(2) 
    # Return tool error messages for use with a script tool 
    arcpy.AddError(msgs) 
    # Print tool error messages for use in Python/PythonWin 
    print msgs
