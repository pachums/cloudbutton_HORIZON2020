"""
Autor = Juanma Cintas Rodríguez
Fecha = 21/03/2019
email = juanmanuel.cintas@fundacionmatrix.es

Descripción:
Produce un Modelo Digital de Elevaciones (DEM por sus siglas en inglés).

Argumentos:
@lasfile = fichero de la nube de puntos LiDAR con extension las o laz.
@outputfile = fichero tif de devuelto.
@resolution = Resolución del fichero de salida en la unidades del sistema de referencia.


La documentación de la libería pdal se puede encontrar en la siguiente
dirección: https://pdal.io/index.html

"""

import pdal
import json

def DEMonizator(lasfile, outputfile, resolution = 1000):
        creating_json = {
                "pipeline": [
                {
                        "type": "readers.las",
                        "filename": f"{lasfile}",
                        "spatialreference": "EPSG:25830"
                },
                {
                        "type": "filters.range",
                        "limits": "Classification[2:2]"
                },
                {
                        "type": "writers.gdal",
                        "gdaldriver": "GTiff",
                        "nodata": "-9999",
                        "output_type": "idw",
                        "resolution": f"{resolution}",
                        "filename": f"{outputfile}"
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
        
if __name__ == "__main__":
        import os
        for file in os.listdir("tiles"):
                if "laz" in file:
                        filez = file.split(".")[0]
                        outputfile = f"mdts/dem_{filez}.tif"
                        DEMonizator(f"tiles/{file}", outputfile, resolution = 5.0)
