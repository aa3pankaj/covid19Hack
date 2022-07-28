import subprocess, os, time
import re
import math
from flask_restful import Resource, Api, reqparse
from flask import request
import logging, threading
from utils.database import db
# from models.model import Entry
# from models.model import Users
from models.model import Merchant
from models.model import Shop_Item

class GetAllMerchantByCategory(Resource):

    def post(self):
        data = request.data
        if "lat" in data and "lng" in data:
            lat = data["lat"]
            long = data["lng"]
            shopCategory = data["category"]
        else:
            message = "Bad request"
            return self.response("408", {}, message)
        # des = data["description"]
        try:
            merchants = db.session.query(Merchant).filter(Merchant.shopCategory == shopCategory).all()
            # merchants = Merchant.query.all()
            # print(merchants)
            # print("type: %s"%merchants[0].merchant_id)
            merchantList = []
            for currentMerchant in merchants:
                merchantDict = {}
                merchantDict["merchantId"] = currentMerchant.merchant_id
                merchantDict["shopName"] = currentMerchant.shopName
                merchantDict["shopCategory"] = currentMerchant.shopCategory
                merchantDict["avgTime"] = currentMerchant.avgTime
                merchantDict["maxPeoplePerSlot"] = currentMerchant.maxPeoplePerSlot
                merchantDict["lat"] = currentMerchant.lat
                merchantDict["lng"] = currentMerchant.long

                items =  db.session.query(Shop_Item).filter(Shop_Item.merchant_id == currentMerchant.merchant_id).all()
                print("length of items: %s"%items)
                itemsList = []
                for item in items:
                    print("item: %s"%item)
                    itemDict = {}
                    itemDict["id"] = item.id
                    itemDict["itemValue"] = item.item_value
                    itemsList.append(itemDict)
                merchantDict["items"] = itemsList
                merchantList.append(merchantDict)

            print(merchantList)
            merchantsToSend = []
            for merchant in merchantList:
                if self.isReachable(float(lat), float(long), float(merchant['lat']), float(merchant['lng']), 15):
                    merchantsToSend.append(merchant)

            # entry = Users(phonenumber="758868814", firstname="Roshan",lastname="Borale",passwordhash="936736332")
            # merchant_id = db.Column(db.Integer, primary_key=True)
            # location = db.Column(db.String, nullable=False)
            # lat = db.Column(db.String, nullable=False)
            # long = db.Column(db.String, nullable=False)
            # shopName = db.Column(db.String, nullable=False)
            # avgTime = db.Column(db.String, nullable=False)
            # maxPeoplePerSlot = db.Column(db.String, nullable=False)
            # user_id = db.Column(db.Integer, db.ForeignKey('Users.id'))


            # merchant =Merchant(location ="pune",lat ="17.4344",long="78.3866",shopName="Dmart",avgTime="60",maxPeoplePerSlot="20",user_id=1)
            #
            # db.session.add(merchant)
            # db.session.commit()
            message = "ok"
            return self.response("200",merchantsToSend,message)
        except threading.ThreadError as err:
            logging.error(str(err))
            result = None

    def isReachable(self, lat, long, mlat, mlong, km):
        ky = float(40000.0 / 360.0)
        kx = float(math.cos(math.pi * lat / 180.0) * ky)
        dx = abs(long - mlong) * kx
        dy = abs(lat - mlat) * ky
        return math.sqrt(dx * dx + dy * dy) <= km

    def response(self, responseCode,data,message):
        response = {}
        response['responseCode'] = responseCode
        response['message'] = message
        response['merchants'] = data
        return response
