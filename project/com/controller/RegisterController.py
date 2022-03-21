import random
import smtplib
import string
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import hashlib

from project import app
from flask import request,render_template,redirect,url_for,session , flash
from project.com.dao.RegisterDAO import RegisterDAO
from project.com.vo.RegisterVO import RegisterVO
from project.com.vo.LoginVO import LoginVO
from project.com.dao.LoginDAO import LoginDAO
from project.com.controller import LoginController



#user load register
@app.route('/loadRegister')
def loadRegister():
    return render_template('user/registration.html')

#user register
@app.route('/registerUser', methods=['get'])
def registerUser():

    registerUserVO = RegisterVO()
    registerUserDAO = RegisterDAO()
    loginVO = LoginVO()
    loginDAO = LoginDAO()


    registerUserVO.registerFirstName = request.args.get("RegisterFirstName")
    registerUserVO.registerLastName = request.args.get("RegisterLastName")
    registerUserVO.registerGender = request.args.get("RegisterGender")
    registerUserVO.registerPhoneNumber = request.args.get("RegisterPhoneNumber")
    loginVO.LoginEmail = request.args.get("RegisterEmail")                       #rstore email in LoginVO
    registerUserVO.registerAddress = request.args.get("RegisterAddress")

    checkUsernameDict = registerUserDAO.isUserExist(loginVO)

    if len(checkUsernameDict)!=0:

        return render_template('user/registration.html', registerErrorDict="This email-id already exists")
    else:
        # generate random password
        loginVO.LoginPassword = registerPassword = ''.join(
            (random.choice(string.ascii_letters + string.digits)) for x in range(8))
        loginVO.LoginPassword = hashlib.md5(registerPassword.encode())
        loginVO.LoginPassword = loginVO.LoginPassword.hexdigest()
        fromaddr = "98765ppp@gmail.com"  # sender email

        toaddr = loginVO.LoginEmail  # receiver email

        msg = MIMEMultipart()

        msg['From'] = fromaddr

        msg['To'] = toaddr

        msg['Subject'] = "Your hand Sign Interpretation Portal Password"

        msg.attach(MIMEText(registerPassword, 'plain'))

        server = smtplib.SMTP('smtp.gmail.com', 587)

        server.starttls()

        server.login(fromaddr, "Nimish@1952")  # sender email and password

        text = msg.as_string()

        server.sendmail(fromaddr, toaddr, text)

        server.quit()

        loginDAO.LoginInsert(loginVO)

        registerUserVO.register_LoginId = str(loginDAO.FetchId()[0]['MAX(loginId)'])

        registerUserDAO.RegisterInsert(registerUserVO)

        return redirect(url_for("loadLogin"))  # redirect to user Login form



#admin view user
@app.route('/viewUser', methods=['get'])
def viewUser():
    if session.get('loginRole') == 'admin':
        registerUserDAO = RegisterDAO()

        userDict = registerUserDAO.viewUser()


        return render_template("admin/viewUser.html", userDict=userDict)

    else:
        return render_template('admin/login.html')



#admin delete user
@app.route('/deleteUser', methods=['get'])
def DeleteUser():
    if session.get('loginRole') == 'admin':
        registerUserVO = RegisterVO()
        registerUserDAO = RegisterDAO()
        registerUserVO.register_LoginId = str(request.args.get("registerId"))

        registerUserDAO.DeleteUser(registerUserVO)

        return redirect(url_for("viewUser"))
    else:
        return render_template("admin/login.html")

@app.route('/update', methods=['get'])
def UpdateUser():

    registerUserVO = RegisterVO()
    registerUserDAO = RegisterDAO()
    registerUserVO.register_LoginId = str(request.args.get("registerId"))
    userDict = registerUserDAO.UpdateUser(registerUserVO)

    return render_template("admin/updateUser.html", userDict=userDict)


@app.route('/insertUpdatedUser', methods=['get'])
def insertUpdatedUser():
    registerUserVO = RegisterVO()
    registerUserDAO = RegisterDAO()
    loginVO = LoginVO()
    loginDAO = LoginDAO()
    registerUserVO.registerFirstName = request.args.get("RegisterFirstName")
    registerUserVO.registerLastName = request.args.get("RegisterLastName")
    registerUserVO.registerGender = request.args.get("RegisterGender")
    registerUserVO.registerPhoneNumber = request.args.get("RegisterPhoneNumber")
    loginVO.LoginId = request.args.get("register_LoginId") 
    loginVO.loginEmail = request.args.get("RegisterEmail") 
    registerUserVO.registerAddress = request.args.get("RegisterAddress")
    registerUserVO.registerUserId = request.args.get("registerUserId")
    userDict = registerUserDAO.updateRegisterUser(registerUserVO)
    userDict = loginDAO.updateRegisterUser(loginVO)
    if session.get('loginRole') == 'admin':
        return redirect(url_for('loadAdminIndex'))
    else:
        return redirect(url_for('loadUserIndex'))




# load forget Password
@app.route('/loadForgetPassword')
def loadForgetPassword():
    return render_template('admin/forgetPassword.html')


#forget password
@app.route('/forgetPassword', methods=['post'])
def forgetPassword():

    registerUserVO = RegisterVO()
    registerUserDAO = RegisterDAO()
    loginVO = LoginVO()
    loginDAO = LoginDAO()


    loginVO.LoginEmail = request.form["loginEmail"]                    #rstore email in LoginVO


    checkDict = loginDAO.checkLogin(loginVO)

    if len(checkDict)!=0:
        # generate random password
        loginVO.LoginPassword    = checkDict[0]['loginPassword']

        fromaddr = "98765ppp@gmail.com"  # sender email

        toaddr = loginVO.LoginEmail  # receiver email

        msg = MIMEMultipart()

        msg['From'] = fromaddr

        msg['To'] = toaddr

        msg['Subject'] = "YOUR EA2U-SYSTEM PASSWORD"

        msg.attach(MIMEText(loginVO.LoginPassword, 'plain'))

        server = smtplib.SMTP('smtp.gmail.com', 587)

        server.starttls()

        server.login(fromaddr, "Nimish@1952")  # sender email and password

        text = msg.as_string()

        server.sendmail(fromaddr, toaddr, text)

        server.quit()
        return redirect(url_for("loadLogin"))  # redirect to user Login form

    else:
        return render_template('user/registration.html', registerErrorDict="This email-id not exists Register First")















