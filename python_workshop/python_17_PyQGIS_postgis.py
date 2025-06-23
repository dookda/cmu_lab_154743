import os
from qgis.core import *
import glob

uri = QgsDataSourceUri()
uri.setConnection("localhost", "5432","geo377", "sakdahomhuan", "1234")
uri.setDataSource("public","cm_tambon_4326", "geom",  "gid >= 0", "gid")

vlayer = QgsVectorLayer(uri.uri(False), "", "sakdahomhuan")
QgsProject.instance().addMapLayer(vlayer)