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

class GetItemsApi(Resource):

    def post(self):
        request_data = request.data
        merchant_id = request_data["merchant_id"]
        try: 
            items=Shop_Item.query.filter_by(merchant_id=merchant_id).all()
            data={}
            itemsList = []
            for item in items:
                print("item: %s"%item)
                itemDict = {}
                itemDict["id"] = item.id
                itemDict["item_value"] = item.item_value
                itemsList.append(itemDict)
            data['items']=itemsList
            message = "Success"
            return self.response("200","false",data,message)
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