import datetime
import logging
import sys

from src.employees.employeeModel import EmployeeModel
from src.util.unexpectedException import UnexpectedException

logger = logging.getLogger(__name__)


class EmployeeView:
    '''
    Clase que representa la vista (entrada y salida) de datos
    para las funcionalidades relativas a los empleados que estarán
    representadas en la clase EmployeeModel (employeeModel.py)
    '''

    def __init__(self):
        self.empleado = EmployeeModel() #Crea un objeto model que se invocará desde esta vista
        #Crea un diccionario con las opciones (key) y los métodos/acciones que se pueden realizar en este objeto (values)
        self.choices = {"1": self.showEmployees,
                        "2": self.showAvgSalary,
                        "3": self.newEmployee,
                        "4": self.showEmployeesByYears,
                        "5": self.quit
                        }

    def displayMenu(self):
        print(""" Opciones: \n
              1.- Lista empleados por compañía \n
              2.- Salario medio por compañia \n
              3.- Insertar empleado \n
              4.- Lista empleados por antiguedad (no activos) \n
              5.- Salir 
              """)

    #Muestra la lista de opciones y permite la selección
    def run(self):
        while True:
            self.displayMenu()
            choice = input("Introducir opción: ")
            action = self.choices.get(choice)
            if not action:
                print("{0} no es una opción valida".format(choice))
                continue
            try:
                action()
            except UnexpectedException as e:
                #Traza el error para diagnóstico y continúa mostrando el menú
                logger.error("Error inesperado de la aplicación", exc_info=True)
                print("Error inesperado (detalle en el registro). Inténtelo de nuevo.")

    #Vista para la HU Listar los empleados de una compañia
    def showEmployees(self):
        name_company = input("Introducir nombre de compañia: ")
        #Invocación al modelo para obtener el id de la compañia
        id_company = self.empleado.getIdCompany(name_company)
        if id_company is None:
            print("No existe la compañia", name_company)
        else:
            #Invoca al objeto model para obtener la lista de empleados
            res1 = self.empleado.getAllEmployees(name_company)
            #Imprime los resultados  
            self.printResults(res1)
            #Idem para obtener el resumen 
            res2 = self.empleado.getSummaryEmployees(name_company)
            for d in res2:
                print(d)

    #Vista para la HU Mostrar salario medio por compañia.
    def showAvgSalary(self):
        res = self.empleado.getAvgSalary()
        self.printResults(res)

    #Vista para la HU Insertar un empleado en una compañia
    def newEmployee(self):
        name_company = input("Introducir nombre de compañia para el empleado: ")
        id_company = self.empleado.getIdCompany(name_company)
        if id_company is None:
            print("No existe la compañia", name_company)
        else:
            #Entrada de datos del empleado
            #Nota: No se comprueba que esas entradas sean válidas (p.e. que la fecha sea válida y/o esté en el formato indicado)
            name = input("Nombre empleado: ")
            salary = int(input("Salario empleado: "))
            birth_date = input("Fecha nacimiento (aaaa-mm-dd): ")
            start_date = input("Fecha alta (aaaa-mm-dd): ")
            end_date = input("Fecha baja (aaaa-mm-dd): ")
            self.empleado.insertEmployee(name, salary, birth_date, start_date, end_date, id_company)

    #Vista para la HU Listar empleados con antiguedad superior a un año
    def showEmployeesByYears(self):
        name_company = input("Introducir nombre de compañia: ")
        #Invocación al modelo para obtener el id de la compañia
        id_company = self.empleado.getIdCompany(name_company)
        if id_company is None:
            print("No existe la compañia", name_company)
        else:
            #Invoca al objeto model para obtener la lista de empleados
            current_date = datetime.date.today().strftime("%Y-%m-%d")
            res = self.empleado.getEmployeesByYears(current_date, name_company)
            #Imprime los resultados  
            self.printResults(res)

    def quit(self):
        print("Cerrando opciones.")
        sys.exit(0)

    #Médodo muy general para imprimir los resultados (res) que vienen del model
    def printResults(self, res):
        if len(res) == 0:
            print("No hay resultados")
        else:
            #cabecera
            print(list(res[0].keys())) # Imprime nombres de columnas (keys del diccionario)
            print("----------------------------------")
            #contenido 
            for row in res:
                print([*row.values()]) # Imprime valor de una fila (values del diccionario)
            print("----------------------------------")