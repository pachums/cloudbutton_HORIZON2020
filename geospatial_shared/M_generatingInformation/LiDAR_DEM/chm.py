"""
Autor = Juanma Cintas Rodríguez
Fecha = 21/03/2019
email = juanmanuel.cintas@fundacionmatrix.es

Descripción:
Crea un Digital Height Model (por defecto), un Canopy Height Model (CHM), un Tree Canopy Height (TCH),
un Shrub Canopy Height (SCH) a partir de una nube de`puntos LiDAR.

Argumentos:
@lasfile = fichero de la nube de puntos LiDAR con extension las o laz.
@outputfile = fichero tif de devuelto.
@resolution = Resolución del fichero de salida en la unidades del sistema de referencia.
@type = Tipo de raster a producir. Puede dejarse en blanco o tomar los valores TCH, SCH y CHM. En el caso de
dejarse en blanco, un DHM será producido.


La documentación de la libería pdal se puede encontrar en la siguiente
dirección: https://pdal.io/index.html

"""

import pdal
import json

def CHMonizator(lasfile, outputfile, resolution = 5.0, type = None):
        
        if type == "TCH":
                kindoftype = {"type": "filters.range", "limits": "Classification[2:2],Classification[5:5]"}
        elif type == "SCH":
                kindoftype = {"type": "filters.range", "limits": "Classification[2:2],Classification[4:4]"}
        elif type == "CHM":
                kindoftype = {"type": "filters.range", "limits": "Classification[2:2],Classification[4:5]"}
        else:
                kindoftype = {"type": "filters.info"}
        creating_json = {
                "pipeline": [
                {
                        "type": "readers.las",
                        "filename": f"{lasfile}",
                        "spatialreference": "EPSG:25830"
                },
                {
                        "type": "filters.hag"
                },
                kindoftype,
                {
                        "type": "filters.ferry",
                        "dimensions": "HeightAboveGround=Z"
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
                        outputfile = f"chms/chm_{filez}.tif"
                        vegetation = "SCH"
                        CHMonizator(f"tiles/{file}", outputfile, resolution = 5.0)
