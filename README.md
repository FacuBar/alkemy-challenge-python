# alkemy-python-test

- Crear entorno virtual `python3 -m venv env`

- Activar entorno virtual (posix) `source env/bin/activate`

- Instalar dependencias `pip install -r requirements.txt`

- [opcional] iniciar postgres en docker `make postgres`

- [opcional] crear db dentro de postgres -docker- `make createdb`

- Configurar db connection en .env

- Migrar esquemas a la base de datos `python3 db/migrate.py up`

- Iniciar aplicación `python3 alkemy core.py`
