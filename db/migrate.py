import sys
import os
import psycopg
import logging
from decouple import config


def migrate_up():
    try:
        sqlf = open(
            os.path.join(
              os.path.dirname(os.path.realpath(__file__)),
              'migrateup.sql'
            ),
            'r'
        )
        sqlcontent = sqlf.read()
        sqlf.close()
        sqlComms = sqlcontent.split(';')

        with psycopg.connect(config('DB_URI')) as conn:
            with conn.cursor() as cur:
                for comm in sqlComms:
                    cur.execute(comm)
                conn.commit()
    except Exception as e:
        logging.error('operation failed; error: %s', e)
    else:
        logging.info('migration completed successfully')


def migrate_down():
    try:
        sqlf = open(
            os.path.join(
              os.path.dirname(os.path.realpath(__file__)),
              'migratedown.sql'
            ),
            'r',
        )
        sqlcontent = sqlf.read()
        sqlf.close()
        sqlComms = sqlcontent.split('\n')

        with psycopg.connect(config('DB_URI')) as conn:
            with conn.cursor() as cur:
                for comm in sqlComms:
                    cur.execute(comm)
                conn.commit()
    except Exception as e:
        logging.error('operation failed; error: %s', e)
    else:
        logging.info('migration completed successfully')


def main():
    if len(os.sys.argv[1]) > 2:
        sys.exit(1)

    if (os.sys.argv[1] == "up"):
        migrate_up()
    elif (os.sys.argv[1] == "down"):
        migrate_down()
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
