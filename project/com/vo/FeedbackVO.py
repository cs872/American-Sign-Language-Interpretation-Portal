from wtforms import *

class FeedbackVO:
    feedbackId = IntegerField
    feedbackRate = IntegerField
    feedbackComment = StringField
    feedbackDate = StringField
    feedbackTime = StringField
    feedbackFrom_LoginId = StringField
    feedbackStatus = StringField