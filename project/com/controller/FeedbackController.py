from project import app
from flask import request,render_template,session , redirect ,url_for
from project.com.dao.FeedbackDAO import FeedbackDAO
from project.com.vo.FeedbackVO import FeedbackVO
import datetime


#user add Feedback form
@app.route('/loadFeedback')
def loadFeedback():
    if session.get('loginRole') == 'user':
        return render_template('user/addFeedback.html', userId=session['loginId'])
    else:
        return render_template('admin/login.html')




#admin view Feedback
@app.route('/adminViewFeedback', methods=['get'])
def adminViewFeedback():
    if session.get('loginRole') == 'admin':
        feedbackDAO = FeedbackDAO()
        feedbackVO = FeedbackVO()
        feedbackVO.feedbackStatus  = 'active'
        feedbackDict = feedbackDAO.AdminViewFeedback(feedbackVO)

        return render_template("admin/viewFeedback.html", feedbackDict=feedbackDict)

    else:
        return render_template('admin/login.html')








#user view feedback
@app.route('/userViewFeedback', methods=['get'])
def userViewFeedback():
    if session.get('loginRole') == 'user':
        feedbackVO = FeedbackVO()
        feedbackDAO = FeedbackDAO()
        feedbackVO.feedbackFrom_LoginId = str(session.get('loginId'))

        feedbackDict = feedbackDAO.UserViewFeedback(feedbackVO)


        return render_template("user/viewFeedback.html",feedbackDict = feedbackDict, userId=session['loginId'])


    else:
        return render_template('admin/login.html')

#user add complain
@app.route('/addFeedback',methods=['get'])
def addFeedback():
    now = datetime.datetime.now()
    feedbackVO = FeedbackVO()
    feedbackDAO = FeedbackDAO()
    feedbackVO.feedbackStatus = 'active'
    feedbackVO.feedbackFrom_LoginId = str(session.get('loginId'))
    feedbackVO.feedbackRate = request.args.get('star')

    feedbackComment = request.args.get('feedbackComment')
    feedbackComment = feedbackComment.replace("'","")
    feedbackVO.feedbackComment = feedbackComment

    feedbackVO.feedbackDate = now.strftime("%d-%m-%Y")           #current date
    feedbackVO.feedbackTime = now.strftime("%H:%M")             #current time

    print(feedbackVO.feedbackRate)
    print(feedbackVO.feedbackComment)
    print(type(feedbackVO.feedbackComment))


    feedbackDAO.addFeedback(feedbackVO)


    return redirect(url_for('userViewFeedback'))


#user load learn handsign
@app.route('/learnHandSign', methods=['get'])
def learnHandSign():

    if session.get('loginRole') == 'user':

        return render_template('user/learnHandSign.html')

    else:
        return render_template('admin/login.html')











