import logging
import sqlite3
from contextlib import contextmanager

from src.util.unexpectedException import UnexpectedException

logger = logging.getLogger(__name__)


class Database:
    '''
    Encapsula la conexión a una base de datos, la ejecución de consultas y scripts para
    generar el esquema y carga inicial de datos.

    Nota: por simplicidad, cada operación abre y cierra su propia conexión.
    El uso de un context manager garantiza que la conexión y el cursor
    se cierran siempre, incluso si se produce una excepción.
    '''

    def __init__(self, db_path):
        self.db_path = db_path

    @contextmanager
    def _connect(self):
        conn = sqlite3.connect(self.db_path)
        #Habilita el manejo de objetos Row para los resultados de la consulta
        conn.row_factory = sqlite3.Row
        curs = conn.cursor()
        try:
            yield conn, curs
        finally:
            curs.close()
            conn.close()

    #Ejecuta un script SQL contenido en el fichero nameFile sobre la base de datos.
    def executeScript(self, name_file):
        with open(name_file, 'r') as sql_file:
            sql_script = sql_file.read()
        self.executeScriptBatch(sql_script)

    #Ejecuta un script SQL contenido en el string sql_script sobre la base de datos.
    def executeScriptBatch(self, sql_script):
        try:
            with self._connect() as (conn, curs):
                curs.executescript(sql_script) #Ejecuta el script
                conn.commit()
        except sqlite3.DatabaseError as e:
            logger.error("Error ejecutando un script sobre la base de datos %s", self.db_path, exc_info=True)
            raise UnexpectedException(e.args)

    #Ejecuta una consulta de selección (select)
    #El resultado es una lista de diccionarios y cada diccionario es una fila,
    #con keys los nombres de las columnas y values los valores de la columna.
    def executeQuery(self, query, *args):
        try:
            with self._connect() as (conn, curs):
                curs.execute(query, args)
                results = [dict(row) for row in curs.fetchall()]
            return results
        except sqlite3.DatabaseError as e:
            logger.error("Error ejecutando la consulta en la base de datos %s", self.db_path, exc_info=True)
            raise UnexpectedException(e.args)

    #Ejecuta una consulta de actualización (insert, update,...)
    def executeUpdateQuery(self, query, *args):
        try:
            with self._connect() as (conn, curs):
                curs.execute(query, args)
                conn.commit()
        except sqlite3.DatabaseError as e:
            logger.error("Error actualizando la base de datos %s", self.db_path, exc_info=True)
            raise UnexpectedException(e.args)