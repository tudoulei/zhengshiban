import gdal
import os
import sys
import osr
import math
import numpy as np
from gdalconst import *


# 给栅格最外圈加一圈
def assignBCs(elevGrid):
    ny, nx = elevGrid.shape
    Zbc = np.zeros((ny + 2, nx + 2))
    Zbc[1:-1, 1:-1] = elevGrid

    Zbc[0, 1:-1] = elevGrid[0, :]
    Zbc[-1, 1:-1] = elevGrid[-1, :]
    Zbc[1:-1, 0] = elevGrid[:, 0]
    Zbc[1:-1, -1] = elevGrid[:, -1]

    Zbc[0, 0] = elevGrid[0, 0]
    Zbc[0, -1] = elevGrid[0, -1]
    Zbc[-1, 0] = elevGrid[-1, 0]
    Zbc[-1, -1] = elevGrid[-1, 0]

    return Zbc


# 计算dx,dy
def calcFiniteSlopes(elevGrid, dx):
    Zbc = assignBCs(elevGrid)

    Sx = (Zbc[1:-1, :-2] - Zbc[1:-1, 2:]) / (2 * dx)  # WE方向
    Sy = (Zbc[2:, 1:-1] - Zbc[:-2, 1:-1]) / (2 * dx)  # NS方向

    return Sx, Sy


# 投影转换
def convertProjection(data, filename):
    landsatData = gdal.Open(filename, GA_ReadOnly)

    oldRef = osr.SpatialReference()
    oldRef.ImportFromWkt(data.GetProjectionRef())

    newRef = osr.SpatialReference()
    newRef.ImportFromWkt(landsatData.GetProjectionRef())

    transform = osr.CoordinateTransformation(oldRef, newRef)

    tVect = data.GetGeoTransform()
    nx, ny = data.RasterXSize, data.RasterYSize
    (ulx, uly, ulz) = transform.TransformPoint(tVect[0], tVect[3])
    (lrx, lry, lrz) = transform.TransformPoint(tVect[0] + tVect[1] * nx, tVect[3] + tVect[5] * ny)

    memDrv = gdal.GetDriverByName('MEM')

    dataOut = memDrv.Create('name', int((lrx - ulx) / dx), int((uly - lry) / dx), 1, gdal.GDT_Float32)

    newtVect = (ulx, dx, tVect[2], uly, tVect[4], -dx)

    dataOut.SetGeoTransform(newtVect)
    dataOut.SetProjection(newRef.ExportToWkt())

    # Perform the projection/resampling
    res = gdal.ReprojectImage(data, dataOut, oldRef.ExportToWkt(), newRef.ExportToWkt(), gdal.GRA_Cubic)

    return dataOut