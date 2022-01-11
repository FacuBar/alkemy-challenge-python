from logging import log
from request import download_csvs
from process import normalize
from decouple import config


def main():
    downloaded = download_csvs()
    df = normalize(downloaded)


if __name__ == '__main__':
    main()
