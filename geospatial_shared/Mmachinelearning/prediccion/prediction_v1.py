from rpy2.robjects.packages import importr
from rpy2 import robjects
from rpy2.robjects.vectors import StrVector
import rpy2.robjects.packages as rpackages

utils = importr("utils")
utils.chooseCRANmirror(ind=1)
base = importr("base")


packages = ("mlr", "sf")
names_to_install = []
for pkg in packages:
     if not rpackages.isinstalled(pkg):
         names_to_install.append(pkg)


if len(names_to_install) > 0:
    utils.install_packages(StrVector(packages_to_install))

robjects.r('''
    source("Rcode/prediction_poly.R")
    load("Model/modelo")
''')

predictsp_poly = robjects.globalenv['predictsp_poly']
modelo = robjects.globalenv['modelo']
toclassify = "vectores/segmented_TopFixed.gpkg"
id = "cat"

final = predictsp_poly(toclassify, modelo, id)
sf = importr("sf")
sf.st_write(final, "primertest.gpkg")