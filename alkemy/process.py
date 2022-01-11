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
          'Domicilio': 'domicilio',
          'IdDepartamento': 'id_departamente',
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
    renamer['Bibliotecas Populares'] = renamer['Salas de Cine']

    for categoria, file in files.items():
        tmpdf = pd.read_csv(file, encoding='utf-8')
        print(tmpdf.columns, categoria)
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
