"""
Autor = Alberto Álvarez Vales
Fecha = 9/04/2019
email = alberto.alvarez@fundacionmatrix.es

Descripción:
Validación del modelo ML para determinar el uso del suelo

Geopandas se  utiliza para leer el formato GPKG y Scikit-learn para verificar los resultados utilizando "Cross Validation" para validar el modelo.
"""
import pandas as pd
import numpy as np 
from geopandas import read_file,GeoDataFrame
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

datosGlobales=read_file("../prediccionV2/segmented_TopFixed.gpkg")
datosEntrenamiento=read_file("../prediccionV2/ForClassifySegments.gpkg")
df=datosEntrenamiento[["cat","tipo"]].merge(datosGlobales,on="cat",how="left").dropna()

columnas=['area', 'perimeter',  'fd', 'compact_circle', 'B1_sum', 'B1_mean', 'B1_median', 'B1_stdev', 'B1_min', 'B1_max', 'B1_variance', 'B2_sum', 'B2_mean', 'B2_median', 'B2_stdev', 'B2_min', 'B2_max', 'B2_variance', 'B3_sum', 'B3_mean', 'B3_median', 'B3_stdev', 'B3_min', 'B3_max', 'B3_variance']
`
y=np.array(df['tipo'])
X=np.array(df[columnas])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2,random_state=0)

clasificador=RandomForestClassifier(n_estimators=30)

from sklearn.model_selection import ShuffleSplit,cross_val_score

cv = ShuffleSplit(n_splits=10,test_size=0.2,random_state=0)

evaluacion=cross_val_score(clasificador,X,y,cv=cv)

print("EN %d PREDICCIONES\nACIERTO media:  %0.2f, desviación típica: %0.2f" % (cv.n_splits,evaluacion.mean(),evaluacion.std()*2))