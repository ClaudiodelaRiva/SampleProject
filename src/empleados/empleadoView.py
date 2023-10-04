
import sys
from src.empleados.empleadoModel import EmpleadoModel

class EmpleadoView:
    '''
    Clase que representa la vista (entrada y salida) de datos
    para las funcionalidades relativas a una compañía que estarán
    representadas en la clase EmpleadoModel (EmpleadoModel.py)
    '''
     
    def __init__ (self):
        self.company = EmpleadoModel () #Crea un objeto model que se invocará desde esta vista
        #Crea un diccionario con las opciones (key) y los métodos/acciones que se pueden realizar en este objeto (values)
        self.choices = { "1": self.showEmployees,
                         "2": self.showAvgSalary,
                         "3": self.newEmployee,
                         "4": self.quit
                       }
    
    def displayMenu (self):
        print(""" Opciones: \n
              1.- Lista empleados por compañía \n
              2.- Salario medio por compañia \n
              3.- Insertar empleado \n
              4.- Salir 
              """)
    
    #Muestra la lista de opciones y permite la selección
    def run (self):
        while True:
            self.displayMenu()
            choice = input("Introducir opción: ")
            action = self.choices.get(choice)
            if action:
                action()
            else:
                print("{0} no es una opción valida".format(choice))
    
    #Vista para la HU Listar los empleados de una compañia
    def showEmployees (self):
        name = input ("Introducir nombre de compañia: ")
        #Invoca al objeto model para obtener la lista de empleados       
        res1 = self.company.getAllEmployees(name)
        #Imprime los resultados  
        self.printResults(res1)
        #Idem para obtener el resumen 
        res2 = self.company.getSummaryEmployees(name)
        for d in res2:
            print (d)
    
    #Vista para la HU Mostrar salario medio por compañia.
    def showAvgSalary (self):
        res = self.company.getAvgSalary()
        self.printResults(res)
    
    #Vista para la HU Insertar un empleado en una compañia
    def newEmployee (self):
        nameCompany = input ("Introducir nombre de compañia para el empleado: ")
        idCompany = self.company.getIdCompany(nameCompany)
        if idCompany==None:
            print ("No existe la compañia", nameCompany)
        else:
            #Entrada de datos del empleado
            #Nota: No se comprueba que esas entradas sean válidas (p.e. que la fecha sea válida y/o esté en el formato indicado)
            name=input ("Nombre empleado: ")
            salary=int(input("Salario empleado: "))
            birthDate=input("Fecha nacimiento (aaaa-mm-dd): ")
            self.company.insertEmploye(name,salary,birthDate,idCompany)
            
    def quit(self):
        print("Cerrando opciones.")
        sys.exit(0)

    #Médodo muy general para imprimir los resultados (res) que vienen del model
    def printResults (self,res):
        if len(res)==0: 
            print ("No hay resultados")
        else:
            #cabecera
            print (list(res[0].keys())) # Imprime nombres de columnas (keys del diccionario)
            print ("----------------------------------")
            #contenido 
            for row in res:
                print ([*row.values()]) # Imprime valor de una fila (values del diccionario)
            print ("----------------------------------")


        