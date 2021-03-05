"""
Autor = Juanma Cintas
Fecha = 20/02/2019
email = juanmanuel.cintas@fundacionmatrix.es

Descripción:


La documentación de la libería pdal se puede encontrar en la siguiente
dirección: https://pdal.io/index.html


"""


import pdal
import json

def remove_noise(lasfile,
                 outputlas
                 ):

    creating_json = {
        "pipeline" : [
            {
                "type": "readers.las",
                "filename": f"{lasfile}"
            },
            {
                # Creates a window to find outliers. If they are found they are classified as noise (7).
                "type": "filters.outlier",
                "method": "statistical",
                "multiplier": 3,
                "mean_k": 8
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
            outputlas = file.split(".")[0] + "_denoise.laz"
            remove_noise(lasfile = file, outputlas = outputlas)
