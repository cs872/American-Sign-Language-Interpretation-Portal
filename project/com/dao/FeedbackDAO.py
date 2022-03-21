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

#admin view feedback
class FeedbackDAO:

    def __init__(self):
        readFactoryObj = readConcreteCreator()
        self.readOperation = readFactoryObj.factory_method()

        updateFactoryObj = updateConcreteCreator()
        self.updateOperation = updateFactoryObj.factory_method()

    def AdminViewFeedback(self,feedbackVO):
        query = "SELECT feedbackId,feedbackDescription,feedbackTime,feedbackStatus,feedbackRate,feedbackDate, loginEmail FROM pythondb.feedbackmaster INNER JOIN pythondb.loginmaster ON pythondb.feedbackmaster.feedbackFrom_LoginId = pythondb.loginmaster.loginId WHERE pythondb.feedbackmaster.feedbackStatus='"+feedbackVO.feedbackStatus+"' "
        feedbackDict = self.readOperation.operation(query)
        return feedbackDict

    def addFeedback(self,feedbackVo):
        query = "INSERT INTO `pythondb`.`feedbackMaster` (`feedbackRate`, `feedbackDescription`, `feedbackDate`, `feedbackTime`, `feedbackFrom_LoginId` ,`feedbackStatus`) VALUES ('"+feedbackVo.feedbackRate+"', '"+feedbackVo.feedbackComment+"', '"+feedbackVo.feedbackDate+"', '"+feedbackVo.feedbackTime+"', '"+feedbackVo.feedbackFrom_LoginId+"','"+feedbackVo.feedbackStatus+"') "
        self.updateOperation.operation(query)

    def UserViewFeedback(self,feedbackVO):
        query = "SELECT feedbackId,feedbackDescription,feedbackTime,feedbackStatus,feedbackRate,feedbackDate, loginEmail FROM pythondb.feedbackmaster LEFT JOIN pythondb.loginmaster ON pythondb.feedbackmaster.feedbackTo_LoginId = pythondb.loginmaster.loginId  WHERE pythondb.feedbackmaster.feedbackStatus='active' AND pythondb.feedbackmaster.feedbackFrom_LoginId = '"+feedbackVO.feedbackFrom_LoginId+"'"
        feedbackDict = self.readOperation.operation(query)
        return feedbackDict

    def countFeedback(self):
        query = "SELECT * FROM feedbackMaster WHERE feedbackStatus = 'active'"
        feedbackDict = self.readOperation.operation(query)
        return feedbackDict



