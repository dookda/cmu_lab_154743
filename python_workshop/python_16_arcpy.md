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

## ตัวอย่างการใช้งาน geoprocessing

การวิเคราะห์หาพื้นที่การใช้ประโยชน์ที่ดินในตำบลที่ต้องการ
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
print("ok")
arcpy.MakeFeatureLayer_management(tam, "lyr_tam")
arcpy.SelectLayerByAttribute_management("lyr_tam", 'NEW_SELECTION',
                                        "TAM_CODE = '501001'")
```

เลือกหมู่บ้าน
```python
arcpy.MakeFeatureLayer_management(vill, "lyr_vill")
arcpy.SelectLayerByLocation_management(in_layer="lyr_vill", overlap_type="INTERSECT",
                                       select_features="lyr_tam",
                                       search_distance=0,
                                       selection_type="NEW_SELECTION")
 ```

 สร้างชั้นข้อมูลใหม่
 ```python
 arcpy.CopyFeatures_management("lyr_vill", out_feature_class=outVill)
print("ok")
```

บัฟเฟอร์หมู่บ้าน
```python
arcpy.Buffer_analysis(in_features=outVill, out_feature_class=buffVill,
                      buffer_distance_or_field=500,
                      line_side="FULL",
                      line_end_type="ROUND",
                      dissolve_option="ALL"
                      )
print("ok")
```

Clip พื้นที่การใช้ประโยชน์ที่ดินเฉพาะพื้นที่หมู่บ้านที่เลือก
```python
arcpy.Clip_analysis(in_features=lu, clip_features=buffVill,
                    out_feature_class=luBuff)
print("ok")
```

การสร้างกล่องเครื่องมือ แก้ใขโค้ดเพื่อรับค่า โดยเพิ่ม arcpy.GetParameterAsText(0) ลงไป
```python
import arcpy

# input
vill = arcpy.GetParameterAsText(0)
tam = arcpy.GetParameterAsText(1)
exp = arcpy.GetParameterAsText(2)
lu = arcpy.GetParameterAsText(3)
bval = arcpy.GetParameterAsText(4)

# output
sel_tam = arcpy.GetParameterAsText(5)
sel_vill = arcpy.GetParameterAsText(6)
buff_vill = arcpy.GetParameterAsText(7)
final = arcpy.GetParameterAsText(8)

print("created varible")
arcpy.AddMessage("created varible")
# select tam
arcpy.MakeFeatureLayer_management(tam, "lyrTam")
arcpy.SelectLayerByAttribute_management(
    in_layer_or_view="lyrTam",
    selection_type="NEW_SELECTION",
    where_clause=exp)

# make selected tambon
arcpy.CopyFeatures_management(in_features="lyrTam", out_feature_class=sel_tam)
print("selected tambon")
arcpy.AddMessage("selected tambon")

# select village by tambon
arcpy.MakeFeatureLayer_management(vill, "lyrVill")
arcpy.SelectLayerByLocation_management(in_layer="lyrVill",
                                       overlap_type="INTERSECT",
                                       select_features=sel_tam,
                                       search_distance=0,
                                       selection_type="NEW_SELECTION")

arcpy.CopyFeatures_management(
    in_features="lyrVill", out_feature_class=sel_vill)
print("selected village")
arcpy.AddMessage("selected village")

# buffer village
arcpy.Buffer_analysis(in_features=sel_vill,
                      out_feature_class=buff_vill,
                      buffer_distance_or_field=bval,
                      line_side="FULL",
                      line_end_type="ROUND",
                      dissolve_option="ALL")
print("created buffer")
arcpy.AddMessage("selected buffer")

# clip
arcpy.Clip_analysis(in_features=lu,
                    clip_features=buff_vill,
                    out_feature_class=final)
