from project import app
from flask import request,render_template, redirect,url_for,session
from project.com.vo.ComplainVO import ComplainVO
from project.com.dao.ComplainDAO import ComplainDAO
import datetime
import string

#user add Complain form
@app.route('/loadComplain')
def loadComplain():
    if session.get('loginRole') == 'user':
        return render_template('user/addComplain.html', userId=session['loginId'])

    else:
        return render_template('admin/login.html')




#admin view Complain
@app.route('/adminViewComplain', methods=['get'])
def adminViewComplain():
    if session.get('loginRole') == 'admin':
        complainVO = ComplainVO()
        complainDAO = ComplainDAO()
        complainVO.complainActiveStatus = 'active'
        complainVO.complainStatus = 'pending'
        complainDict = complainDAO.adminViewComplain(complainVO)

        return render_template("admin/viewComplain.html", complainDict=complainDict)

    else:
        return render_template('admin/login.html')






#user view complain
@app.route('/userViewComplain', methods=['get'])
def userViewComplain():
    if session.get('loginRole') == 'user':
        complainVO = ComplainVO()
        complainDAO = ComplainDAO()


        complainVO.complainFrom_LoginId = str(session.get('loginId'))
        UserComplainDict = complainDAO.viewUserComplain(complainVO)

        return render_template("user/viewComplain.html",UserComplainDict=UserComplainDict, userId=session['loginId'] )

    else:
        return render_template("admin/login.html")

#user add complain
@app.route('/addComplain',methods=['get'])
def addComplain():
    now = datetime.datetime.now()               #for date/time
    complainVO = ComplainVO()
    complainDAO = ComplainDAO()

    complainSubject = request.args.get('complainSubject')
    complainSubject = complainSubject.replace("'","")
    complainVO.complainSubject = complainSubject

    complainDescription = request.args.get('complainDescription')
    complainDescription = complainDescription.replace("'", "")

    complainVO.complainDescription = complainDescription
    complainVO.complainFrom_LoginId = str(session.get('loginId'))
    complainVO.complainDate = now.strftime("%d-%m-%Y")           #current date
    complainVO.complainTime = now.strftime("%H:%M")             #current time
    complainVO.complainActiveStatus = 'active'
    complainVO.complainStatus = 'pending'

    complainDAO.addComplain(complainVO)

    return redirect(url_for('userViewComplain'))






#admin load reply Complain
@app.route('/loadReplayComplain', methods=['get'])
def complaintReply():

    complainVO = ComplainVO()
    complainDAO = ComplainDAO()

    complainVO.complainId = request.args.get("complainId")

    UserComplainDict = complainDAO.selectComplain(complainVO)

    return render_template("admin/replyComplain.html", UserComplainDict = UserComplainDict)


#admin add reply to complain
@app.route('/addComplainReply' , methods=['get'])
def addComplainReply():

    complainVO = ComplainVO()
    complainDAO = ComplainDAO()

    complainVO.complainId = str(request.args.get("complainId"))
    complainReply = request.args.get("complainReply")
    complainReply = complainReply.replace("'","")
    complainVO.complainReply = complainReply
    complainVO.complainTo_LoginId = str(session.get('loginId'))
    complainVO.complainStatus = 'replied'



    complainDAO.addComplainReply(complainVO)
    return redirect(url_for("adminViewComplain"))






