from src.config import DATA_PATH, DB_PATH, SCHEMA_PATH
from src.employees.employeeView import EmployeeView
from src.util.database import Database

def main():
    """Inicializa la base de datos y ejecuta la interfaz de empleados."""
    db = Database(DB_PATH)
    db.executeScript(SCHEMA_PATH)
    db.executeScript(DATA_PATH)
    EmployeeView().run()


if __name__ == "__main__":
    main()
