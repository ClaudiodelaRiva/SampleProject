from src.config import DATA_PATH, DB_PATH, SCHEMA_PATH
from src.employees.employeeView import EmployeeView
from src.util.database import Database

'''
    Inicialización de la aplicación: 
    Crea el esquema de la BBDD, realiza una carga inicial de datos en la BD y muestra un menú

    Nota: se recrea el esquema y se recargan los datos en cada ejecución.
''' 

db = Database(DB_PATH)
db.executeScript(SCHEMA_PATH) #Genera el esquema ejecutando el script SCHEMA
db.executeScript(DATA_PATH) #Carga incial de datos especificada en el script DATA

EmployeeView().run() #Muestra menú para ejecutar la aplicación