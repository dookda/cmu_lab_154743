import os
from qgis.core import *
import glob

vill = "/Users/sakdahomhuan/Dev/workspace/cm_dwr/cm_dwr_village_4326.shp"
lyr = iface.addVectorLayer(vill, "cm village", 'ogr')

#iface.showAttributeTable(lyr)

# for f in lyr.fields():
#     print(f)
n = 0
lyr.setSubsetString("VILL_NAM_T LIKE '%ห้วย%'")
for f in lyr.getFeatures():
    print(n, f["VILL_NAM_T"])
    n += 1

