from src.util.database import DataBase

class EmpleadoModel:
    '''
    Clase que representa los objetos de negocio (model) relativos a las funcionalidades de 
    los empleados. Varios métodos de esta clase se invocarán desde la vista (EmpleadoView), y los resultados
    se devolverán nuevamente a la vista para su visualización
    '''
    
    def __init__ (self):
        self.db = DataBase ("CompanyDB.db")
    
    #Obtiene la lista de empleados para una compañia especificada por su nombre
    def getAllEmployees (self,companyName):
        query = """select Company.name as Compania, Employee.id as IdEmpleado, Employee.name as NombreEmpleado, Employee.salary as Salario 
                   from Company inner join Employee on Company.id=Employee.idCompany
                   where Compania = ? order by Employee.id asc
                """
        return self.db.executeQuery(query,companyName)

    #Obtiene la lista de empleados para una compañia especificada por su nombre con antiguedad superior a una año (incluyendo a no activos)
    #fechaActual es la fecha que se quiere indicar para la fecha actual (a efectos de pruebas)
    def getEmployeesByYears (self,fechaActual,companyName):
        query = """select Company.name as Compania, Employee.name as NombreEmpleado, 
	                    case 
                            when Employee.endDate isnull then trunc((julianday (?) - julianday(Employee.startDate))/365)
		                    else trunc((julianday(Employee.endDate) - julianday(Employee.startDate))/365) 
	                    end as Years
	                from Company inner join Employee on Company.id=Employee.idCompany
                    where Compania = ? and Years>=1 and  
                """
        return self.db.executeQuery(query,fechaActual,companyName)

    #Obtiene resumen (total empleados y media de salario) para una compañia especificada por su nombre
    def getSummaryEmployees (self, companyName): 
        query = """select count(Employee.id) as total, avg(Employee.salary) as average
                   from Company inner join Employee on Company.id=Employee.idCompany
                   where Company.name = ?
                   group by (Company.id)
                """
        return  self.db.executeQuery(query,companyName)
    
    #Obtiene el salario medio de todos los empleado por compañia
    def getAvgSalary (self):
        query = """select Company.name, avg(Employee.salary) as avgSalary
                  from Company left join Employee on Company.id=Employee.idCompany
                  group by (Company.id)
                """
        return self.db.executeQuery(query)
    
    #Inserción de lo datos de un empleado (name,salary,birthdate) en una compañia
    #Notar que no es necesario indicar explícitamente el valor de la clave del empleado (id),
    #ya que cuando éste es null, sqlite lo genera de forma autoincremental
    def insertEmploye (self,name,salary,birthDate,startDate,endDate,idCompany):
        query = """
                insert into Employee(id,name,salary,birthDate,startDate,endDate,idCompany) values (null,?,?,?,?) 
                """
        self.db.executeUpdateQuery(query,name,salary,birthDate,idCompany)
    
    #Obtiene el id de una compañia especificada por su nombre.
    def getIdCompany (self,companyName):
        query = """select id from Company
                   where Company.name = ?
                """
        res = self.db.executeQuery(query,companyName) 
        if len(res)==1:
            return res[0].get("id")
        else:
            return None
