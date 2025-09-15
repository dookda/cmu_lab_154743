import os
from qgis.core import *
import glob

# vill = "/Users/sakdahomhuan/Dev/workspace/cm_dwr/cm_dwr_village_4326.shp"
# iface.addVectorLayer(vill, "cm village", 'ogr')

dir = os.chdir("/Users/sakdahomhuan/Dev/workspace/cm_dwr")
shp = glob.glob("*.shp")

for s in shp:
    print(s.split('.'))
    sname = s.split('.')[0]
    iface.addVectorLayer(s, sname, 'ogr')
