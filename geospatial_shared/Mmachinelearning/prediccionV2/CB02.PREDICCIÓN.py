"""
Autor = Alberto Álvarez Vales
Fecha = 7/03/2019
email = alberto.alvarez@fundacionmatrix.es

Descripción:
Utiliza el modelo ML generado con el script de entrenamiento para intentar predecir el uso del suelo.

Se utiliza Geopandas para leer los formatos de archivo y Apache Spark para procesar los datos y generar el modelo.
"""

from pyspark import SparkContext
from pyspark.sql import SQLContext
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.classification import RandomForestClassificationModel
from geopandas import read_file,GeoDataFrame
import pandas as pd

sc = SparkContext.getOrCreate()
spark = SQLContext(sc)

datosGlobales=read_file("segmented_TopFixed.gpkg")

dfGlobal=spark.createDataFrame(datosGlobales)

columnas=['area', 'perimeter',  'fd', 'perimeter', 'compact_circle', 'fd', 'B1_sum', 'B1_mean', 'B1_median', 'B1_stdev', 'B1_min', 'B1_max', 'B1_variance', 'B2_sum', 'B2_mean', 'B2_median', 'B2_stdev', 'B2_min', 'B2_max', 'B2_variance', 'B3_sum', 'B3_mean', 'B3_median', 'B3_stdev', 'B3_min', 'B3_max', 'B3_variance']
constructor=VectorAssembler(inputCols=columnas,outputCol="features")

dfEF=constructor.transform(dfGlobal).select("cat","features")

modelo=RandomForestClassificationModel().read().load("modelorf")

pred=modelo.transform(dfEF).select("cat","prediction")

predPandas=pd.merge(datosGlobales, pred.toPandas(), on='cat', how='inner')

geoPredPandas=GeoDataFrame(predPandas)

geoPredPandas.to_file("prediccion.gpkg",driver="GPKG")