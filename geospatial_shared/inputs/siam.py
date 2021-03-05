"""
Este módulo contiene métodos de utilidad para la consulta
de información meteorológica del Sistema de Información
Agrario de Murcia (SIAM)

AUTOR: Juanjo

FECHA DE CREACIÓN: 11/02/2019

"""

import errno
import os
import requests
import urllib.parse
from bs4 import BeautifulSoup

RESULTS_DIR = 'results'
SIAM_RESULTS_DIR = 'siam'


def download_weather_info():
    """
    Descarga un fichero CSV con la información meteorológica
    correspondiente con el informe: "INFORME AGROMETEOROLÓGICO
    DE UN DÍA". Los datos del informe se corresponden con los
    del día anterior al momento de la ejecución de este script.
    """

    url = 'http://siam.imida.es'

    response = requests.get(url)
    if response.status_code != 200:
        print('>>>>>>>>>>> Error: ' + response.text)
        exit(response.status_code)
    soup = BeautifulSoup(response.text, 'lxml')
    report_link = soup.find('a', text='INFORME AGROMETEOROLÓGICO DE UN DÍA')
    report_page_link = urllib.parse.urljoin(url, '/apex/' + report_link['href'])

    response = requests.get(report_page_link)
    if response.status_code != 200:
        print('>>>>>>>>>>> Error: ' + response.text)
        exit(response.status_code)
    soup = BeautifulSoup(response.text, 'lxml')
    date_str = soup.find('input', {'id': 'P47_FECHA'})['value']
    date_str = date_str.replace('/', '_')
    csv_report_link = report_page_link + ':CSV::::'
    response = requests.get(csv_report_link)
    if response.status_code != 200:
        print('>>>>>>>>>>> Error: ' + response.text)
        exit(response.status_code)
    else:
        result_dir = os.path.join(RESULTS_DIR, SIAM_RESULTS_DIR)
        file_path = os.path.join(result_dir, 'siam_' + date_str + '.csv')
        with open(file_path, 'wb') as siam_csv_file:
            siam_csv_file.write(response.content)
    print('>>> Terminó')


if __name__ == '__main__':
    if not os.path.exists(RESULTS_DIR):
        try:
            os.makedirs(RESULTS_DIR)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
    result_dir = os.path.join(RESULTS_DIR, SIAM_RESULTS_DIR)
    if not os.path.exists(result_dir):
        try:
            os.makedirs(result_dir)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
    download_weather_info()
