from project.com.dao import con_db
from abc import ABC, abstractmethod

class Builder(ABC):
    """
    The Builder interface specifies methods for creating the different parts of
    the objects.
    """

    @property
    @abstractmethod
    def returnQueryResult(self) -> None:
        pass
    def createConnection(self) -> None:
        pass
    def closeConnection(self) -> None:
        pass


class LoginConcrete(Builder):
    """
    The Concrete Builder classes follow the Builder interface and provide
    specific implementations of the building steps.
    """
    def __init__(self) -> None:
        """
        A fresh builder instance should contain a blank product object, which is
        used in further assembly.
        """
        self.reset()

    def reset(self) -> None:
        self._login = LoginOperationDirector()

    def returnQueryResult(self, outputDict) -> None:
        return self._login.saveDict(outputDict)

    def createConnection(self) -> None:
        return self._login.openConnection()

    def closeConnection(self) -> None:
        self._login.closeConnection()



class LoginOperationDirector():

    def __init__(self) -> None:
        self.loginDict = []
        self.databaseConnection=con_db()

    def saveDict(self, loginDict) -> None:
        self.loginDict = loginDict
        return self.loginDict

    def openConnection(self) -> None:
        databaseCursor = self.databaseConnection.cursor()
        return databaseCursor

    def closeConnection(self) -> None:
        self.databaseConnection.close()



class LoginDAO:

    def LoginInsert(self,LoginVO):

        builder = LoginConcrete()
        cursor1 = builder.createConnection()
        cursor1.execute("INSERT INTO loginmaster(`loginEmail`,`loginPassword`) VALUES ('"+LoginVO.LoginEmail+"','"+LoginVO.LoginPassword+"')")

        builder._login.databaseConnection.commit()
        cursor1.close()
        builder.closeConnection()

    #fetch max id
    def FetchId(self):

        builder = LoginConcrete()
        cursor1 = builder.createConnection()
        cursor1.execute("SELECT MAX(loginId) FROM loginmaster")
        LoginIdDict = builder.returnQueryResult(cursor1.fetchall())

        cursor1.close()
        builder.closeConnection()
        return LoginIdDict

    def checkLogin(self,loginVO):
        builder = LoginConcrete()
        cursor1 = builder.createConnection()
        cursor1.execute("SELECT * FROM pythondb.loginmaster WHERE loginEmail = '"+loginVO.LoginEmail+"'  ")
        loginDict = builder.returnQueryResult(cursor1.fetchall())

        cursor1.close()
        builder.closeConnection()
        return loginDict

    def updateRegisterUser(self, loginVO):
        builder = LoginConcrete()
        cursor1 = builder.createConnection()
        cursor1.execute(" UPDATE `loginmaster` SET `loginEmail` = '" + loginVO.loginEmail + "' WHERE (`loginId` = '" + loginVO.LoginId + "') ")
        builder._login.databaseConnection.commit()
        cursor1.close()
        builder.closeConnection()






