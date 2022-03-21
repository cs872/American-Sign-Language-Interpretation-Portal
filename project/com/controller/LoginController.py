import hashlib
from project import app
from flask import request, render_template, redirect, url_for, session, flash
from project.com.dao.LoginDAO import LoginDAO
from project.com.dao.ComplainDAO import ComplainDAO
from project.com.dao.FeedbackDAO import FeedbackDAO
from project.com.vo.LoginVO import LoginVO
from project.com.dao.RegisterDAO import RegisterDAO

#load   login
@app.route('/')
def loadLogin():
    return render_template('admin/login.html')

@app.route('/checkLogin',methods=['post'])
def checkLogin():
    loginVO= LoginVO()
    loginDAO = LoginDAO()

    loginVO.LoginEmail = request.form["loginEmail"]
    loginVO.LoginPassword = request.form["loginPassword"]
    loginVO.LoginPassword = hashlib.md5(loginVO.LoginPassword.encode())
    loginVO.LoginPassword = loginVO.LoginPassword.hexdigest()
    loginDict = loginDAO.checkLogin(loginVO)



    if len(loginDict) == 0:

        return render_template('admin/login.html',loginerrorDict="Invalid Email-Id!!")

    elif loginDict[0]['loginPassword'] != loginVO.LoginPassword :

        return render_template('admin/login.html', loginerrorDict="Invalid Password!!")

    elif loginDict[0]['loginActiveStatus'] != 'active' :

        return render_template('admin/login.html', loginerrorDict=loginVO.LoginEmail+" This User Is Blocked!!")


    elif loginDict[0]['loginRole']=="admin":
        session['loginId']= loginDict[0]['loginId']
        session['loginRole'] = 'admin'
        return redirect(url_for('loadAdminIndex'))

    elif loginDict[0]['loginRole']=="user":
        session['loginId'] = loginDict[0]['loginId']
        session['loginRole'] = 'user'
        return redirect(url_for('loadUserIndex'))

#admin dashboard
@app.route('/admin')
def loadAdminIndex():
    if session.get('loginRole') == 'admin':

        registerDAO = RegisterDAO()
        userDict = registerDAO.countUser()
        countUser = 0
        for i in userDict:
            countUser = countUser+1


        complainDAO = ComplainDAO()
        complainDict = complainDAO.countComplain()
        countComplain = 0
        for i in complainDict:
            countComplain = countComplain + 1


        feedbackDAO = FeedbackDAO()
        feedbackDict = feedbackDAO.countFeedback()
        countFeedback = 0
        for i in feedbackDict:
            countFeedback = countFeedback + 1

        count = [countUser-1,countComplain,countFeedback]


        return render_template('admin/index.html' , count= count)

    else:
        return render_template('admin/login.html')




#user dashboard
@app.route('/user')
def loadUserIndex():
    if session.get('loginRole') == 'user':
        return render_template('user/index.html', userId=session['loginId'])
    else:
        return render_template('admin/login.html')

@app.route('/logout')
def logout():
    session.clear()
    return render_template('admin/login.html', loginerrorDict="logout successfully")








