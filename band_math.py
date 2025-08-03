def cal_ndvi(nir, red):
    ndvi = (nir - red)/(nir + red)
    return ndvi


def cal_ndwi(nir, swir):
    ndwi = (nir - swir) / (nir + swir)
    return ndwi
