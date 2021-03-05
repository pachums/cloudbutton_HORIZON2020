"""
This module contains useful methods for downloading
Sentinel-2 satellite imagery.

The different tiles of the MGRS coordinate system in which
Spain is divided can be found at https://www.asturnatura.com/sinflac/utm-mgrs.php

The documentation of the sentinelsat library can be consulted
at the following address:
https://sentinelsat.readthedocs.io/en/stable/api.html

SENT_USER and SENT_PASS must be provided with your username and password for Sentinel.

AUTHOR: Juanjo

DATE: 12/03/2019

"""

import collections
import os
import os.path
import zipfile

import sentinelsat

SENT_USER = 'YOUR USERNAME'
SENT_PASS = 'YOUR PASS'


ZIP_EXTENSION = ".zip"


def download_products(tiles, start_date, end_date, output_folder, show_progressbars=True):
    """
    Download all Sentinel-2 satellite products for product types S2MS2Ap and S2MSI1C

    :param tiles: Tiles to filter the download
    :param start_date: Starting date images were taken
    :param end_date: Final date images were taken
    :param output_folder: Directory in which the images will be stored
    :param show_progressbars: Indicates if progress bars are displayed during download
    """

    print('Downloading products')
    api = sentinelsat.SentinelAPI(user=SENT_USER,
                                  password=SENT_PASS,
                                  api_url='https://scihub.copernicus.eu/dhus',
                                  show_progressbars=show_progressbars)

    query_kwargs = {
        'platformname': 'Sentinel-2',
        'producttype': ('S2MS2Ap', 'S2MSI1C'),
        'cloudcoverpercentage': (0, 15),
        'date': (start_date, end_date)
    }

    products = collections.OrderedDict()
    for tile in tiles:
        kw = query_kwargs.copy()
        kw['tileid'] = tile
        pp = api.query(**kw)
        products.update(pp)

    api.download_all(products, output_folder)


def unzip_bands_dirs(sentinel_downloads_dir):
    print('Unzipping bands')
    sentinel_file_names = [os.path.join(sentinel_downloads_dir, f) for f in os.listdir(sentinel_downloads_dir) if
                           (os.path.isfile(os.path.join(sentinel_downloads_dir, f))) and (f.endswith(ZIP_EXTENSION))]
    for sentinel_zip_filename in sentinel_file_names:
        print(f'Unzipping {sentinel_zip_filename}')
        zip_ref = zipfile.ZipFile(sentinel_zip_filename)
        zip_ref.extractall(sentinel_downloads_dir)
        zip_ref.close()


def download_bands(tiles, start_date, end_date, sentinel_downloads_dir):

    print('Downloading bands from Sentinel')
    download_products(tiles=tiles,
                      start_date=start_date,
                      end_date=end_date,
                      output_folder=sentinel_downloads_dir)
    unzip_bands_dirs(sentinel_downloads_dir)
    print('Downloading bands from Sentinel finished')


if __name__ == '__main__':
    # Example of use
    start_date = '20190106'
    end_date = '20190107'
    TILES = ['30SXG']
    DOWNLOADS_DIR = '.'
    download_bands(TILES, start_date, end_date, DOWNLOADS_DIR)
