"""
Autor = Juanma Cintas
Fecha = 13/02/2019
email = juanmanuel.cintas@fundacionmatrix.es

Descripción:
Crea un archivo .laz/las a partir de una cosulta sql a una base de datos postgresql con la opción, recomendada, de indicar el extent máximo o 
la ruta a una capa vectorial desde donde obtener el extent. El archivo creado, si es demasiado grande, debe ser divido en tiles a posteriori.

La documentación de la libería pdal se puede encontrar en la siguiente
dirección: https://pdal.io/index.html

La documentación de la librería ogr se puede encontrar en la siguiente
dirección: https://gdal.org/1.11/ogr/

"""

import pdal
import json
import ogr

# Getting Layer extent to subset points in the database
def get_layerextent(layer):
        longitud = len(layer.split("."))
        driver_name = layer.split(".")[longitud - 1]
        if driver_name == "gpkg":
                driver = ogr.GetDriverByName("GPKG")
        if driver_name == "shp":
                driver = ogr.GetDriverByName("ESRI Shapefile")
                
        ds = driver.Open(layer)
        xmin, xmax, ymin, ymax = ds.GetLayer().GetExtent()
        extent = f"{xmin}, {ymin}, {xmax}, {ymax}"        
        
        del ds
        
        return(extent)

def read_dbLiDAR(outputlas,
                 table,
                 dbname,
                 column = "pa",
                 srs = "25830+3855",
                 postgres_user = "postgres",
                 postgres_host = "localhost",
                 postgres_password = "postgres",
                 extent = None,
                 layer_extent = None ):
        
        # Creating extent from layer path
        if layer_extent is not None:
                exent = get_layerextent(layer_extent)
        
        # Creating sql query
        if extent is not None:
                where_sql = extent + ", " + srs
                
                creating_json = {
            "pipeline" : [
                {
                    "type":"readers.pgpointcloud",
                    "connection": f"dbname='{dbname}' user='{postgres_user}' password ='{postgres_password}' host='{postgres_host}'",
                    "table": f"{table}",
                    "column": f"{column}",
                    "spatialreference": f"EPSG:{srs}",
                    "where": f"PC_Intersects(pa, ST_MakeEnvelope({where_sql}))"
                },
                {
                    "type": "writers.las",
                    "filename": f"{outputlas}"
                }    

            ]
        }
        
        else:
                creating_json = {
            "pipeline" : [
                {
                    "type":"readers.pgpointcloud",
                    "connection": f"dbname='{dbname}' user='{postgres_user}' password ='{postgres_password}' host='{postgres_host}'",
                    "table": f"{table}",
                    "column": f"{column}",
                    "spatialreference": f"EPSG:{srs}"
                },
                {
                    "type": "writers.las",
                    "filename": f"{outputlas}"
                }    

            ]
        }
                
        

        consulta = json.dumps(creating_json, indent = 4)
        print(consulta)

        pipeline = pdal.Pipeline(consulta)
        pipeline.validate()  # Check if json options are good
        pipeline.loglevel = 8
        count = pipeline.execute()
        print(count)

if __name__ == '__main__':

    outputlas = "results/test.laz"
    database = "lidar_test"
    tabla = "tabla_prueba"
    srs = "25830"
    layer = "for_test/murcia.gpkg"

    read_dbLiDAR(outputlas, tabla, database, srs = srs, layer_extent = layer)