print("yesh!! finish")
arcpy.AddMessage("finish")
```


## Raster processing with ArcPy
ตัวอย่าง การวิเคราะห์ข้อมูลปริมาณน้ำฝนด้วยการประมาณค่าเชิงพื้นที่ (IDW interpolation) โดยกำหนดพารามิเตอร์ที่ใช้ในการวิเคราะห์ ดังนี้

```python
import arcpy
from arcpy.sa import *

# input
inPoint = r"C:\lab_arcpy\data4326\cm_rain_32647.shp"

# Execute IDW
outIDW = Idw(in_point_features=inPoint,
             z_field="APR",
             cell_size=100,
             power=2)

# Save the output
outIDW.save(r"C:\lab_arcpy\output\r_apr")
print("finish")
arcpy.AddMessage("finish")
```

กำหนด environment ให้กับข้อมูล
```python

inPoint = r"C:\lab_arcpy\data4326\cm_rain_32647.shp"
zone = r"C:\lab_arcpy\data4326\cm_tambon_32647.shp"

arcpy.env.extent = zone
arcpy.env.mask = zone

outIDW = arcpy.sa.Idw(in_point_features=inPoint,
                      z_field="MAY",
                      cell_size=100,
                      power=2)

# Save the output
outIDW.save(r"C:\lab_arcpy\output\\"+"MAY")
print("finish")
arcpy.AddMessage("finish")
```

วิเคราะห์ความลาดชัน
```python
slopeRas = r"C:\lab_arcpy\output\cm_slope32647"
outSlope = arcpy.sa.Slope(inDem,
                          output_measurement="DEGREE",
                          z_factor="#",
                          method="#",
                          z_unit="#"
                          )
outSlope.save(slopeRas)
print("slope success")
arcpy.AddMessage("slope success")
```

วิเคราะห์ด้วย con พื้นที่ที่มีความลาดชันมากกว่า 20 องศา
```python
slopCon = r"C:\lab_arcpy\output\cm_conras"
outCon = arcpy.sa.Con(slopeRas, 1, 0, "VALUE >= 20")
outCon.save(slopCon)
print("con success")
arcpy.AddMessage("con success")
```

set workspace และสั่งลบ raster เดิม

```python
arcpy.env.workspace = r"C:\lab_arcpy\output"

ras = arcpy.ListRasters()

if(len(ras) >= 1):
    for r in ras:
        print(r)
        arcpy.Delete_management(r)
print("delete old raster")
arcpy.AddMessage("delete old raster")
```

การวนลูปให้ทำงานซ้ำ
```python
import arcpy
from arcpy.sa import *
from arcpy import env

# input
inPoint = r"C:\lab_arcpy\data4326\cm_rain_32647.shp"
zone = r"C:\lab_arcpy\data4326\cm_tambon_32647.shp"

arcpy.env.mask = zone
arcpy.env.extent = zone

fld = arcpy.ListFields(inPoint)

for f in fld:
    # print(f.name)
    if(f.name == "APR" or f.name == "MAY"):
        print(f.name)
        # Execute IDW
        # arcpy.sa.Idw()
        outIDW = Idw(in_point_features=inPoint,
                     z_field=f.name,
                     cell_size=100,
                     power=2)

        # Save the output
        outIDW.save(r"C:\lab_arcpy\output\\"+str(f.name))
        print("finish")
arcpy.AddMessage("finish")
```

สร้าง con เพื่อกำหนดให้พื้นที่มีปริมาณน้ำฝนมากกว่า 50 มม. และ slope ที่มีมากกว่า 20 องศา
```python
        outRas = r"C:\lab_arcpy\output\\"+str(f.name)
        final = r"C:\lab_arcpy\output\fn_"+f.name
        outIDW.save(outRas)
        print("idw success")

        outFinal = arcpy.sa.Con(
            ((outRas > 50) & (slopCon == 1)), outRas, 0)
        print(outFinal)
        outFinal.save(final)

        print("final success")
        arcpy.AddMessage("final success")
```


