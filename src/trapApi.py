from flask_api import FlaskAPI, status, exceptions
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS, cross_origin
from utils.ConfigReader import ConfigReader
from api.GetAllMerchant import userApi.GetAllMerchant
from api.InsertItem import InsertItem
from api.Authenticate import Authenticate
from api.GetAllMerchantByCategory import userApi.GetAllMerchantByCategory
from api.GetAvailableSlotsApi import userApi.GetAvailableSlotsApi
from api.ReturnSlotInformationApi import commonApi.ReturnSlotInformationApi
from api.BookSlot import userApi.BookSlotApi
from flask_migrate import Migrate
from utils.database import *
import configparser
import getopt
import logging
import time

api = Api(app)
app.config['SECRET_KEY'] = b"\x9c\x9a\xd7qam\x95W\xeb\xbc\x88O'T\x12\\\x99\x11\n[\xfd\xaa\rL"
from models import model
CORS(app)

if __name__ == "__main__":

    confFile = None
    # handle the command line parameter to receive the configuration file
    try:

        confFile = "conf/setting.cfg"
    except:

        print("errorCode ")
        sys.exit(1)
    try:
        cmdConfig = configparser.ConfigParser()
        #configReader = ConfigReader(cmdConfig, confFile)
        #print("Logs Path " + configReader.apiLog)
        api.add_resource(GetAllMerchant, "/getAllMerchantDetails")
        api.add_resource(GetAllMerchantByCategory, "/getAllMerchantDetailsByCategory")
        api.add_resource(Authenticate, "/login")
        api.add_resource(GetAvailableSlotsApi, "/getAvailableSlots")
        api.add_resource(BookSlotApi, "/bookSlot")
        api.add_resource(ReturnSlotInformationApi, "/getSlotInformation")
        
        # api.add_resource(GenerateTestSuite, "/lma/generateTestSuite")
        #logging.info("Api Running on port %s " % (configReader.apiPort))
        app.run(debug=False, host='0.0.0.0', port=5051, threaded=True)
    except Exception as e:
        print(e)
