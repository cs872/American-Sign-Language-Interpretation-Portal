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


class RegisterConcrete(Builder):
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
        self._register = RegisterOperationDirector()

    def returnQueryResult(self, outputDict) -> None:
        return self._register.saveDict(outputDict)

    def createConnection(self) -> None:
        return self._register.openConnection()

    def closeConnection(self) -> None:
        self._register.closeConnection()



class RegisterOperationDirector():

    def __init__(self) -> None:
        self.registerDict = []
        self.databaseConnection=con_db()

    def saveDict(self, registerDict) -> None:
        self.registerDict = registerDict
        return self.registerDict

    def openConnection(self) -> None:
        databaseCursor = self.databaseConnection.cursor()
        return databaseCursor

    def closeConnection(self) -> None:
        self.databaseConnection.close()


class RegisterDAO:
    def RegisterUser(self, RegisterVO):
        builder = RegisterConcrete()

        cursor1 = builder.createConnection()
        cursor1.execute("SELECT * FROM registermaster; ")
        searchtuple = builder.returnQueryResult(cursor1.fetchall())
        cursor1.close()
        builder.closeConnection()
        return searchtuple



    def RegisterInsert(self,registerVO):
        builder = RegisterConcrete()

        cursor1=builder.createConnection()
        cursor1.execute("INSERT INTO registermaster( `registerFirstName`, `registerLastName`, `registerPhoneNumber`, `registerAddress`, `registerGender`, `register_LoginId`) VALUES('"+registerVO.registerFirstName+"', '"+ registerVO.registerLastName+"', '"+registerVO.registerPhoneNumber +"', '"+registerVO.registerAddress +"', '"+registerVO.registerGender+"', '"+registerVO.register_LoginId+"')" )
        builder._register.databaseConnection.commit()
        cursor1.close()
        builder.closeConnection()



    def viewUser(self):
        builder = RegisterConcrete()

        cursor1=builder.createConnection()
        cursor1.execute("SELECT register_LoginId,registerUserId,registerFirstName, registerLastName,registerPhoneNumber,registerAddress,registerGender,registerActiveStatus, loginEmail FROM pythondb.registermaster INNER JOIN pythondb.loginmaster ON pythondb.registermaster.register_LoginId = pythondb.loginmaster.loginId WHERE pythondb.loginmaster.loginActiveStatus='active' AND pythondb.loginmaster.loginRole = 'user' ;")
        searchDict = builder.returnQueryResult(cursor1.fetchall())

        cursor1.close()
        builder.closeConnection()

        return searchDict

    def DeleteUser(self, userVO):
        builder = RegisterConcrete()

        cursor1=builder.createConnection()
        #cursor1.execute(" UPDATE `loginmaster` SET `loginActiveStatus` = 'block'   WHERE (`loginId` = '" + userVO.register_LoginId + "') ")
        cursor1.execute(" DELETE FROM `loginmaster` WHERE (`loginId` = '" + userVO.register_LoginId + "') ")
        builder._register.databaseConnection.commit()
        cursor1.close()
        builder.closeConnection()

    def updateRegisterUser(self, registerUserVO):
        builder = RegisterConcrete()

        cursor1=builder.createConnection()
        cursor1.execute(" UPDATE `registermaster` SET `registerFirstName` = '" + registerUserVO.registerFirstName + "', `registerLastName` = '" + registerUserVO.registerLastName + "',`registerPhoneNumber` = '" + registerUserVO.registerPhoneNumber + "',`registerAddress` = '" + registerUserVO.registerAddress + "'   WHERE (`registerUserId` = '" + registerUserVO.registerUserId + "') ")
        builder._register.databaseConnection.commit()
        cursor1.close()
        builder.closeConnection()

    def UpdateUser(self, userVO):
        builder = RegisterConcrete()

        cursor1=builder.createConnection()
        cursor1.execute("SELECT register_LoginId,registerUserId,registerFirstName, registerLastName,registerPhoneNumber,registerAddress,registerGender,registerActiveStatus, loginEmail FROM pythondb.registermaster INNER JOIN pythondb.loginmaster ON pythondb.registermaster.register_LoginId = pythondb.loginmaster.loginId WHERE (`register_LoginId` = '" + userVO.register_LoginId + "');")
        userDict = builder.returnQueryResult(cursor1.fetchall())
        builder._register.databaseConnection.commit()
        cursor1.close()
        builder.closeConnection()
        return userDict

    def isUserExist(self,loginVO):
        builder = RegisterConcrete()
        cursor1 = builder.createConnection()
        cursor1.execute("SELECT * FROM pythondb.loginmaster WHERE loginEmail = '"+loginVO.LoginEmail+"' AND loginActiveStatus != 'block' ")
        userExist = builder.returnQueryResult(cursor1.fetchall())

        cursor1.close()
        builder.closeConnection()
        return userExist

    def countUser(self):
        builder = RegisterConcrete()

        cursor2=builder.createConnection()
        cursor2.execute("select * from `loginmaster` WHERE `loginActiveStatus` = 'active' ")
        userDict = builder.returnQueryResult(cursor2.fetchall())
        builder._register.databaseConnection.commit()
        cursor2.close()
        builder.closeConnection()
        return userDict








