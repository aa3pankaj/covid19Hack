from flask_api import FlaskAPI, status, exceptions
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS, cross_origin
from utils.ConfigReader import ConfigReader
from api.userApi.GetAllMerchant import GetAllMerchant
from api.commonApi.Authenticate import Authenticate
from api.userApi.GetAllMerchantByCategory import GetAllMerchantByCategory
from api.userApi.GetAvailableSlotsApi import GetAvailableSlotsApi
from api.commonApi.ReturnSlotInformationApi import ReturnSlotInformationApi
from api.commonApi.RegistrationApi import RegistrationApi
from api.commonApi.GetProfileInfoApi import GetProfileInfoApi

from api.userApi.BookSlotApi import BookSlotApi

from api.merchantApi.CreateItemApi import CreateItemApi
from api.merchantApi.UpdateItemApi import UpdateItemApi
from api.merchantApi.DeleteItemApi import DeleteItemApi
from api.merchantApi.GetItemsApi import GetItemsApi
from api.userApi.BuyGift import BuyGift



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
        api.add_resource(RegistrationApi, "/register")
        api.add_resource(GetProfileInfoApi, "/getProfileInfo")
        api.add_resource(CreateItemApi, "/newItem")
        api.add_resource(UpdateItemApi, "/updateItem")
        api.add_resource(DeleteItemApi, "/deleteItem")
        api.add_resource(GetItemsApi, "/getItemAll")
        api.add_resource(BuyGift, "/buyGift")
        


        # api.add_resource(GenerateTestSuite, "/lma/generateTestSuite")
        #logging.info("Api Running on port %s " % (configReader.apiPort))
        app.run(debug=False, host='0.0.0.0', port=5051, threaded=True)
    except Exception as e:
        print(e)
