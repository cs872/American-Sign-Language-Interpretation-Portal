from project.com.dao import con_db
from abc import ABC, abstractmethod


class Creator(ABC):
    """
    The Creator class declares the factory method that is supposed to return an
    object of a  class. The Creator's subclasses usually provide the
    implementation of this method.
    """

    @abstractmethod
    def factory_method(self):
        """
        Note that the Creator may also provide some default implementation of
        the factory method.
        """
        pass

class readConcreteCreator(Creator):

    def factory_method(self):
        return readOperations()

class updateConcreteCreator(Creator):

    def factory_method(self):
        return updateOperations()

class readOperations():

    def __init__(self) -> None:
        self.resultDict = []
        self.databaseConnection=con_db()

    def operation(self, query):
        cursor1 = self.databaseConnection.cursor()
        cursor1.execute(query)
        resultDict = cursor1.fetchall()
        cursor1.close()
        self.databaseConnection.close()
        return resultDict

class updateOperations():

    def __init__(self) -> None:
        self.databaseConnection=con_db()

    def operation(self, query):
        cursor1 = self.databaseConnection.cursor()
        cursor1.execute(query)
        self.databaseConnection.commit()
        cursor1.close()
        self.databaseConnection.close()


class ComplainDAO:

    def __init__(self):
        readFactoryObj = readConcreteCreator()
        self.readOperation = readFactoryObj.factory_method()

        updateFactoryObj = updateConcreteCreator()
        self.updateOperation = updateFactoryObj.factory_method()


    def adminViewComplain(self,complainVO):
        query = "SELECT complainId,complainDescription,complainSubject,complainTime,complainDate,complainStatus, loginEmail FROM pythondb.complainmaster INNER JOIN pythondb.loginmaster ON pythondb.complainmaster.complainFrom_LoginId = pythondb.loginmaster.loginId WHERE pythondb.complainmaster.complainActiveStatus='"+complainVO.complainActiveStatus+"' AND pythondb.complainmaster.complainStatus = '"+complainVO.complainStatus+"' "
        complainDict = self.readOperation.operation(query)
        return complainDict


    def addComplain(self,complainVO):
        query = "INSERT INTO `pythondb`.`complainmaster` (`complainSubject`, `complainDescription`, `complainDate`, `complainTime`,  `complainFrom_LoginId`, `complainStatus` , `complainActiveStatus`) VALUES ('"+complainVO.complainSubject+"', '"+complainVO.complainDescription+"', '"+complainVO.complainDate+"', '"+complainVO.complainTime+"', '"+complainVO.complainFrom_LoginId+"', '"+complainVO.complainStatus+"','"+complainVO.complainActiveStatus+"')"
        self.updateOperation.operation(query)

    def viewUserComplain(self,complainVO):
        query = "SELECT complainId,complainStatus,complainDescription,complainSubject,complainDate,complainTime,complainReply,complainStatus, loginEmail FROM pythondb.complainmaster LEFT JOIN pythondb.loginmaster ON pythondb.complainmaster.complainTo_LoginId = pythondb.loginmaster.loginId WHERE pythondb.complainmaster.complainActiveStatus='active' AND pythondb.complainmaster.complainFrom_LoginId = '"+complainVO.complainFrom_LoginId+"' "
        complainDict = self.readOperation.operation(query)
        return complainDict

    def selectComplain(self,complainVo):
        query = "SELECT complainId,complainDescription,complainSubject,complainTime,complainDate,complainStatus, loginEmail FROM pythondb.complainmaster INNER JOIN pythondb.loginmaster ON pythondb.complainmaster.complainFrom_LoginId = pythondb.loginmaster.loginId WHERE complainId = '"+complainVo.complainId+"' "
        complainDict = self.readOperation.operation(query)
        return complainDict

    def addComplainReply(self,complainVO):
        query = " UPDATE `pythondb`.`complainmaster` SET `complainReply` = '"+complainVO.complainReply+"', `complainTo_LoginId` = '"+complainVO.complainTo_LoginId+"' ,`complainStatus` = '"+complainVO.complainStatus+"' WHERE (`complainId` = '"+complainVO.complainId+"') "
        self.updateOperation.operation(query)

    def countComplain(self):
        query = "SELECT * FROM complainMaster WHERE complainStatus = 'pending'"
        complainDict = self.readOperation.operation(query)
        return complainDict

