
import unittest
from src.empleados.empleadoModel import EmpleadoModel
from src.util.database import DataBase

class TestEmpleado (unittest.TestCase):

    def setUp (self):
        DBNAME="CompanyDB.db"
        SCHEMA = "resources/schema.sql"
                
        self.db = DataBase(DBNAME) #Conexión a la base de datos DBNAME, si no existe la crea
        self.db.executeScript(SCHEMA) #Genera el esquema ejecutando el script SCHEMA

        testData = """insert into Company(id,id2,name,startDate) values(1,null,'Company 1','2020-05-03'); 
                      insert into Company(id,id2,name,startDate) values(2,3333,'Company 2','1999-12-24');
                      insert into Employee (id,name,salary,birthDate,startDate,endDate,idCompany) values (null,'E1',2000,'2000-01-01','2020-01-01',null,2);
                      insert into Employee (id,name,salary,birthDate,startDate,endDate,idCompany) values (null,'E1',2000,'2000-01-01','2020-01-01','2021-01-01',2); 
                      insert into Employee (id,name,salary,birthDate,startDate,endDate,idCompany) values (null,'E1',2000,'2000-01-01','2020-01-01','2020-10-01',2);
                   """
                
        self.db.executeScriptBatch(testData) #Carga incial de datos especificada en el script testData
        
    def testGetAllEmpleados1 (self):
        self.empleado = EmpleadoModel()
        listEmpleadosC1 = self.empleado.getAllEmployees('Company 1')
        listEmpleadosC2 = self.empleado.getAllEmployees('Company 2')
        self.assertEquals(len(listEmpleadosC1), 0)
        self.assertEquals(len(listEmpleadosC2), 3)
        
    def testGetAllEmpleados2 (self):
        self.empleado = EmpleadoModel()
        listEmpleadosC1 = self.empleado.getAllEmployees('Company 1')
        self.assertEquals(len(listEmpleadosC1), 0)
        listEmpleadosC2 = self.empleado.getAllEmployees('Company 2')
        expectedOutput = [{"Compania":'Company 2',"IdEmpleado":1,"NombreEmpleado":'E1','Salario':2000}]
        self.assertEquals(listEmpleadosC2,expectedOutput)

    def testGetEmpleadosByYears (self):
         self.empleado = EmpleadoModel()
         listEmpleados = self.empleado.getAllEmployees('Company 2')

if __name__ == '__main__':
    unittest.main()




    