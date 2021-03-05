"""
Autor = Juanma Cintas
Fecha = 19/02/2019
email = juanmanuel.cintas@fundacionmatrix.es

Descripción:
Devuelve un shapefile con puntos de temperatura desde una base de datos. La creación de la base de datos está aún por realizarse. 
Contendrá datos AEMET de temperatura para el periodo 1971-2017.

"""

import geopandas as gpd
import ogr
import psycopg2
import shapely
import shapely.wkt
from read_dbLiDAR import get_layerextent


def read_temperaturas(database, table, periodo, out_file,
                        user = "postgres", password = "postgres", 
                        layer = None, extent = None, srs = 25830,
                        temperatura_variable = "tm_mes", temperatura_name = "tmed",
                        rango_de_años = 15):
        
        if layer is not None:
                extent = get_layerextent(layer)
        
        if extent is not None:
                sql_envelope = f"{extent}, {srs}"
        
        # Conexión con la base de datos
        connection = psycopg2.connect(database = database,
                              user = user, password  = password)
        cursor = connection.cursor()
        
        # Consulta sql para un periodo de tiempo
        p1 = periodo[0]
        p2 = periodo[1]
        cursor.execute( 
               f"""WITH subst AS (
                        select
                                indicativo,
                                count(distinct(year)) as len
                        from
                                {table}
                        where
                                variable = '{temperatura_variable}'
                                and
                                year between {p1} and  {p2}
                        group by
                                indicativo
                        )
                    select
                        a.indicativo,
                        avg(a.values)/10 as {temperatura_name},
                        st_astext(a.geom) as geom
                    from
                        {table} as a
                    inner join
                        subst as b
                    using
                        (indicativo)
                    where
                        a.year between {p1} and {p2}
                        and
                        b.len >= {rango_de_años}
                        and
                        a.variable = '{temperatura_variable}'
                        and
                        st_intersects(a.geom, st_MakeEnvelope({sql_envelope}))
                    group by
                        a.indicativo,
                        a.geom;"""                            
        )
        
        # Guardando puntos de temperatura en una capa.
        lista = rows_list = []
        for indicativo, temperatura, geom in cursor:
                data = {'indicativo':indicativo, f'{temperatura_name}':temperatura, 'geometry':shapely.wkt.loads(geom)}
                lista.append(data)
        
        gdf = gpd.GeoDataFrame(lista, crs = f'epsg:{srs}').set_index('indicativo')
        gdf[f'{temperatura_name}'] = gdf[f'{temperatura_name}'].astype("float")
        gdf.to_file(out_file)
        print("Archivo creado")       
        
        
  
if __name__=="__main__":
        database = "climvac"
        table = "monthly_temperature_point"
        periodo = [1971, 2000]
        layer_extent = "murcia.gpkg"
        out_file = "temperatura_murcia.gpkg"
        
        read_temperaturas(database = database, table = table, periodo = periodo, out_file = out_file, layer = layer_extent)
           
        
        
