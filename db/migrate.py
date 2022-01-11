import sys
import os
import psycopg


def migrate_up():
    try:
        sqlf = open('migrateup.sql', 'r')
        sqlcontent = sqlf.read()
        sqlf.close()

        sqlComms = sqlcontent = sqlcontent.split(';')
        with psycopg.connect("") as conn:
            with conn.cursor() as cur:
                for comm in sqlComms:
                    cur.execute(comm)

                conn.commit()
    except Exception as e:
        print('operation failed')


def migrate_down():
    try:
        sqlf = open('migratedown.sql', 'r')
        sqlcontent = sqlf.read()
        sqlf.close()

        sqlComms = sqlcontent = sqlcontent.split(';')
        with psycopg.connect("") as conn:
            with conn.cursor() as cur:
                for comm in sqlComms:
                    cur.execute(comm)

                conn.commit()
    except Exception as e:
        print('operation failed')


def main():
    if len(os.sys.argv[1]) > 2:
        sys.exit(1)

    if (os.sys.argv[1] == "up"):
        pass
    elif (os.sys.argv[1] == "down"):
        pass
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
