import logging
import os
import pandas as pd
import numpy as np


def normalize(files):
    normalizedfs = []
    # filters used by pandas
    selector = {
      'Salas de Cine': [
          'Nombre',
          'Web',
          'Mail',
          'Dirección',
          'IdDepartamento',
          'Localidad',
          'Cod_Loc',
          'Provincia',
          'IdProvincia',
          'CP',
          'Categoría',
          'Teléfono',
          'Fuente'  # not required on spec but necessary for processing
      ],
      'Museos': [
          'nombre',
          'web',
          'mail',
          'direccion',
          'localidad',
          'localidad_id',
          'provincia',
          'provincia_id',
          'codigo_postal',
          'telefono',
          'fuente'
      ]
    }
    selector['Bibliotecas Populares'] = selector['Salas de Cine'].copy()
    selector['Bibliotecas Populares'].remove('Dirección')
    selector['Bibliotecas Populares'].append('Domicilio')
    # filters used by pandas
    renamer = {
      'Salas de Cine': {
          'Nombre': 'nombre',
          'Web': 'web',
          'Mail': 'mail',
          'Dirección': 'domicilio',
          'IdDepartamento': 'id_departamento',
          'Localidad': 'localidad',
          'Cod_Loc': 'cod_localidad',
          'Provincia': 'provincia',
          'IdProvincia': 'id_provincia',
          'CP': 'código_postal',
          'Teléfono': 'número_de_teléfono',
          'Categoría': 'categoría',
          'Fuente': 'fuente'
      },
      'Museos': {
          'localidad_id': 'cod_localidad',
          'provincia_id': 'id_provincia',
          'direccion': 'domicilio',
          'telefono': 'número_de_teléfono',
          'codigo_postal': 'código_postal'
      }
    }
    renamer['Bibliotecas Populares'] = renamer['Salas de Cine'].copy()
    del renamer['Bibliotecas Populares']['Dirección']
    renamer['Bibliotecas Populares']['Domicilio'] = 'domicilio'

    for categoria, file in files.items():
        logging.info('normalizing %s', file)
        tmpdf = pd.read_csv(file, encoding='utf-8')
        # selecting only the required fields
        tmpdf = tmpdf[selector[categoria]]
        # renaming fields to coincide with the db ones
        tmpdf = tmpdf.rename(columns=renamer[categoria])
        # adding field required to aggregate
        if categoria == 'Museos':
            tmpdf['categoría'] = 'Museos'

        normalizedfs.append(tmpdf)

    normalizedf = normalizedfs[0].append(normalizedfs[1]).append(normalizedfs[2])  # noqa
    normalizedf.replace('s/d', np.nan, inplace=True)
    normalizedf.replace('', np.nan, inplace=True)
    return normalizedf


def registros_totales(df):
    logging.info('aggregations on records')
    regCateg = (df['categoría'].value_counts()
                .rename_axis('categoría')
                .reset_index(name='total'))

    regProvCat = (df[['provincia', 'categoría']].value_counts()
                  .rename_axis(['provincia', 'categoría'])
                  .reset_index(name='total'))

    regFuente = (df[['fuente']].value_counts()
                 .rename_axis(['fuente'])
                 .reset_index(name='total'))

    return regCateg, regProvCat, regFuente


def cine_aggregation(cinefile):
    logging.info('aggregations on cine dataframe')
    cinedf = pd.read_csv(cinefile, encoding='utf-8')

    cinedf = cinedf[[
      'Provincia',
      'Pantallas',
      'Butacas',
      'espacio_INCAA'
    ]]

    cinedf = cinedf.rename(columns={
        'Pantallas': 'pantallas',
        'Butacas': 'butacas',
        'espacio_INCAA': 'espacios_incaa',
        'Provincia': 'provincia'
    })

    # espaciosInca = (cinedf[['provincia', 'espacios_incaa']]
    #                 .replace('^(?i)(si)', 1 , regex=True)
    #                 .value_counts()
    #                 .rename_axis(['provincia'])
    #                 .reset_index(name='espacios_incaa'))

    incaa = (cinedf[['provincia', 'espacios_incaa']]
             .replace('', np.nan)
             .groupby(['provincia'])
             .count())
    cinedf = cinedf.groupby('provincia').sum()
    cinedf['espacios_incaa'] = incaa
    cinedf = cinedf.reset_index()

    return cinedf
