from osgeo import gdal_array as ga
import gdal, ogr, os, osr
import numpy as np
from osgeo import gdal

def Calculation_NDVI(in_filename,output_filename,Band1=1,Band2=2):
    gdal_data = gdal.Open(filename)

    img = gdal_data.ReadAsArray()

    arr=img[Band1,:,:]
    arr1=img[Band2,:,:]
    ga.numpy.seterr(all="ignore")

    ndvi=((arr1-arr)*1.0)/((arr1+arr)*1.0)
    ndvi1=ga.numpy.nan_to_num(ndvi)
    
    out=ga.SaveArray(ndvi1,output_filename,format = "GTiff",prototype =gdal_data)
    out=None
    print("Calculation NDVI success")