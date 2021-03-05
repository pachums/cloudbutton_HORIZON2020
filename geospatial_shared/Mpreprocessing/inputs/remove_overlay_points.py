"""
Autor = Juanma Cintas
Fecha = 21/02/2019
email = juanmanuel.cintas@fundacionmatrix.es

Descripción:
Clasifica los puntos de solape como ruido, de esta forma es más sencillo de ignorarlos en los posteriores procesos.

La documentación de la libería pdal se puede encontrar en la siguiente
dirección: https://pdal.io/index.html


"""


import pdal
import json

def remove_overlay_points(lasfile,
                 outputlas
                 ):

    creating_json = {
        "pipeline" : [
            {
                "type": "readers.las",
                "filename": f"{lasfile}"
            },
            {
                # Filter assigning points of class overlay (12) to class noise (7)
                "type": "filters.assign",
                "assignment": "Classification[12:12]=7"
            },
            {
                "type": "writers.las",
                "compression": "laszip",
                "filename": f"{outputlas}"
            }
        ]
    }

    consulta = json.dumps(creating_json, indent=4)
    print(consulta)

    pipeline = pdal.Pipeline(consulta)
    pipeline.validate()  # Check if json options are good
    pipeline.loglevel = 8
    count = pipeline.execute()
    print(count)

if __name__ == '__main__':
    import os
    files = os.listdir("for_test")
    for file in files:
        if ".las" in file or ".laz" in file:
            outputlas = file.split(".")[0] + "_noOverlay.laz"
            remove_overlay_points(lasfile = file, outputlas = outputlas)
