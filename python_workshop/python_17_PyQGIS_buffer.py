import os
from qgis.core import *
import glob

vill = "/Users/sakdahomhuan/Dev/workspace/cm_dwr/cm_dwr_village_4326.shp"
# iface.addVectorLayer(vill, "cm village", 'ogr')

vlayer = iface.addVectorLayer(vill, "village", "ogr")
vlayer.setSubsetString("VILL_NAM_T LIKE '%ห้วย%'")

param = {
    'INPUT':vlayer,
    'DISTANCE':0.1,
    'SEGMENTS':5,
    'END_CAP_STYLE':0,
    'JOIN_STYLE':0,
    'MITER_LIMIT':2,
    'DISSOLVE':False,
    'OUTPUT':'memory:'}

result = processing.run("native:buffer",param)

QgsProject.instance().addMapLayer(result["OUTPUT"])




    
