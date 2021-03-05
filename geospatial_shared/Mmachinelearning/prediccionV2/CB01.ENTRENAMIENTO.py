"""
Autor = Alberto Álvarez Vales
Fecha = 7/03/2019
email = alberto.alvarez@fundacionmatrix.es

Descripción:
Genera un modelo ML para determinar el uso del suelo

Se utiliza Geopandas para leer los formatos de archivo y Apache Spark para procesar los datos y generar el modelo.
"""
from geopandas import read_file,GeoDataFrame
from pyspark import SparkContext
from pyspark.sql import SQLContext
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.classification import RandomForestClassifier # este algoritmo es el que ofreció mejores resultados en las pruebas
from pyspark.ml.evaluation import MulticlassClassificationEvaluator

sc = SparkContext.getOrCreate()
spark = SQLContext(sc)

datosGlobales=read_file("segmented_TopFixed.gpkg")
datosEntrenamiento=read_file("ForClassifySegments.gpkg")

dfGlobal=spark.createDataFrame(datosGlobales)
dfEntrenamiento=spark.createDataFrame(datosEntrenamiento)
dfE=dfEntrenamiento.select("cat","tipo").join(dfGlobal,"cat","inner")

columnas=['area', 'perimeter',  'fd', 'perimeter', 'compact_circle', 'fd', 'B1_sum', 'B1_mean', 'B1_median', 'B1_stdev', 'B1_min', 'B1_max', 'B1_variance', 'B2_sum', 'B2_mean', 'B2_median', 'B2_stdev', 'B2_min', 'B2_max', 'B2_variance', 'B3_sum', 'B3_mean', 'B3_median', 'B3_stdev', 'B3_min', 'B3_max', 'B3_variance']
constructor=VectorAssembler(inputCols=columnas,outputCol="features")

dfEF=constructor.transform(dfE).select("cat","features","tipo")

entrena,evalua=dfEF.randomSplit([0.8,0.2])

rf=RandomForestClassifier(labelCol="tipo")

modelo=rf.fit(entrena)

pred=modelo.transform(evalua)

evaluador=MulticlassClassificationEvaluator(labelCol="tipo",metricName="accuracy")

evaluador.evaluate(pred)

modeloOk=rf.fit(dfEF)

modeloOk.write().overwrite().save("modelorf") #eliminar overwrite() si no se quiere sobreescribir el modelo

