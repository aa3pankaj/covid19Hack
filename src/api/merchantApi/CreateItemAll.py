import subprocess, os, time
import re
from flask_restful import Resource, Api, reqparse
from flask import request
import logging, threading
import shutil
from models.model import Slot
from utils.database import db
import json
import copy
from sqlalchemy import or_
import random,string
import calendar;
import time;
from datetime import datetime,timedelta
from sqlalchemy import and_
from models.model import Shop_Item


class CreateItemAll(Resource):

    def post(self):
        try:    
            request_data = request.data
            merchant_id = request_data["merchantId"]
            data_items = request_data["items"]
            itemList=[]
            for item_request in data_items:
               
                items=Shop_Item.query.filter_by(item_value=item_request["itemValue"], merchant_id = merchant_id, status = "active")
                itemsInactive=Shop_Item.query.filter_by(item_value=item_request["itemValue"], merchant_id = merchant_id, status = "inactive")
            
                itemInfo={}
                if itemsInactive.count() > 0:
                    item=itemsInactive.first()
                    item.status = "active"
                    db.session.add(item)
                    db.session.commit()
                    itemInfo["id"] = item.id
                    itemInfo["itemValue"] = item.item_value 
                elif(items.count() == 0):
                    item=Shop_Item(merchant_id=merchant_id, item_value=item_request["itemValue"], status = "active")
                    db.session.add(item)
                    db.session.commit()
                    itemInfo["id"] = item.id
                    itemInfo["itemValue"] = item.item_value
                    itemList.append(itemInfo)
            
            message = "success"
            return self.response("200","false",itemList,message)
        except Exception as err:
            message = str(err)
            return self.response("503", "true",{}, message)


    def response(self, responseCode,hasError,data,message):
        response = {}
        response['responseCode'] = responseCode
        response['message'] = message
        response['hasError'] = hasError
        response['data'] = data
        return response