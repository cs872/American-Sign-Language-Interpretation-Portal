from wtforms import *

class DatasetVO:
    datasetId = IntegerField
    datasetType = StringField
    datasetFile = StringField
    datasetPath = StringField
    datasetName = StringField
    datasetActiveStatus = StringField