from wtforms import *

class ComplainVO:
    complainId = IntegerField
    complainReply = StringField
    complainSubject = StringField
    complainDescription = StringField
    complainFrom_LoginId = StringField
    complainTo_LoginId = StringField
    complainDate = StringField
    complainTime = StringField
    complainStatus = StringField
    complainActiveStatus = StringField