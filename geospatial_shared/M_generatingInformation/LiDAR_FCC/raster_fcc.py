"""
Autor = Juanma Cintas Rodríguez
Fecha = 21/03/2019
email = juanmanuel.cintas@fundacionmatrix.es

Descripción:
Crea una proporción de una clase respecto al total de puntos, basado en el cálculo de Fracción Cabida Cubierta (FCC)
presentado por García et al (2011) (DOI:10.10016/j.jag.2011.03.006). Dependerá del raster introducido en la función
si es calculada la FCC, la TCC o la SCC.

Argumentos:
@input = Raster del cual será computada la relación (FCC, TCC o SCC)
@output = Nombre del raster a generar.
@winodw = Tamaño de la ventana móvil usada para calcular la relación. A cosiderar que, cuanto menor sea la resolución,
mayor deberá ser la ventana móvil para conseguir buenos resultados. Una medida puede ser 4 veces la resolución del raster.
@breakpoint = Valor a partir del cual se consideraran las celdas del raster como vegetación.


La documentación de la libería pdal se puede encontrar en la siguiente
dirección: https://pdal.io/index.html

Documentación acerca de gdal/ogr y su API de python puede ser encontrada en el siguiente enlace:
https://gdal.org

Documentación acerca de la librería scipy puede ser encontrada en el siguiente enlace:
https://www.scipy.org/

Documentación acerca de la libreri numpy puede ser encontrada en el siguiente enlace:
http://www.numpy.org/
"""

from osgeo import gdal
from osgeo import osr
from scipy import ndimage
import numpy as np


def compute_fraction(array):
    nveg = np.sum(array == 1)
    total = len(array)
    out = (nveg/total)*100
    return(out)


def FCC(input, output, window = 3, breakpoint = 0.01):
    # Reading data needed
    tch = input
    in_ds = gdal.Open(tch)
    rows = in_ds.RasterYSize
    cols = in_ds.RasterXSize
    in_band = in_ds.GetRasterBand(1)
    data = in_band.ReadAsArray(0, 0, cols, rows).astype(np.float)

    # Reclassifying data
    data[data > breakpoint] = 1
    data[data <= breakpoint] = 0

    # Computing fraction on the whole raster through a moving window.
    TCC = ndimage.generic_filter(data, compute_fraction, size = window)

    # Setting output
    gtiff_driver = gdal.GetDriverByName("GTiff")
    out_ds = gtiff_driver.Create(output, cols, rows, 1, in_band.DataType)
    out_ds.SetProjection(in_ds.GetProjection())
    out_ds.SetGeoTransform(in_ds.GetGeoTransform())

    # Writing data
    out_band = out_ds.GetRasterBand(1)
    out_band.WriteArray(TCC)
    # out_ds.BuildOverviews("Average", [2, 4, 8, 16, 32])

    out_ds.FlushCache()

    del in_ds, out_ds

if __name__ == "__main__":
    FCC(input = "sch5.tif", output = "scci5.tif", window = 20, breakpoint = 0.2)