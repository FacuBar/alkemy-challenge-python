import logging
from request import download_csvs
from process import normalize, registros_totales, cine_aggregation
from decouple import config
from sqlalchemy import create_engine
import sys

logging.basicConfig(
    level=logging.DEBUG,
    format='(%(asctime)s) [%(levelname)s] %(message)s',
    datefmt='%I:%M:%S %p'
    )


def main():
    # csvs are downloaded from gov api
    downloaded = download_csvs()
    # all data is normalized into one table
    df = normalize(downloaded)
    # the ammount of records are counted accourding to various params
    regCateg, regProvCat, regFuente = registros_totales(df)
    # cine aggregation
    cineAgg = cine_aggregation(downloaded['Salas de Cine'])

    try:
        engine = create_engine(config('DB_URI'))
    except Exception as e:
        logging.error('error while trying to connect to the db %s', e)
        sys.exit(1)
    try:
        engine.execute('TRUNCATE espacios_culturales, registros_categoria, registros_provincia_categoria, registros_fuente, cines_aggr_provincia')  # noqa
        logging.info('all tables on the database have been truncated')

        df.to_sql(
          name='espacios_culturales',
          con=engine,
          if_exists='append',
          method='multi',
          index=False
        )
        logging.info('rows inserted on espacios_culturales successfully')

        regCateg.to_sql(
          name='registros_categoria',
          con=engine,
          if_exists='append',
          method='multi',
          index=False
        )
        logging.info('rows inserted on registros_categoria successfully')

        regProvCat.to_sql(
          name='registros_provincia_categoria',
          con=engine,
          if_exists='append',
          method='multi',
          index=False
        )
        logging.info('rows inserted on registros_provincia_categoria successfully')  # noqa

        regFuente.to_sql(
          name='registros_fuente',
          con=engine,
          if_exists='append',
          method='multi',
          index=False
        )
        logging.info('rows inserted on registros_fuente successfully')

        cineAgg.to_sql(
          name='cines_aggr_provincia',
          con=engine,
          if_exists='append',
          method='multi',
          index=False
        )
        logging.info('rows inserted on cines_aggr_provincia successfully')
    except Exception as e:
        # error handling to be improved
        print(e.__str__()[0:1500])
        sys.exit(1)


if __name__ == '__main__':
    main()
