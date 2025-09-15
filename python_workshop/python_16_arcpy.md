# การใช้งาน ArcPy เบื้องต้น

## ArcPy คืออะไร
ArcPy เป็นไลบรารีของ Python ที่พัฒนาโดย Esri เพื่อใช้ในการทำงานกับข้อมูลเชิงพื้นที่ (spatial data) และการวิเคราะห์เชิงพื้นที่ (spatial analysis) ในซอฟต์แวร์ ArcGIS

## การติดตั้ง ArcPy
ArcPy มาพร้อมกับการติดตั้ง ArcGIS Desktop หรือ ArcGIS Pro ดังนั้นหากคุณมี ArcGIS ติดตั้งอยู่แล้ว คุณไม่จำเป็นต้องติดตั้ง ArcPy 

การใช้งาน ArcPy เบื้องต้น
การนำเข้าไลบรารี ArcPy
```python
import arcpy
```
การตั้งค่าสภาพแวดล้อม
```python
arcpy.env.workspace = "C:/path/to/your/workspace"
arcpy.env.overwriteOutput = True
```
การสร้างฟีเจอร์คลาสใหม่
```python
arcpy.CreateFeatureclass_management("C:/path/to/your/workspace", "new_feature_class.shp", "POINT")
```
การเพิ่มฟิลด์ใหม่
```python
arcpy.AddField_management("new_feature_class.shp", "NewField", "TEXT")
```
การเพิ่มข้อมูลลงในฟีเจอร์คลาส
```python
with arcpy.da.InsertCursor("new_feature_class.shp", ["SHAPE@", "NewField"]) as cursor:
    point = arcpy.Point(1, 1)
    cursor.insertRow([point, "Sample Data"])
```   
การคัดลอกฟีเจอร์คลาส
```python
arcpy.CopyFeatures_management("new_feature_class.shp", "C:/path/to/your/workspace/copied_feature_class.shp")
```
การลบฟีเจอร์คลาส
```python
arcpy.Delete_management("new_feature_class.shp")
```
เรียกใช้งาน ArcPy โดยกำหนด workspace
```python
import os
import arcpy
from arcpy import env

env.workspace = r"C:\lab_arcpy"

# list workspace
workspaces = arcpy.ListWorkspaces("*", "Folder")
for wp in workspaces:
    print(wp)
```
การ list ไฟล์ใน workspace
```python
# list files in workspace
files = arcpy.ListFiles("*.shp")
for f in files:
    print(f)
```
การ list ฟีเจอร์คลาสใน workspace
```python
# list feature classes in workspace
fcs = arcpy.ListFeatureClasses()
for fc in fcs:
    print(fc)
```

สามารถกำหนดประเภทของข้อมูลที่ต้องการ list ได้ เช่น point, polygon, polyline
```python
# list feature classes in workspace
fcs = arcpy.ListFeatureClasses(feature_type="Point")
for fc in fcs:
    print(fc)
```

การแสดงรายการของ raster
```python
# list raster in workspace
rasters = arcpy.ListRasters()
for raster in rasters:
    print(raster)
```

การ list ฟิลด์ในฟีเจอร์คลาส
```python
fields = arcpy.ListFields(r"C:\lab_arcpy\data4326\cm_village_4326.shp")
for fld in fields:
    # print(fld.name, fld.type, fld.length)
    print("name: {0}, type: {1}, length: {2}"
          .format(fld.name, fld.type, fld.length))
```

การเข้าถึงข้อมูลในฟีเจอร์คลาสด้วย SearchCursor
```python
fc = r"C:\lab_arcpy\data4326\cm_village_4326.shp"
field = "VILL_CODE"
rows = arcpy.SearchCursor(fc, fields='VILL_CODE')
for row in rows:
    print(row.getValue("VILL_CODE"))
```

การเลือกข้อมูล
```python
import os
import arcpy
from arcpy import env

env.workspace = r"C:\lab_arcpy\data4326"
arcpy.MakeFeatureLayer_management("cm_tambon_4326.shp", "lyr")
arcpy.SelectLayerByAttribute_management("lyr", 'NEW_SELECTION',
                                        "TAM_CODE = '501001'")

arcpy.CopyFeatures_management("lyr", 'tambon')
print("ok")
```

การ select by location
```python
arcpy.MakeFeatureLayer_management("cm_village_4326.shp", "villLyr")
arcpy.SelectLayerByLocation_management('villLyr', 'INTERSECT',
                                       'lyr', 0,
                                       'NEW_SELECTION')
arcpy.CopyFeatures_management("villLyr", 'villSel')
print("ok")
```

การคำนวณฟิลด์
```python
import os
import arcpy
from arcpy import env

env.workspace = r"C:\lab_arcpy\data4326"
arcpy.MakeFeatureLayer_management("cm_tambon_4326.shp", "lyr")
arcpy.SelectLayerByAttribute_management("lyr", 'NEW_SELECTION',
                                        "TAM_CODE = '501001'")

arcpy.CopyFeatures_management("lyr", 'tambon')
print("ok")
arcpy.AddField_management("tambon", "Area", "DOUBLE")
arcpy.CalculateField_management("tambon", "Area", "!SHAPE.area!", "PYTHON3")
print("ok")
```

การตั้งค่า workspace ผ่าน parameter
```python
import arcpy
from arcpy import env

folder = arcpy.GetParameterAsText(0)
env.workspace = folder

# list file
files = arcpy.ListFiles("*.dbf")
for f in files:
    print(f)
    arcpy.AddMessage(f)
```

การบัฟเฟอร์
```python
import os
import arcpy
from arcpy import env

env.workspace = r"C:\lab_arcpy\data4326"
arcpy.Buffer_analysis("tambon", "tambon_buffer", "100 Meters")
print("ok")
```

ตัวอย่างการใช้งาน geoprocessing : การวิเคราะห์หาพื้นที่การใช้ประโยชน์ที่ดินในตำบลที่ต้องการ
```python
import arcpy
from arcpy import env

tam = r"C:\lab_arcpy\data4326\cm_tambon_4326.shp"
vill = r"C:\lab_arcpy\data4326\cm_village_4326.shp"
lu = r"C:\lab_arcpy\data4326\cm_lu2543_plu.shp"

outVill = r"C:\lab_arcpy\out\cm_vill_select.shp"
buffVill = r"C:\lab_arcpy\out\cm_vill_buff.shp"
luBuff = r"C:\lab_arcpy\out\cm_lu_buff.shp"
```

เลือกตำบลที่ต้องการ
```python
