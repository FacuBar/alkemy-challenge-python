import sys
import requests
import pandas as pd
import os
import datetime
import logging

fecha = datetime.date.today().isoformat()

meses = {
    '01': 'enero',
    '02': 'febrero',
    '03': 'marzo',
    '04': 'abril',
    '05': 'mayo',
    '06': 'junio',
    '07': 'julio',
    '08': 'agosto',
    '09': 'septiembre',
    '10': 'octubre',
    '11': 'noviembre',
    '12': 'diciembre'
}

fetchUrlsFrom = 'https://datos.gob.ar/api/3/action/package_show?id=cultura-mapa-cultural-espacios-culturales'  # noqa
topicsOfInterest = ['Museos', 'Salas de Cine', 'Bibliotecas Populares']


def download_csvs():
    try:
        urls = requests.get(fetchUrlsFrom)
        body = urls.json()
    except Exception as e:
        logging.error('error while fetching/decoding urls: %s', e)
        sys.exit(1)

    for resource in body['result']['resources']:
        categoria = resource['name']
        logging.info('downloading .csv for %s', categoria)

        if categoria in topicsOfInterest:
            try:
                csv = requests.get(resource['url'])
            except Exception as e:
                logging.error(
                    '.csv for %s could not be downloaded; error: %s',
                    categoria, e
                )
            else:
                topicsOfInterest.remove(categoria)
                _save_to_file(csv.content, categoria)
                csv.close()

    urls.close()


def _save_to_file(bytes, categoria):
    directory, filename = _get_directory_and_filename(categoria)

    if not os.path.exists(directory):
        os.makedirs(directory)

    fileDir = os.path.join(directory, filename)
    if os.path.isfile(fileDir):
        os.remove(fileDir)

    open(fileDir, 'wb').write(bytes)

    logging.info('file %s downloaded successfully', filename)


def _get_directory_and_filename(categoria):
    base = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    fechaA = fecha.split('-')
    fechaDirectory = f'{fechaA[0]}-{meses[fechaA[1]]}'
    directory = os.path.join(base, categoria.lower(), fechaDirectory)
    filename = f'{categoria.lower()}-{fecha}.csv'

    return(directory, filename)


download_csvs()
