import subprocess, os, time
import re
import math
from flask_restful import Resource, Api, reqparse
from flask import request
import logging, threading
from utils.database import db
import sqlalchemy
from sqlalchemy.sql.expression import cast

# from models.model import Entry
# from models.model import Users
from models.model import Merchant,Slot
from models.model import Shop_Item

class GetAllMerchant(Resource):
    def get_nearest(lat, lon):
        # find the nearest point to the input coordinates
        # convert the input coordinates to a WKT point and query for nearest point
        pt = WKTElement('POINT({0} {1})'.format(lon, lat), srid=4326)
        return Merchant.query.order_by(Merchant.geom.distance_box(pt)).first()

    def post(self):
        data = request.data
        if "latitude" in data and "longitude" in data:
            lat = data["latitude"]
            lng = data["longitude"]
        else:
            message = "Bad request"
            return self.response("408", {}, message)
        try:
            #finding nearest row
            #result=self.get_nearest(lat,lng)

            #math operations not possible in sqlLite3, so using Merchant.all()
            #merchants = db.session.query(Merchant,Merchant.distance(latitude,longitude).label('distance')).having(cast('distance', sqlalchemy.Integer) < 25).order_by('distance').all()
            merchants = Merchant.query.all()
            
            merchantList = []
            for currentMerchant in merchants:
                merchantDict = {}
                merchantDict["merchantId"] = currentMerchant.merchant_id
                merchantDict["shopName"] = currentMerchant.shopName
                merchantDict["shopCategory"] = currentMerchant.shopCategory
                merchantDict["avgTime"] = currentMerchant.avgTime
                merchantDict["maxPeoplePerSlot"] = currentMerchant.maxPeoplePerSlot
                merchantDict["lat"] = str(currentMerchant.lat)
                merchantDict["lng"] = str(currentMerchant.lng)

                items =  db.session.query(Shop_Item).filter(Shop_Item.merchant_id == currentMerchant.merchant_id).all()
                print("length of items: %s"%items)
                itemsList = []
                for item in items:
                    print("item: %s"%item)
                    itemDict = {}
                    itemDict["id"] = item.id
                    itemDict["item_value"] = item.item_value
                    itemsList.append(itemDict)
                merchantDict["items"] = itemsList
                merchantList.append(merchantDict)

            print(merchantList)
            merchantsToSend = []
            for merchant in merchantList:
                if self.isReachable(float(lat), float(lng), float(merchant['lat']), float(merchant['lng']), 500):
                    merchantsToSend.append(merchant)
            print("merchant to send: %s"%merchantsToSend)
            message = "ok"
            return self.response("200",merchantsToSend,message)
            return self.response("200","","")
        except threading.ThreadError as err:
            logging.error(str(err))
            result = None

    def isReachable(self, lat, lng, mlat, mlng, km):
        ky = float(40000.0 / 360.0)
        kx = float(math.cos(math.pi * lat / 180.0) * ky)
        dx = abs(lng - mlng) * kx
        dy = abs(lat - mlat) * ky
        return math.sqrt(dx * dx + dy * dy) <= km

    def response(self, responseCode,data,message):
        response = {}
        response['responseCode'] = responseCode
        response['message'] = message
        response['merchants'] = data
        return response
