import subprocess, os, time
import re
import math
from flask_restful import Resource, Api, reqparse
from flask import request
import logging, threading
from utils.database import db
import sqlalchemy
from sqlalchemy.sql.expression import cast
from models.model import Merchant,Slot
from models.model import Shop_Item
from sqlalchemy.sql.expression import func
from utils.Constants import radius


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

            merchants = Merchant.query.filter((func.degrees(func.acos(func.sin(func.radians(lat)) * \
                      func.sin(func.radians(Merchant.lat)) \
                      + func.cos(func.radians(lat)) * func.cos(func.radians(Merchant.lat)) * \
                      func.cos(func.radians(lng-Merchant.lng)))) * 60 * 1.1515 * 1.609344) <= radius).all()
            #merchants = db.session.query(Merchant,Merchant.distance(float(lat),float(lng)).label('distance')).having(cast('distance', sqlalchemy.Integer) < 500).order_by('distance').all()
           
            for currentMerchant in merchants:
                print(currentMerchant.merchant_id)
                
            #merchants = Merchant.query.all()
            
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

                items =  Shop_Item.query.filter_by(merchant_id = currentMerchant.merchant_id, status = "active").all()
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
                #if self.isReachable(float(lat), float(lng), float(merchant['lat']), float(merchant['lng']), 500):
                merchantsToSend.append(merchant)
            print("merchant to send: %s"%merchantsToSend)
            message = "ok"
            return self.response("200","false",merchantsToSend,message)
        except threading.ThreadError as err:
            logging.error(str(err))
            result = None

    def isReachable(self, lat, lng, mlat, mlng, km):
        ky = float(40000.0 / 360.0)
        kx = float(math.cos(math.pi * lat / 180.0) * ky)
        dx = abs(lng - mlng) * kx
        dy = abs(lat - mlat) * ky
        return math.sqrt(dx * dx + dy * dy) <= km

    def response(self, responseCode,hasError,data,message):
        response = {}
        response['responseCode'] = responseCode
        response['hasError'] = hasError
        response['message'] = message
        response['data'] = data
        

        return response
