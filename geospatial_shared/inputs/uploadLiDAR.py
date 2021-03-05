"""
Autor = Juanma Cintas
Fecha = 13/02/2019
email = juanmanuel.cintas@fundacionmatrix.es

Descripción:
Este módulo contiene un método para la subida de nubes de puntos
a un servidor postgresql basado en pdal.

La documentación de la libería pdal se puede encontrar en la siguiente
dirección: https://pdal.io/index.html

"""

import pdal
import json
import os

def uploadLiDAR(las,
                table,
                dbname,
                srs = "25830+3855",
                postgres_user = "postgres",
                postgres_host = "localhost",
                postgres_password = "postgres",
                overwrite = "false",
                column = "pa"):
                        
                        # JSON filter for pdal
                        creating_json = {
                                "pipeline": [

                                        {
                                        "type": "readers.las",
                                        "filename": f"{las}",
                                        "spatialreference": f"EPSG:{srs}"
                                        },
                                        {
                                        # It saves only 500 points
                                        "type": "filters.chipper",
                                        "capacity": "500"
                                        },
                                        {
                                        # Argumments needed to communicate with the database
                                        "type":"writers.pgpointcloud",
                                        "connection": f"dbname='{dbname}' user='{postgres_user}' host='{postgres_host}' password='{postgres_password}'",
                                        "table": f"{table}",
                                        "overwrite": f"{overwrite}",
                                        "compression": "laszip",
                                        "srid": f"{srs}",
                                        "column": f"{column}"
                                        }
                                 ]
                        }

                        consulta = json.dumps(creating_json, indent=4)
                        print(consulta)

                        pipeline = pdal.Pipeline(consulta)
                        pipeline.validate() # Check if json options are good
                        pipeline.loglevel = 8
                        
                        # Executing JSON filter
                        count = pipeline.execute()
                        print(count)

if __name__=='__main__':

        database = "lidar_test"
        tabla = "tabla_prueba"
        folder_with_las = "for_test"

        for file in os.listdir(folder_with_las):
                if "laz" in file:
                        archivolas = f"{folder_with_las}/{file}"
                        uploadLiDAR(las = archivolas, dbname = database, table = tabla, srs = "25830")
        
        
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                                
                        
                
                
